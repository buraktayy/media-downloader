from PIL import Image

img = Image.open(r"C:\Users\Burak\.gemini\antigravity\brain\988d219f-8ed2-411d-9d9f-dd747dc02162\media_atelier_icon_1789027244238.jpg")

# We want to crop out all the white padding
# Convert to grayscale
gray = img.convert("L")

# Create a mask where anything darker than light gray is 255 (keep), and white is 0 (discard)
mask = Image.eval(gray, lambda x: 0 if x > 240 else 255)
bbox = mask.getbbox()

if bbox:
    img = img.crop(bbox)

# Ensure it's square
width, height = img.size
size = min(width, height)
left = (width - size) / 2
top = (height - size) / 2
right = (width + size) / 2
bottom = (height + size) / 2
img = img.crop((left, top, right, bottom))

# Save as icon3.ico to bypass cache again
img.save(r"c:\Users\Burak\Desktop\url downloader\icon3.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
print("icon3.ico created successfully.")
