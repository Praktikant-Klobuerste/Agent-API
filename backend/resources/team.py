from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TeamSchema, Agent_to_TeamSchema
from resources.lair import Lair
from resources.agent import Agent

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

    def space(self):
        return self.lair.cap - self.__len__()

    def add_agent(self, agent:Agent):
        if self.space() > 0 and self.lair.secret:
            self.agents[agent.id] = agent
            return True
        else:
            return False


    def contains(self, agent:Agent):
        return agent.code in self.agents


    def flee(self, other):
        agents_copy = self.agents.copy()
        for agent in agents_copy.values():
            if not other.contains(agent) and other.space():
                other.add_agent(agent)
                self.agents.pop(agent.code)


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
    
    @blp.arguments(TeamSchema)
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
    
    
@blp.route("/team/<int:team_id>/agent")
class TeamAgent(MethodView):
    def get(self, team_id):
        team = Team.get(team_id)

        if team is not None: 
            return team.to_dict()["agents"]
        else:
            abort(404, message=f"No such team: {team_id}")



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