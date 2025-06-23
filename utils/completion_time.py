import numpy as np
import pandas as pd
def daily_completion_time(df):
    """
    APPROVED된 퀘스트(questId)에 한해,
    최초 PENDING_APPROVAL 시각(2시간 bin) 분포 반환
    """
    # 1. APPROVED된 questId만 추출
    approved_ids = set(df[df["currentState"] == "APPROVED"]["questId"].values)
    if not approved_ids:
        return {"result": []}
    
    # 2. 전체에서 PENDING_APPROVAL + 위 questId만 추출
    pending = df[(df["currentState"] == "PENDING_APPROVAL") &
                 (df["questId"].isin(approved_ids))].copy()
    if pending.empty:
        return {"result": []}
    
    # 3. questId별 최초 PENDING_APPROVAL 시각만 남김
    pending = pending.sort_values("actionTime").drop_duplicates(subset=["questId"], keep="first")
    
    # 4. 시간 binning
    pending["hour"] = pending["actionTime"].dt.hour
    bins = np.arange(0, 25, 2)
    labels = [f"{i}-{i+2}" for i in range(0, 24, 2)]
    pending["time_bin"] = pd.cut(pending["hour"], bins=bins, labels=labels, right=False, include_lowest=True)
    
    # 5. questName별 분포 집계
    result = []
    for quest, group in pending.groupby("questName"):
        dist = group["time_bin"].value_counts().sort_index()
        dist = dist.reindex(labels, fill_value=0)
        distribution = [{"time_bin": label, "count": int(dist[label])} for label in labels]
        result.append({"quest_name": quest, "distribution": distribution})
    
    return {"result": result}

def parent_completion_time(df):
    """
    APPROVED된 부모퀘스트(questId)에 한해,
    최초 PENDING_APPROVAL 시각(2시간 bin) 분포를 label별로 반환
    """
    # 1. APPROVED된 questId만 추출
    approved_ids = set(df[df["currentState"] == "APPROVED"]["questId"].values)
    if not approved_ids:
        return {"result": []}
    
    # 2. 전체에서 PENDING_APPROVAL + 위 questId만 추출
    pending = df[(df["currentState"] == "PENDING_APPROVAL") &
                 (df["questId"].isin(approved_ids))].copy()
    if pending.empty:
        return {"result": []}
    
    # 3. questId별 최초 PENDING_APPROVAL 시각만 남김
    pending = pending.sort_values("actionTime").drop_duplicates(subset=["questId"], keep="first")
    
    # 4. 시간 binning
    pending["hour"] = pending["actionTime"].dt.hour
    bins = np.arange(0, 25, 2)
    labels = [f"{i}-{i+2}" for i in range(0, 24, 2)]
    pending["time_bin"] = pd.cut(pending["hour"], bins=bins, labels=labels, right=False, include_lowest=True)
    
    # 5. label별 분포 집계 (label이 없으면 'Unknown'으로 표기)
    result = []
    for label, group in pending.groupby("label"):
        label_name = label if pd.notnull(label) else "Unknown"
        dist = group["time_bin"].value_counts().sort_index()
        dist = dist.reindex(labels, fill_value=0)
        distribution = [{"time_bin": lbl, "count": int(dist[lbl])} for lbl in labels]
        result.append({"label": label_name, "distribution": distribution})
    
    return {"result": result}