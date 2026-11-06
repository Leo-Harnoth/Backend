# Assistant Backend: Web-Interface für Betreuungspersonen

Team **Assistant Backend** · Projekt Software Engineering (HWR Berlin) · Roboter zur Unterstützung blinder und sehbehinderter Menschen (Turtlebot3, ROS 2 Jazzy)

Eine Betreuungsperson stellt in einer Webseite die **Sprache des Roboters** ein. Die Einstellung wird über rosbridge in eine SQLite-Datenbank im Roboter-System geschrieben und kann von anderen Teams per ROS-Service abgerufen werden.

**Stand PI-1:** nur die Sprache (Deutsch, English). Weitere Einstellungen, Notruf-Mail und Benachrichtigungen folgen in späteren PIs (siehe `docs/`).

## Architektur

```
Browser ──HTTP:5000──► Web-App (Flask) ──roslibpy──► rosbridge (WebSocket :9090)
                                                          │ ROS-2-Service-Aufruf
                                                          ▼
                              Backend-Node (rclpy) ──► preferences_db.py ──► SQLite
                                                                    ~/.assistant/assistant.db
```

| Baustein | Datei | Aufgabe |
|---|---|---|
| Service-Definitionen | `ros2_ws/src/assistant_interfaces/srv/*.srv` | Vertrag: Felder von Anfrage und Antwort |
| Datenbank-Logik (ohne ROS) | `ros2_ws/src/assistant_backend/assistant_backend/preferences_db.py` | Lesen, Schreiben, Validierung |
| Backend-Node (dünne ROS-Hülle) | `ros2_ws/src/assistant_backend/assistant_backend/backend_node.py` | Bietet `/assistant/get_preferences` und `/assistant/set_preferences` an |
| Web-App | `webapp/app.py` | Formular, Validierung, optionaler PIN-Schutz, Demo-Modus |
| Testskript | `tools/test_roslibpy.py` | Ruft beide Services über rosbridge auf |

## Voraussetzungen

Ubuntu 24.04 (VM), ROS 2 Jazzy, `ros-jazzy-rosbridge-suite`, Python 3.

```bash
sudo apt install -y python3-pip python3-flask git ros-jazzy-rosbridge-suite sqlite3
pip install roslibpy --break-system-packages
```

## Bauen

```bash
cd ros2_ws
colcon build
source install/setup.bash
```

Nach jeder Änderung an `.srv`-Dateien neu bauen, `source` ausführen und rosbridge sowie Node neu starten.

## Starten (je ein Terminal, in jedem zuerst `source ros2_ws/install/setup.bash`)

| Terminal | Befehl |
|---|---|
| 1 | `ros2 launch rosbridge_server rosbridge_websocket_launch.xml` |
| 2 | `ros2 run assistant_backend backend_node` |
| 3 | `cd webapp && python3 app.py` (Seite: http://localhost:5000) |
| 4 | Tests und Gegenprobe (siehe unten) |
| 5 | `tools/watch_db.sh` (Datenbank live anzeigen) |

Reihenfolge einhalten: erst rosbridge, dann Node, dann Web-App.

Optionen für die Web-App (Umgebungsvariablen): `MOCK=1` (Demo ohne ROS), `ACCESS_PIN=1234` (PIN-Schutz), `ROSBRIDGE_HOST`, `ROSBRIDGE_PORT`, `PORT`.

## Prüfen

```bash
# Gegenprobe direkt am Service (ohne Web und rosbridge)
ros2 service call /assistant/get_preferences assistant_interfaces/srv/GetPreferences "{user_id: 1}"

# Durchstich über rosbridge
python3 tools/test_roslibpy.py

# Unit-Tests der Datenbank-Logik (ohne ROS)
python3 -m unittest discover -s ros2_ws/src/assistant_backend/test -v
```

## Bekannte Grenzen (PI-1)

- rosbridge hat ab Werk keine Authentifizierung: nur im lokalen Netz betreiben, nur Testdaten.
- Die PIN schützt nur das Speichern in der Web-App, läuft über unverschlüsseltes HTTP und hat kein Limit für Fehlversuche.
- Erlaubte Sprachen stehen doppelt (`app.py` und `preferences_db.py`), müssen mit Conversational abgestimmt werden.
- Ein fester Nutzer (`user_id = 1`).
- Zugangsdaten, Datenbankdateien und `config.yaml` gehören nicht ins Repo (siehe `.gitignore`).

## Dokumentation

- `docs/tech-stack.md`: Tech-Stack, gebaut und geplant
- `docs/epic-and-stories-pi1.md`: Epic und Stories für PI-1
- `docs/decisions/`: Decision Records
