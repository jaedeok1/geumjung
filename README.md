# 카포스 금중자동차공업사 홈페이지

남양주 화도읍 자동차 정비소 원페이지 사이트. 스크롤에 따라 자동차 도면이
타이어 → 엔진 → 오일 → 브레이크 순으로 확대되며 실사 컷으로 전환되는
인터랙티브 구조이며, 전환 목표는 전화 문의(010-2370-0303)다.

## 구조

- `page.src.html` — 소스 (스타일·마크업·스크립트). **수정은 이 파일에.**
- `assets/*.webp` — higgsfield로 생성한 실사 컷 (빌드 시 base64로 내장)
- `build.py` — `python3 build.py` 실행 시 `index.html`(배포용 단일 파일) 생성
- `index.html` — 빌드 결과물. 직접 수정하지 말 것.

## 배포

`main`에 푸시하면 GitHub Actions가 GitHub Pages로 자동 배포한다.
커스텀 도메인 연결 시 `build.py`의 `SITE_URL`과 `robots.txt`·`sitemap.xml`의
주소를 함께 바꿔서 다시 빌드할 것.
