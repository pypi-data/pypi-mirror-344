from .main import server


def main():
    import uvicorn
    """启动 FastAPI 服务器"""
    uvicorn.run(server)

# if __name__ == "__main__":
#     main()