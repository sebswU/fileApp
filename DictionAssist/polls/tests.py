from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
"""
As long as your tests are sensibly arranged, they won’t become unmanageable. 

Good rules-of-thumb include having:

a separate TestClass for each model or view
a separate test method for each set of conditions you want to test
test method names that describe their function
"""
# Create your tests here.
class QuestionModelTests(TestCase):
    def dateTimeTest(self):
        """check to see if works for the future (which it shouldn't)"""
        date = timezone.now() + datetime.timedelta(days=30)
        tester = Question(pub_date=date)
        #it should be FALSE or else will print an error statement
        # "AssertionError: True is not False"
        self.assertIs(tester.wasPublishedRecently(), False)
