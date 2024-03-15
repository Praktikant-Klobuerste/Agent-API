from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TeamSchema, TeamCreateSchema, TeamUpdateSchema, Agent_to_TeamSchema, TeamFleeSchema
from resources.lair import Lair
from resources.agent import Agent
import random

teams = {}
blp = Blueprint("Team", __name__, description="Operations on Teams")



class Team:
    """
    Repräsentiert ein Team, das eine Gruppe von Agenten in einem Versteck (Lair) enthält.
    
    Attribute:
        name (str): Der Name des Teams.
        lair (Lair): Das Versteck des Teams.
        id (int): Die eindeutige ID des Teams.
        agents (dict): Ein Dictionary, das Agenten-Objekte enthält, mit Agenten-IDs als Schlüssel.
        
    Klassenattribute:
        _nTeams (int): Zählt die Gesamtanzahl der erstellten Team-Instanzen.
        teams (dict): Ein Klassenweites Dictionary, das Team-Objekte enthält, mit Team-IDs als Schlüssel.
    """

    _nTeams = 0
    teams = {}

    def __init__(self, name, lair:Lair):
        """
        Initialisiert eine neue Instanz der Klasse Team.
        
        Parameter:
            name (str): Der Name des Teams.
            lair (Lair): Das Versteck des Teams, in dem es operiert.
        """
        self.name = name
        self.lair = lair
        self.id = Team._nTeams
        self.agents = {}
        Team._nTeams += 1
        Team.teams[self.id] = self

    def __len__(self):
        """
        Gibt die Anzahl der Agenten im Team zurück.
        
        Returns:
            int: Die Anzahl der Agenten.
        """
        return len(self.agents)

    def __eq__(self, other:'Team'):
        """
        Überprüft, ob zwei Teams gleich sind, basierend auf ihrer ID.
        
        Parameter:
            other (object): Das andere Team, mit dem der Vergleich durchgeführt wird.
            
        Returns:
            bool: True, wenn die IDs beider Teams gleich sind, sonst False.
        """
        return self.id == other.id

    def space(self):
        """
        Berechnet den verfügbaren Platz im Versteck des Teams.
        
        Returns:
            int: Die Anzahl der zusätzlichen Agenten, die das Team aufnehmen kann.
        """
        return self.lair.cap - len(self)

    def add_agent(self, agent:Agent):
        """
        Fügt einen Agenten zum Team hinzu, wenn im Versteck Platz ist und das Versteck geheim ist.
        
        Parameter:
            agent (Agent): Der hinzuzufügende Agent.
            
        Returns:
            bool: True, wenn der Agent erfolgreich hinzugefügt wurde, sonst False.
        """
        if not self.lair.secret or self.space() <= 0:
            return False
        self.agents[agent.id] = agent
        return True

    def contains(self, agent):
        """
        Überprüft, ob ein bestimmter Agent im Team enthalten ist.
        
        Parameter:
            agent (Agent): Der Agent, dessen Vorhandensein überprüft wird.
            
        Returns:
            bool: True, wenn der Agent im Team ist, sonst False.
        """
        return agent.id in self.agents

    def flee(self, other:'Team'):
        """
        Überträgt Agenten zum anderen Team, 
        wenn im anderen Team Platz ist und der Agent nicht bereits dort ist.
        
        Parameter:
            other (Team): Das Team, zu dem die Agenten fliehen.
        """
        agents_copy = list(self.agents.values())
        for agent in agents_copy:
            if not other.contains(agent) and other.space():
                other.add_agent(agent)
                del self.agents[agent.id]

    def to_dict(self) -> dict:
        """
        Konvertiert das Team-Objekt in ein Dictionary für die Serialisierung oder ähnliche Zwecke.
        
        Returns:
            dict: Ein Dictionary, das die Attribute des Teams repräsentiert.
        """
        return {"name": self.name,
                "lair": self.lair.to_dict(),
                "id": self.id,
                "agents": [agent.to_dict() for agent in self.agents.values()]}


    @classmethod
    def get(cls, team_id:int):
        """
        Ermöglicht den Zugriff auf ein Team-Objekt anhand seiner ID.
        
        Parameter:
            team_id (int): Die ID des Teams, das abgerufen werden soll.
            
        Returns:
            Team: Das Team-Objekt mit der angegebenen ID, falls vorhanden, sonst None.
        """
        return cls.teams.get(team_id)

    @classmethod
    def name_exists(cls, name:str):
        """
        Überprüft, ob bereits ein Team mit dem angegebenen Namen existiert.
        
        Parameter:
            name (str): Der Name, der überprüft werden soll.
            
        Returns:
            bool: True, wenn ein Team mit dem Namen existiert, sonst False.
        """
        return any(team.name == name for team in cls.teams.values())



def get_resource_or_404(model:object, resource_id, resource_name:str):
    """
    Versucht, eine Ressource anhand ihrer ID aus einem Datenmodell abzurufen. 
    Gibt die Ressource zurück, wenn sie gefunden wird. Löst einen 404 Fehler aus, 
    wenn die Ressource nicht gefunden werden kann.

    Parameter:
        model (object): Das Datenmodell, aus dem die Ressource abgerufen wird. 
               Es wird erwartet, dass dieses Modell eine 'get'-Methode hat.
        resource_id (int or str): Die ID der abzurufenden Ressource.
        resource_name (str): Der Name der Ressource, verwendet für die Fehlermeldung, 
                             falls die Ressource nicht gefunden wird.

    Returns:
        Die abgerufene Ressource, wenn sie gefunden wird.

    Raises:
        HTTPException: Eine Exception mit einem 404 Statuscode, 
                       wenn die Ressource nicht gefunden werden kann, 
                       mit einer Nachricht, die das Fehlen der Ressource angibt.
    """
    resource = model.get(resource_id)
    if resource is None:
        abort(404, message=f"{resource_name} with id {resource_id} not found.")
    return resource



@blp.route("/team")
class TeamsList(MethodView):
    def get(self):
        return [team.to_dict() for team in Team.teams.values()]

    @blp.arguments(TeamCreateSchema)
    @blp.response(201, TeamSchema)
    def post(self, new_data):
        # Prüfen, ob der Teamname schon vergeben ist.
        if Team.name_exists(new_data["name"]):
            abort(400, message=f"Team name '{new_data['name']}' is already in use.")

        lair = Lair.get(new_data["lair_id"])
        if lair is None:
            abort(404, message="Lair with the specified id not found.")
        team = Team(name=new_data["name"], lair=lair)
        return team.to_dict(), 201



@blp.route("/team/<int:team_id>")
class TeamDetail(MethodView):
    def get(self, team_id):
        team = get_resource_or_404(Team, team_id, "Team")
        return team.to_dict()

    # Zum Aktualisieren eines Teams (PUT)
    @blp.arguments(TeamUpdateSchema)
    def put(self, update_data, team_id):
        team = get_resource_or_404(Team, team_id, "Team")    
        if 'name' in update_data:
            team.name = update_data['name']

        if 'lair_id' in update_data:
            # Hier wird das Lair-Objekt basierend auf der lair_id abgefragt und aktualisiert.
            new_lair = Lair.get(update_data['lair_id'])
            if new_lair is None:
                abort(404, message=f"Lair with id {update_data['lair_id']} not found.")
            team.lair = new_lair

        return team.to_dict(), 200


    def delete(self, team_id):
        get_resource_or_404(Team, team_id, "Team")
        del Team.teams[team_id] # Löscht die Referenz zum Team
        return {"message" : f"removed team {team_id}"},  204



@blp.route("/team/<int:team_id>/agent")
class TeamAgent(MethodView):
    def get(self, team_id):
        team = get_resource_or_404(Team, team_id, "Team")
        return team.to_dict()["agents"]



    @blp.arguments(Agent_to_TeamSchema)
    def post(self, new_data, team_id):
        team = get_resource_or_404(Team, team_id, "Team")
        agent = get_resource_or_404(Agent, new_data.get("agent_id"), "Agent")


        if team.add_agent(agent):
            return team.to_dict()["agents"], 201

        abort(418, message=f"Team {team_id} is full or lair is unsecret")


    
@blp.route("/team/<int:team_id>/space")
class TeamSpace(MethodView):
    def get(self, team_id):
        team = get_resource_or_404(Team, team_id, "Team")
        return {"space": team.space()}


@blp.route("/team/<int:team_id>/flee")
class TeamFlee(MethodView):
    @blp.arguments(TeamFleeSchema)
    def put(self, update_data, team_id):
        random_choice = update_data.get('random', False)
        other_team_id = update_data.get('other_team')

        # Validiere die Eingabedaten
        if random_choice and other_team_id is not None:
            abort(400, message='Cannot specify "other_team" when "random" is true.')
        if not random_choice and other_team_id is None:
            abort(400, message='Must specify "other_team" when "random" is false.')

        # Hole das Team
        team = get_resource_or_404(Team, team_id, "Team")
        # Wähle ein zufälliges Team oder ein spezifisches Team
        if random_choice:
            # Team kann nicht vor sich selbst fliehen
            team_list = [t for t in Team.teams.values() if t != team]  
            if not team_list:
                abort(404, message="No other teams available to flee to.")
            other_team = random.choice(team_list)
        else:
            other_team = Team.get(other_team_id)

        if other_team is None:
            abort(404, message=f"Other Team with id {other_team_id} not found.")

        if team == other_team:
            abort(404, message="Can't flee to same team.")

        # Führe den Fluchtvorgang aus
        team.flee(other_team)
        return {"message": "Flee operation successful"}, 200


@blp.route("/team/<int:team_id>/agent/<int:agent_id>")
class TeamAgentDetail(MethodView):
    def delete(self, team_id, agent_id):
        team = get_resource_or_404(Team, team_id, "Team")
        if agent_id not in team.agents:
            abort(404, message=f"Agent {agent_id} in Team {team_id} not found.")

        del team.agents[agent_id]  # Entfernt den Agenten aus dem Team
        return {"message" : f"removed agent {agent_id} from Team with id {team_id}"}, 204
