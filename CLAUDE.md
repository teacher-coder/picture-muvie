# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PicMuvie — 초등학교 교사가 노래 가사를 검색하고, 학급 인원수에 맞게 조정한 뒤 Word 문서로 다운로드하는 풀스택 웹 앱.

- **Frontend**: Vue 3 + Vite + Tailwind CSS + Pinia
- **Backend**: Django 4.1 + Django Ninja (REST API)
- **DB**: PostgreSQL 14
- **Infra**: Docker Compose + Nginx + GitHub Actions CD → AWS Lightsail
- **Production**: `https://picmuvie.zzolab.com`

## Development Commands

### Docker (권장)

```bash
# 개발 환경 실행
docker-compose -f docker-compose.dev.yml up --build

# 프로덕션 환경 실행
docker-compose -f docker-compose.yml up --build -d
```

### Frontend (`/frontend`)

```bash
npm install
npm run dev          # Vite dev server (port 5173)
npm run build        # Production build
npm run test:unit    # Vitest (jsdom)
npm run lint         # ESLint + Prettier
```

### Backend (`/backend`)

```bash
poetry install
python manage.py runserver 0.0.0.0:8000
python manage.py makemigrations && python manage.py migrate
python manage.py collectstatic --no-input
```

Production: `gunicorn picture_muvie.wsgi -w 3 -b 0.0.0.0:8000`

## Architecture

```
frontend/src/
├── views/HomeView.vue        # 메인 UI (단일 페이지)
├── api/
│   ├── SetAxios.js           # Axios 인스턴스
│   ├── urls.js               # 엔드포인트 정의
│   └── modules/lyrics.js     # getLyrics, downloadLyricsDocx
├── utils.js                  # 파일 다운로드, 한글/영문 감지
└── components/               # TheHeader, TheFooter, ButtonDropDown

backend/picture_muvie/
├── api.py                    # Django Ninja 라우트
├── docs.py                   # docxtpl 기반 Word 문서 생성
├── settings.py               # Django 설정 (ko-kr, Asia/Seoul)
├── utils/
│   ├── naver_search.py       # 네이버 웹 검색 API
│   ├── scraper.py            # 지니/멜론/벅스/lyrics.com 스크래핑
│   ├── search_lyrics.py      # Musixmatch API + iTunes 검색
│   └── optimize_lyrics.py    # 글자 수 기반 폰트 크기 최적화
└── templates/title.docx      # Word 문서 템플릿
```

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/lyrics?query=` | 가사 검색 (source, title, artist, lyrics 반환) |
| POST | `/api/makedocx` | Word 문서 생성 및 다운로드 |

### Data Flow

1. 사용자가 곡 검색 → Naver 웹 검색 → 지니/멜론/벅스 스크래핑으로 가사 획득
2. 사용자가 학생 수에 맞게 가사 줄 수 조정
3. 다운로드 요청 → `docxtpl`로 Word 문서 생성 (한글/영문 비율에 따라 폰트 크기 자동 최적화)

## Environment Variables

`.env.sample` 파일 참고. 백엔드(`/backend/.env`)와 프론트엔드(`/frontend/.env`) 각각 필요.

**Backend 필수**: `MUSIXMATCH_API_KEY`, `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET`, `DJANGO_SECRET_KEY`, DB 관련 변수
**Frontend 필수**: `VITE_API_URL`

## Deployment

GitHub Actions CD: `main` 브랜치 push → SSH로 Lightsail 접속 → `docker-compose up --build -d`

## Conventions

- Django admin 경로: `/muviemaker/`
- 로깅: `/backend/logs/picture_muvie.log` (rotating, 5MB)
- Nginx dev: 포트 8000에서 프론트/백엔드 프록시, prod: SSL + SPA fallback
