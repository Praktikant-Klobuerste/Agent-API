from flask import Flask
from flask_smorest import Api

from resources.agent import blp as AgentBlueprint
from resources.lair import blp as LairBlueprint
from resources.team import blp as TeamBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Agent API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(AgentBlueprint)
api.register_blueprint(LairBlueprint)
api.register_blueprint(TeamBlueprint)

# if __name__ == "__main__":
#     app.run(debug=True)