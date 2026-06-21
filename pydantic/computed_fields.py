

from pydantic import BaseModel,EmailStr,AnyUrl,Field,computed_field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
   name: str
   email:EmailStr
   url:AnyUrl
   age: int
   weight: float
   height: float
   married: bool      
   allergies: List[str] 
   contact_details:Dict[str,str]

   @computed_field
   @property
   def calculate_bmi(self) -> float:
       bmi = round(self.weight/(self.height**2),4)
       return bmi

                                
def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.married)
    print(patient.contact_details)
    print("Data inserted successfully") 
    print('BMi', patient.calculate_bmi)   

patient_info ={'name': 'aditya','email':'abc@icici.com','url':'http://www.google.com','age': "67",'weight':44.5,'height':'1.56','married':'false','allergies':['pollen','dust'],'contact_details':{'phone no.':'123456789','emergency':'213'}} 

patient1 = Patient(**patient_info)

insert_patient_data(patient1)



