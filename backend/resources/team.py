from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TeamSchema
from resources.lair import Lair

teams = {}
blp = Blueprint("Team", __name__, description="Operations on Teams")



class Team:
    _nTeams = 0
    _teams = {}
    def __init__(self, name, lair):
        self.name = name
        self.lair = lair
        self.id = Team._nTeams
        self.agents = {}
        Team._nTeams += 1
        Team._teams[self.id] = self


    def to_dict(self):
        return {"name" : self.name,
                "lair" : self.lair.to_dict(),
                "id" : self.id,
                "agents" : [agents.to_dict() for agents in self.agents.values()]}
    
    @classmethod
    def get(cls, team_id):
        return cls._teams.get(team_id)
    

@blp.route("/team")
class TeamsList(MethodView):
    def get(self):
        return [team.to_dict() for team in Team._teams.values()]
    
    @blp.arguments(TeamSchema)
    def post(self, new_data):
        print(new_data)
        lair = Lair.get(new_data["lair_id"])
        if lair is None:
            abort(404, message="No such lair_id")
        else:
            team = Team(name = new_data["name"], lair = lair)
            return team.to_dict()
        
    

@blp.route("/team/<int:team_id>")
class TeamList(MethodView):
    def get(self,team_id):
        print(Team.get(team_id))
        return Team.get(team_id).to_dict()
    
    
    def post(self, team_id):
        return