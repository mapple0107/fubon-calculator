import shutil

path = "dca.html"
shutil.copy(path, path + ".bak_link"); print("已備份")

with open(path, "r", encoding="utf-8") as f:
    c = f.read()

ok = True

# 1. renderFundChart：不再寫死 10000，改成讀取「每月投入金額」欄位的值
old1 = "  const monthlyInvest = 10000;"
new1 = "  const monthlyInvest = parseFloat(document.getElementById('dcaMonthly').value) || 10000;"
if old1 in c:
    c = c.replace(old1, new1)
    print("✅ 走勢圖改為讀取每月投入金額")
else:
    print("❌ 找不到 monthlyInvest 區塊"); ok = False

# 2. 每月投入金額欄位輸入時，同步重新畫圖（若目前有選基金）
old2 = '''<input type="number" id="dcaMonthly" value="10000" step="1000">'''
new2 = '''<input type="number" id="dcaMonthly" value="10000" step="1000" oninput="onMonthlyChange()">'''
if old2 in c:
    c = c.replace(old2, new2)
    print("✅ 每月投入金額欄位已加上連動事件")
else:
    print("❌ 找不到每月投入金額欄位"); ok = False

# 3. 加入 onMonthlyChange 函式
old3 = "function onFundSelectChange() {"
new3 = '''function onMonthlyChange() {
  const key = document.getElementById('dcaFundSelect').value;
  if (key) renderFundChart(key);
}

function onFundSelectChange() {'''
if old3 in c:
    c = c.replace(old3, new3, 1)
    print("✅ 已加入 onMonthlyChange 函式")
else:
    print("❌ 找不到 onFundSelectChange 區塊"); ok = False

if ok:
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("\\n✅ 全部修改完成")
else:
    print("\\n⚠️ 部分修改失敗，請檢查上面錯誤訊息")
