from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
# from .database import get_db, Session
from model import predict_sentiment

app = FastAPI()

class Review(BaseModel):
    text: str

@app.post("/predict")
def predict(review: Review): # , db: Session = Depends(get_db)
    try:
         sentiment = predict_sentiment(review.text)
        # Store review and prediction in database (optional)
        # ...
         return {"sentiment": sentiment}
        # return {"message": "Test prediction endpoint"} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))