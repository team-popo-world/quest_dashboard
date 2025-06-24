import pandas as pd
import numpy as np

def completion_rate(df):

    """
    일일퀘스트(df_daily)는 questName별, 
    부모퀘스트(df_parent)는 label별로 완료율 집계.
    """
        
    # questId별로 가장 최신 상태만 추출
    df = df.copy()
    df["actionTime"] = pd.to_datetime(df["actionTime"])
    latest_status = df.sort_values("actionTime").groupby("questId").tail(1)

    # group_col 판단
    if "questType" in df.columns:
        if latest_status["questType"].eq("parent").all():
            group_col = "label"
        elif latest_status["questType"].eq("daily").all():
            group_col = "questName"
        else:
            raise ValueError("혼합 데이터셋입니다. 분리해서 주세요.")
    else:
        raise ValueError("questType 정보가 필요합니다.")

    # group별 전체 개수 및 COMPLETED 개수 집계
    total = latest_status[group_col].value_counts().sort_index()
    completed = latest_status[latest_status["currentState"] == "COMPLETED"][group_col].value_counts().sort_index()

    result = pd.DataFrame({
        group_col: total.index,
        "completion_rate": completed / total
    }).fillna(0)

    return result
