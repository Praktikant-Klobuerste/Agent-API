from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import AgentSchema
import random


blp = Blueprint("Agent", __name__, description="Operations on Agents")

class Agent:
    _nAgents = 0
    _registry = {}
cd
    def __init__(self, name, eye_color):
        self.name = name
        self.eye_color = eye_color
        self.id = Agent._nAgents
        Agent._nAgents += 1
        Agent._registry[self.id] = self
    
    def __eq__(self, other):
        if type(other) != Agent:
            return False
        else:
            return other.id == self.id
        
    def __repr__(self):
        return f'{self.name, self.eye_color, self.id}'
    
    def to_dict(self):
        return {"name" : self.name, "eye_color" : self.eye_color, "id" : self.id}
    
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
        

@blp.route("/agent/random")
class AgentList(MethodView):
    def get(self):
        agent_id_list = list(Agent._registry.keys())
        if len(agent_id_list):
            random_agent_id = random.choice(agent_id_list)
            return Agent.get(random_agent_id).to_dict()
            # return [agent.to_dict() for agent in Agent._registry.values()]
        else:
            abort(404, message="Agent not found.")