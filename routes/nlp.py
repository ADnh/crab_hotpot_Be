# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# # from routes.producer.producer import predict_class_from_text

# router = APIRouter()

# class TextInput(BaseModel):
#     text: str

# def predict_class_from_text():
#     return ""

# @router.post("/test_phoBert_cnn")
# async def predict(input_text: TextInput):
#     try:
#         predicted_class, probs = predict_class_from_text(input_text.text)
#         return {
#             "sentence": input_text.text,
#             "predicted_class": predicted_class,
#             "probabilities": probs.tolist()
#         }
#     except ValueError as ve:
#         raise HTTPException(status_code=400, detail=str(ve))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    
