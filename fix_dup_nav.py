path = "index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

nav_block = '''  <div class="nav-cards">
    <a href="index.html" class="nav-card active">
      <div class="nav-icon">💰</div>
      <div><div class="nav-title">配息計算機</div><div class="nav-sub">VCCT 月配息試算</div></div>
    </a>
    <a href="dca.html" class="nav-card">
      <div class="nav-icon">📈</div>
      <div><div class="nav-title">定期定額</div><div class="nav-sub">複利累積試算</div></div>
    </a>
  </div>

'''

count = content.count(nav_block)
print(f"目前找到 {count} 份重複的導覽方塊區塊")

if count > 1:
    # 只保留第一份，其餘刪除
    first_idx = content.find(nav_block)
    before = content[:first_idx + len(nav_block)]
    after = content[first_idx + len(nav_block):]
    after = after.replace(nav_block, "")
    content = before + after
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ 已移除多餘的重複區塊，只保留一份")
else:
    print("沒有發現重複，不需修改。")
