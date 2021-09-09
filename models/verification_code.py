
from mongoengine import connect
from mongoengine.document import Document
from mongoengine.fields import IntField, StringField, DateField

connect('pharma')

class Verification_codes(Document):
    code = IntField(required=True)
    phone_number = StringField(required=True)
    creation_date = DateField(required=True)

