from sklearn.cluster import KMeans
import numpy as np
import cv2
from PIL import Image
import os

def pil_to_cv2(pil_image):
    open_cv_image = np.array(pil_image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image

def cv2_to_pil(cv2_image):
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(cv2_image)
    return pil_image

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def get_dominant_color(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image = image.reshape((image.shape[0] * image.shape[1], 3))

    kmeans = KMeans(n_clusters=1)
    kmeans.fit(image)

    return kmeans.cluster_centers_[0]

def get_complementary_color(rgb):
    comp_rgb = [round(255 - float(rgb[0])), round(255 - float(rgb[1])), round(255 - float(rgb[2]))]
    return [int(val) for val in comp_rgb]

def load_image(image_path):
    """ Charge une image à partir du chemin spécifié. """

    try:
        image = Image.open(image_path)
        return image
    except FileNotFoundError:
        print(f"Erreur : Le fichier {image_path} est introuvable.")
        return None

def append_text(text, output_path):
    """ Ajoute du texte à la suite du fichier spécifié. """

    directory = os.path.dirname(output_path)

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Répertoire créé avec succès : {directory}")
        except Exception as e:
            print(f"Erreur lors de la création du répertoire {directory} : {e}")
            return

    try:
        with open(output_path, 'a') as file:
            file.write(text)
        print(f"Texte ajouté avec succès à : {output_path}")
    except Exception as e:
        print(f"Erreur lors de l'ajout du texte : {e}")

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = load_image(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

if __name__ == "__main__":
    repertoire = f"{os.getcwd()}/assets/backgrounds/"
    infos_path = f"{os.getcwd()}/helpers/infos_couleur.txt"

    images = load_images_from_folder(repertoire)

    for id, img in enumerate(images):
        filename = os.path.basename(img.filename)
        couleur_dominante = get_dominant_color(pil_to_cv2(img))
        couleur_complementaire = get_complementary_color(couleur_dominante)
        append_text(f"{filename}\n\t=> Couleur dominante {rgb_to_hex(couleur_dominante)} | Couleur complémentaire {rgb_to_hex(couleur_complementaire)}\n", infos_path)
