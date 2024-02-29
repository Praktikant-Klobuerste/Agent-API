from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import AgentSchema


blp = Blueprint("Agent", __name__, description="Operations on Agents")

class Agent:
    _nAgents = 0
    _registry = {}

    def __init__(self, name, eye_color):
        self.name = name
        self.eye_color = eye_color
        self.code = Agent._nAgents
        Agent._nAgents += 1
        Agent._registry[self.code] = self
    
    def __eq__(self, other):
        if type(other) != Agent:
            return False
        else:
            return other.code == self.code
        
    def __repr__(self):
        return f'{self.name, self.eye_color, self.code}'
    
    def to_dict(self):
        return {"name" : self.name, "eye_color" : self.eye_color, "code" : self.code}
    
    @classmethod
    def get(cls, agent_id):
        return cls._registry.get(agent_id)



@blp.route("/agent")
class AgentList(MethodView):
    def get(self):
        """Idiot"""
        return [agent.to_dict() for agent in Agent._registry.values()]
    

    @blp.arguments(AgentSchema)
    @blp.response(201, AgentSchema)
    def post(self, new_data):
        # print(new_data)
        agent = Agent(**new_data)
        print(Agent._registry)
        return agent.to_dict()
    
    

@blp.route("/agent/<int:agent_id>")
class AgentResource(MethodView):
    @blp.response(200, AgentSchema)
    def get(self, agent_id):
        agent = Agent.get(agent_id)
        if agent is None:
            abort(404, message="Agent not found.")
        else:
            return agent.to_dict()

    def delete(self, agent_id):
        agent = Agent.get(agent_id)
        if agent is None:
            abort(404, message="Agent not found.")
        else:
            del Agent._registry[agent_id]
            return {"message" : f"removed agent {agent_id}"}
        