from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
    def dateTimeTest(self):
        """check to see if works for the future (which it shouldn't)"""
        date = timezone.now() + datetime.timedelta(days=30)
        tester = Question(pub_date=date)
        #it should be FALSE or else will print an error statement
        # "AssertionError: True is not False"
        self.assertIs(tester.wasPublishedRecently(), False)
