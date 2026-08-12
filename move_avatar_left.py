import shutil

path = "index.html"
shutil.copy(path, path + ".bak5")
print("已備份")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_header = ''' <div style="text-align:center; margin: 20px 0;">
  <img src="avatar.png" alt="頭像" style="width:150px; height:150px; border-radius:50%; box-shadow:0 2px 8px rgba(0,0,0,0.15);">
  <p style="margin-top:8px; font-size:14px; color:#555;">買樂</p>
</div>
<div class="container">
  <h1>配息計算機</h1>
  <p class="subtitle">富邦人壽真豐利變額年金保險（VCCT）</p>'''

new_header = '''<div class="container">
  <div style="display:flex; align-items:center; gap:16px; margin-bottom: 2.5rem;">
    <img src="avatar.png" alt="頭像" style="width:64px; height:64px; border-radius:50%; box-shadow:0 2px 8px rgba(0,0,0,0.15); flex-shrink:0;">
    <div>
      <h1 style="margin-bottom:2px;">配息計算機</h1>
      <p class="subtitle" style="margin-bottom:0;">富邦人壽真豐利變額年金保險（VCCT）</p>
    </div>
  </div>'''

if old_header not in content:
    print("❌ 找不到符合的區塊，請手動檢查。")
else:
    content = content.replace(old_header, new_header)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ 已成功修改")
