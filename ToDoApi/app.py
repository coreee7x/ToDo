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

# Liefert alle Einträge einer Todo-Liste zurück.
@app.route('/todo-list/<uuid:liste_id>/entries', methods=['GET'])
def getAllEinträgeById(liste_id):

    liste_id = str(liste_id)
    
    einträge = []
    for eintrag in todo_einträge:
        if eintrag['liste_id'] == liste_id:
            einträge.append(eintrag)

    if not einträge:
        return jsonify({"error": "Keine Einträge zu dieser Listen-ID gefunden"}), 404
    
    return jsonify(einträge), 200

# Route die alle Listen zurückgibt
@app.route('/todo-lists', methods=['GET'])
def getAllListen():
    return jsonify(todo_listen), 200

# Fügt eine neue Todo-Liste hinzu.
@app.route('/todo-list', methods=['POST'])
def insertListe():
    params = request.json

    if 'name' not in params:
        return jsonify({"error": "Name der Liste fehlt"}), 400
    
    liste_id = str(uuid.uuid4())
    todo_listen.append({"id": liste_id, "name": params['name']})

    return jsonify({"id": liste_id, "name": params['name']}), 200

# Fügt einen Eintrag zu einer bestehenden Todo-Liste hinzu.
@app.route('/todo-list/<uuid:liste_id>/entry', methods=['POST'])
def insertEintrag(liste_id):
    params = request.json

    if 'name' not in params or 'beschreibung' not in params:
        return jsonify({"error": "Fehlende Felder: name, beschreibung oder liste_id"}), 400
    
    if not any(liste['id'] == str(liste_id) for liste in todo_listen):
        return jsonify({"error": "Liste mit der angegebenen ID existiert nicht"}), 404
    
    eintrag_id = str(uuid.uuid4())

    todo_einträge.append({
        "id": eintrag_id,
        "name": params['name'],
        "beschreibung": params['beschreibung'],
        "liste_id": liste_id
    })
    return jsonify({"id": eintrag_id, "name": params['name'], "beschreibung": params['beschreibung']}), 200

# Aktualisiert einen bestehenden Eintrag einer Todo-Liste.
@app.route('/todo-list/<uuid:liste_id>/entry/<uuid:eintrag_id>', methods=['PUT'])
def updateEintrag(liste_id, eintrag_id):
    params = request.json

    if 'name' not in params or 'beschreibung' not in params:
        return jsonify({"error": "Fehlende Felder: id, name oder beschreibung"}), 400

    eintrag = []
    
    for item in todo_einträge:
        if item['id'] == eintrag_id:
            eintrag = item
            break

    if not eintrag:
        return jsonify({"error": "Eintrag mit der angegebenen ID existiert nicht"}), 404

    # Aktualisiere die Felder des Eintrags
    eintrag['name'] = params['name']
    eintrag['beschreibung'] = params['beschreibung']

    return jsonify({"id": eintrag_id, "name": params['name'], "beschreibung": params['beschreibung']}), 200

# Löscht einen einzelnen Eintrag einer Todo-Liste. 
@app.route('/todo-list/<uuid:liste_id>/entry/<uuid:eintrag_id>', methods=['DELETE'])
def deleteEintrag(liste_id, eintrag_id):
    
    eintrag = []

    for item in todo_einträge:
        if item['id'] == eintrag_id:
            eintrag = item
            break
    
    if not eintrag:
        return jsonify({"error": "Eintrag mit der angegebenen ID existiert nicht"}), 404

    todo_einträge.remove(eintrag)
                                                        # Für UI hinzugefügt
    return jsonify({"message": "Eintrag wurde gelöscht", "id": eintrag_id}), 200

# Löscht eine komplette Todo-Liste mit allen Einträgen
@app.route('/todo-list/<string:liste_id>', methods=['DELETE'])
def deleteListe(liste_id):

    liste = []

    for item in todo_listen:
        if item['id'] == liste_id:
            liste = item
            break
    
    if not liste:
        return jsonify({"error": "Liste mit der angegebenen ID existiert nicht"}), 404

    todo_listen.remove(liste)
    eintrag_delete = []

    for eintrag in todo_einträge:
        if(eintrag['liste_id'] == liste_id):
            eintrag_delete.append(eintrag)

    for eintrag in eintrag_delete:
        todo_einträge.remove(eintrag)
                                                                    # Für UI hinzugefügt
    return jsonify({"message": "Liste mit Einträgen wurde gelöscht", "id": liste_id}), 200

if __name__ == '__main__':
 # starte Flask-Server
 app.run(host='0.0.0.0', port=5000)