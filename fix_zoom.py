import shutil

for path in ["index.html", "dca.html"]:
    shutil.copy(path, path + ".bakZ")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    old = "  .container { width: 80%; max-width: 1200px; margin: 0 auto; }"
    new = "  .container { width: 80%; max-width: 1200px; margin: 0 auto; zoom: 1.2; }"

    if old in c:
        c = c.replace(old, new)
        print(f"✅ {path} 已加上放大效果")
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
    else:
        print(f"❌ {path} 找不到符合區塊")
