from PIL import Image
import os

def load_image(image_path):
    """ Charge une image à partir du chemin spécifié. """

    try:
        image = Image.open(image_path)
        return image
    except FileNotFoundError:
        print(f"Erreur : Le fichier {image_path} est introuvable.")
        return None

def load_images_from_folder(folder, format):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(format):
            img = load_image(os.path.join(folder, filename))
            if img is not None:
                images.append(img)
    return images

def convert_images(images, input_format='PNG', output_format='JPEG'):
    converted_images = []
    for img in images:
        if img.format == input_format:
            rgb_img = img.convert('RGB')
            converted_images.append(rgb_img)
        else:
            print(f"Warning: Image format is {img.format}, not {input_format}")
    return converted_images

def save_image(image, output_path):

    """ Sauvegarde l'image modifiée au chemin spécifié. """

    directory = os.path.dirname(output_path)
    
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Répertoire créé avec succès : {directory}")
        except Exception as e:
            print(f"Erreur lors de la création du répertoire {directory} : {e}")
            return

    try:
        image.save(output_path)
        print(f"Image sauvegardée avec succès à : {output_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'image : {e}")

def save_images(images, output_format, output_folder, original_names):
    for img, name in zip(images, original_names):
        output_path = os.path.join(output_folder, f"{os.path.splitext(name)[0]}.{output_format.lower()}")
        save_image(img, output_path)

if __name__ == "__main__":
    repertoire = f"{os.getcwd()}/assets/logos"

    images = load_images_from_folder(repertoire, "png")
    images = convert_images(images)

    for id, img in enumerate(images):
        save_image(img, f"{repertoire}/episteme.jpg")
