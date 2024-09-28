import os

from imager import *

def main():

    # generate_all_events_publications()

    # generate_all_hebdo_calendar()

    # generate_all_themes_publications()

    # text = ""
    # generate_official("recrutement", text)

    # generate_association_presentation()

    # TODO : mail format en HTML
    # TODO : ajouter les événements
    # TODO : ajouter les associations à Events
    # TODO : production du calendrier

    assos = Association.load_association()
    print(assos.present_association())
    print(assos.present_members())

if __name__ == "__main__":
    main()
