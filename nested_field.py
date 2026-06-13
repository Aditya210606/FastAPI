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


    address_info = {'house_no':"2","city":"virar","state":"maharashtra",'pincode':"401303"}

    address = Address(**address_info)

    


