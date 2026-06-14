# def insert_patient_data(name : str,age: int):
 
#  if type(name) ==str and type(age) == int:
#     if age < 0:
#         raise ValueError("Age cannot be negative")
#     else:
#         print(name)
#         print(age)
#         print("Data inserted successfully")
#  else:
#     raise TypeError("Data type mismatch. Please provide correct data types for name and age.")   
 
# insert_patient_data("aditya",30)

from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name:Annotated [str, Field(max_length=50,title='Name of the patient',description='give the name of the patient in less then 50 chars')]
    email:EmailStr
    url:AnyUrl
    age: int = Field(gt=0)
    weight: Annotated[float,Field(gt=0, lt=120, strict=True)]
    married: Optional[bool] = None        #Always put a default value if optional is used 
    allergies: List[str] = Field(max_length=5)
    contact_details:Dict[str,str]


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.contact_details)
    print("Data inserted successfully")    

patient_info ={'name': 'aditya','email':'abc@gmail.com','url':'http://linkedin.com','age': 30,'weight':44.5,'allergies':['pollen','dust'],'contact_details':{'phone no.':'123456789'}} 

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
 
 
