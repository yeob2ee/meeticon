from __future__ import annotations

import os
import time
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
HF_API_BASE = "https://router.huggingface.co/hf-inference/models"


class HFError(Exception):
    pass


def hf_text_to_image_bytes(prompt: str, model: str, timeout: int = 120) -> bytes:
    """
    Hugging Face Inference API로 text->image 생성 후 이미지 bytes 반환.
    무료 티어에서 503(로딩/대기) 나올 수 있어 2~3회 재시도.
    """
    if not HF_TOKEN:
        raise HFError("HF_TOKEN이 비어 있어요. 프로젝트 루트의 .env를 확인하세요.")

    url = f"{HF_API_BASE}/{model}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Accept": "image/png",  # 가능하면 PNG로 받기
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "num_inference_steps": 35,
            "guidance_scale": 8.5,
            "width": 512,
            "height": 512,
            "negative_prompt": 
                "grid, sprite sheet, collage, multiple panels, icon set, contact sheet, "
                "background scene, room, landscape, text, watermark, logo, frame, border, "
                "photo, realistic, blurry, messy"
            },
        }

    last_err: Optional[str] = None

    for attempt in range(3):
        r = requests.post(url, headers=headers, json=payload, timeout=timeout)

        # 성공: 이미지 bytes
        if r.status_code == 200 and r.headers.get("content-type", "").startswith("image/"):
            return r.content

        # 모델 로딩/대기(무료에서 흔함)
        if r.status_code == 503:
            try:
                j = r.json()
                wait = float(j.get("estimated_time", 5))
            except Exception:
                wait = 5.0
            time.sleep(min(10.0, max(2.0, wait)))
            last_err = f"503 모델 대기(재시도 {attempt+1}/3)"
            continue

        # 그 외 오류
        try:
            last_err = r.text
        except Exception:
            last_err = f"HTTP {r.status_code}"
        break

    raise HFError(f"Hugging Face 호출 실패: {last_err}")

    