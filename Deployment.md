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
>Während der Benutzererstellung wirst du zur Eingabe eines Passworts aufgefordert. Danach folgen weitere optionale Angaben (wie Name, >Telefonnummer usw.), die leer gelassen werden können.

### Benutzer `willi` erstellen:
```bash
sudo adduser willi                      # Passwort: Test123
sudo usermod -s /usr/sbin/nologin willi # SSH Rechte entfernen
```

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
> Danach erneut mit dem Benutzer einloggen, damit die Gruppenzugehörigkeit aktiv wird.

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

