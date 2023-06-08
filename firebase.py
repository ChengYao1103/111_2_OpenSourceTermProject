# 設定開發環境
# pip install --upgrade firebase-admin

# 在伺服器上初始化
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import pandas as pd

# 透過金鑰使用服務帳戶
cred = credentials.Certificate(
    "firebaseAdminsdkConfig.json"
)

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# data object 儲存 sensor 讀取到的值
humidity = 11
lightness = 72
temperature = 13
isSoilWet = 1
currentTime = datetime.now()

data = {
    "humidity": humidity,
    "lightness": lightness,
    "temperature": temperature,
    "isSoilWet": isSoilWet,
    # firebase 會自動補上時區資訊，因此將欄位內的時間先剪去時區的 offset
    "time": pd.Timestamp(currentTime).replace(hour=(currentTime.hour - 8))
}

# 將 data object 加入 firebase 中
doc_ref = db.collection("sensor").document(currentTime.strftime("%Y-%m-%d %H:%M:%S"))
doc_ref.set(data)
