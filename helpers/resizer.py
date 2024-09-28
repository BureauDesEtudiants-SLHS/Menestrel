import os
from PIL import Image

def resize_images_in_folder(folder_path, size=(500, 500)):
   
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".jpg"):
            image_path = os.path.join(folder_path, filename)
            
            with Image.open(image_path) as img:
                resized_img = img.resize(size, Image.LANCZOS)
                
                resized_img.save(image_path)
                print(f"Image {filename} redimensionnée à {size} pixels.")

repertoire = os.getcwd()
folder_path = f"{repertoire}/assets/backgrounds/"

resize_images_in_folder(folder_path)
