from marshmallow import Schema, fields, validate

class AgentSchema(Schema):
    id = fields.Int(dump_only=True, description="The unique id of an Agent")
    name = fields.Str(required=True, description="The Name of an Agent", validate=validate.Length(min=1))
    eye_color = fields.Str(required=True, validate=validate.OneOf(["blue", "green", "brown", "hazel", "gray", "amber"]))

class LairSchema(Schema):
    id = fields.Int(dump_only=True, description="The unique id of the Lair")
    secret = fields.Bool(dump_only=True, description="Indicates if the Lair is secret")
    name = fields.Str(required=True, description="The Name of the Lair", validate=validate.Length(min=1))
    cap = fields.Int(required=True, description="The capacity of the Lair", validate=validate.Range(min=1))

class TeamSchema(Schema):
    id = fields.Int(dump_only=True, description="The unique id of the Team")
    name = fields.Str(required=True, description="The Name of the Team")
    lair = fields.Nested(LairSchema, description="Information about the team's lair")
    lair_id = fields.Int(required=True, description="The id of the Lair associated with the Team")

class Agent_to_TeamSchema(Schema):
    agent_id = fields.Int(required=True, description="The id of the Agent being added to the Team", validate=validate.Range(min=0))