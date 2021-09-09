
from mongoengine import connect
from mongoengine.document import Document
from mongoengine.fields import DateField, IntField, StringField

connect('pharma')

class Users(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    date_of_birth = DateField(required=True)
    phone_number = StringField(required=True, unique=True)
    country_iso = StringField()
    gender = StringField(required=True)
    token= StringField(required=True)

    def __init___(self, name, email, date_of_birth, phone_number, country_iso, gender, token):

        self.name = name
        self.email = email
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.country_iso = country_iso
        self.gender = gender
        self.token = token





    


