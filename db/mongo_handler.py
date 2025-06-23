import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(override=True)

from bson import ObjectId, Binary

def bson_to_str(val):
    import bson
    if isinstance(val, bson.binary.Binary):
        return bytes(val).hex()
    elif isinstance(val, bytes):
        return val.hex()
    elif isinstance(val, bson.ObjectId):
        return str(val)
    else:
        return str(val)


def load_mongo_data(fields=None, collection: str = "quest_history"):
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME")
    client = MongoClient(uri)
    db = client[db_name]
    col = db[collection]

    projection = {field: 1 for field in fields} if fields else None
    if projection is not None:
        projection['_id'] = 0

    data = list(col.find({}, projection))
    if not data:
        return pd.DataFrame(), pd.DataFrame()
    df = pd.DataFrame(data)

    # 1. 모든 컬럼 str/hex 변환
    for col in df.columns:
        if col != "actionTime":
            df[col] = df[col].apply(bson_to_str)

    # 2. actionTime는 datetime으로 변환
    df["actionTime"] = pd.to_datetime(df["actionTime"], errors="coerce")

    # 3. rewardPoint는 숫자로 변환
    df["rewardPoint"] = pd.to_numeric(df["rewardPoint"], errors="coerce")

    df_parent = df[df['questType'] == 'parent'].reset_index(drop=True)
    df_daily = df[df['questType'] == 'daily'].reset_index(drop=True)
    return df_parent, df_daily