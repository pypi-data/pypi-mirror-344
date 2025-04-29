from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="获取IP API",
    version="1.0.0",
    description="根据当前请求获取其公网IP地址",
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/get_log_client_ip", summary="获取当前客户端IP")
async def log_client_ip(request: Request)-> str:
    # 获取真实 IP（支持反向代理）
    client_ip = (
            request.headers.get("x-forwarded-for", "").split(",")[0]
            or request.client.host
    )
    # 将 IP 存入请求状态，供后续路由使用
    request.state.client_ip = client_ip
    print(f"Client IP: {client_ip}")  # 打印到日志
    return client_ip


