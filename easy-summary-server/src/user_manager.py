import json
import os
from time import time

USERS_FILE = "users.json"
SUMMARY_FILE = "summaries.json"
SUMMARY_RESERV = "summaries_copy.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def user_exists(email):
    users = load_users()
    return any(u["email"] == email for u in users)


def create_user(email, password, name=""):
    users = load_users()
    users.append({
        "email": email,
        "password": password,
        "name": name,
        "id_token": generate_token(email)
    })
    save_users(users)


def authenticate(email, password):
    users = load_users()
    for u in users:
        if u["email"] == email and u["password"] == password:
            return u
    return None


def generate_token(email):
    timestamp = int(time() * 1000)
    email_hash = 0
    for char in email:
        email_hash = email_hash * 131 + ord(char)
        email_hash &= 0xFFFFFFFFFFFFFFFF
    return (email_hash ^ timestamp) & 0xFFFFFFFFFFFFFFFF


def get_token(email):
    users = load_users()
    result = list(filter(lambda x: x.get('email') == email, users))[0]
    return result["id_token"]


def load_summaries():
    if not os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
            json.dump(dict(), f)
    data = dict()
    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        with open(SUMMARY_RESERV, "w", encoding="utf-8") as f:
            json.dump(data, f)
    return data
    


def save_summaries(summaries):
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=4)


def add_summary(token, text):
    if token == "-1":
        return
    summaries = load_summaries()
    texts = summaries.get(token, [])[:]
    if text not in texts:
        texts.append(text)
    summaries[token] = texts
    save_summaries(summaries)

def delete_summary(token, summary_text):
    if token == "-1":
        return
    summaries = load_summaries()
    if token in summaries:
        texts = summaries[token][:]
        if summary_text in texts:
            texts.remove(summary_text)
            summaries[token] = texts
            save_summaries(summaries)

def edit_summary(token, old, new):
    if token == "-1":
        return
    summaries = load_summaries()
    if token in summaries:
        texts = summaries[token][:]
        if old in texts:
            idx = texts.index(old)
            texts[idx] = new
            summaries[token] = texts
            save_summaries(summaries)

def get_summaries(token):
    summaries = load_summaries()
    return summaries.get(token, [])
