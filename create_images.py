from PIL import Image, ImageDraw
import os

# Make sure the images directory exists
if not os.path.exists('images'):
    os.makedirs('images')

# Define standard size
size = (32, 32)

# Create hero_idle1.png
try:
    img = Image.new('RGBA', size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Body
    draw.rectangle([8, 4, 24, 28], fill=(51, 102, 204), outline=(0, 0, 0))
    # Head
    draw.ellipse([10, 6, 22, 18], fill=(255, 255, 204), outline=(0, 0, 0))
    # Eyes
    draw.ellipse([13, 9, 15, 11], fill=(0, 0, 0))
    draw.ellipse([17, 9, 19, 11], fill=(0, 0, 0))
    # Mouth
    draw.line([13, 15, 19, 15], fill=(0, 0, 0), width=1)
    # Feet
    draw.rectangle([12, 28, 16, 32], fill=(102, 51, 0))
    draw.rectangle([16, 28, 20, 32], fill=(102, 51, 0))
    img.save('images/hero_idle1.png')
    print("Created hero_idle1.png")
except Exception as e:
    print(f"Error creating hero_idle1.png: {e}")

# Create hero_idle2.png - slightly different for animation
img = Image.new('RGBA', size, color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# Body
draw.rectangle([8, 4, 24, 28], fill=(51, 102, 204), outline=(0, 0, 0))
# Head
draw.ellipse([10, 6, 22, 18], fill=(255, 255, 204), outline=(0, 0, 0))
# Eyes
draw.ellipse([13, 9, 15, 11], fill=(0, 0, 0))
draw.ellipse([17, 9, 19, 11], fill=(0, 0, 0))
# Mouth - slightly different
draw.line([13, 16, 19, 16], fill=(0, 0, 0), width=1)
# Feet
draw.rectangle([12, 28, 16, 32], fill=(102, 51, 0))
draw.rectangle([16, 28, 20, 32], fill=(102, 51, 0))
img.save('images/hero_idle2.png')

# Create hero_walk1.png
img = Image.new('RGBA', size, color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# Body
draw.rectangle([8, 4, 24, 28], fill=(51, 102, 204), outline=(0, 0, 0))
# Head
draw.ellipse([10, 6, 22, 18], fill=(255, 255, 204), outline=(0, 0, 0))
# Eyes
draw.ellipse([13, 9, 15, 11], fill=(0, 0, 0))
draw.ellipse([17, 9, 19, 11], fill=(0, 0, 0))
# Mouth
draw.line([13, 15, 19, 15], fill=(0, 0, 0), width=1)
# Feet - positioned differently for walking
draw.rectangle([10, 28, 14, 32], fill=(102, 51, 0))
draw.rectangle([18, 28, 22, 32], fill=(102, 51, 0))
img.save('images/hero_walk1.png')

# Create hero_walk2.png
img = Image.new('RGBA', size, color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# Body
draw.rectangle([8, 4, 24, 28], fill=(51, 102, 204), outline=(0, 0, 0))
# Head
draw.ellipse([10, 6, 22, 18], fill=(255, 255, 204), outline=(0, 0, 0))
# Eyes
draw.ellipse([13, 9, 15, 11], fill=(0, 0, 0))
draw.ellipse([17, 9, 19, 11], fill=(0, 0, 0))
# Mouth
draw.line([13, 15, 19, 15], fill=(0, 0, 0), width=1)
# Feet - positioned differently for walking
draw.rectangle([14, 28, 18, 32], fill=(102, 51, 0))
draw.rectangle([20, 28, 24, 32], fill=(102, 51, 0))
img.save('images/hero_walk2.png')

# Create enemy_idle1.png
img = Image.new('RGBA', size, color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# Body
draw.rectangle([8, 6, 24, 26], fill=(204, 51, 51), outline=(0, 0, 0))
# Head
draw.ellipse([10, 7, 22, 19], fill=(255, 204, 153), outline=(0, 0, 0))
# Eyes
draw.ellipse([13, 9, 15, 11], fill=(0, 0, 0))
draw.ellipse([17, 9, 19, 11], fill=(0, 0, 0))
# Mouth - angry
draw.line([13, 14, 19, 14], fill=(0, 0, 0), width=1)
# Horn
draw.rectangle([14, 2, 18, 6], fill=(204, 51, 51))
# Feet
draw.rectangle([11, 26, 15, 30], fill=(51, 51, 51))
draw.rectangle([17, 26, 21, 30], fill=(51, 51, 51))
img.save('images/enemy_idle1.png')

# Create enemy_idle2.png
img = Image.new('RGBA', size, color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# Body
draw.rectangle([8, 6, 24, 26], fill=(204, 51, 51), outline=(0, 0, 0))
# Head
draw.ellipse([10, 7, 22, 19], fill=(255, 204, 153), outline=(0, 0, 0))
# Eyes
draw.ellipse([13, 9, 15, 11], fill=(0, 0, 0))
draw.ellipse([17, 9, 19, 11], fill=(0, 0, 0))
# Mouth - angry, slightly different
draw.line([13, 13, 19, 15], fill=(0, 0, 0), width=1)
# Horn
draw.rectangle([14, 2, 18, 6], fill=(204, 51, 51))
# Feet
draw.rectangle([11, 26, 15, 30], fill=(51, 51, 51))
draw.rectangle([17, 26, 21, 30], fill=(51, 51, 51))
img.save('images/enemy_idle2.png')

# Create enemy_walk1.png
img = Image.new('RGBA', size, color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# Body
draw.rectangle([8, 6, 24, 26], fill=(204, 51, 51), outline=(0, 0, 0))
# Head
draw.ellipse([10, 7, 22, 19], fill=(255, 204, 153), outline=(0, 0, 0))
# Eyes
draw.ellipse([13, 9, 15, 11], fill=(0, 0, 0))
draw.ellipse([17, 9, 19, 11], fill=(0, 0, 0))
# Mouth - angry
draw.line([13, 14, 19, 14], fill=(0, 0, 0), width=1)
# Horn
draw.rectangle([14, 2, 18, 6], fill=(204, 51, 51))
# Feet - positioned differently for walking
draw.rectangle([9, 26, 13, 30], fill=(51, 51, 51))
draw.rectangle([19, 26, 23, 30], fill=(51, 51, 51))
img.save('images/enemy_walk1.png')

# Create enemy_walk2.png
img = Image.new('RGBA', size, color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# Body
draw.rectangle([8, 6, 24, 26], fill=(204, 51, 51), outline=(0, 0, 0))
# Head
draw.ellipse([10, 7, 22, 19], fill=(255, 204, 153), outline=(0, 0, 0))
# Eyes
draw.ellipse([13, 9, 15, 11], fill=(0, 0, 0))
draw.ellipse([17, 9, 19, 11], fill=(0, 0, 0))
# Mouth - angry
draw.line([13, 14, 19, 14], fill=(0, 0, 0), width=1)
# Horn
draw.rectangle([14, 2, 18, 6], fill=(204, 51, 51))
# Feet - positioned differently for walking
draw.rectangle([13, 26, 17, 30], fill=(51, 51, 51))
draw.rectangle([21, 26, 25, 30], fill=(51, 51, 51))
img.save('images/enemy_walk2.png')

# Create wall.png
img = Image.new('RGBA', size, color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.rectangle([0, 0, 31, 31], fill=(85, 85, 85), outline=(51, 51, 51), width=2)
for x in range(0, 32, 8):
    draw.line([x, 0, x, 31], fill=(51, 51, 51), width=1)
for y in range(0, 32, 8):
    draw.line([0, y, 31, y], fill=(51, 51, 51), width=1)
img.save('images/wall.png')

# Create floor.png
img = Image.new('RGBA', size, color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.rectangle([0, 0, 31, 31], fill=(187, 187, 187), outline=(153, 153, 153), width=1)
draw.point([8, 8], fill=(153, 153, 153))
draw.point([24, 8], fill=(153, 153, 153))
draw.point([8, 24], fill=(153, 153, 153))
draw.point([24, 24], fill=(153, 153, 153))
draw.point([16, 16], fill=(153, 153, 153))
img.save('images/floor.png')

# Create treasure.png
img = Image.new('RGBA', size, color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# Chest
draw.rectangle([8, 12, 24, 24], fill=(204, 153, 51), outline=(153, 102, 0), width=1)
# Chest top
draw.rectangle([8, 10, 24, 14], fill=(255, 204, 102), outline=(153, 102, 0), width=1)
# Lock
draw.ellipse([14, 10, 18, 14], fill=(255, 204, 0), outline=(153, 102, 0), width=1)
img.save('images/treasure.png')

print("All images created successfully!")