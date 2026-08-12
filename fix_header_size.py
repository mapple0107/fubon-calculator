import shutil

for path in ["index.html", "dca.html"]:
    shutil.copy(path, path + ".bakH")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    old = '''<img src="avatar.png" alt="頭像" style="width:64px; height:64px; border-radius:50%; box-shadow:0 2px 8px rgba(0,0,0,0.15); flex-shrink:0;">'''
    new = '''<img src="avatar.png" alt="頭像" style="width:100px; height:100px; border-radius:50%; box-shadow:0 2px 8px rgba(0,0,0,0.15); flex-shrink:0;">'''

    if old in c:
        c = c.replace(old, new)
        print(f"✅ {path} 頭像已放大")
    else:
        print(f"❌ {path} 找不到頭像區塊")

    old_h1 = '''<h1 style="margin-bottom:2px;">'''
    new_h1 = '''<h1 style="margin-bottom:2px; font-size:2.6rem;">'''

    if old_h1 in c:
        c = c.replace(old_h1, new_h1)
        print(f"✅ {path} 標題字體已放大")
    else:
        print(f"❌ {path} 找不到標題區塊")

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
