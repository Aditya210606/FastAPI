

from pydantic import BaseModel,EmailStr,AnyUrl,Field,model_validator
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

   @model_validator(mode='after')
   def validate_emergency_contact(cls,model):
       
       if model.age > 60 and 'emergency' not in model.contact_details :
           raise ValueError("Patient above 60 should have emergency contact in contact details ")
       return model
                                
def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.married)
    print(patient.contact_details)
    print("Data inserted successfully")    

patient_info ={'name': 'aditya','email':'abc@icici.com','url':'http://linkedin.com','age': "67",'weight':44.5,'married':'false','allergies':['pollen','dust'],'contact_details':{'phone no.':'123456789','emergency':'213'}} 

patient1 = Patient(**patient_info)

insert_patient_data(patient1)



