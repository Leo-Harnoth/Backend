# Epic und Stories PI-1

## Epic: Web-Interface für Betreuungspersonen, Sprache des Roboters einstellen

**Benefit hypothesis:** Wenn eine Betreuungsperson die Sprache des Roboters über eine einfache Webseite einstellen kann und die Einstellung im Roboter-System abrufbar ist, passt sich der Roboter an den Nutzer an, ohne dass jemand Code oder Konfigurationsdateien anfassen muss. Der Durchstich zeigt außerdem früh, ob die Verbindung zwischen Web und ROS trägt.

**Definition of done**
- Webseite zum Ändern und Speichern der Sprache (Deutsch, English), mit Bestätigung oder Fehlermeldung
- Eingabe wird in Web-App und Backend geprüft
- Sprache in SQLite gespeichert, Standardwert Deutsch für unbekannte Nutzer
- ROS-Services zum Lesen und Speichern, per `ros2 service call` prüfbar
- Verbindung Web-App zu Backend über rosbridge und roslibpy
- Optionaler PIN-Schutz
- Live-Demo: Änderung im Browser, sichtbar in der Datenbank und über die Gegenprobe

## Stories

| # | Story | Status |
|---|---|---|
| S1 | Als Betreuungsperson möchte ich die Sprache auswählen und speichern, damit der Roboter in der Sprache des Nutzers spricht. | Fertig |
| S2 | Als Betreuungsperson möchte ich verständliche Fehlermeldungen, damit ich weiß, was ich tun kann. | Fertig |
| S3 | Als Betreuungsperson möchte ich, dass nur Berechtigte Einstellungen ändern (PIN). | Fertig (minimal) |
| S4 | Als Betreuungsperson möchte ich, dass die Einstellung dauerhaft gespeichert wird. | Fertig, Neustart des Nodes noch gezielt testen |
| S5 | Als Entwickler eines anderen Teams möchte ich die Sprache per ROS-Service abrufen. | Fertig, ungetestet mit echtem Aufrufer |
| S6 | Als Teammitglied möchte ich eine Verbindung vom Browser bis ins Backend. | Fertig |
| S7 | Als Teammitglied möchte ich die Web-App auch ohne ROS starten (Demo-Modus). | Fertig |
| S8 | Als Publikum der System Demo möchte ich sehen, dass die Einstellung in der Datenbank landet. | Fertig |
| E1 | Als Teammitglied möchte ich eine reproduzierbare Umgebung und Dokumentation (Enabler). | Teilweise |

## Bewusst nicht in PI-1

Weitere Einstellungen, echte Anbindung von Conversational, Notruf mit Testmail, `notify()` und Routing, mehrere Profile, Absicherung von rosbridge, HTTPS, echte Anmeldung.
