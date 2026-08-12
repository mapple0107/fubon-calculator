import shutil

for path in ["index.html", "dca.html"]:
    shutil.copy(path, path + ".bakS2")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    old = "  .container { width: 80%; max-width: 1200px; margin: 0 auto; zoom: 1.2; }"
    new = "  .container { width: 70%; max-width: 1100px; margin: 0 auto; zoom: 1.4; }"

    if old in c:
        c = c.replace(old, new)
        print(f"✅ {path} 已調整寬度70%、放大1.4倍")
    else:
        print(f"❌ {path} 找不到符合區塊")

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
