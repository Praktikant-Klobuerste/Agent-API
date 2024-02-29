from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import AgentSchema

agents = {}
blp = Blueprint("Agent", __name__, description="Operations on Agents")

class Agent:
    nAgents = 0
    def __init__(self, name, eye_color):
        self.name = name
        self.eye_color = eye_color
        self.code = Agent.nAgents
        Agent.nAgents += 1
    
    def __eq__(self, other):
        if type(other) != Agent:
            return False
        else:
            return other.code == self.code
    
    def __repr__(self):
        return f'{self.name, self.eye_color, self.code}'
    
    
@blp.route("/agent")
class AgentList(MethodView):
    def get(self):
        """Idiot"""
        return agents
    
    @blp.arguments(AgentSchema)
    def post(self, request_data):
        print(request_data)
        agent = Agent(request_data["name"], request_data["eye_color"])
        agents[agent.code] = {"name" : agent.name,
                              "eye_color" : agent.eye_color,
                              "code" : agent.code}
        print(agents)
        return agent.__dict__, 201
    
    

@blp.route("/agent/<int:agent_id>")
class Agentt(MethodView):
    @blp.response(200, AgentSchema)
    def get(self, agent_id):
        try:
            return agents[agent_id]
        
        except KeyError:
            abort(404, message="Agent not found.")

    def delete(self, agent_id):
        try:
            del agents[agent_id]
            return {"message" : "removed agent"}
        
        except KeyError:
            abort(404, message="Agent not found.")
        