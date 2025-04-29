from .main import server


def main():
    server.run(transport="stdio")