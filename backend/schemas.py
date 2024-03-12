from marshmallow import Schema, fields


class AgentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    eye_color = fields.Str(required=True)


class LairSchema(Schema):
    id = fields.Int(dump_only=True)
    secret = fields.Bool(dump_only=True)
    name = fields.Str(required=True)
    cap = fields.Int(required=True)

class TeamSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    lair_id = fields.Int(required=True)

class Agent_to_TeamSchema(Schema):
    agent_id = fields.Int(required=True)