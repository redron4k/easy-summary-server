from fastapi import FastAPI, UploadFile, File, HTTPException
from transformers import pipeline
import uvicorn
import easyocr
import requests

from plain_object import *
import user_manager
from secret import *


app = FastAPI()

# OCR модель
ocr_reader = easyocr.Reader(['en', 'ru'])


@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    contents = await file.read()        # Получение multipart файла из запроса
    with open("temp.jpg", "wb") as f:   # Запись в локальный файл
        f.write(contents)

    result = ocr_reader.readtext("temp.jpg", detail=0, decoder='wordbeamsearch', paragraph=True)
    text = " ".join(result)
    return {"text": text}

@app.post("/summarize")
async def summarize(request: TextRequest):

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": model_key,
            "messages": [
                {"role": "user", "content": get_content(request.text)}
            ],
            "stream": False
        }
    )

    out = response.json()
    return {"summary": out["message"]["content"]}

@app.post("/register")
def register(req: RegisterRequest):
    # Если в БД существует такой пользователь
    if user_manager.user_exists(req.email):
          # Выбрасываем сетевое исключение
        raise HTTPException(status_code=400, detail="User already exists")
    # Создается пользователь с учетными данными
    user_manager.create_user(req.email, req.password, req.name)
    # Возвращается json-ответ
    return {"success": True}

@app.post("/login")
def login(req: LoginRequest):
    user = user_manager.authenticate(req.email, req.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "success": True, "name": user["name"], "email": user["email"],
        "token": user_manager.get_token(req.email)
    }

@app.post("/user_exists")
def user_exists(req: TextRequest):
    return {"exists": user_manager.user_exists(req.text)}

@app.post("/save_summary")
def save_summary(req: SaveSummaryRequest):
    user_manager.add_summary(str(req.token), req.text)

@app.post("/get_summaries")
def get_summaries(req: GetSummariesRequest):
    return {"success": True, "summaries": user_manager.get_summaries(str(req.token)) }

@app.post("/delete_summary")
def delete_summary(req: DeleteSummaryRequest):
    user_manager.delete_summary(str(req.token), req.text)
    return {"success": True}

@app.post("/edit_summary")
def edit_summary(req: EditSummaryRequest):
    user_manager.edit_summary(str(req.token), req.old_text, req.new_text)
    return {"success": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

