from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import uuid

# initialisiere Flask-Server
app = Flask(__name__)

CORS(app)
# Swagger UI-Konfiguration
SWAGGER_URL = '/docs'  # URL für Swagger UI
API_URL = '/swagger.yml'  # Endpunkt für die Swagger-Datei

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "ToDo-Api"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Route für Swagger-Datei
@app.route('/swagger.yml', methods=['GET'])
def get_swagger():
    return send_file('swagger.yml', mimetype='application/yml')

todo_listen = []  # [{id, name}]
todo_einträge = []  # [{id, name, beschreibung, liste_id}]

if __name__ == '__main__':
 # starte Flask-Server
 app.run(host='0.0.0.0', port=5000)