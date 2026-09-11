from PIL import Image, ImageDraw

# Create a test red apple image
img = Image.new('RGB', (300, 300), color='white')
draw = ImageDraw.Draw(img)
# Draw apple body (red ellipse)
draw.ellipse([50, 50, 250, 250], fill=(220, 20, 30))
# Draw stem (brown rectangle)
draw.rectangle([145, 20, 155, 60], fill=(100, 50, 20))
# Draw green leaf
draw.polygon([(155, 30), (200, 15), (180, 45)], fill=(34, 139, 34))

img.save(r"C:\Users\lenovo\.gemini\antigravity\scratch\material-rebirth-ai\backend\test_apple.jpg")
print("Saved test apple image")
