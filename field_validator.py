

from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name: str
    email:EmailStr
    url:AnyUrl
    age: int
    weight: float
    married: bool      
    allergies: List[str] 
    contact_details:Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):

      valid_domain = ['hdfc.com','icici.com']
      valid_email = value.split('@')[-1]

      if valid_email in valid_domain:
         return (f"{value} is valid for treatment offer")
      else:
         raise ValueError("invalid email for offer ")
      
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
       
       return value.upper()
                                
def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.married)
    print(patient.contact_details)
    print("Data inserted successfully")    

patient_info ={'name': 'aditya','email':'abc@icici.com','url':'http://linkedin.com','age': 30,'weight':44.5,'married':'false','allergies':['pollen','dust'],'contact_details':{'phone no.':'123456789'}} 

patient1 = Patient(**patient_info)

insert_patient_data(patient1)



