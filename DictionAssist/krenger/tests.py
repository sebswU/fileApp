from django.test import TestCase
import datetime
from django.utils import timezone
from .models import TxtRec, WordCard, Person
# Create your tests here.
class TxtRecTests(TestCase):
    def multipleAutoGen():
        counter = 0
        fields = TxtRec._meta.auto_field
        assert len(fields) <= 1

class WordCardTests(TestCase):
    def multipleAutoGen():
        counter = 0
        fields = WordCard._meta.auto_field
        assert len(fields) <= 1
class PersonTests(TestCase):
    def multipleAutoGen():
        counter = 0
        fields = Person._meta.auto_field
        assert len(fields) <= 1


    #TODO: cannot have more than one autogen field