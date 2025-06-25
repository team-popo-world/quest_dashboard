from datetime import datetime, timedelta, timezone
import pandas as pd
from db.mongo_handler import load_mongo_data

def filter_date(df):
    # 날짜 컬럼을 datetime으로 변환
    df["actionTime"] = pd.to_datetime(df["actionTime"])
    
    # 한국시간으로 통일
    KST = timezone(timedelta(hours=9))

    # 오늘 자정과 7일 전 자정 계산
    today = datetime.now(KST).date()
    start_date = today - timedelta(days=6)  # 오늘 포함 7일
    start_datetime = datetime.combine(start_date, datetime.min.time())

     # 필터링: start_date ~ 오늘 자정까지 (시간 포함)
    df = df[(df["actionTime"] >= start_datetime)]

    return df