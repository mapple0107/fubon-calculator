import shutil

path = "index.html"
shutil.copy(path, path + ".bak6")
print("已備份")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. 加入導覽方塊的 CSS
old_css = '''  .subtitle { font-size: 14px; color: #86868b; margin-bottom: 2.5rem; }'''

new_css = '''  .subtitle { font-size: 14px; color: #86868b; margin-bottom: 2.5rem; }
  .nav-cards { display:flex; gap:12px; margin-bottom:1.5rem; }
  .nav-card {
    flex:1; background:#fff; border-radius:18px; padding:14px 16px;
    display:flex; align-items:center; gap:12px; text-decoration:none; color:#1d1d1f;
    box-shadow:0 4px 14px rgba(0,0,0,0.04); border:1.5px solid transparent; transition:all .15s;
  }
  .nav-card:hover { transform:translateY(-1px); box-shadow:0 6px 18px rgba(0,0,0,0.08); }
  .nav-card.active { border-color:#0071e3; background:linear-gradient(135deg,#eef6ff,#f5faff); }
  .nav-icon {
    width:40px; height:40px; border-radius:12px; display:flex; align-items:center;
    justify-content:center; font-size:20px; background:#eef6ff; flex-shrink:0;
  }
  .nav-card.active .nav-icon { background:#0071e3; }
  .nav-title { font-size:14px; font-weight:700; }
  .nav-sub { font-size:11px; color:#86868b; }'''

# 2. 加入導覽方塊的 HTML（放在標題下方、基本設定卡片之前）
old_html = '''  </div>

  <div class="card">
    <h2>基本設定</h2>'''

new_html = '''  </div>

  <div class="nav-cards">
    <a href="index.html" class="nav-card active">
      <div class="nav-icon">💰</div>
      <div><div class="nav-title">配息計算機</div><div class="nav-sub">VCCT 月配息試算</div></div>
    </a>
    <a href="dca.html" class="nav-card">
      <div class="nav-icon">📈</div>
      <div><div class="nav-title">定期定額</div><div class="nav-sub">複利累積試算</div></div>
    </a>
  </div>

  <div class="card">
    <h2>基本設定</h2>'''

ok = True
if old_css not in content:
    print("❌ 找不到 CSS 區塊"); ok = False
else:
    content = content.replace(old_css, new_css)

if old_html not in content:
    print("❌ 找不到 HTML 區塊"); ok = False
else:
    content = content.replace(old_html, new_html)

if ok:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ 已成功修改 index.html")
