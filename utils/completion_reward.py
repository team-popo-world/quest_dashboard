import numpy as np
import pandas as pd

def completion_reward(df):
    """
    부모퀘스트에 한해서, label별 평균 보상과 완료율 계산.
    그리고 보상-완료율 선형회귀 결과까지 반환.
    """
    # 1. label별 집계
    # (label, reward, completion_rate) DataFrame 만들기
    df = df.copy()
    df["actionTime"] = pd.to_datetime(df["actionTime"])
    latest_status = df.sort_values("actionTime").groupby("questId").tail(1)

    # 집계
    group = latest_status.groupby("label").agg(
        reward=("rewardPoint", "mean"),
        total_count=("label", "count"),
        completed_count=("currentState", lambda x: (x == "COMPLETED").sum())
    ).reset_index()
    group["completion_rate"] = group["completed_count"] / group["total_count"]

    # 2. 리턴용 리스트
    result = []
    for _, row in group.iterrows():
        result.append({
            "label": row["label"],
            "reward": float(row["reward"]),
            "completion_rate": float(round(row["completion_rate"], 4)),
        })

    # 3. 회귀선(최소제곱 직선) 계산
    if len(group) >= 2:
        x = group["reward"].values
        y = group["completion_rate"].values
        coef = np.polyfit(x, y, 1)  # 1차식 계수: 기울기, 절편
        x_line = np.array([x.min(), x.max()])
        y_line = coef[0] * x_line + coef[1]
        regression_line = [
            {"reward": float(x_line[0]), "completion_rate": float(round(y_line[0], 4))},
            {"reward": float(x_line[1]), "completion_rate": float(round(y_line[1], 4))}
        ]
    else:
        regression_line = []

    return {
        "result": result,
        "regression_line": regression_line
    }