from fastapi import FastAPI
from pydantic import BaseModel, Field , computed_field
from typing import Literal,Annotated
from fastapi.responses import JSONResponse
import pickle
import pandas as pd

with open ('model.pkl' , 'rb') as f :  # read binary means rb 
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

#created a pydantic model for userinput 

class UserInput(BaseModel):

    age : int = Field(...,gt=0,lt=120,description="Age of the patient")
    height : float = Field(...,gt=0,description="Height of the patient")
    weight : float = Field(...,gt=0,description="Weight of the patient")
    smoker : bool = Field(...,description="Is the patient smoker?")
    income_lpa : float = Field(...,gt = 0, description="Income of the patient in LPA")
    city : str = Field(...,description="Enter the city of the patient")
    occupation : Annotated[str, Literal['retired', 'government_job', 'business_owner',
                'private_job', 'unemployeed', 'student', 'freelancer'],Field(..., description="Occupation of the patient")]
    

    @computed_field
    @property
    def bmi(self) -> float :
        bmi = round(self.weight/(self.height**2),2)
        return bmi 
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str :
     
     if self.smoker and self.bmi > 30:
        return "high"
     elif self.smoker or self.bmi > 27:
        return "medium"
     else:
        return "low"
     

    @computed_field
    @property
    def age_group(self) -> str :
     if self.age < 25:
        return "young"
     elif self.age < 45:
        return "adult"
     elif self.age < 60:
        return "middle_aged"
     else :
      return "senior"
     
    @computed_field
    @property
    def city_tier(self) -> int :
     if self.city in tier_1_cities:
        return 1
     elif self.city in tier_2_cities:
        return 2
     else:
        return 3

@app.post('/perdict')
def perdict_premium(data : UserInput):

   input_df = pd.DataFrame([{
      
      'bmi' : data.bmi,
      'age_group' : data.age_group,
      'lifestyle_risk' : data.lifestyle_risk,
      'city_tier' : data.city_tier,
      'income_lpa' : data.income_lpa,
      'occupation' : data.occupation
   }])  
    
   prediction = model.predict(input_df)[0]


   return JSONResponse (status_code=200 , content={'prediction category': prediction})



