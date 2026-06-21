import json
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Optional

app = FastAPI()

class Patient(BaseModel):
   id : Annotated[str, Field(...,description='Enter the patient id',examples=['P001'])]
   name :Annotated[str , Field(...,description='Name of the patient')] 
   city : Annotated[str,Field(...,description='enter the city where the patient is living')]
   age : Annotated[int,Field(...,gt=0,lt=120,description='enter the age of the patient')]
   gender : Annotated[str,Field(...,description='enter the gender of the patient')]
   height : Annotated[float,Field(...,description='enter the height of the patient')]
   weight : Annotated[float,Field(...,description='Enter the weight of the patient')]
    
   @computed_field
   @property
   def bmi(self) -> float :
      
      bmi = round(self.weight/(self.height**2),2)
      return bmi
   
   @computed_field
   @property
   def calculate_verdict(self) -> str:
      if self.bmi < 18.5 :
         return "underweight"
      elif self.bmi < 25 :
         return 'normal'
      else:
         return 'overweight'

class PatientUpdate(BaseModel):
   
   name :Annotated[Optional[str], Field(default=None)] 
   city : Annotated[Optional[str], Field(default=None)]
   age : Annotated[Optional[int], Field(default=None,gt=0,lt=120)]
   gender : Annotated[Optional[str], Field(default=None)]
   height : Annotated[Optional[float], Field(default=None)]
   weight : Annotated[Optional[float], Field(default=None)]

   
def load_data():
    with open ('patients.json', 'r') as f:
        data = json.load(f)

        return data
    
def save_data(data):
   with open ('patients.json' , 'w') as f :
      json.dump(data,f)  

@app.get("/")
def hello():
    return {'message':'Hello welcome to world'}

@app.get("/about")
def about():
    return {'message':'Here you will learn about Fastapi'}


@app.get('/view')
def view():
    data = load_data()

    return data 

@app.get("/patient/{patient_id}")

def view_patient(patient_id:str = Path(...,description='Enter patient ID' , example='P002')):    #(...) means this part is required 
     #load data for all the patients
    data=load_data()

    if patient_id in data :
        return data[patient_id]
    else:
        raise HTTPException (status_code=404,detail='Patient not found enter valid patient')

@app.get('/sort')
def sort_patient(sort_by: str = Query(...,description='Sort the patient on the bases of height, weight or bmi'),order : str = Query('asc', description='Sort the patient in asc or dsc order') ):

  valid_fields = ['height','weight','bmi']

  if sort_by not in valid_fields:
    raise HTTPException(status_code=400, detail=f"Invalid sort_by value. Must be one of {valid_fields}")
  
  if order not in ['asc','dsc']:
    raise HTTPException(status_code=400, detail="Invalid order value. Must be 'asc' or 'dsc'")
  
  data = load_data()
  sort_order = True if order == 'asc' else False
  sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse= sort_order)
  return sorted_data


@app.post('/create')
def create_patient(patient:Patient):
   # all the data is loaded 
   data = load_data()

   # checking ig patient already eixst or not 
   if patient.id in data : 
      raise HTTPException(status_code=400 , detail='Patient already exists')
   
   #insert data in to the data
   data[patient.id] = patient.model_dump(exclude=['id'])

   save_data(data)

   return JSONResponse (status_code=201 ,content={'message':'Patient added successfully, thank you'})


@app.put('/edit/{patient_id}')
def update_patient_info(patient_id:str ,update_patient: PatientUpdate):

   data = load_data

   if patient_id not in data :
      raise HTTPException(status_code=404 , detail='patient not found')
   
   existing_patient_info = data[patient_id]

   update_patient_info.model_dump(exclude_unset=True)

   for key,value in update_patient_info.items():
      existing_patient_info [key] = value

      existing_patient_info['id'] = patient_id

      existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

      patient_pydantic_obj = Patient(**existing_patient_info)

      data[patient_id] = existing_patient_info

      #save_data 

      save_data(data)

      return JSONResponse(status_code=201 , content={'message' : 'patient updated successfully'})
   
@app.delete('delete/{patient_id}')
def delete_patient(patient_id:str):

   data = load_data

   if patient_id not in data :
      raise HTTPException(status_code=404,detail="patient not found")

   del data[patient_id]  

   return JSONResponse(status_code=200,content={'message':'Patient deleted successfully'}) 

