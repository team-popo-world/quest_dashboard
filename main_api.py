from fastapi import FastAPI
from routers import graph

app = FastAPI()

# '/graph' prefix로 모든 그래프 관련 엔드포인트 제공
app.include_router(graph.router, prefix="/graph")