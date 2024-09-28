from PIL import Image, ImageDraw, ImageFont
import os
import datetime

from event import Event
from format import Format
from theme import Theme

def load_image(image_path):
    """ Charge une image à partir du chemin spécifié. """

    try:
        image = Image.open(image_path)
        return image
    except FileNotFoundError:
        print(f"Erreur : Le fichier {image_path} est introuvable.")
        return None

def add_text(draw, text, font_path, font_size, position):

    """ Ajoute du texte à une image avec la police spécifiée. """
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill="black")

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

def line(draw, coords):
    draw.line(coords, fill="black", width=3)

def draw_transparent_square(background, color, position, opacity=0.6):
    """
    Dessine un carré transparent avec une opacité spécifiée sur une image existante.

    :param background: L'image de fond (objet PIL Image).
    :param color: Un tuple (R, G, B) pour la couleur du carré.
    :param position: Un tuple (x, y) pour la position du coin supérieur gauche du carré.
    :param square_size: La taille du carré (largeur et hauteur).
    :param opacity: L'opacité du carré (entre 0 et 1).
    :return: L'image avec le carré dessiné dessus.
    """
    
    opacity = int(255 * opacity)
    r, g, b = color

    marge = position[0]*2, position[1]*2
    square_size = background.width - marge[0], background.height - marge[1]

    carre = Image.new("RGBA", (background.width, background.height), (255, 255, 255, 0))
    cdraw = ImageDraw.Draw(carre)
    
    left, top = position
    right, bottom = left + square_size[0], top + square_size[1]
    cdraw.rounded_rectangle([left, top, right, bottom], fill=(r, g, b, opacity), radius=30)

    combined = Image.alpha_composite(background.convert('RGBA'), carre)
    
    return combined

def resize_and_crop(image, size):
    """
    Redimensionne et recadre une image pour qu'elle corresponde à la taille spécifiée.

    :param image: Objet PIL Image.
    :param size: Tuple (largeur, hauteur) pour la nouvelle taille.
    :return: Nouvelle image redimensionnée et recadrée.
    """

    original_ratio = image.width / image.height
    target_ratio = size[0] / size[1]

    if original_ratio > target_ratio:
        new_height = size[1]
        new_width = int(new_height * original_ratio)
    else:
        new_width = size[0]
        new_height = int(new_width / original_ratio)

    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    left = (new_width - size[0]) / 2
    top = (new_height - size[1]) / 2
    right = (new_width + size[0]) / 2
    bottom = (new_height + size[1]) / 2

    cropped_image = resized_image.crop((left, top, right, bottom))
    return cropped_image

def load_font(font_path, font_size):
    if font_path is None:
        repertoire = os.getcwd()
        font_path = f"{repertoire}/assets/fonts/point-didot.ttf"

    font = ImageFont.truetype(font_path, font_size)

    return font

def add_text(background, position, text, font_path, font_size=40, font_color=(0, 0, 0), center=True):
    """ Ajoute du texte à une image avec la police spécifiée. """
    
    draw = ImageDraw.Draw(background)
    font = load_font(font_path, font_size)

    if center:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x, y = position
        x = x - text_width / 2
        y = y - text_height / 2
        
        position = (x, y)
    
    draw.text(position, text, font=font, fill=font_color)

def line(background, coords, color=(0, 0, 0)):
    draw = ImageDraw.Draw(background)
    draw.line(coords, fill=color, width=3)

def paste_img(background, img, position, size):
    """
    Colle une image sur un fond à une position spécifiée et avec une taille donnée.

    :param background_path: Chemin de l'image de fond
    :param img_to_paste_path: Chemin de l'image à coller
    :param position: Tuple (x, y) spécifiant la position où coller l'image
    :param size: Tuple (width, height) spécifiant la taille de l'image à coller
    """

    img = img.resize(size, Image.LANCZOS)
    img.convert("RGBA")

    background.paste(img, position)

    return background

def add_logo(background, logo, opaque_square, size):

    x = opaque_square[0]
    y = size[1] - opaque_square[1] - logo.height

    background = paste_img(background, logo, (x, y), (60, 60))

def add_event_elements(background, format, event, fonts_paths, theme, logo):

    draw = ImageDraw.Draw(background)
    ## TITRE, HORODATEUR & LIEU
    add_text(background, format.positions["title"], event.title, fonts_paths["title"], format.font_sizes["title"], theme.getRGBfont())
    add_text(background, format.positions["date_time"], f"{event.date} à {event.time}", fonts_paths["text"], format.font_sizes["date_time"], theme.getRGBfont())
    add_text(background, format.positions["location"], event.location, fonts_paths["text"], format.font_sizes["location"], theme.getRGBfont())

    ## BARRE DE SEPARATION & DESCRIPTION
    line(background, format.positions["separator_line"], theme.getRGBfont())
    add_text(background, format.positions["description"], event.description, fonts_paths["text"], format.font_sizes["description"], theme.getRGBfont())

    ## LOGO & PARTENAIRES
    add_logo(background, logo, format.positions["opaque_square"], format.size)

def add_event_logos(background, logo, format):
    add_logo(background, logo, format.positions["opaque_square"], format.size)

def get_text_size(draw, text, font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), text, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    return text_width, text_height

def format_official_text(draw, text, format, font_path):

    image_width, image_height = format.size
    text_y = format.positions["location"][1]
    font_size = format.font_sizes["location"]
    available_height = image_height - text_y

    formatted_lines = []
    words = text.split()
    current_line = ""

    for word in words:
        line_width, _ = get_text_size(draw, current_line + " " + word, font_path, font_size)
        if line_width <= image_width:
            current_line += " " + word
        else:
            formatted_lines.append(current_line.strip())
            current_line = word

    formatted_lines.append(current_line.strip())
    formatted_lines = formatted_lines[:available_height // font_size]
    text_x = image_width // 2

    return "\n".join(formatted_lines), text_x

def save_text(text, output_path):
    """ Sauvegarde le texte au chemin spécifié. """

    directory = os.path.dirname(output_path)

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Répertoire créé avec succès : {directory}")
        except Exception as e:
            print(f"Erreur lors de la création du répertoire {directory} : {e}")
            return

    try:
        with open(output_path, 'w') as file:
            file.write(text)
        print(f"Texte sauvegardé avec succès à : {output_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du texte : {e}")


def write_event_presentation(event):
    description = f"L'événement '{event.title}' aura lieu le {event.date_complete()} à {event.time} à {event.location}.\n"
    
    if len(event.description) > 0:
        description += "Voici quelques informations pratiques concernant l'événement :\n"
        description += f"{event.description}\n"
    if event.partners:
        description += f"Cet événement est organisé en partenariat avec : {', '.join(event.partners)}.\n"
    return description

def generate_event_presentation(event, save_path):
    
    description = generate_event_description(event)
    save_text(description, save_path)

def write_mail(object, content):
    mail = f"Objet : {object}\n\n"
    mail += "Bonjour,\n\n"
    mail += content
    mail += "Cordialement,\n"
    mail += "L'Episteme"

    return mail

def generate_mail_event_presentation(event, save_path):
    content = f"L'Association de l'Episteme à le plaisir de vous convier à son événement {event.title}.\n\n"
    content += write_event_presentation(event)
    content += "\n\nNous espérons vous y voir nombreux.\n"
    
    save_text(write_mail(event.title, content), save_path)

def generate_all_events_publications():
    repertoire = os.getcwd()

    themes, association = Theme.load_themes()
    events = Event.load_events()
    formats = Format.load_formats()

    logo_path = f"{repertoire}/assets/logos/{association["logo"]}"
    logo = load_image(logo_path)

    for event in events:
        theme = Theme.get_theme_from_month(event.get_month(), themes)

        fonts_paths = theme.get_fonts_path()
        background_path = f"{repertoire}/assets/backgrounds/{theme.background}"

        generate_event_presentation(event, f"{repertoire}/assets/results/{event.title}/presentation.txt")
        generate_mail_event_presentation(event, f"{repertoire}/assets/results/{event.title}/mail.txt")

        for format in formats:

            ## FOND & DIMENSION
            background = load_image(background_path)
            background = resize_and_crop(background, format.size)

            # CARRE OPPAQUE
            background = draw_transparent_square(background, theme.getRGBcolor(), format.positions["opaque_square"])

            ## ELEMENTS TEXTUELS & LOGOS
            add_event_elements(background, format, event, fonts_paths, theme, logo)

            ## SAUVEGARDE
            output_path = f"{repertoire}/assets/results/{event.title}/{format.name}.png"
            save_image(background, output_path)

def generate_all_themes_publications():
    repertoire = os.getcwd()

    themes = Theme.get_themes()
    formats = Format.load_formats()

    for theme in themes:

        fonts_paths = theme.get_fonts_path()
        background_path = f"{repertoire}/assets/backgrounds/{theme.background}"

        for format in formats:

            ## FOND & DIMENSIONS
            background = load_image(background_path)
            background = resize_and_crop(background, format.size)

            back1 = background.copy() # première page : sans carré oppaque

            ## CARRE OPPAQUE
            background = draw_transparent_square(background, theme.getRGBcolor(), format.positions["opaque_square"])

            back2 = background.copy()
            back3 = background.copy()
            back4 = background.copy()

            ## PREMIER
            add_text(back1, format.positions["title"], theme.month.capitalize(), fonts_paths["title"], format.font_sizes["title"], theme.getRGBfont())

            ## DEUXIEME
            add_text(back2, format.positions["title"], theme.theme, fonts_paths["text"], format.font_sizes["title"], theme.getRGBfont())
            line(back2, format.positions["separator_line"], theme.getRGBfont())
            add_text(back2, format.positions["description"], theme.origine, fonts_paths["text"], format.font_sizes["description"], theme.getRGBfont())

            ## TROISIEME
            events = Event.get_events_from_month(theme.month)
            text = "".join([f"\n{event.date} - {event.title}" for event in events])

            add_text(back3, format.positions["title"], "Dans le mois", fonts_paths["text"], format.font_sizes["title"], theme.getRGBfont())
            add_text(back3, format.positions["location"], text, fonts_paths["text"], format.font_sizes["description"], theme.getRGBfont())

            ## DERNIER
            add_text(back4, format.positions["title"], "Les voeux", fonts_paths["text"], format.font_sizes["title"], theme.getRGBfont())
            line(back4, format.positions["separator_line"], theme.getRGBfont())
            add_text(back4, format.positions["description"], theme.voeux, fonts_paths["text"], format.font_sizes["description"], theme.getRGBfont())
            
            ## SAUVEGARDE
            for i, bg in enumerate([back1, back2, back3, back4]):
                output_path = f"{repertoire}/assets/results/Themes/{theme.month}/{format.name}/{theme.month}-{format.name}-{i}.png"
                save_image(bg, output_path)

def generate_all_hebdo_calendar():
    repertoire = os.getcwd()

    themes, association = Theme.load_themes()
    events = Event.get_events_from_week()
    formats = Format.load_formats()

    logo_path = f"{repertoire}/assets/logos/{association["logo"]}"
    logo = load_image(logo_path)

    for week_num in events:
        week = events[week_num]
        event = week[0]
        theme = Theme.get_theme_from_month(event.get_month(), themes)

        background_path = f"{repertoire}/assets/backgrounds/{theme.background}"
        fonts_paths = theme.get_fonts_path()


        text = "".join([f"\n{event.date} - {event.title}" for event in week])

        for event in week:
            for format in formats:
                ## FOND & DIMENSIONS
                background = load_image(background_path)
                background = resize_and_crop(background, format.size)

                ## CARRE OPPAQUE
                ## CARRE OPPAQUE
                background = draw_transparent_square(background, theme.getRGBcolor(), format.positions["opaque_square"])

                ## CALENDRIER
                add_text(background, format.positions["title"], "Dans la semaine", fonts_paths["title"], format.font_sizes["title"], theme.getRGBfont())
                add_text(background, format.positions["location"], text, fonts_paths["text"], format.font_sizes["description"], theme.getRGBfont())

                ## LOGO
                add_logo(background, logo, format.positions["opaque_square"], format.size)

                ## SAUVEGARDE
                output_path = f"{repertoire}/assets/results/Hebdomadaire/{week_num}/{format.name}.png"
                save_image(background, output_path)

def generate_official(subjet, text):
    repertoire = os.getcwd()

    date = datetime.datetime.today().date()
    month = Event.get_month_from_date(Event.date_to_str_date(date))

    themes, association = Theme.load_themes()
    formats = Format.load_formats()

    theme = Theme.get_theme_from_month(month, themes)

    fonts_paths = theme.get_fonts_path()
    background_path = f"{repertoire}/assets/backgrounds/{theme.background}"

    for format in formats:
        ## FOND & DIMENSIONS
        background = load_image(background_path)
        backgroud = resize_and_crop(background, format.size)

        back1 = backgroud.copy()

        # PREMIER
        add_text(back1, format.positions["title"], "L'Officiel", fonts_paths["title"], format.font_sizes["title"], theme.getRGBfont())
        back2 = back1.copy()
        add_text(back1, format.positions["date_time"], subjet, fonts_paths["text"], format.font_sizes["date_time"], theme.getRGBfont())

        # SECOND
        formatted_text, text_x = format_official_text(ImageDraw.Draw(back2), text, format, fonts_paths["text"])
        add_text(back2, (text_x, format.positions["description"][1]), formatted_text, fonts_paths["text"], format.font_sizes["description"], theme.getRGBfont())

        # PRESENTATION
        save_text(f"Officiel Episteme\n{subjet}\n\n{text}", f"{repertoire}/assets/results/Officiel/{date}/presentation.txt")
        save_text(write_mail(f"Officiel Episteme - {subjet}", text), f"{repertoire}/assets/results/Officiel/{date}/mail.txt")

        ## SAUVEGARDE
        output_path = f"{repertoire}/assets/results/Officiel/{date}/{format.name}/page(1).png"
        save_image(back1, output_path)
        output_path = f"{repertoire}/assets/results/Officiel/{date}/{format.name}/page(2).png"
        save_image(back2, output_path)
