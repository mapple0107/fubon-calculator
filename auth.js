// 共用密碼鎖：首頁、理財工具選單、建議書系統都共用同一道鎖，
// 同一個瀏覽器分頁內只要解鎖過一次，其他頁面就不用再輸入密碼。
// 這只是客戶端 JS 檢查，不是真正的安全機制（看原始碼就能繞過），
// 目的只是避免別人誤點進來，不是用來保護機密資料。
// 要改密碼，改下面這行就好。
(function () {
  const SITE_PASSWORD = "0000";
  const STORAGE_KEY = "mapleSiteUnlocked";

  function unlockPage() {
    const lock = document.getElementById('lock-screen');
    if (lock) lock.remove();
    const main = document.getElementById('main-content');
    if (main) main.style.display = '';
  }

  function injectLockScreen() {
    const lock = document.createElement('div');
    lock.id = 'lock-screen';
    lock.innerHTML = `
      <div class="lock-card">
        <div class="lock-icon">🔒</div>
        <h1>買樂理財工具</h1>
        <p>請輸入密碼以繼續</p>
        <input type="password" id="password-input" placeholder="●●●●" maxlength="20" autocomplete="off">
        <button id="unlock-btn">進入</button>
        <div id="lock-error"></div>
      </div>
    `;
    document.body.appendChild(lock);

    function tryUnlock() {
      const input = document.getElementById('password-input');
      const errorEl = document.getElementById('lock-error');
      if (input.value === SITE_PASSWORD) {
        sessionStorage.setItem(STORAGE_KEY, '1');
        unlockPage();
      } else {
        errorEl.textContent = '密碼錯誤，請再試一次';
        input.value = '';
        input.focus();
      }
    }
    document.getElementById('unlock-btn').addEventListener('click', tryUnlock);
    document.getElementById('password-input').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') tryUnlock();
    });
    document.getElementById('password-input').focus();
  }

  document.addEventListener('DOMContentLoaded', function () {
    if (sessionStorage.getItem(STORAGE_KEY) === '1') {
      unlockPage();
    } else {
      injectLockScreen();
    }
  });
})();
