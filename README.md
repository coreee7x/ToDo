# ToDo App

## Übersicht

Dies ist eine einfache ToDo-Anwendung, die aus einer API (ToDoApi) und einer Benutzeroberfläche (ToDoUi) besteht. Beide Komponenten können über Docker-Container bereitgestellt werden und sind über eine `docker-compose`-Datei gemeinsam startbar.

## Architektur

- **ToDoApi** (Backend)

  - Erreichbar unter: [http://coreee7x.de:5000](http://coreee7x.de:5000)
  - API-Spezifikation (Swagger/OpenAPI): [http://coreee7x.de:5000/docs](http://coreee7x.de:5000/docs)
  - Implementiert als Flask REST-API
  - Enthält CRUD-Operationen für ToDo-Elemente
  - Docker-Container verfügbar

- **ToDoUi** (Frontend)
  - Erreichbar unter: [http://coreee7x.de:5001](http://coreee7x.de:5001)
  - Implementiert mit Blazor
  - Web-Oberfläche zur Verwaltung von ToDo-Listen
  - Kommuniziert mit der ToDoApi
  - Docker-Container verfügbar

## Installation & Deployment

### Manuelles Starten

1. Klone das Repository:
   ```bash
   git clone https://github.com/coreee7x/ToDo.git
   cd ToDo
   ```
2. Starte die API:
   ```bash
   cd ToDoApi
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```
3. Starte die UI:
   ```bash
   cd ../ToDoUi
   dotnet run
   ```

### Mit Docker Compose

Um sowohl die API als auch die UI über Docker bereitzustellen, kannst du einfach folgenden Befehl ausführen:

```bash
docker-compose up -d
```

Dadurch werden die beiden Container gestartet und die Anwendung ist unter den oben angegebenen Ports erreichbar.

## Lizenz

Dieses Projekt steht unter der [MIT License](LICENSE).
