from django.test import TestCase
import datetime
from django.utils import timezone
from .models import TxtRec, WordCard, Person

# Create your tests here.
class TxtRecTests(TestCase):
    def multipleAutoGen(self):
        counter = 0
        fields = TxtRec._meta.auto_field
        self.assertIs(len(fields) <= 1, True)

class WordCardTests(TestCase):
    def multipleAutoGen(self):
        counter = 0
        fields = WordCard._meta.auto_field
        self.assertIs(len(fields) <= 1, True)
class PersonTests(TestCase):
    def multipleAutoGen(self):
        counter = 0
        fields = Person._meta.auto_field
        self.assertIs(len(fields) <= 1, True)


    #TODO: cannot have more than one autogen field