import shutil

path = "index.html"
backup = path + ".bak2"
shutil.copy(path, backup)
print(f"已備份至 {backup}")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. HTML：美金匯率欄位加上即時匯率提示
old_html = '''      <div class="field">
        <label>美金匯率</label>
        <div class="input-wrap">
          <input type="number" id="usdRate" value="31.5" step="0.1">
          <span class="unit">TWD/USD</span>
        </div>
      </div>'''

new_html = '''      <div class="field">
        <label>美金匯率</label>
        <div class="input-wrap">
          <input type="number" id="usdRate" value="31.5" step="0.1">
          <span class="unit">TWD/USD</span>
        </div>
        <div class="fee-info" id="rate-info" style="margin-top:6px;">載入即時匯率中…</div>
      </div>'''

# 2. CSS：加上 rate-info 樣式
old_css = '''  .fee-info {
    font-size: 12px; color: #0071e3; background: #eef6ff;
    border-radius: 10px; padding: 8px 12px; margin-top: 8px; font-weight: 500;
    font-family: "SF Mono", "SFMono-Regular", Menlo, Consolas, monospace;
    font-variant-numeric: tabular-nums;
  }'''

new_css = old_css + '''
  #rate-info { background: #f5f5f7; color: #86868b; font-weight: 400; cursor: pointer; }
  #rate-info:hover { background: #eef6ff; color: #0071e3; }'''

# 3. JS：加上 fetchLiveRate 函式
old_js = "function updateFeeRate() { updateFeeInfo(); }"

new_js = '''function updateFeeRate() { updateFeeInfo(); }

async function fetchLiveRate() {
  const info = document.getElementById('rate-info');
  if (!info) return;
  info.textContent = '載入即時匯率中…';
  try {
    const res = await fetch('https://open.er-api.com/v6/latest/USD');
    const data = await res.json();
    const twd = data.rates && data.rates.TWD;
    if (twd) {
      document.getElementById('usdRate').value = twd.toFixed(3);
      const now = new Date();
      const hh = String(now.getHours()).padStart(2,'0');
      const mm = String(now.getMinutes()).padStart(2,'0');
      info.textContent = `即時匯率 ${twd.toFixed(3)}（更新於 ${hh}:${mm}，點擊重新整理）`;
    } else {
      info.textContent = '無法取得即時匯率，請手動輸入（點擊重試）';
    }
  } catch (e) {
    info.textContent = '無法取得即時匯率，請手動輸入（點擊重試）';
  }
}
document.addEventListener('DOMContentLoaded', () => {
  const el = document.getElementById('rate-info');
  if (el) el.addEventListener('click', fetchLiveRate);
});'''

# 4. JS：初始化那幾行加上 fetchLiveRate()
old_init = '''addAllocFund();
addCompareFund();
onPremiumChange();'''

new_init = '''addAllocFund();
addCompareFund();
onPremiumChange();
fetchLiveRate();'''

replacements = [
    ("HTML 匯率欄位", old_html, new_html),
    ("CSS 樣式", old_css, new_css),
    ("JS fetchLiveRate 函式", old_js, new_js),
    ("JS 初始化", old_init, new_init),
]

ok = True
for label, old, new in replacements:
    if old not in content:
        print(f"❌ 找不到符合的區塊：{label}，請手動檢查。")
        ok = False
    else:
        content = content.replace(old, new)
        print(f"✅ 已修改：{label}")

if ok:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("\n✅ 全部修改完成，已寫入 index.html")
else:
    print("\n⚠️ 部分區塊修改失敗，index.html 尚未變更，請檢查上面錯誤訊息。")
