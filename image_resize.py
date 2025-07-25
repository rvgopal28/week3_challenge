from PIL import Image

img = Image.open("data/waffestry_logo.png")
img = img.resize((1000, int(img.height * (1000 / img.width))))
img.save("data/waffestry_logo_resized.png")