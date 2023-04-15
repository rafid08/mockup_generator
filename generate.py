import os
import random
import math
from PIL import Image, ImageDraw, ImageFilter

# Set folder to current working directory
root_path = os.getcwd()

# Define folder
folder_path = os.path.join(root_path, 'input')
output_folder = os.path.join(root_path, 'output')

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define function to get mid relevant color
def get_mid_color(colors):
    colors.sort()
    mid_index = len(colors) // 2
    return colors[mid_index]

# Loop through all files in folder
for filename in os.listdir(folder_path):
    # Check if file is an image
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # Open image and get all color swatches
        image = Image.open(os.path.join(folder_path, filename))
        swatches = image.getcolors(image.size[0] * image.size[1])
        swatch_colors = [swatch[1] for swatch in swatches]
        
        # Get mid relevant color and create background image
        mid_color = get_mid_color(swatch_colors)
        background = Image.new('RGB', (1900, 2400), mid_color)
        
        # Resize and round the corners of the image
        size = (1100, int((1100/image.width)*image.height))
        radius = 50
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, size[0], size[1]), radius, fill=255)
        image = image.resize(size, resample=Image.LANCZOS)
        image.putalpha(mask)
        
        # Rotate the image randomly by -20 to 20 degrees
        angle = random.randint(5, 15)
        random_changer = random.randint(0, 1)
        if random_changer == 1:
            angle  = angle * -1
        rotated_image = image.rotate(angle, expand=True)
        
        # Calculate padding and paste rotated image onto background
        x_pad = (background.width - rotated_image.width) // 2
        y_pad = (background.height - rotated_image.height) // 2
        paste_box = (x_pad, y_pad, x_pad + rotated_image.width, y_pad + rotated_image.height)

        dx = 10
        dy = 10
        if random_changer == 1:
            dx *= -1
        shadow_size = (size[0]+dx*2, size[1]+dy*2)
        shadow_box = Image.new('RGBA', shadow_size, (0, 0, 0, 100))
        shadow_mask = Image.new('L', shadow_size, 0)
        shadow_draw = ImageDraw.Draw(shadow_mask)
        shadow_draw.rounded_rectangle((0, 0, shadow_size[0], shadow_size[1]), radius, fill=24) # opacity of shadow
        shadow_box.putalpha(shadow_mask)
        shadow_box = shadow_box.rotate(angle, expand=True)
        shadow_box = shadow_box.filter(ImageFilter.GaussianBlur(radius=16))

        shadow_paste_box = (x_pad+dx, y_pad+dy, x_pad + shadow_box.width+dx, y_pad + shadow_box.height+dy)
        background.paste(shadow_box, shadow_paste_box, shadow_box)

        background.paste(rotated_image, paste_box, rotated_image)
        
        # Save edited image to output folder
        output_filename = os.path.splitext(filename)[0] + '_edited.png'
        output_path = os.path.join(output_folder, output_filename)
        background.save(output_path)

