from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import pandas as pd
import os
import io
from Visa.utils.utils import load_object
import numpy as np
from Visa.pipeline.pipeline import Pipeline

app = FastAPI()
templates = Jinja2Templates(directory="templates")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the prediction directory path
PREDICTION_DIR = "./prediction_directory"

@app.get("/")
async def get_index_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict_route(file: UploadFile):
    try:
        # Read contents of uploaded CSV file
        contents = await file.read()

        # Convert CSV file to DataFrame
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

        # Create the prediction directory if it doesn't exist
        os.makedirs(PREDICTION_DIR, exist_ok=True)

        # Apply data transformations if available
        preprocessor = load_object(file_path='preprocessed_files/preprocessed_object_file_name')

        # Apply transformations using preprocessor
        X_array = preprocessor.transform(df)

        # Load and use the best model for prediction
        model = load_object(file_path='saved_models/20230528001245/model.pkl')

        # Make predictions
        y_pred = model.predict(X_array)

        # Create a DataFrame from y_pred
        df_pred = pd.DataFrame(y_pred, columns=['Prediction'])

        # Save the predicted DataFrame to a CSV file
        predicted_csv_path = os.path.join(PREDICTION_DIR, "predicted_results.csv")
        df_pred.to_csv(predicted_csv_path, index=False)

        message = "Prediction completed successfully."
        return JSONResponse(content={"message": message})

    except Exception as e:
        return JSONResponse(content={"message": f"Error occurred! {e}"}, status_code=500)

@app.get('/train')
def train_pipeline():
    try:
        # Code for training the model goes here
        Train=Pipeline()
        Train.run_pipeline()
        response = {
            'message': 'Training pipeline completed successfully!'
        }
        return response
    except Exception as e:
        return JSONResponse(content={"message": f"Error occurred! {e}"}, status_code=500)

@app.get('/upload')
def bucket_upload():
    try:
        # Code for uploading to a bucket goes here
        # ...
        response = {
            'message': 'Upload to bucket successful!'
        }
        return response
    except Exception as e:
        return JSONResponse(content={"message": f"Error occurred! {e}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)