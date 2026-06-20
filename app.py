from fastapi import FastAPI
from pydantic import BaseModel, Field , computed_field
from typing import Literal,Annotated
import pickle
import pandas as pd

with open ('model.pkl' , 'rb') as f :  # read binary means rb 
    model = pickle.load(f)

app = FastAPI()

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
    




