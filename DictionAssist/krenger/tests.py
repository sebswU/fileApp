from django.test import TestCase
import datetime
from django.utils import timezone
from .models import TxtRec, WordCard, Person
# Create your tests here.
class TxtRecTests(TestCase):
    def multipleAutoGen():
        counter = 0
        fields = TxtRec._meta.auto_field
        if len(fields)>1:
            raise Exception("You made a whoopsie: you cant have more than one auto_field!")

class WordCardTests(TestCase):
    def multipleAutoGen():
        counter = 0
        fields = WordCard._meta.auto_field
        if len(fields)>1:
            raise Exception("You made a whoopsie: you cant have more than one auto_field!")

class PersonTests(TestCase):
    def multipleAutoGen():
        counter = 0
        fields = Person._meta.auto_field
        if len(fields)>1:
            raise Exception("You made a whoopsie: you cant have more than one auto_field!")
    


    #TODO: cannot have more than one autogen field