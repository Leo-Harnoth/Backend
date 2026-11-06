# Tech Stack

## Stand PI-1 (gebaut)

| Tech element | What for | Why |
|---|---|---|
| Python 3 (rclpy, roslibpy, Flask, sqlite3) | Backend-Node, Datenbank-Logik, Web-Interface, Client für rosbridge | Eine Sprache für alle Teile, Logik von ROS getrennt, einzeln testbar |
| ROS 2 Jazzy | Kommunikation mit den Nodes der anderen Teams | Vorgabe des Kurses |
| `.srv`-Definitionen (`assistant_interfaces`) | Vertrag zu anderen Teams | Service statt Topic, weil die Web-Seite eine Antwort braucht (siehe ADR 0001) |
| SQLite | Präferenzen pro Nutzer | Eine Datei, kein Server, leichtgewichtig (ADR 0003) |
| rosbridge | Brücke Web zu ROS (WebSocket, Port 9090) | Vorgabe der Aufgabe (ADR 0002) |
| Ubuntu 24.04 VM, colcon | Entwicklung und Build | Vorgabe, Jazzy läuft nur auf Ubuntu 24.04 |
| Git, GitHub `hwr-sew26` | Versionsverwaltung | Vorgabe des Kurses |

## Geplant (tbd, mit anderen Teams abzustimmen)

| Tech element | PI | What for |
|---|---|---|
| Weitere `.srv`-Felder | 2 | Lautstärke, Sprechgeschwindigkeit, Rückmeldungsart |
| Python: smtplib, `notify()`, pytest | 2 | Notfall-Mail, zentraler Meldungseingang mit Log, Tests mit Mock |
| `rules.yaml`, `config.yaml` | 2 | Routing Typ zu Kanal, Standardwerte; Zugangsdaten nur per Umgebungsvariable |
| ROS-Topic `/assistant/events` (`.msg`) | 2/3 | Eingehende Ereignisse (Notruf, Akku, Kontaktverlust) |
| Absicherung rosbridge | 2/3 | Zugriffsschutz und verschlüsselte Übertragung |
| Audio- und Haptik-Kanäle | 3 | Meldungen an den Nutzer über Conversational und Haptic |
| Mehrere Profile, Offline-Verhalten | 3 | Profilwechsel, Warteschlange ohne WLAN |
| Raspberry Pi, systemd-Autostart | 4 | Zielplattform, Start beim Booten |
| Datenschutz | 4 | Speicherort, Löschfunktion, nur nötige Daten |
| Gazebo (optional) | – | Integrationstests ohne freien Roboter |
