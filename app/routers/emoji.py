from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.emoji_hf import hf_text_to_image_bytes, HFError
from app.emoji_store import (
    init_emoji_db, insert_emoji_item, update_emoji_filename_png,
    list_recent_emoji_items, get_emoji_item, delete_emoji_item
)
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path


router = APIRouter(prefix="/emoji", tags=["emoji"])
templates = Jinja2Templates(directory="templates")

DUMMY_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"


@router.get("", response_class=HTMLResponse)
def emoji_home(request: Request):
    init_emoji_db()
    return templates.TemplateResponse(
        "emoji.html",
        {"request": request, "result": None},
    )


@router.post("/generate", response_class=HTMLResponse)
def emoji_generate(request: Request, prompt: str = Form(...)):
    init_emoji_db()

    prompt = prompt.strip()
    if not prompt:
        return templates.TemplateResponse(
            "emoji.html",
            {"request": request, "result": "프롬프트가 비어 있어요.", "image_url": None},
        )

    # 1) 먼저 DB에 row 만들고 id 확보
    new_id = insert_emoji_item(
        prompt=prompt,
        model=DUMMY_MODEL,
        filename_png="pending.png",
    )

    hf_prompt = (
        f"single cute {prompt} emoji sticker, one object only, centered, isolated, "
        f"simple flat vector icon, thick clean outline, high contrast, "
        f"no background, sticker cutout, minimal detail"
    )



    # 2) Hugging Face로 이미지 생성
    try:
        img_bytes = hf_text_to_image_bytes(prompt=hf_prompt, model=DUMMY_MODEL)
    except HFError as e:
        return templates.TemplateResponse(
            "emoji.html",
            {"request": request, "result": f"이미지 생성 실패: {e}", "image_url": None},
        )

    # 3) 파일 저장
    out_dir = Path("data/emoji/images")
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"emoji_{new_id}.png"
    out_path = out_dir / filename
    out_path.write_bytes(img_bytes)

    # 4) DB 파일명 업데이트
    update_emoji_filename_png(new_id, filename)

    # 5) 결과 페이지에 미리보기
    image_url = f"/media/emoji/{filename}"
    return templates.TemplateResponse(
        "emoji.html",
        {"request": request, "result": f"생성 완료! id={new_id}", "image_url": image_url},
    )

@router.get("/gallery", response_class=HTMLResponse)
def emoji_gallery(request: Request):
    init_emoji_db()
    items = list_recent_emoji_items(limit=50)
    return templates.TemplateResponse(
        "emoji_gallery.html",
        {"request": request, "items": items},
    )



@router.post("/{item_id}/delete")
def emoji_delete(request: Request, item_id: int):
    init_emoji_db()

    item = get_emoji_item(item_id)
    if not item:
        return RedirectResponse(url="/emoji/gallery", status_code=303)

    # 파일 삭제
    filename = item.get("filename_png")
    if filename and filename != "pending.png":
        path = Path("data/emoji/images") / filename
        if path.exists():
            path.unlink()

    # DB 삭제
    delete_emoji_item(item_id)

    return RedirectResponse(url="/emoji/gallery", status_code=303)