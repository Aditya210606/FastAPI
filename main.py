import json
from fastapi import FastAPI, Path, HTTPException, Query

app = FastAPI()

def load_data():
    with open ('patients.json', 'r') as f:
        data = json.load(f)

        return data

@app.get("/")

def hello():
    return {'message':'Hello welcome to AI world'}

@app.get("/about")
def about():
    return {'message':'Here you will learn about Fastapi'}


@app.get('/view')
def view():
    data = load_data()

    return data 

@app.get("/patient/{patient_id}")

def view_patient(patient_id:str = Path(...,description='Enter patient ID' , example='P001')):    #(...) means this part is required 
     #load data for all the patients
    data=load_data()

    if patient_id in data :
        return data[patient_id]
    else:
        raise HTTPException (status_code=404,detail='Patient not found')

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