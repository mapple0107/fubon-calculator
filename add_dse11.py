import shutil

path = "dca.html"
shutil.copy(path, path + ".bak_dse11")
print("已備份")

with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# 1. 在「投資設定」卡片裡加入基金選擇欄位
old_card = '''  <div class="card">
    <h2>投資設定</h2>
    <div class="grid3">
      <div class="field">
        <label>每月投入金額</label>
        <div class="input-wrap">
          <input type="number" id="dcaMonthly" value="10000" step="1000">
          <span class="unit">元</span>
        </div>
      </div>
      <div class="field">
        <label>預期年化報酬率</label>
        <div class="input-wrap">
          <input type="number" id="dcaRate" value="6" step="0.1">
          <span class="unit">%</span>
        </div>
      </div>
      <div class="field">
        <label>投資年期</label>
        <div class="input-wrap">
          <input type="number" id="dcaYears" value="10" step="1">
          <span class="unit">年</span>
        </div>
      </div>
    </div>
  </div>'''

new_card = '''  <div class="card">
    <h2>投資設定</h2>
    <div class="field" style="margin-bottom:16px;">
      <label>參考基金績效（選填）</label>
      <select id="dcaFundSelect" onchange="onFundSelectChange()">
        <option value="">手動輸入年化報酬率</option>
        <option value="DSE11">DSE11｜安聯台灣科技證券投資信託基金</option>
      </select>
    </div>
    <div id="dcaFundChart" style="display:none; margin-bottom:16px;"></div>
    <div class="grid3">
      <div class="field">
        <label>每月投入金額</label>
        <div class="input-wrap">
          <input type="number" id="dcaMonthly" value="10000" step="1000">
          <span class="unit">元</span>
        </div>
      </div>
      <div class="field">
        <label>預期年化報酬率</label>
        <div class="input-wrap">
          <input type="number" id="dcaRate" value="6" step="0.1">
          <span class="unit">%</span>
        </div>
      </div>
      <div class="field">
        <label>投資年期</label>
        <div class="input-wrap">
          <input type="number" id="dcaYears" value="10" step="1">
          <span class="unit">年</span>
        </div>
      </div>
    </div>
  </div>'''

ok = True
if old_card not in c:
    print("❌ 找不到投資設定卡片，請確認 dca.html 內容")
    ok = False
else:
    c = c.replace(old_card, new_card)
    print("✅ 已加入基金選擇欄位")

# 2. 加入 select 的樣式（沿用 .field select 樣式即可，不用額外加）

# 3. 加入 JS：基金資料 + 選擇邏輯 + 走勢圖
old_js = "function fmt(n, dec=0)"
new_js = '''const FUND_PERFORMANCE = {
  DSE11: {
    label: "DSE11｜安聯台灣科技證券投資信託基金",
    oneYearReturn: 217.46,
    updated: "2026/08/06",
    monthly: [
      {m:"2025/08", r:12.85}, {m:"2025/09", r:5.36}, {m:"2025/10", r:16.34},
      {m:"2025/11", r:7.16},  {m:"2025/12", r:10.37},{m:"2026/01", r:16.38},
      {m:"2026/02", r:9.48},  {m:"2026/03", r:-1.37},{m:"2026/04", r:40.5},
      {m:"2026/05", r:17.65}, {m:"2026/06", r:3.55}, {m:"2026/07", r:-21.78}
    ]
  }
};

function renderFundChart(key) {
  const fund = FUND_PERFORMANCE[key];
  const box = document.getElementById('dcaFundChart');
  if (!fund) { box.style.display = 'none'; box.innerHTML = ''; return; }

  const vals = fund.monthly.map(x => x.r);
  const maxAbs = Math.max(...vals.map(Math.abs), 1);
  const barW = 100 / vals.length;

  let bars = '';
  fund.monthly.forEach((x, i) => {
    const h = (Math.abs(x.r) / maxAbs) * 45;
    const color = x.r >= 0 ? '#0071e3' : '#d0392b';
    const yTop = x.r >= 0 ? 50 - h : 50;
    bars += `<div style="position:absolute; left:${i*barW}%; width:${barW*0.7}%; bottom:${x.r>=0?'50%':(50-h/45*45)+'%'}; height:${h}%; background:${color}; border-radius:2px;" title="${x.m}: ${x.r}%"></div>`;
  });

  box.innerHTML = `
    <div style="background:#f9f9fb; border-radius:14px; padding:14px 16px;">
      <div style="font-size:12px; color:#86868b; margin-bottom:8px;">近12個月月報酬率（資料時間 ${fund.updated}）</div>
      <div style="position:relative; height:90px; border-bottom:1px solid #e5e5ea;">${bars}</div>
      <div style="font-size:12px; color:#0071e3; margin-top:8px; font-weight:600;">近一年累積報酬率：${fund.oneYearReturn}%</div>
    </div>
  `;
  box.style.display = 'block';
}

function onFundSelectChange() {
  const key = document.getElementById('dcaFundSelect').value;
  renderFundChart(key);
  const rateInput = document.getElementById('dcaRate');
  if (key && FUND_PERFORMANCE[key]) {
    rateInput.value = FUND_PERFORMANCE[key].oneYearReturn;
  }
}

function fmt(n, dec=0)'''

if old_js not in c:
    print("❌ 找不到 fmt 函式，請確認 dca.html 內容")
    ok = False
else:
    c = c.replace(old_js, new_js)
    print("✅ 已加入基金績效與走勢圖邏輯")

if ok:
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("\\n✅ dca.html 已全部修改完成")
else:
    print("\\n⚠️ 部分修改失敗，dca.html 內容未變更")
