from marshmallow import Schema, fields, validate

class AgentSchema(Schema):
    id = fields.Int(dump_only=True, description="The unique id of an Agent")
    name = fields.Str(required=True, description="The Name of an Agent", metadata={"example": "Mimoo"}, validate=validate.Length(min=1))
    eye_color = fields.Str(required=True, metadata={"example": "brown"}, validate=validate.OneOf(["blue", "green", "brown", "hazel", "gray", "amber"]))

class LairSchema(Schema):
    id = fields.Int(dump_only=True, description="The unique id of the Lair")
    secret = fields.Bool(dump_only=True, description="Indicates if the Lair is secret")
    name = fields.Str(required=True, description="The Name of the Lair", metadata={"example": "Tom's Unterhose"}, validate=validate.Length(min=1))
    cap = fields.Int(required=True, description="The capacity of the Lair", metadata={"example": 5}, validate=validate.Range(min=1))

class TeamSchema(Schema):
    id = fields.Int(dump_only=True, description="The unique id of the Team")
    name = fields.Str(required=True,  description="The Name of the Team", metadata={"example": "Gummibärenbande"}, validate=validate.Length(min=1))
    lair = fields.Nested(LairSchema, description="Information about the team's lair")
    lair_id = fields.Int(required=True, description="The id of the Lair associated with the Team")

class Agent_to_TeamSchema(Schema):
    agent_id = fields.Int(required=True, description="The id of the Agent being added to the Team", metadata={"example": 5}, validate=validate.Range(min=0))