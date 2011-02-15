import datetime
import os
import glob
from django.conf import settings
from django.db import connection, transaction
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = 'Fix user profiles that have assessments but no start dates'
    
    def handle_noargs(self, **options):
        transaction.enter_transaction_management()
        transaction.managed(True)
        from users.models import UserProfile
        from questionnaires.models import Assessment
        
        for patient in UserProfile.objects.filter(therapist__isnull=False, user__is_staff=False, treatment_start_date__isnull=True):
            
            try:
                first_start_date = Assessment.objects.filter(user=patient.user).order_by('start_date')[0].start_date
                last_due_date = Assessment.objects.filter(user=patient.user).order_by('-start_date')[0].due_date
            except IndexError:
                continue
            #patient.treatment_start_date = first_start_date
            print repr(patient)
            j = patient.user.date_joined
            joined = datetime.date(j.year, j.month, j.day)
            if first_start_date < joined:
                patient.treatment_start_date = joined
            else:
                patient.treatment_start_date = first_start_date
                
            patient.treatment_end_date = last_due_date + datetime.timedelta(days=30)
            print patient.treatment_start_date
            print patient.treatment_end_date
            patient.save()

        
        #transaction.rollback()
        transaction.commit()