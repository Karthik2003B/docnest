import requests
import os
import smtplib
from email.mime.text import MIMEText
from datetime import date

BASE_URL = "http://127.0.0.1:8000"



def send_email(to_email, subject, message):
    sender_email = "your_email@gmail.com"
    password = "your_app_password"   # 🔥 not real password

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)
        
def check_and_send_alerts(docs, user_email):
    today = date.today()

    for doc in docs:
        if doc.get("expiry_date"):
            expiry = date.fromisoformat(doc["expiry_date"])
            days_left = (expiry - today).days

            # 🔔 Expiring soon
            if days_left == 3:
                send_email(
                    user_email,
                    "Document Expiry Alert",
                    f"{doc['title']} will expire in 3 days."
                )

            # 🚨 Already expired
            if days_left < 0:
                send_email(
                    user_email,
                    "Document Expired",
                    f"{doc['title']} has expired."
                )

def build_file_url(file_path):
    if not file_path:
        return None

    normalized = file_path.replace("\\", "/")

    if normalized.startswith("uploads/"):
        return f"{BASE_URL}/{normalized}"

    filename = os.path.basename(normalized)
    return f"{BASE_URL}/uploads/{filename}"


def fetch_file_bytes(file_path):
    file_url = build_file_url(file_path)
    if not file_url:
        return None, None

    response = requests.get(file_url)
    if response.status_code != 200:
        return None, None

    filename = os.path.basename(file_path.replace("\\", "/"))
    return response.content, filename

def register_user(name, email, password):
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"name": name, "email": email, "password": password},
    )
    return response


def login_user(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password},
    )
    return response


def create_document(data, file_obj=None):
    files = None
    if file_obj is not None:
        files = {
            "file": (file_obj.name, file_obj, file_obj.type)
        }

    response = requests.post(
        f"{BASE_URL}/documents/",
        data=data,
        files=files
    )
    return response


def get_documents(user_id):
    response = requests.get(f"{BASE_URL}/documents/{user_id}")
    return response


def get_expiring_soon_documents(user_id):
    response = requests.get(f"{BASE_URL}/documents/expiring-soon/{user_id}")
    return response


def get_expired_documents(user_id):
    response = requests.get(f"{BASE_URL}/documents/expired/{user_id}")
    return response


def delete_document(document_id):
    response = requests.delete(f"{BASE_URL}/documents/{document_id}")
    return response