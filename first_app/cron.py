from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail
from django.conf import settings
import logging

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 2 # every 24 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'first_app.my_cron_job'    # a unique code
    
    def do(self):
        logging.debug('My cron job executed')
        send_mail(
            'Subject',
            'Message',
            settings.EMAIL_HOST_USER,
            ['tejaswini.s@prodapt.com'],
            fail_silently=False,
        )
        logging.debug('Next run time: %s', self.schedule.get_next_run()) # add this line

