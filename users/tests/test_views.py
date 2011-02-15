# python
import re
import datetime

# django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core import mail

# app
from base import TestCase
from users.models import UserProfile


class ViewsTestCase(TestCase):

    def test_add_new_patient(self):
        url = reverse('users:add-user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(settings.LOGIN_URL in response['Location'])

        assert self.client.login(username='admin', password='secret')
       
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {'cancel':'yes'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse('users:admin') in response['Location'])

        response = self.client.post(url, {'email':'kat', 'first_name':''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('errorlist' in response.content)

        richard = User.objects.get(username='richard')

        email = 'kat+will@willi-ams.com'
        response = self.client.post(url, {'email':email,
                                          'first_name':'Kat',
                                          'last_name':'Williams',
                                          'password': 'test123',
                                          'therapist': richard.id,
                                          })
        self.assertEqual(response.status_code, 302)

        kat = User.objects.get(first_name='Kat')
        profile = kat.get_profile()
        self.assertEqual(profile.therapist, richard)
        self.assertEqual(profile.treatment_start_date, None)
        self.assertEqual(profile.treatment_end_date, None)
        
        # render the User administration page
        url = reverse('users:admin')
        response = self.client.get(url)
        self.assertTrue(response.content.count('Not set'), 2)

        # it should now be possible to log in as this user
        self.client.logout()

        url = reverse('website:login')
        data = dict(username=email,
                    password='test123',
                    next=reverse('website:dashboard'))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse('website:dashboard') in response['Location'])

    def test_add_repeated_email_address(self):
        url = reverse('users:add-user')

        assert self.client.login(username='admin', password='secret')
        richard = User.objects.get(username='richard')

        email = 'kat+WILL@willi-ams.com'
        response = self.client.post(url, {'email':email,
                                          'first_name':'Kat',
                                          'last_name':'Williams',
                                          'password': 'test123',
                                          'therapist': richard.id,
                                          })
        self.assertEqual(response.status_code, 302)

        User.objects.get(first_name='Kat')
        email = 'kat+will@WILLI-ams.com'
        response = self.client.post(url, {'email':email,
                                          'first_name':'Petra',
                                          'last_name':'Kolleby',
                                          'password': 'test123',
                                          'therapist': richard.id,
                                          })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Already registered' in response.content)



    def test_change_user_password(self):
        url = reverse('users:edit-user-password', args=[self.kate.username])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(settings.LOGIN_URL in response['Location'])

        self.client.login(username='richard', password='secret')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, dict(new_password='test123',
                                              email_password_reminder=1))
        self.assertEqual(response.status_code, 302)

        self.client.logout()
        self.assertEquals(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertTrue(self.kate.username in email.body)
        self.assertTrue('test123' in email.body)
        self.assertTrue(settings.PROJECT_NAME in email.body)

        assert self.client.login(username=self.kate.username, password='test123')

    def test_edit_patient(self):
        url = reverse('users:edit-user', args=[self.kate.username])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(settings.LOGIN_URL in response['Location'])

        assert self.client.login(username='admin', password='secret')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


        data = {'first_name': 'Kate 2',
                'last_name': 'Blom 2',
                'email': 'kate2@gmail.com',
                'is_active': 'sure',
                'therapist': self.richard.id,
                }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        kate = User.objects.get(first_name='Kate 2')
        self.assertEqual(kate.last_name, 'Blom 2')
        self.assertEqual(kate.email, 'kate2@gmail.com')
        self.assertTrue(kate.is_active)

        self.assertEqual(kate.get_profile().therapist, self.richard)

        david = User.objects.create(username="david",
                                    first_name="David",
                                    is_staff=True)

        data['therapist'] = david.id
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        kate = User.objects.get(pk=kate.id)
        self.assertEqual(kate.get_profile().therapist, david)

        # make her a therapist
        data['is_therapist'] = "on"
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        kate = User.objects.get(pk=kate.id)
        self.assertTrue(kate.is_staff)

        # and make her patient again
        data['is_therapist'] = ""
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        kate = User.objects.get(pk=kate.id)
        self.assertTrue(not kate.is_staff)

        # make her inactive and she should not be able to log in
        data.pop('is_active')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        kate = User.objects.get(pk=kate.id)
        self.assertTrue(not kate.is_active)

        self.client.logout()

        self.assertTrue(not self.client.login(username=kate.username,
                                              password='secret'))


    def test_set_settings(self):
        url = reverse('users:user-settings')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(settings.LOGIN_URL in response['Location'])

        assert self.client.login(username='kate', password='secret')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # basic stuff, change mobile number
        data = {'mobile_number':'0779 102 4747',
                'sms_alerts': 'sure',
                'email_alerts': 'sure',
                }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        user_profile = UserProfile.objects.get(user__username='kate')
        self.assertEqual(user_profile.mobile_number, '07791024747')
        self.assertEqual(user_profile.sms_alerts, True)
        self.assertEqual(user_profile.email_alerts, True)

        # try to switch on sms_alerts without a number
        data['mobile_number'] = ' '
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        user_profile = UserProfile.objects.get(user__username='kate')
        self.assertEqual(user_profile.sms_alerts, False)

        # international numbers should work
        data['mobile_number'] = '+44779 - 1024646'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        user_profile = UserProfile.objects.get(user__username='kate')
        self.assertEqual(user_profile.mobile_number, '+447791024646')

        data['mobile_number'] = '00447791024646'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        data['mobile_number'] = '00447791024646'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        data['mobile_number'] = 'xx'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('errorlist' in response.content)

        data['mobile_number'] = '12356'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('errorlist' in response.content)

        data['mobile_number'] = '1235609128309182309'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('errorlist' in response.content)

        data['mobile_number'] = '+44779102474700'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('errorlist' in response.content)

    def test_change_own_password(self):

        assert self.client.login(username='kate', password='secret')
        response = self.client.get(reverse('users:user-settings'))
        self.assertContains(response, reverse('users:change-password'))

        url = reverse('users:change-password')
        response = self.client.get(url)
        # if you logged in seconds ago the "current password" field won't be there

        #print response.content
        self.assertNotContains(response, 'id_current_password')
        self.assertContains(response, 'id_new_password')
        self.assertContains(response, 'id_confirm_new_password')

        data = dict(cancel="sure")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse('users:user-settings') in response['Location'])

        data = dict(new_password="123", confirm_new_password="123")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'too short')

        data = dict(new_password="test123", confirm_new_password="123test")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'password mismatch')

        data = dict(new_password="test123", confirm_new_password="test123")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        assert self.client.login(username='kate', password='test123')

        # pretend that it's been a while since this user logged in, then we to
        # fill in the old password too
        user = User.objects.get(username='kate')
        user.last_login = datetime.datetime.now() - datetime.timedelta(minutes=60)
        user.save()

        response = self.client.get(url)
        self.assertContains(response, 'id_current_password')
        self.assertContains(response, 'id_new_password')
        self.assertContains(response, 'id_confirm_new_password')

        data = dict(new_password="test123", confirm_new_password="test123",
                    current_password="bajs")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'password incorrect')

        data = dict(new_password="secret", confirm_new_password="secret",
                    current_password="test123")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        assert self.client.login(username='kate', password='secret')


    def test_redirecting_page(self):

        url = reverse('users:redirecting')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        #print response.content
        def get_redirect_url(html):
            return re.findall('<a.*?id="redirect_to".*?href=\"([^"]+)\"',
                              html, re.DOTALL|re.M)[0]
        redirect_to = get_redirect_url(response.content)
        from urlparse import urlparse
        self.assertEqual(urlparse(redirect_to).path, '/')

        response = self.client.get(url, dict(next=reverse('users:user-settings')))
        self.assertEqual(response.status_code, 200)

        redirect_to = get_redirect_url(response.content)
        self.assertTrue(redirect_to.endswith(reverse('users:user-settings')))
        
        
    def test_admin_home(self):
        """test the list of patients"""
        url = reverse('users:admin')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(settings.LOGIN_URL in response['Location'])

        assert self.client.login(username='richard', password='secret')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, 'Kate Blomstet') # see setUp()

        self.kate.date_joined = self.kate.date_joined - datetime.timedelta(days=1)
        self.kate.save()
        
        # add another patient
        chris = User.objects.create(username='chris', email='chris@fry-ut.com',
                                   first_name='Chris', last_name='West',
                                   )
                                   
        david = User.objects.create(username='david', email='david@click.com',
                                   first_name='David', last_name='Click',
                                   is_staff=True
                                   )                                   

        UserProfile.objects.create(user=chris, therapist=david)
        
        response = self.client.get(url)
        self.assertContains(response, 'Chris West') # see setUp()
        
        # default is to sort by firstname, lastname
        self.assertTrue(-1 < response.content.find('Chris') < \
          response.content.find('Kate'))
          
        response = self.client.get(url, {'sort-patients':'name'})
        # same
        self.assertTrue(-1 < response.content.find('Chris') < \
          response.content.find('Kate'))
        
        response = self.client.get(url, {'sort-patients':'email'})
        self.assertTrue(-1 < response.content.find('chris@') < \
          response.content.find('kate@'))
          
        response = self.client.get(url, {'sort-patients':'therapist'})
        content = response.content.split('Patients')[1]
        self.assertTrue(-1 < content.find('David') < \
          content.find('Richard'))
          
        response = self.client.get(url, {'sort-patients':'date added'})
        self.assertTrue(-1 < response.content.find('chris@') < \
          response.content.find('kate@'))
          
    def test_reset_password(self):
        """reset password"""
        url = reverse('website:login')
        response = self.client.get(url)
        url = reverse('users:reset-password')
        self.assertContains(response, url)
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(url, dict(email=''))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "field is required")
        
        response = self.client.post(url, dict(email='kiss'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid")
        
        response = self.client.post(url, dict(email='bob@peterbe.com'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "address not registered")
        
        response = self.client.post(url, dict(email='Kate@gmail.com')) # see setUp()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse('users:reset-password-done') in response['Location'])
        
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, [self.kate.email])
        self.assertTrue(settings.PROJECT_NAME in email.subject)
        self.assertTrue(self.kate.first_name in email.body)
        self.assertTrue(settings.PROJECT_NAME in email.body)
        
        url_regex = re.compile(r'/users/rp/[\w/]+\b')
        recover_url = url_regex.findall(email.body)[0] + '/'
        
        # first fuck it up once
        wrong_recover_url = recover_url.replace('a','0').replace('b','9')\
          .replace('c','0').replace('d','9')
        response = self.client.get(wrong_recover_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('not valid' in response.content)
        
        response = self.client.get(recover_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse('users:change-password') in response['Location'])
        response = self.client.get(reverse('website:dashboard'))
        self.assertTrue(settings.WELCOME_PAGE_PATIENTS in response['Location'])
        response = self.client.get(reverse('website:dashboard'))
        self.assertTrue(reverse('users:logout') in response.content)
        
    def test_new_user_with_default_assessments(self):
        url = reverse('users:add-user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(settings.LOGIN_URL in response['Location'])

        assert self.client.login(username='richard', password='secret')
        response = self.client.get(url)
        # being a therapist isn't good enough
        self.assertEqual(response.status_code, 302)
        
        assert self.client.login(username='admin', password='secret')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # fill in the form and chose to select setup default assessments
        today = datetime.date.today()
        data = dict(setup_default_assessments='true',
                    first_name='Bob', last_name='Builder',
                    email='bob@builder.com', password='secret',
                    therapist=User.objects.get(username='richard').pk,
                    treatment_start_date=\
                      today.strftime('%A, %d %B, %Y')
                    )
                    
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        bob = User.objects.get(first_name='Bob')
        
        default_assessments_url = \
          reverse('users:setup-default-assessments', args=[bob.username])
        self.assertTrue(default_assessments_url in response['Location'])
        
        profile = bob.get_profile()
        self.assertTrue(profile.treatment_start_date)
        self.assertTrue(not profile.treatment_end_date)
        
        from questionnaires.models import Assessment, Questionnaire
        self.assertTrue(not Assessment.objects.filter(user=bob))
        
        # now take the redirect!
        # but first we need to create some questionnaires
        settings.DEFAULT_ASSESSMENT_START = (
          # first
          dict(questionnaires=("QS1", "QS2"), delay_start=0, duration=2),
          # second
          dict(questionnaires=("QS2", "QS3"), delay_start=1, duration=3),
        )
        Questionnaire.objects.create(
          name="QS1",
        )
        Questionnaire.objects.create(
          name="QS2",
        )
        Questionnaire.objects.create(
          name="QS3",
        )
        response = self.client.get(default_assessments_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Assessment.objects.filter(user=bob))
        self.assertEqual(Assessment.objects.filter(user=bob).count(), 2)
        
        _first = True
        for assessment in Assessment.objects.filter(user=bob).order_by('start_date'):
            if _first:
                self.assertEqual(assessment.start_date, today)
                self.assertEqual(assessment.due_date, today + datetime.timedelta(days=2))
                _first = False
            else:
                self.assertEqual(assessment.start_date, today + datetime.timedelta(days=3))
                self.assertEqual(assessment.due_date, today + datetime.timedelta(days=6))
                
        
        


