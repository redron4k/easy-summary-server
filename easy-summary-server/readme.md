## libs installation
`.\venv\Scripts\pip.exe install -r requirements.txt`

## ngrok config
`ngrok config add-authtoken <your_token_here>`

## startup
`.\venv\Scripts\python.exe .\src\ocr_server.py`


`ngrok http --url=<your_url_here> <your local port here>`


`ollama run qwen2.5:7b-instruct`




## Contracts

### /register
registers a new user by email and password, name (optinal), default = user

- POST
- request:
```json
{
    "email": string,
    "password": string,
    "name": string?
}
```
- response(success):
```json
{
    "success": true
}
```
- response(error) - HTTP 400
```json
{
    "detail": "User already exists"
}
```

### /login

logs in to account by email and password

- POST
- request
```json
{
    "email": string,
    "password": string
}
```
- response (success)
```json
{
    "success": true,
    "name": string,
    "email": string
}
```
- response (error) - HTTP 401
```json
{
    "detail": "Invalid email or password"
}
```
