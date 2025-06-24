import pandas as pd
import numpy as np

def completion_rate(df):
    """
    일일퀘스트(df_daily)는 questName별, 
    부모퀘스트(df_parent)는 label별로 완료율 집계.
    """
    # NaN일 경우 문자열로 바꿔서 안전하게 처리
    df = df.copy()
    # 일일퀘스트: label이 NaN이면서 questType == "daily"
    if "questType" in df.columns:
        if (
            df["questType"].eq("daily").all()
            or (df["label"].isnull().all() and df["questType"].eq("daily").all())
        ):
            group_col = "questName"
        elif (
            df["questType"].eq("parent").all()
            or (df["label"].notnull().any() and df["questType"].eq("parent").all())
        ):
            group_col = "label"
        else:
            # 혼합 데이터면 group_col을 동적으로 처리
            group_col = np.where(
                df["questType"] == "daily", "questName", "label"
            )
            raise ValueError("혼합 데이터셋입니다. questType별로 분리해서 사용해주세요.")
    elif "questName" in df.columns and df["label"].isnull().all():
        group_col = "questName"
    elif "label" in df.columns and df["label"].notnull().any():
        group_col = "label"
    else:
        raise ValueError("적절한 집계 기준 컬럼이 없습니다.")

    # 집계 (group_col이 str이면 바로, 배열이면 groupby)
    if isinstance(group_col, str):
        total_counts = df[group_col].value_counts().sort_index()
        approved_counts = df[df["currentState"] == "APPROVED"][group_col].value_counts().sort_index()
        result = pd.DataFrame({
            "total_count": total_counts,
            "approved_count": approved_counts
        }).fillna(0)
        result["completion_rate"] = result["approved_count"] / result["total_count"]
        result = result.reset_index().rename(columns={"index": group_col})
        
        # group_col과 completion_rate만 추출
        result = result[[group_col, "completion_rate"]]
    else:
        raise ValueError("혼합 데이터셋은 현재 지원하지 않습니다. daily/parent 분리해서 주세요.")

    return result
