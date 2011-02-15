# python
import datetime

# django
from django.contrib.auth.models import User
from django.conf import settings

# app
from base import TestCase
from users.models import *

class ModelsTestCase(TestCase):
    
    def test_setup_default_assessments(self):
        kat = User.objects.create(
          username="kat",
          first_name="Kat",
          last_name="Will",
          email="kat@will.com",
        )
        profile = UserProfile.objects.create(
          user=kat,
          therapist=self.richard,
        )
        
        self.assertRaises(SystemError, profile.setup_default_assessments)
        profile.treatment_start_date = datetime.date.today()
        profile.save()
        
        from questionnaires.models import Assessment, Questionnaire
        Questionnaire.objects.create(name="Peter", code="PB")
        Questionnaire.objects.create(name="Ashley")
        Questionnaire.objects.create(name="Chris")
        assert not Assessment.objects.all()
        settings.DEFAULT_ASSESSMENT_START = (
          dict(questionnaires=('pb','ashley','chris'),
               delay_start=0,
               duration=10),
               
          dict(questionnaires=('peter','chris'),
               delay_start=2,
               duration=5),               
        )
        profile.setup_default_assessments()
        self.assertTrue(profile.treatment_end_date)
        
        self.assertEqual(Assessment.objects.filter(user=kat).count(), 2)
        for each in Assessment.objects.filter(user=kat):
            self.assertTrue(each.questionnaires.all().count())
        
    
    def test_treatment_dates(self):
        kat = User.objects.create(
          username="kat",
          first_name="Kat",
          last_name="Will",
          email="kat@will.com",
        )
        profile = UserProfile.objects.create(
          user=kat,
          therapist=self.richard
        )
        
        self.assertRaises(AssertionError, profile.treatment_has_started)
        self.assertRaises(AssertionError, profile.treatment_has_ended)
        
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        profile.treatment_start_date = tomorrow
        assert profile.treatment_start_date, "no start date set"
        self.assertFalse(profile.treatment_has_started())
        profile.treatment_start_date = today
        self.assertTrue(profile.treatment_has_started())
        
        profile.treatment_end_date = tomorrow
        self.assertFalse(profile.treatment_has_ended())
        profile.treatment_end_date = today
        self.assertFalse(profile.treatment_has_ended())
        yesterday = today - datetime.timedelta(days=1)
        profile.treatment_end_date = yesterday
        self.assertTrue(profile.treatment_has_ended())
        
        