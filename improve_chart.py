import shutil

path = "dca.html"
shutil.copy(path, path + ".bak_improve")
print("已備份")

with open(path, "r", encoding="utf-8") as f:
    c = f.read()

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

  const monthlyInvest = 10000;
  let principal = 0, value = 0;
  const points = [];
  fund.annualReturns.forEach(yr => {
    const monthlyRate = Math.pow(1 + yr.r / 100, 1/12) - 1;
    for (let m = 0; m < 12; m++) {
      value = value * (1 + monthlyRate) + monthlyInvest;
      principal += monthlyInvest;
    }
    points.push({ year: yr.y, principal, value });
  });

  const maxVal = Math.max(...points.map(p => p.value));
  const w = 600, h = 260, padTop = 20, padBottom = 30, padLeft = 10, padRight = 10;
  const plotH = h - padTop - padBottom;
  const n = points.length;

  const toXY = (i, val) => {
    const x = padLeft + (i / (n - 1)) * (w - padLeft - padRight);
    const y = padTop + plotH - (val / maxVal) * plotH;
    return [x, y];
  };

  // 平滑曲線：用簡單的三次貝茲近似 (Catmull-Rom 轉換)
  function smoothPath(pts) {
    if (pts.length < 3) return `M ${pts.map(p=>p.join(',')).join(' L ')}`;
    let d = `M ${pts[0][0]},${pts[0][1]}`;
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[i === 0 ? i : i - 1];
      const p1 = pts[i];
      const p2 = pts[i + 1];
      const p3 = pts[i + 2 < pts.length ? i + 2 : i + 1];
      const cp1x = p1[0] + (p2[0] - p0[0]) / 6;
      const cp1y = p1[1] + (p2[1] - p0[1]) / 6;
      const cp2x = p2[0] - (p3[0] - p1[0]) / 6;
      const cp2y = p2[1] - (p3[1] - p1[1]) / 6;
      d += ` C ${cp1x},${cp1y} ${cp2x},${cp2y} ${p2[0]},${p2[1]}`;
    }
    return d;
  }

  const valuePts = points.map((p, i) => toXY(i, p.value));
  const principalPts = points.map((p, i) => toXY(i, p.principal));
  const valuePath = smoothPath(valuePts);
  const principalPath = smoothPath(principalPts);
  const lastV = valuePts[valuePts.length - 1];
  const areaPath = `${valuePath} L ${lastV[0]},${padTop+plotH} L ${valuePts[0][0]},${padTop+plotH} Z`;

  const finalPrincipal = points[points.length-1].principal;
  const finalValue = points[points.length-1].value;
  const cagr = calcCAGR(fund.cumulativeReturnSinceInception, fund.inceptionDate);

  const yearLabels = points.map((p, i) => {
    const x = padLeft + (i / (n - 1)) * (w - padLeft - padRight);
    return `<text x="${x}" y="${h-8}" font-size="10" fill="#86868b" text-anchor="middle">${p.year}</text>`;
  }).join('');

  box.innerHTML = `
    <div style="background:linear-gradient(135deg,#f4f8ff,#fbfcff); border-radius:16px; padding:18px 20px; border:1px solid #e8f0ff;">
      <div style="font-size:13px; font-weight:700; color:#1d1d1f; margin-bottom:2px;">近10年模擬定期定額累積走勢</div>
      <div style="font-size:11px; color:#a0a0a5; margin-bottom:12px;">每月投入 ${fmt(monthlyInvest)} 元｜依年度實際報酬率換算，僅供參考，過去績效不代表未來表現</div>
      <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
        <svg viewBox="0 0 ${w} ${h}" style="flex:1; min-width:280px; height:220px;">
          <defs>
            <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#0071e3" stop-opacity="0.35"/>
              <stop offset="100%" stop-color="#0071e3" stop-opacity="0.02"/>
            </linearGradient>
          </defs>
          <path d="${areaPath}" fill="url(#areaGrad)"></path>
          <path d="${valuePath}" fill="none" stroke="#0071e3" stroke-width="2.5" stroke-linecap="round"></path>
          <path d="${principalPath}" fill="none" stroke="#c7c7cc" stroke-width="1.5" stroke-dasharray="4,3"></path>
          ${yearLabels}
        </svg>
        <div style="min-width:150px; display:flex; flex-direction:column; gap:14px;">
          <div>
            <div style="font-size:11px; color:#86868b; margin-bottom:2px;">累積金額</div>
            <div style="font-size:22px; font-weight:800; color:#0071e3; font-family:'SF Mono',Menlo,monospace;">${fmt(finalValue)}</div>
          </div>
          <div>
            <div style="font-size:11px; color:#86868b; margin-bottom:2px;">投入本金</div>
            <div style="font-size:16px; font-weight:700; color:#8a8a8e; font-family:'SF Mono',Menlo,monospace;">${fmt(finalPrincipal)}</div>
          </div>
          <div>
            <div style="font-size:11px; color:#86868b; margin-bottom:2px;">CAGR</div>
            <div style="font-size:16px; font-weight:700; color:#1a8a3c; font-family:'SF Mono',Menlo,monospace;">${cagr.toFixed(2)}%</div>
          </div>
        </div>
      </div>
    </div>
  `;
  box.style.display = 'block';
}

'''
    c = c[:start_idx] + new_func + c[end_idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("✅ 已改成漸層面積圖+右側大字標示")
