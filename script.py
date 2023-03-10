import os
import math
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
from tqdm import tqdm

img_scale = int(input('Logo scale (recommended value is 5): ') or '5')
img_padding = int(input('Image padding (recommended value is 20): ') or '20')

text_size = int(input('Text size (recommended value is 64): ') or '64')
text_padding = int(input('Text padding (recommended value is 35): ') or '35')

logo_file = input('Logo file path: ') or 'logo.png'
font_file = input('Font file path: ') or 'OpenSans-SemiBold.ttf'

try:
    logo = Image.open(logo_file)
    font = ImageFont.truetype(font_file, text_size)

    print('\nTimestamp adder script started...\n')

    for file in tqdm(os.listdir('.')):

        if file.split('.')[-1].lower() in ['png', 'jpeg', 'jpg', 'ppm', 'gif', 'tiff', 'bmp']:

            try:
                img = Image.open(file)

                # Add timestamp
                exif = img.getexif()
                if exif is None:
                    raise Exception('No exif data is found')
                
                datetime_str = exif.get(306)
                if datetime_str is None:
                    raise Exception('No datetime value is found in exif data')

                datetime_form = datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')

                img_editable = ImageDraw.Draw(img)

                text_box = font.getbbox(datetime_form)
                text_width = text_box[2] - text_box[0]
                text_height = text_box[3] - text_box[1]

                img_editable.text((math.floor(img.size[0]/2 - text_width/2), img.size[1] - text_padding - text_height), datetime_form, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=2, font=font)

                # Add logo
                logo = logo.resize((math.floor(img.size[0]/img_scale), math.floor(img.size[0]/img_scale*logo.size[1]/logo.size[0])))
                img.paste(logo, (math.floor(img.size[0]/2 - logo.size[0]/2), img.size[1] - logo.size[1] - img_padding - text_height), logo)

                # Save modified image
                if not os.path.exists('result'):
                    os.makedirs('result')

                img.save(f'result/{file}')
            
            except Exception as e:
                tqdm.write(f'Problem encoutered while processing {file}:\t{str(e)}')

except Exception as e:
    print(f'Problem encoutered:\t{str(e)}')

input("\nPress enter to exit...")