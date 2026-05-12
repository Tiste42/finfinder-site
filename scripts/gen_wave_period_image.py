import os, sys, io
from google import genai
from google.genai import types
from PIL import Image

API_KEY = "AIzaSyDBy5XHqNXqvWxR3HoAhLM6FjRiyyuCf4A"
SLUG = "wave-period-fin-choice-swell-variable"
OUT = os.path.join(os.path.dirname(__file__), "..", "static", f"{SLUG}.webp")

prompt = (
    "Editorial surf photography, photorealistic, warm natural tones. A clean, glassy "
    "long-period groundswell wave peeling right across a turquoise reef, shot from a "
    "distance with the horizon line crisp. No people in frame, empty lineup, golden "
    "afternoon light catching the lip, fine spray drifting offshore. Wide editorial "
    "landscape composition, cinematic, magazine cover feel, subtle teal and blue water "
    "with white foam line. Shot from shore, slightly elevated angle. "
    "No text, no logos, no readable letters, no faces."
)

client = genai.Client(api_key=API_KEY)
resp = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="16:9", image_size="2K"),
    ),
)

img_bytes = None
for part in resp.candidates[0].content.parts:
    if getattr(part, "inline_data", None) and part.inline_data.data:
        img_bytes = part.inline_data.data
        break

if not img_bytes:
    print("No image returned")
    sys.exit(1)

img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
W, H = 1200, 448

scale = W / img.width
new_h = int(img.height * scale)
img = img.resize((W, new_h), Image.LANCZOS)
if img.height < H:
    scale = H / img.height
    new_w = int(img.width * scale)
    img = img.resize((new_w, H), Image.LANCZOS)

w, h = img.size
left = (w - W) // 2
top = (h - H) // 2
img = img.crop((left, top, left + W, top + H))
img.save(OUT, "WEBP", quality=85)
print(f"Saved: {OUT} ({W}x{H})")
