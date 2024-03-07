from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import LairSchema

lairs = {}
blp = Blueprint("Lair", __name__, description="Operations on Lairs")

class Lair():
    _nLairs = 0
    _registry = {}

    def __init__(self, name, cap):
        self.id = Lair._nLairs
        self.name = name
        self.cap = cap
        self.secret = True
        Lair._nLairs += 1
        Lair._registry[self.id] = self

    def unmask(self):
        self.secret = False

    def to_dict(self):
        return {"id": self.id, "name": self.name, "cap": self.cap, "secret": self.secret}

    @classmethod
    def get(cls, lair_id):
        return cls._registry.get(lair_id)
    

@blp.route("/lair")
class LairsList(MethodView):

    @blp.response(200, LairSchema(many=True))
    def get(self):
        print(Lair._registry)
        return [lair.to_dict() for lair in Lair._registry.values()]
        # return {lair.id : lair.to_dict() for lair in Lair._registry.values()}

    @blp.arguments(LairSchema)
    @blp.response(201, LairSchema)
    def post(self, new_data):
        lair = Lair(**new_data)
        return lair.to_dict()
    

@blp.route("/lair/<int:lair_id>")
class LairResource(MethodView):

    @blp.response(200, LairSchema)
    def get(self, lair_id):
        lair = Lair.get(lair_id)
        if lair is None:
            abort(404, message="Lair not found.")
        return lair.to_dict()



@blp.route('/lair//<int:lair_id>/unmask')
class LairUnmaskResource(MethodView):
    @blp.response(200, LairSchema)
    def put(self, lair_id):
        lair = Lair.get(lair_id)
        if lair is None:
            abort(404, message="Lair not found.")
        lair.unmask()
        return lair.to_dict()