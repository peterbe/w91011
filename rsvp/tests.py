from django.test import TestCase
from django.conf import settings
from models import RSVP, Food, User

class SimpleTest(TestCase):

    def test_rsvp(self):
        assert Food.objects.all() # fixtures
        r = self.client.get('/')
        assert r.status_code == 200
        assert 'Log in' in r.content
        r = self.client.get('/', {'i':'junk'})
        assert 'Invalid invitation link' in r.content
        i = settings.INVITATION_KEYS[0].encode('rot13')
        r = self.client.get('/', {'i': i})
        assert r.status_code == 302
        assert '/welcome/' in r['Location']
        r = self.client.get('/', {'i': i}, follow=True)
        data = {'first_name':'Peter', 'last_name':'Bengtsson',
                'email':'test@email.com'}
        r = self.client.post('/welcome/', data)
        assert r.status_code == 302
        assert '/rsvp/' in r['Location']
        r = self.client.get('/rsvp/')
        assert 'Peter' in r.content
        data = {'coming':'yes',
                'people':'\n Peter Bengtsson\n\n Ashley \t',
                'song_requests':'Elton\nJohn',
        }
        r = self.client.post('/rsvp/', data)
        assert r.status_code == 302
        assert '/rsvp/food/' in r['Location']
        rsvp, = RSVP.objects.all()
        assert rsvp.user.email == 'test@email.com'
        assert rsvp.people == ['Peter Bengtsson', 'Ashley']
        assert rsvp.no_people == 2
        assert rsvp.coming

        food1, food2 = Food.objects.all()[:2]

        r = self.client.get('/rsvp/food/')
        # peter wants the first dish, ashley the second
        food1, food2 = Food.objects.all()[:2]

        data = {'food_1': food1.pk,
                'food_2': food2.pk,}
        r = self.client.post('/rsvp/food/', data)
        assert '/rsvp/thanks/' in r['Location']
        rsvp, = RSVP.objects.all()
        assert rsvp.food['Ashley']
        assert rsvp.food['Peter Bengtsson']

    def test_login(self):
        peter = User.objects.create(
          username='dontmatter',
          email='test@email.com',
          first_name='Peter',
          last_name='Be'
        )
        peter.set_password('secret')
        peter.save()

        r = self.client.get('/')
        assert "You'll need to login" in r.content

        data = {'email':'Test@email.com',
                'password':'secret'}
        r = self.client.post('/', data)
        print r
        r = self.client.get('/')
        assert "You'll need to login" not in r.content
