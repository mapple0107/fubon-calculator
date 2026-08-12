import shutil

for path in ["index.html", "dca.html"]:
    shutil.copy(path, path + ".bakF")
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. 整體字體放大 (body 加 font-size 基準值)
    old_body_index = '''  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: linear-gradient(180deg, #eef4fb 0%, #f7f9fc 40%, #f5f5f7 100%);
    color: #1d1d1f;
    min-height: 100vh;
    padding: 2.5rem 1rem;
  }'''
    new_body_index = '''  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: linear-gradient(180deg, #eef4fb 0%, #f7f9fc 40%, #f5f5f7 100%);
    color: #1d1d1f;
    min-height: 100vh;
    padding: 2.5rem 1rem;
    font-size: 18px;
  }'''

    old_body_dca = '''  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: linear-gradient(180deg, #eef4fb 0%, #f7f9fc 40%, #f5f5f7 100%);
    color: #1d1d1f; min-height: 100vh; padding: 2.5rem 1rem;
  }'''
    new_body_dca = '''  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: linear-gradient(180deg, #eef4fb 0%, #f7f9fc 40%, #f5f5f7 100%);
    color: #1d1d1f; min-height: 100vh; padding: 2.5rem 1rem;
    font-size: 18px;
  }'''

    if old_body_index in c:
        c = c.replace(old_body_index, new_body_index)
        print(f"✅ {path} 字體放大 (index版)")
    elif old_body_dca in c:
        c = c.replace(old_body_dca, new_body_dca)
        print(f"✅ {path} 字體放大 (dca版)")
    else:
        print(f"❌ {path} 找不到 body 區塊")

    # 2. 頭像+標題置中
    old_header = '''  <div style="display:flex; align-items:center; gap:16px; margin-bottom: 2.5rem;">'''
    new_header = '''  <div style="display:flex; align-items:center; justify-content:center; gap:16px; margin-bottom: 2.5rem; text-align:left;">'''

    if old_header in c:
        c = c.replace(old_header, new_header)
        print(f"✅ {path} 頭像列已置中")
    else:
        print(f"❌ {path} 找不到 header 區塊")

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
