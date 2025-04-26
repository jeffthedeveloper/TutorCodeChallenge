import os
import cairosvg

# Get all SVG files in the images directory
image_dir = 'images'
svg_files = [f for f in os.listdir(image_dir) if f.endswith('.svg')]

for svg_file in svg_files:
    # Construct input and output paths
    svg_path = os.path.join(image_dir, svg_file)
    png_file = svg_file.replace('.svg', '.png')
    png_path = os.path.join(image_dir, png_file)
    
    # Convert SVG to PNG
    print(f"Converting {svg_file} to {png_file}...")
    cairosvg.svg2png(url=svg_path, write_to=png_path)
    
print("Conversion completed successfully!")