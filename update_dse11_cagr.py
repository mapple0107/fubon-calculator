import shutil

path = "dca.html"
shutil.copy(path, path + ".bak_cagr")
print("已備份")

with open(path, "r", encoding="utf-8") as f:
    c = f.read()

start_marker = "const FUND_PERFORMANCE = {"
end_marker = "function fmt(n, dec=0)"

start_idx = c.find(start_marker)
end_idx = c.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("❌ 找不到區塊標記，請確認 dca.html 內容")
else:
    new_block = '''const FUND_PERFORMANCE = {
  DSE11: {
    label: "DSE11｜安聯台灣科技證券投資信託基金",
    inceptionDate: "2001-04-03",
    cumulativeReturnSinceInception: 8235.10,
    annualReturns: [
      {y:2016, r:26.79}, {y:2017, r:41.09}, {y:2018, r:0.29},
      {y:2019, r:56.27}, {y:2020, r:37.04}, {y:2021, r:67.98},
      {y:2022, r:-32.11},{y:2023, r:72.47}, {y:2024, r:32.57},
      {y:2025, r:69.05}
    ]
  }
};

function calcCAGR(cumPct, inceptionDateStr) {
  const inception = new Date(inceptionDateStr);
  const now = new Date();
  const years = (now - inception) / (1000*60*60*24*365.25);
  const totalMultiplier = 1 + cumPct / 100;
  return (Math.pow(totalMultiplier, 1/years) - 1) * 100;
}

function renderFundChart(key) {
  const fund = FUND_PERFORMANCE[key];
  const box = document.getElementById('dcaFundChart');
  if (!fund) { box.style.display = 'none'; box.innerHTML = ''; return; }

  const vals = fund.annualReturns.map(x => x.r);
  const maxAbs = Math.max(...vals.map(Math.abs), 1);
  const barW = 100 / vals.length;
  const cagr = calcCAGR(fund.cumulativeReturnSinceInception, fund.inceptionDate);

  let bars = '';
  fund.annualReturns.forEach((x, i) => {
    const h = (Math.abs(x.r) / maxAbs) * 45;
    const color = x.r >= 0 ? '#0071e3' : '#d0392b';
    bars += `<div style="position:absolute; left:${i*barW}%; width:${barW*0.7}%; bottom:${x.r>=0?'50%':(50-h/45*45)+'%'}; height:${h}%; background:${color}; border-radius:2px;" title="${x.y}: ${x.r}%"></div>`;
  });

  let labels = '';
  fund.annualReturns.forEach((x, i) => {
    labels += `<div style="position:absolute; left:${i*barW}%; width:${barW}%; text-align:center; font-size:10px; color:#86868b;">${x.y}</div>`;
  });

  box.innerHTML = `
    <div style="background:#f9f9fb; border-radius:14px; padding:14px 16px;">
      <div style="font-size:12px; color:#86868b; margin-bottom:8px;">近十年單年報酬率(%)</div>
      <div style="position:relative; height:90px; border-bottom:1px solid #e5e5ea;">${bars}</div>
      <div style="position:relative; height:16px; margin-top:2px;">${labels}</div>
      <div style="font-size:12px; color:#3a3a3c; margin-top:10px;">成立日 ${fund.inceptionDate}｜成立至今累積報酬率 ${fund.cumulativeReturnSinceInception}%</div>
      <div style="font-size:13px; color:#0071e3; margin-top:4px; font-weight:700;">成立至今年化報酬率（CAGR）：${cagr.toFixed(2)}%</div>
    </div>
  `;
  box.style.display = 'block';
}

function onFundSelectChange() {
  const key = document.getElementById('dcaFundSelect').value;
  renderFundChart(key);
  const rateInput = document.getElementById('dcaRate');
  if (key && FUND_PERFORMANCE[key]) {
    const fund = FUND_PERFORMANCE[key];
    const cagr = calcCAGR(fund.cumulativeReturnSinceInception, fund.inceptionDate);
    rateInput.value = cagr.toFixed(2);
  }
}

'''
    c = c[:start_idx] + new_block + c[end_idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("✅ 已更新為成立至今年化報酬率計算")
