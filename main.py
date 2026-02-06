from fastapi import FastAPI
from app.routers.emoji import router as emoji_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="templates/static"), name="static")
app.mount("/media/emoji", StaticFiles(directory="data/emoji/images"), name="emoji_media")

app.include_router(emoji_router)

@app.get("/")
def root():
    return RedirectResponse(url="/emoji")
