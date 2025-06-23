from fastapi import APIRouter, Query
from utils.make_graph import (
    make_daily_completion_rate_graph,
    make_parent_completion_rate_graph,
    make_daily_completion_time_graph,
    make_parent_completion_time_graph,
    make_parent_completion_reward_graph,
    make_parent_approval_time_graph,
    make_daily_approval_time_graph
)

router = APIRouter()

@router.get("/daily/completion_rate")
def daily_completion_rate(childId: str, period: str = Query("all")):
    filter_val = period == "recent7"
    return make_daily_completion_rate_graph(childId, filter=filter_val)

@router.get("/parent/completion_rate")
def parent_completion_rate(childId: str, period: str = Query("all")):
    filter_val = period == "recent7"
    return make_parent_completion_rate_graph(childId, filter=filter_val)

@router.get("/daily/completion_time")
def daily_completion_time(childId: str, period: str = Query("all")):
    filter_val = period == "recent7"
    return make_daily_completion_time_graph(childId, filter=filter_val)

@router.get("/parent/completion_time")
def parent_completion_time(childId: str, period: str = Query("all")):
    filter_val = period == "recent7"
    return make_parent_completion_time_graph(childId, filter=filter_val)

@router.get("/parent/completion_reward")
def parent_completion_reward(childId: str, period: str = Query("all")):
    filter_val = period == "recent7"
    return make_parent_completion_reward_graph(childId, filter=filter_val)

@router.get("/parent/approval_time")
def parent_approval_time(childId: str, period: str = Query("all")):
    filter_val = period == "recent7"
    return make_parent_approval_time_graph(childId, filter=filter_val)

@router.get("/daily/approval_time")
def daily_approval_time(childId: str, period: str = Query("all")):
    filter_val = period == "recent7"
    return make_daily_approval_time_graph(childId, filter=filter_val)

target_id = '72474ee2a388a1d05e88e89ce507f795'
result = make_parent_completion_reward_graph(target_id, True)
print(result)