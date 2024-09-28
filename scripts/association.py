import json
import os

class Association:

    def __init__(self, name, logo, object, activity, month_events, organigramme):
        self.name = name
        self.logo = logo
        self.object = object
        self.activity = activity
        self.month_events = month_events
        self.organigramme = organigramme

    def save_association(self, file_path=None):
        if file_path is None:
            repertoire = os.getcwd()
            file_path = f"{repertoire}/assets/data/{self.name.lower().replace(' ', '_')}.json"

        with open(file_path, 'w') as file:
            json.dump(self.__dict__, file, indent=4)

    @staticmethod
    def load_association(association_name="epistemes", file_path=None):
        if file_path is None:
            repertoire = os.getcwd()
            file_path = f"{repertoire}/assets/data/association.json"

        with open(file_path, 'r') as file:
            association_data = json.load(file)[f"{association_name.lower().replace(' ', '_')}"]

        return Association(**association_data)

    def __str__(self):
        return json.dumps(vars(self), indent=4)

    def present_association(self):
        presentation = f"Bienvenue à {self.name}!\n\n"

        presentation += "Notre association a pour objectifs de "
        for i, obj in enumerate(self.object):
            if i == len(self.object) - 1:
                presentation += f"et {obj}. "
            elif i == len(self.object) - 2:
                presentation += f"{obj} "
            else:
                presentation += f"{obj}, "

        presentation += "Nous sommes actifs dans les domaines suivants : "
        for i, act in enumerate(self.activity):
            if i == len(self.activity) - 1:
                presentation += f"et {act}. "
            elif i == len(self.activity) - 2:
                presentation += f"{act} "
            else:
                presentation += f"{act}, "

        presentation += "Chaque mois, nous organisons ou participons à des événements tels que : "
        for i, event in enumerate(self.month_events):
            if i == len(self.month_events) - 1:
                presentation += f"et {event}. "
            elif i == len(self.month_events) - 2:
                presentation += f"{event} "
            else:
                presentation += f"{event}, "

        return presentation

    def present_members(self):
        presentation = ""
        
        for member in self.organigramme:
            presentation += f"- {member['prenom']} {member['nom']}, Filière {member['filiere']}, Rôle {member['role']} Rattachement {member['rattachement']}.\n"

        return presentation
