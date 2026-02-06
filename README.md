# 🫐 Meeticon

Meeticon은 텍스트 프롬프트를 입력하면  
AI가 이미지를 생성해주는 **개인용 이모지 / 스티커 생성 웹 서비스**입니다.

Hugging Face Inference API를 활용하여  
가볍게 사용할 수 있는 “나만의 이모티콘 만들기”를 목표로 했습니다.

---

## ✨ 주요 기능

- 🖊️ 텍스트 프롬프트 기반 이미지 생성
- 🖼️ 생성된 이미지 갤러리 조회
- ⬇️ PNG 이미지 다운로드
- 🗑️ 생성 이미지 삭제
- 🔐 Hugging Face API Token을 `.env`로 안전하게 관리

---

## 🛠️ 기술 스택

- **Backend**: FastAPI
- **Frontend**: Jinja2 (Server-side HTML)
- **AI**: Hugging Face Inference API (Stable Diffusion 계열)
- **Database**: SQLite
- **Language**: Python 3.9+

---

## 📂 프로젝트 구조
```
Meeticon/
├── app/
│   ├── emoji_hf.py          # Hugging Face API 호출
│   ├── emoji_store.py       # SQLite 저장 로직
│   └── routers/
│       └── emoji.py         # 라우팅
├── templates/
│   ├── emoji.html           # 생성 페이지
│   ├── emoji_gallery.html   # 갤러리
│   └── static/
│       └── portal.css       # 스타일
├── main.py
├── requirements.txt
├── .env.example
└── README.md

```
---

## 🚀 실행 방법

### 1) 가상환경 생성 및 활성화

```
python -m venv .venv

source .venv/bin/activate
```

### 2) 라이브러리 설치

```
pip install -r requirements.txt
```

### 3) 환경변수 설정

.env.example을 참고하여 .env 파일을 생성합니다.

### 4) 서버 실행

```
uvicorn main:app --reload
```

브라우저에서 아래 주소로 접속합니다.

```
http://127.0.0.1:8000/emoji
```

---
## 🧪 사용 예시

울고 있는 딸기

happy face grape

simple pink candy

위 예시와 같이 짧고 단순한 프롬프트일수록

이모지/스티커 형태에 적합한 결과가 생성됩니다.

---
## ⚠️ 참고 사항


생성된 이미지는 개인용 / 실험용을 목적으로 합니다.

Hugging Face 무료 티어의 호출 제한이 적용될 수 있습니다.

env 파일은 GitHub에 업로드하지 않습니다.

---

## 📌 향후 개선 아이디어

	•	프롬프트 프리셋 제공
	•	스타일 선택 (line art, flat, cute 등)
	•	투명 배경 PNG 지원
	•	모바일 / 태블릿 최적화 UI
