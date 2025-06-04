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

Wenn sich im Repository etwas ändern sollte kann man sich mit
´´´bash
git pull
´´´
Den aktuellen Stand herunterladen
Danach muss der Container erneut gestartet werden

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