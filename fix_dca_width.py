path = "dca.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = '''  .grid3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }'''
new = '''  .grid3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }
  .grid3 .input-wrap input { min-width: 0; width: 100%; }'''

if old not in content:
    print("❌ 找不到符合的區塊，請手動檢查。")
else:
    content = content.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ 已成功修改")
