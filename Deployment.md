# Deployment der App - Raspberry Pi Setup

## Feste IP-Adresse setzen

1. Netzwerkstatus anzeigen:
   ```bash
   networkctl list
   ```

2. Netzwerk-Konfiguration bearbeiten:
   ```bash
   sudo nano /etc/systemd/network/10-eth0.network
   ```

   Inhalt der Datei:
   ```ini
   [Match]
   Name=eth0

   [Network]
   Address=192.168.24.114/24
   Gateway=192.168.24.254
   DNS=192.168.24.254
   ```
   Gateway und DNS müssen so angepasst werden, dass sie zu dem eigenen Netzwerk passen. Als IP-Adresse kann eine beliebige freie im Netzwerk gewählt werden. 

3. Netzwerkdienst aktivieren und neu starten:
   ```bash
   sudo systemctl enable systemd-networkd
   sudo systemctl restart systemd-networkd
   ```

---

## Benutzer erstellen

### Benutzer `fernzugriff` erstellen (mit `sudo`-Rechten):
```bash
sudo adduser fernzugriff                # Passwort: Test123
sudo usermod -aG sudo fernzugriff       # Sudo Rechte vergeben
```

### Benutzer `willi` erstellen:
```bash
sudo adduser willi                      # Passwort: Test123
sudo usermod -s /usr/sbin/nologin willi # SSH Rechte entfernen
```
Während der Benutzererstellung wirst du zur Eingabe eines Passworts aufgefordert. Danach folgen weitere optionale Angaben (wie Name, Telefonnummer usw.), die leer gelassen werden können.

---

## Docker installieren

Docker über das offizielle Installationsskript:
```bash
sudo curl -fsSL https://get.docker.com | sudo sh
```

### Docker-Rechte für Benutzer `fernzugriff`:
```bash
sudo usermod -aG docker fernzugriff
```

### Neu anmelden (empfohlen):
```bash
exit
```
> Danach erneut mit dem Benutzer einloggen, damit die Rechte aktiviert werden.

---

## Repository vom Programm holen

### Möglichkeit 1: Manuell per SSH oder Dateiübertragung
Wenn man schon über SSH mit dem Raspberry Pi verbunden ist kann man (bspw. über VS Code) das Repository einfach per Drag und Drop auf den Raspberry Pi ziehen. Wenn sich die Software allerdings öfters ändert ist es meist einfacher mit Möglichkeit 2 das Repo auf den Pi zu bekommen.

### Möglichkeit 2: Per `git clone`

1. Git installieren:
   ```bash
   sudo apt-get install git
   ```

2. In gewünschtes Verzeichnis wechseln:
   ```bash
   cd <Verzeichnis>
   ```

3. Repository klonen:
   ```bash
   git clone https://github.com/coreee7x/ToDo.git
   ```

> Wenn sich im Repository etwas ändern sollte muss man den aktuellen Stand aus dem Git herunterladen.
> Danach muss der Container erneut gebuilded und gestartet werden
> ```bash
> git pull
> sudo docker compose down
> sudo docker compose up -d --build
> ```

---

## Docker-Container starten

```yaml
version: "3.9"

services:
# Reverse Proxy Container
  traefik:
    image: traefik:v2.11
    container_name: traefik
    command:
      - "--api.dashboard=true"                 # Aktiviert das Traefik-Dashboard zur Überwachung
      - "--providers.docker=true"              # Aktiviert die automatische Konfiguration basierend auf Docker-Labels
      - "--entrypoints.web.address=:80"        # Legt den EntryPoint für HTTP auf Port 80 fest
      - "--log.level=DEBUG"                    # Detailliertes Logging für Debugging aktivieren
# Über Standardport erreichbar (alles läuft über den Proxy)
    ports:
      - "80:80"                                # Exposed Traefik auf Port 80 nach außen
# Das Volume sorgt dafür, dass die Daten des Proxys auch nach einem Neustart/Build gespeichert bleiben
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"  
# Labels
    labels:
      - "traefik.http.routers.traefik.rule=PathPrefix(`/dashboard`) || PathPrefix(`/api`)"  # Zugriff auf Dashboard und internen API-Endpunkt
      - "traefik.http.routers.traefik.service=api@internal"  # Interner Service für das Dashboard
      - "traefik.http.routers.traefik.entrypoints=web"       # Verwendet den HTTP EntryPoint (Port 80)
    networks:
      - traefik-net

# Backend-API Container
  todoapi:
    container_name: ToDoApi
    build: ToDoApi                             # Verwendet das lokale Build-Context-Verzeichnis `ToDoApi`
    restart: unless-stopped                   # Startet den Container automatisch neu, außer er wurde manuell gestoppt
    labels:
      - "traefik.http.routers.api.rule=PathPrefix(`/api`)"   # Leitet alle Anfragen mit /api an diesen Service
      - "traefik.http.routers.api.priority=10"               # Priorität gegenüber allgemeineren Regeln
      - "traefik.http.services.api.loadbalancer.server.port=3000"  # Interner Port der API-Anwendung
      - "traefik.http.middlewares.api-strip.stripprefix.prefixes=/api"  # Entfernt /api aus dem Pfad vor Weiterleitung
      - "traefik.http.routers.api.middlewares=api-strip"     # Middleware wird dem Router zugewiesen
    networks:
      - traefik-net

# Frontend-UI Container
  todoui:
    container_name: ToDoUi
    build: ToDoUi                              # Verwendet das lokale Build-Context-Verzeichnis `ToDoUi`
    restart: unless-stopped                   # Startet den Container automatisch neu, außer er wurde manuell gestoppt
    labels:
      - "traefik.http.routers.web.rule=PathPrefix(`/ui`)"      # Fängt alle sonstigen Pfade ab
      - "traefik.http.routers.web.priority=1"                # Niedrigere Priorität als `/api`, damit API eher erreichbar ist
      - "traefik.http.services.web.loadbalancer.server.port=8080"  # Interner Port der UI-Anwendung 
    depends_on:
      - todoapi                                 # Startet `ToDoUi` erst, wenn `ToDoApi` verfügbar ist
    networks:
      - traefik-net

networks:
  traefik-net:                                  # Alle Container im gleichen Netzwerk
    driver: bridge                              # Standard Docker-Netzwerktyp (lokales virtuelles Netzwerk)

```

Falls du dich noch nicht im Projektverzeichnis befindest:
```bash
cd <Verzeichnis>
```

Dann Container im Hintergrund starten:
```bash
sudo docker compose up -d
```
> Das Argument `-d` führt dazu, dass der Container im Hintergrund gestartet wird, wenn man diesen weglässt kommt man in die CLI des Programms.

# Bonusaufgaben
## 1) ufw konfigurieren

> ufw (uncomplicated Firewall) ist eine Firewall, welche den Raspberry Pi schützt, indem sie nur ausgewählte Netzwerkzugriffe erlaubt. So bleiben interne Dienste und Ports vor unbefugtem Zugriff von außen sicher.

### ufw installieren
```bash
sudo apt install ufw
```

### Benötigte Ports freigeben
Nun müssen die benötigten Ports, in diesem Fall für SSH (22) und Websites (80 | 443) freigegeben werden, damit man den Pi noch sowohl über SSH erreicht, zum weiteren konfigurieren, als auch die Website erreichen kann.
```bash
# SSH-Zugriff erlauben
sudo ufw allow ssh

# HTTP (für unverschlüsselte Webzugriffe)
sudo ufw allow 80

# HTTPS (für verschlüsselte Webzugriffe)
sudo ufw allow 443
```
> [!WARNING]
> Wenn du diesen Schritt überspringst ist er Raspberry Pi nach dem aktivieren der Firewall nicht mehr über SSH zu erreichen und du musst den Pi an Monitor, Maus und Tastatur anschließen um weiter zu machen!

### Firewall aktivieren
```bash
sudo ufw enable
```
Die Firewall ist nun aktiviert und lässt nur Kommunikation mit den oben genannten Ports zu.

Nun kann noch der Status der Firewall überprüft werden, um sicher zu gehen, dass alles Funktioniert.
```bash
sudo ufw status
```

| Port       | Aktion | Quelle           |
|------------|--------|------------------|
| 22/tcp     | ALLOW  | Anywhere         |
| 80         | ALLOW  | Anywhere         |
| 443        | ALLOW  | Anywhere         |
| 22/tcp (v6)| ALLOW  | Anywhere (v6)    |
| 80 (v6)    | ALLOW  | Anywhere (v6)    |
| 443 (v6)   | ALLOW  | Anywhere (v6)    |

Wenn es so aussieht hat alles geklappt und die Firewall ist aktiviert.

## 2) Reverse Proxy einrichten

Die Einrichtung des Reverse Proxys wurde in der docker-compose.yml durchgeführt, dafür wurde ein neuer Traefik Container hochgezogen, die Endpunkt der API und UI entfernt und stattdessen durch ein Label gesagt, wie sie erreichbar sein sollen.