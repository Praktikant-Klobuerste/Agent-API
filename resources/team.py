from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from schemas import AgentSchema

teams = {}
blp = Blueprint("Team", __name__, description="Operations on Teams")



class Team():
    def __init__(self) -> None:
        pass

@blp.route("/team")
class TeamsList(MethodView):
    def get():
        return {}
    
    def post():
        return {}
    
@blp.route("/team/<string:team_id>")
class TeamList(MethodView):
    def get(team_id):
        return {team_id}
    
    def put():
        return {}
    
    def delete():
        return {}