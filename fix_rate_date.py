import shutil

path = "index.html"
shutil.copy(path, path + ".bak3")
print("已備份")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_js = '''      const now = new Date();
      const hh = String(now.getHours()).padStart(2,'0');
      const mm = String(now.getMinutes()).padStart(2,'0');
      info.textContent = `即時匯率 ${twd.toFixed(3)}（更新於 ${hh}:${mm}，點擊重新整理）`;'''

new_js = '''      const now = new Date();
      const yyyy = now.getFullYear();
      const mm = String(now.getMonth()+1).padStart(2,'0');
      const dd = String(now.getDate()).padStart(2,'0');
      info.textContent = `即時匯率 ${twd.toFixed(3)}（更新於 ${yyyy}/${mm}/${dd}，點擊重新整理）`;'''

if old_js not in content:
    print("❌ 找不到符合的區塊，請手動檢查。")
else:
    content = content.replace(old_js, new_js)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ 已成功修改")
