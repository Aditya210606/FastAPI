
from pydantic import BaseModel

class Address(BaseModel):
    house_no: int 
    city: str
    state: str
    pincode:int

class Patient(BaseModel):
    name: str
    age: str
    address : Address


address_info = {'house_no':'2','city':'virar','state':'maharashtra','pincode':'401303'}

address1 = Address(**address_info)

patient_dict = {'name':'aditya','age':'19','address':address1}

patient1 = Patient(**patient_dict)

print(patient1.address.city)

    