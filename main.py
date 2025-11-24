from http.client import HTTPException
import io
import pickle
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

app = FastAPI()

class Question(BaseModel):
    text: str

# Load models from disk (Model Trained and Stored by Fatima)
def load_model(path: str):
    model = None
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model

# Load the language model for Q&A
model_name = "microsoft/Phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Load the trained models
# logistic_regression = load_model("models/logistic_regression.pkl")

# Define API endpoints

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello World"}


# Endpoint for Q&A using the language model (Medical Bot)
@app.post("/ask")
async def ask(q: Question):
    answer = "This is a placeholder answer."
    inputs = tokenizer(q.text, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=200)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"answer": answer}


# Use this function to run your ML model on the image
def run_model(image: Image.Image):
    # Dummy prediction for example
    return {"label": "cat", "confidence": 0.98}

# Endpoint to handle image upload and prediction
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid image type")

    # Read raw bytes
    image_bytes = await file.read()

    # Open with PIL
    image = Image.open(io.BytesIO(image_bytes))

    # TODO: preprocess image for your model
    # TODO: run your ML model prediction
    prediction = run_model(image)

    return JSONResponse(content={"prediction": prediction})