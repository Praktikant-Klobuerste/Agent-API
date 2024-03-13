from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TeamSchema, TeamCreateSchema, TeamUpdateSchema, Agent_to_TeamSchema, TeamFleeSchema
from resources.lair import Lair
from resources.agent import Agent
import random

teams = {}
blp = Blueprint("Team", __name__, description="Operations on Teams")



class Team:
    _nTeams = 0
    _teams = {}
    def __init__(self, name, lair:Lair):
        self.name = name
        self.lair = lair
        self.id = Team._nTeams
        self.agents = {}
        Team._nTeams += 1
        Team._teams[self.id] = self

    def __len__(self):
        return len(self.agents)
    
    def __eq__(self, other: object) -> bool:
        return self.id == other.id

    def space(self):
        return self.lair.cap - self.__len__()

    def add_agent(self, agent:Agent):
        if self.space() > 0 and self.lair.secret:
            self.agents[agent.id] = agent
            return True
        else:
            return False


    def contains(self, agent:Agent):
        return agent.id in self.agents


    def flee(self, other):
        agents_copy = self.agents.copy()
        for agent in agents_copy.values():
            if not other.contains(agent) and other.space():
                other.add_agent(agent)
                self.agents.pop(agent.id)


    def to_dict(self):
        return {"name" : self.name,
                "lair" : self.lair.to_dict(),
                "id" : self.id,
                "agents" : [agent.to_dict() for agent in self.agents.values()]}
    
    @classmethod
    def get(cls, team_id):
        return cls._teams.get(team_id)
    
    

@blp.route("/team")
class TeamsList(MethodView):
    def get(self):
        return [team.to_dict() for team in Team._teams.values()]
    
    @blp.arguments(TeamCreateSchema)
    @blp.response(201, TeamSchema)
    def post(self, new_data):
        # Prüfen, ob der Teamname schon vergeben ist.
        if any(team.name == new_data["name"] for team in Team._teams.values()):
            abort(400, message=f"Team name '{new_data['name']}' is already in use.")

        lair = Lair.get(new_data["lair_id"])
        if lair is None:
            abort(404, message="Lair with the specified id not found.")
        team = Team(name=new_data["name"], lair=lair)
        return team.to_dict(), 201
        
    

@blp.route("/team/<int:team_id>")
class TeamDetail(MethodView):
    def get(self, team_id):
        team = Team.get(team_id)
        if team is None:
            abort(404, message=f"Team with id {team_id} not found.")
        return team.to_dict()
    
    # Zum Aktualisieren eines Teams (PUT)
    @blp.arguments(TeamUpdateSchema)
    def put(self, update_data, team_id):
        team = Team.get(team_id)
        if team is None:
            abort(404, message=f"Team with id {team_id} not found.")
        
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
        team = Team.get(team_id)
        if team is None:
            abort(404, message=f"Team with id {team_id} not found.")
        
        del Team._teams[team_id] # Löscht die Referenz zum Team
        return {"message" : f"removed agent {team_id}"},  204
    
    

@blp.route("/team/<int:team_id>/agent")
class TeamAgent(MethodView):
    def get(self, team_id):
        team = Team.get(team_id)
        if team is None: 
            abort(404, message=f"Team with id {team_id} not found.")

        return team.to_dict()["agents"]



    @blp.arguments(Agent_to_TeamSchema)
    def post(self, new_data, team_id):
        team = Team.get(team_id)
        if team is None:
            abort(404, message=f"Team with id {team_id} not found.")
        
        agent = Agent.get(new_data["agent_id"])
        if agent is None:
            abort(404, message=f"Agent with id {new_data['agent_id']} not found.")

        if team.add_agent(agent):
            return team.to_dict()["agents"], 201
        
        abort(418, message=f"Team {team_id} is full or lair is unsecret")
            

    
@blp.route("/team/<int:team_id>/space")
class TeamSpace(MethodView):
    def get(self, team_id):
        team = Team.get(team_id)
        if team is None:
            abort(404, message=f"Team with id {team_id} not found.")
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
        team = Team.get(team_id)
        if team is None:
            abort(404, message=f"Team with id {team_id} not found.")

        # Wähle ein zufälliges Team oder ein spezifisches Team
        if random_choice:
            team_list = [t for t in Team._teams.values() if t != team]  # Team kann nicht vor sich selbst fliehen
            if not team_list:
                abort(404, message="No other teams available to flee to.")
            other_team = random.choice(team_list)
        else:
            other_team = Team.get(other_team_id)
            if team == other_team:
                abort(404, message="Can't flee to same team.")

            elif other_team is None:
                abort(404, message=f"Other Team with id {other_team_id} not found.")

        # Führe den Fluchtvorgang aus
        team.flee(other_team)
        return {"message": "Flee operation successful"}, 200
    

@blp.route("/team/<int:team_id>/agent/<int:agent_id>")
class TeamAgentDetail(MethodView):
    def delete(self, team_id, agent_id):
        team = Team.get(team_id)
        if team is None or agent_id not in team.agents:
            abort(404, message=f"Agent {agent_id} in Team {team_id} not found.")
        
        del team.agents[agent_id]  # Entfernt den Agenten aus dem Team
        return {"message" : f"removed agent {agent_id} from Team with id {team_id}"}, 204