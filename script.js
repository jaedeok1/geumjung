/* 카포스 금중자동차공업사 — 인터랙션 */
(function () {
  'use strict';

  /* ---------- 모바일 메뉴 토글 ---------- */
  var toggle = document.getElementById('navToggle');
  var menu = document.getElementById('navMenu');

  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
    });

    menu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        menu.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', '메뉴 열기');
      });
    });
  }

  /* ---------- 푸터 연도 자동 갱신 ---------- */
  var yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  /* =====================================================================
     네이버 지도 임베드
     ---------------------------------------------------------------------
     ▶ 사용 방법 (무료)
       1) https://www.ncloud.com 가입 후 콘솔 접속
       2) Services > AI·Application Service > Maps 신청 (Web 다이내믹 지도)
       3) 애플리케이션 등록 시 "Web 서비스 URL"에 실제 홈페이지 도메인 등록
       4) 발급된 Client ID(키)를 아래 NAVER_MAP_CLIENT_ID 에 붙여넣기
       5) 정확한 좌표는 https://map.naver.com 에서 위치 확인 후 위/경도 교체

     키를 넣지 않으면 지도 대신 "네이버 지도에서 보기" 폴백이 표시됩니다.
     ===================================================================== */
  var NAVER_MAP_CLIENT_ID = ''; // ← 여기에 네이버 지도 Client ID 입력

  // 카포스 금중자동차공업사 좌표 (대략값 — 실제 좌표로 교체 권장)
  var SHOP_LAT = 37.6416;
  var SHOP_LNG = 127.3096;

  var mapWrap = document.querySelector('.location__map');
  var mapEl = document.getElementById('naverMap');

  if (NAVER_MAP_CLIENT_ID && mapEl) {
    var s = document.createElement('script');
    // 구버전 키는 파라미터명이 ncpClientId 일 수 있습니다.
    s.src = 'https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId=' + NAVER_MAP_CLIENT_ID;
    s.async = true;
    s.onload = function () {
      if (!window.naver || !window.naver.maps) return;
      var center = new naver.maps.LatLng(SHOP_LAT, SHOP_LNG);
      var map = new naver.maps.Map(mapEl, {
        center: center,
        zoom: 16,
        scrollWheel: false
      });
      new naver.maps.Marker({ position: center, map: map, title: '카포스 금중자동차공업사' });
      if (mapWrap) mapWrap.classList.add('is-live');
    };
    s.onerror = function () {
      // 로드 실패 시 폴백 유지 (아무것도 하지 않음)
    };
    document.head.appendChild(s);
  }
})();
