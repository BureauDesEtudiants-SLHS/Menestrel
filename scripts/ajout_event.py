import os
import calendar
from datetime import datetime, timedelta

from event import Event

def save_joviaux():
    start_date = datetime(2024, 9, 2)
    end_date = datetime(2025, 8, 31)
    delta = timedelta(days=1)

    while start_date <= end_date:
        if start_date.weekday() == 3:  # Jeudi
            last_day_of_month = calendar.monthrange(start_date.year, start_date.month)[1]
            last_thursday_of_month = last_day_of_month - (calendar.weekday(start_date.year, start_date.month, last_day_of_month) - 3) % 7
            if start_date.day == last_thursday_of_month:
                event = Event("Soiree tombola", start_date.strftime("%d/%m/%Y"), "18:00", "LaFontaine", "4 Rue des Boucheries, 25000 Besancon. 1€ de participation pour des consomations offertes par Michel", ["lafontaine.png"])
            else:
                event = Event("Jovial", start_date.strftime("%d/%m/%Y"), "18:00", "LaFontaine", "4 Rue des Boucheries, 25000 Besancon", ["lafontaine.png"])
            event.save_event()
        start_date += delta

def save_reunions():
    start_date = datetime(2024, 9, 2)
    end_date = datetime(2025, 8, 31)
    delta = timedelta(days=1)

    while start_date <= end_date:
        if start_date.weekday() == 1:  # Mardi
            last_day_of_month = calendar.monthrange(start_date.year, start_date.month)[1]
            last_tuesday_of_month = last_day_of_month - (calendar.weekday(start_date.year, start_date.month, last_day_of_month) - 1) % 7
            if start_date.day == last_tuesday_of_month:
                event = Event("Conseil d'Administration", start_date.strftime("%d/%m/%Y"), "18:00", "Amphi", "", [])
            else:
                event = Event("Reunion hebdomadaire", start_date.strftime("%d/%m/%Y"), "18:00", "Amphi", "", [])
            event.save_event()
        start_date += delta

def save_film_screenings():
    screening_dates = [datetime(2024, 9, 20), datetime(2024, 10, 18)]

    for date in screening_dates:
        event = Event("Soirée projection de film", date.strftime("%d/%m/%Y"), "18:00", "LiVE", "48 Av. de l'Observatoire, 25000 Besançon", ["crous.png"])
        event.save_event()

def save_handball_events():
    event_dates = [datetime(2024, 9, 27), datetime(2024, 10, 25)]

    for date in event_dates:
        event = Event("Soirée handball", date.strftime("%d/%m/%Y"), "18:00", "Palais des sports", "42 Av. Léo Lagrange, 25000 Besançon. Billet gratuit, bière gratuite après match, une place au QG gratuite pour le soir même.", ["gbdh.png"])
        event.save_event()

def save_visits():
    citadelle = Event("Visite de la Citadelle de Vauban", "", "", "Citadelle de Besançon", "99 Rue des Fusillés de la Résistance, 25000 Besançon", ["avantagesjeunes.png"])
    musee_temps = Event("Visite du Musée du Temps", "", "", "Musée du Temps", "96 Grande Rue, 25000 Besançon", ["avantagesjeunes.png"])
    beaux_arts = Event("Visite musée Beaux-arts & Archéo.", "", "", "Musée des Beaux-Arts et d'Archéologie", "1 Pl. de la Révolution, 25000 Besançon", ["avantagesjeunes.png"])
    maison_natale = Event("Visite maison natale V.Hugo", "", "", "Maison natale de Victor Hugo", "140 Grande Rue, 25000 Besançon", ["avantagesjeunes.png"])
    stjean_horloge_astro = Event("Visite St-Jean et horloge astro.", "", "", "Cathédrale St-Jean de Besançon", "10 Rue de la Convention, 25000 Besançon", [])
    musee_resistance = Event("Visite musée de la Résistance", "", "", "Citadelle de Besançon", "99 Rue des Fusillés de la Résistance, 25000 Besançon", ["avantagesjeunes.png"])

    save_event(citadelle)
    save_event(musee_temps)
    save_event(beaux_arts)
    save_event(maison_natale)
    save_event(stjean_horloge_astro)
    save_event(musee_resistance)

def main():
    # event = Event("titre", "j/m/a", "h:m", "localisation", "description", [])
    # event.save_event()

    # TODO : attendre les matchs du GBDH pour répartir les quatres événements mensuels

if __name__ == "__main__":
    main()
