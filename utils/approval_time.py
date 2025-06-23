import pandas as pd

def approval_time(df):
    """
    완료된 퀘스트(questId)에 대해
    'PENDING_APPROVAL' → 'APPROVED'까지 평균 소요 시간을 'X시간 Y분'으로 반환
    """
    pending = df[df["currentState"] == "PENDING_APPROVAL"][["questId", "actionTime"]]
    approved = df[df["currentState"] == "APPROVED"][["questId", "actionTime"]]
    merged = pd.merge(pending, approved, on="questId", suffixes=("_pending", "_approved"))

    if merged.empty:
        return {"avg_minutes": None, "formatted": None}

    merged["duration"] = (merged["actionTime_approved"] - merged["actionTime_pending"]).dt.total_seconds()
    avg_seconds = merged["duration"].mean()
    avg_minutes = int(avg_seconds // 60)
    avg_hours = int(avg_minutes // 60)
    avg_minutes_remain = int(avg_minutes % 60)
    formatted = f"{avg_hours}시간 {avg_minutes_remain}분"

    return {
        "avg_minutes": avg_seconds / 60 if avg_seconds is not None else None,
        "formatted": formatted,
    }