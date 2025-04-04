import configparser
import firebase_admin
from firebase_admin import credentials, db

# 读取 config.ini
config = configparser.ConfigParser()
config.read("config.ini")

# 将 Firebase 配置从 .ini 读出
firebase_config = {
    "type": config["firebase"]["type"],
    "project_id": config["firebase"]["project_id"],
    "private_key_id": config["firebase"]["private_key_id"],
    "private_key": config["firebase"]["private_key"].replace("\\n", "\n"),
    "client_email": config["firebase"]["client_email"],
    "client_id": config["firebase"]["client_id"],
    "auth_uri": config["firebase"]["auth_uri"],
    "token_uri": config["firebase"]["token_uri"],
    "auth_provider_x509_cert_url": config["firebase"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": config["firebase"]["client_x509_cert_url"],
    "universe_domain": config["firebase"]["universe_domain"]
}

# 初始化 Firebase Admin SDK
cred = credentials.Certificate(firebase_config)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': config["firebase"]["databaseURL"]
    })

def store_message(chat_id, user_message, bot_reply):
    ref = db.reference(f"messages/{chat_id}")
    ref.push({
        "user": user_message,
        "bot": bot_reply
    })
