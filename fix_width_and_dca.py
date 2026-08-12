import shutil

# ===== 1. index.html：寬度改成 80% =====
path1 = "index.html"
shutil.copy(path1, path1 + ".bak7")
with open(path1, "r", encoding="utf-8") as f:
    c1 = f.read()

old1 = '''  .container { max-width: 760px; margin: 0 auto; }'''
new1 = '''  .container { width: 80%; max-width: 1200px; margin: 0 auto; }'''

if old1 in c1:
    c1 = c1.replace(old1, new1)
    with open(path1, "w", encoding="utf-8") as f:
        f.write(c1)
    print("✅ index.html 寬度已修改")
else:
    print("❌ index.html 找不到符合區塊")

# ===== 2. dca.html：寬度改成 80% + 拿掉自動試算 =====
path2 = "dca.html"
shutil.copy(path2, path2 + ".bak2")
with open(path2, "r", encoding="utf-8") as f:
    c2 = f.read()

old2a = '''  .container { max-width: 760px; margin: 0 auto; }'''
new2a = '''  .container { width: 80%; max-width: 1200px; margin: 0 auto; }'''

old2b = '''calcDca();
</script>'''
new2b = '''</script>'''

ok2 = True
if old2a in c2:
    c2 = c2.replace(old2a, new2a)
    print("✅ dca.html 寬度已修改")
else:
    print("❌ dca.html 找不到寬度區塊"); ok2 = False

if old2b in c2:
    c2 = c2.replace(old2b, new2b)
    print("✅ dca.html 已移除自動試算")
else:
    print("❌ dca.html 找不到自動試算區塊"); ok2 = False

with open(path2, "w", encoding="utf-8") as f:
    f.write(c2)
