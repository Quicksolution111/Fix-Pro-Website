from PIL import Image
import os
import glob

def process_directory(base_dir):
    MAX_WIDTH = 1200
    MAX_HEIGHT = 1200
    QUALITY = 80
    
    count = 0
    saved_total = 0

    print(f"Processing {base_dir}...")
    
    for root, _, files in os.walk(base_dir):
        for fname in files:
            # We want to convert jpg, jpeg, png to webp
            # If it's already webp, skip or re-compress? Let's process all images.
            if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')): 
                continue
                
            fpath = os.path.join(root, fname)
            original_size = os.path.getsize(fpath)
            
            # The new filename will be the old one but with .webp extension
            name_without_ext, ext = os.path.splitext(fname)
            new_fpath = os.path.join(root, name_without_ext + '.webp')
            
            try:
                with Image.open(fpath) as img:
                    img = img.convert("RGB")
                    w, h = img.size
                    if w > MAX_WIDTH or h > MAX_HEIGHT:
                        img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.LANCZOS)
                        
                    # Save as WebP
                    img.save(new_fpath, "WEBP", quality=QUALITY, method=6)
                
                new_size = os.path.getsize(new_fpath)
                
                # If we created a new webp file from a jpg/png, we should delete the old one
                if fpath != new_fpath:
                    os.remove(fpath)
                    
                saved = original_size - new_size
                saved_total += saved
                count += 1
                print(f"  {fname} -> {name_without_ext}.webp: {original_size//1024}KB -> {new_size//1024}KB")
                
            except Exception as e:
                print(f"  ERROR processing {fname}: {e}")

    print(f"Done processing {base_dir}! {count} images converted. Total saved: {saved_total//1024//1024}MB\n")

if __name__ == "__main__":
    process_directory("Plumber works")
    process_directory("Electriccal work")
