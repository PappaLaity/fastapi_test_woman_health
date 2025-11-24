import io
from fastapi import APIRouter,File, HTTPException, UploadFile
from PIL import Image
import logging

from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)
router = APIRouter()

# Use this function to run your ML model on the image
def run_model(image: Image.Image):
    # Dummy prediction for example
    return {"label": "cat", "confidence": 0.98}

# Endpoint to handle image upload and prediction
@router.post("/predict")
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
