from PIL import Image
import os

base = "Plumber works"
MAX_WIDTH = 900
MAX_HEIGHT = 900
QUALITY = 75

saved_total = 0
count = 0

for root, dirs, files in os.walk(base):
    for fname in files:
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')): continue
        fpath = os.path.join(root, fname)
        original_size = os.path.getsize(fpath)
        try:
            with Image.open(fpath) as img:
                img = img.convert("RGB")
                # Resize if too big
                w, h = img.size
                if w > MAX_WIDTH or h > MAX_HEIGHT:
                    img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.LANCZOS)
                img.save(fpath, "JPEG", quality=QUALITY, optimize=True)
            new_size = os.path.getsize(fpath)
            saved = original_size - new_size
            saved_total += saved
            count += 1
            print(f"  {fname}: {original_size//1024}KB -> {new_size//1024}KB (saved {saved//1024}KB)")
        except Exception as e:
            print(f"  ERROR {fname}: {e}")

print(f"\nDone! {count} images compressed. Total saved: {saved_total//1024}KB ({saved_total//1024//1024}MB)")
