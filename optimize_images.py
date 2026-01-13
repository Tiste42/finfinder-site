import os
from PIL import Image
import concurrent.futures

STATIC_DIR = '/workspace/static'
TARGET_SIZES = [400, 800, 1200, 1920]

def process_image(filename):
    if not (filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.png')):
        return
    
    filepath = os.path.join(STATIC_DIR, filename)
    try:
        with Image.open(filepath) as img:
            # Convert to RGB if needed (e.g. for PNGs with transparency)
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGBA')
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Generate WebP at original size
            webp_filename = os.path.splitext(filename)[0] + '.webp'
            webp_path = os.path.join(STATIC_DIR, webp_filename)
            
            # Only generate if it doesn't exist or we want to overwrite (skipping check for now to ensure all are processed)
            img.save(webp_path, 'WEBP', quality=85)
            print(f"Generated WebP for {filename}")

            # Generate responsive sizes
            original_width, original_height = img.size
            
            for width in TARGET_SIZES:
                if width >= original_width:
                    continue
                
                height = int((width / original_width) * original_height)
                resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Save as WebP
                resized_filename = f"{os.path.splitext(filename)[0]}-{width}w.webp"
                resized_path = os.path.join(STATIC_DIR, resized_filename)
                resized_img.save(resized_path, 'WEBP', quality=85)
                print(f"Generated {width}w WebP for {filename}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

def main():
    files = [f for f in os.listdir(STATIC_DIR) if os.path.isfile(os.path.join(STATIC_DIR, f))]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_image, files)

if __name__ == "__main__":
    main()
