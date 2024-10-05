import os

from imager import *

def main():

    generate_all_events_publications()

    # generate_all_hebdo_calendar()

    # generate_all_themes_publications()

    # text = ""
    # generate_official("recrutement", text)

    # generate_association_presentation()

    # TODO : changement des thèmes
    # TODO : changement d'application d'image

    """
    assos = Association.load_association()
    print(assos.present_association())
    print(assos.present_members())
    """

if __name__ == "__main__":
    main()
