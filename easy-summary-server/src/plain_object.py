from pydantic import BaseModel

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str = "User"


class LoginRequest(BaseModel):
    email: str
    password: str


class TextRequest(BaseModel):
    text: str


class SaveSummaryRequest(BaseModel):
    text: str
    token: int

class GetSummariesRequest(BaseModel):
    token: int

class DeleteSummaryRequest(BaseModel):
    token: int
    text: str

class EditSummaryRequest(BaseModel):
    token: int
    old_text: str
    new_text: str
