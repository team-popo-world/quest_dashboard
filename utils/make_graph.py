import pandas as pd
from db.mongo_handler import load_mongo_data
from utils.date_filter import filter_date
from utils.completion_rate import completion_rate
from utils.completion_time import daily_completion_time
from utils.completion_time import parent_completion_time
from utils.completion_reward import completion_reward
from utils.approval_time import approval_time
import json

df_parent, df_daily = load_mongo_data()

# 일일퀘스트 완료율 집계 함수
def make_daily_completion_rate_graph(childId, filter: bool = False):
    global df_daily
    df = df_daily[df_daily["childId"] == childId].copy()
    if filter:
        df = filter_date(df)
    result = completion_rate(df)
    result = result.to_dict(orient="records")

    # childId 포함한 구조로 반환
    return {
        "childid": childId,
        "result": result
    }

# 부모퀘스트 완료율 집계 함수
def make_parent_completion_rate_graph(childId, filter: bool = False):
    global df_parent
    df = df_parent[df_parent["childId"] == childId].copy()
    if filter:
        df = filter_date(df)
    result = completion_rate(df)
    result = result.to_dict(orient="records")
    return {
        "childid": childId,
        "result": result
    }

# 일일퀘스트 시간분포 함수
def make_daily_completion_time_graph(childId, filter: bool = False):
    global df_daily
    df = df_daily[df_daily["childId"] == childId].copy()
    if filter:
        df = filter_date(df)
    result = daily_completion_time(df)
    return {
        "childid": childId,
        "result": result
    }

# 부모퀘스트 시간분포 함수
def make_parent_completion_time_graph(childId, filter: bool = False):
    global df_parent
    df = df_parent[df_parent["childId"] == childId].copy()
    if filter:
        df = filter_date(df)
    result = parent_completion_time(df)
    return {
        "childid": childId,
        "result": result
    }

# 부모퀘스트에 대해 보상-완료율 관계 및 회귀직선 계산 함수
def make_parent_completion_reward_graph(childId, filter: bool = False):
    global df_parent
    df = df_parent[df_parent["childId"] == childId].copy()
    if filter:
        df = filter_date(df)
    result = completion_reward(df)

    # childId 포함한 전체 구조로 감싸기
    output = {
        "childid": childId,
        "result": result.get("result", []),
        "regression_line": result.get("regression_line", [])
    }

    return output

# 부모퀘스트 평균 승인대기시간 함수
def make_parent_approval_time_graph(childId, filter: bool = False):
    global df_parent
    df = df_parent[df_parent["childId"] == childId].copy()
    if filter:
        df = filter_date(df)
    result = approval_time(df)
    return {
        "childid": childId,
        "result": result
    }

# 일일퀘스트 평균 승인대기시간 함수
def make_daily_approval_time_graph(childId, filter: bool = False):
    global df_daily
    df = df_daily[df_daily["childId"] == childId].copy()
    if filter:
        df = filter_date(df)
    result = approval_time(df)
    return {
        "childid": childId,
        "result": result
    }

