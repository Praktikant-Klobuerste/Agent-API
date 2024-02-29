from marshmallow import Schema, fields


class AgentSchema(Schema):
    code = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    eye_color = fields.Str(required=True)


class LairSchema(Schema):
    id = fields.Int(dump_only=True)
    secret = fields.Bool(dump_only=True)
    name = fields.Str(required=True)
    cap = fields.Int(required=True)