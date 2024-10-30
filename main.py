from app import create_app
from config.config import settings

app = create_app(settings)


@app.get("/healthcheck")
async def healthcheckk():
    return "ok. 8"