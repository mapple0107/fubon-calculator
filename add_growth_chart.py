import shutil

path = "dca.html"
shutil.copy(path, path + ".bak_growth")
print("已備份")

with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# 找到 renderFundChart 函式，整段替換成新版（改成累積走勢面積圖）
start_marker = "function renderFundChart(key) {"
end_marker = "function onFundSelectChange() {"

start_idx = c.find(start_marker)
end_idx = c.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("❌ 找不到 renderFundChart 區塊，請確認 dca.html 內容")
else:
    new_func = '''function renderFundChart(key) {
  const fund = FUND_PERFORMANCE[key];
  const box = document.getElementById('dcaFundChart');
  if (!fund) { box.style.display = 'none'; box.innerHTML = ''; return; }

  // 模擬每月投入固定金額，用年度報酬率換算成月報酬率複利計算
  const monthlyInvest = 10000; // 模擬用每月投入金額(元)
  let principal = 0, value = 0;
  const points = []; // {year, principal, value}
  fund.annualReturns.forEach(yr => {
    const monthlyRate = Math.pow(1 + yr.r / 100, 1/12) - 1;
    for (let m = 0; m < 12; m++) {
      value = value * (1 + monthlyRate) + monthlyInvest;
      principal += monthlyInvest;
    }
    points.push({ year: yr.y, principal, value });
  });

  const maxVal = Math.max(...points.map(p => p.value));
  const w = 100, h = 100;
  const n = points.length;

  const toXY = (i, val) => {
    const x = (i / (n - 1)) * w;
    const y = h - (val / maxVal) * h;
    return [x, y];
  };

  const valuePath = points.map((p, i) => toXY(i, p.value).join(',')).join(' L ');
  const principalPath = points.map((p, i) => toXY(i, p.principal).join(',')).join(' L ');
  const areaClose = `L ${w},${h} L 0,${h} Z`;

  const finalPrincipal = points[points.length-1].principal;
  const finalValue = points[points.length-1].value;
  const cagr = calcCAGR(fund.cumulativeReturnSinceInception, fund.inceptionDate);

  const yearLabels = points.map((p, i) =>
    `<div style="position:absolute; left:${(i/(n-1))*100}%; transform:translateX(-50%); font-size:10px; color:#86868b;">${p.year}</div>`
  ).join('');

  box.innerHTML = `
    <div style="background:#f9f9fb; border-radius:14px; padding:14px 16px;">
      <div style="font-size:12px; color:#86868b; margin-bottom:2px;">近10年模擬定期定額累積走勢（每月投入 ${fmt(monthlyInvest)} 元）</div>
      <div style="font-size:11px; color:#c7c7cc; margin-bottom:10px;">依年度實際報酬率換算，僅供參考，過去績效不代表未來表現</div>
      <svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width:100%; height:180px; display:block;">
        <path d="M 0,${h} L ${valuePath} ${areaClose}" fill="#cfe4ff" opacity="0.6"></path>
        <path d="M ${valuePath}" fill="none" stroke="#0071e3" stroke-width="1"></path>
        <path d="M ${principalPath}" fill="none" stroke="#1d1d1f" stroke-width="0.8" stroke-dasharray="2,1.5"></path>
      </svg>
      <div style="position:relative; height:16px; margin-top:2px;">${yearLabels}</div>
      <div style="display:flex; gap:16px; margin-top:10px; font-size:12px;">
        <div><span style="display:inline-block;width:10px;height:10px;background:#0071e3;border-radius:2px;margin-right:4px;"></span>累積金額 ${fmt(finalValue)} 元</div>
        <div><span style="display:inline-block;width:10px;height:2px;background:#1d1d1f;margin-right:4px;vertical-align:middle;"></span>投入本金 ${fmt(finalPrincipal)} 元</div>
      </div>
      <div style="font-size:13px; color:#0071e3; margin-top:8px; font-weight:700;">成立至今年化報酬率（CAGR）：${cagr.toFixed(2)}%</div>
    </div>
  `;
  box.style.display = 'block';
}

'''
    c = c[:start_idx] + new_func + c[end_idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("✅ 已改成累積走勢面積圖")
