import re, os, urllib.parse

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Check all image src
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
print(f"Total <img> tags in index.html: {len(imgs)}")

missing = []
found = 0
for src in imgs:
    # Unquote URL encoding
    path = urllib.parse.unquote(src)
    # Check if file exists relative to workspace
    if os.path.exists(path):
        found += 1
    else:
        missing.append((src, path))

print(f"Verified files on disk: {found}/{len(imgs)}")
if missing:
    print("MISSING FILES:")
    for src, path in missing:
        print(f"   src: {src} -> path: {path}")
else:
    print("ALL IMAGES EXIST ON DISK! ZERO 404s!")

# 2. Check tabs
tabs = ["pprc", "pvc", "gi", "electrical", "solar"]
print("\nChecking Tabs:")
for t in tabs:
    has_btn = f'data-tab="{t}"' in html
    has_div = f'id="{t}-details"' in html
    print(f"   Tab '{t}': button={has_btn}, content={has_div}")

# 3. Check Social Links
print("\nChecking Social & Contact:")
print("   TikTok links found:", len(re.findall(r'tiktok', html, re.I)))
print("   Facebook links found:", len(re.findall(r'facebook', html, re.I)))
print("   WhatsApp links found:", len(re.findall(r'wa\.me', html)))
print("   Khurram phone found:", "0341-2872003" in html or "03412872003" in html)
print("   Muneeb phone found:", "0312-9282263" in html or "03129282263" in html)
print("   Image Modal found:", 'id="imageModal"' in html)
