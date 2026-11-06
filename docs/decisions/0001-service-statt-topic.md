# ADR 0001: ROS-Service statt Topic für Präferenzen

**Status:** akzeptiert (PI-1)

**Kontext:** Die Web-Seite muss erfahren, ob das Speichern geklappt hat, und der Wert muss abfragbar sein.

**Entscheidung:** Zwei Services, `/assistant/get_preferences` und `/assistant/set_preferences`. Der Vertrag steht in `assistant_interfaces/srv/*.srv`.

**Folgen:** Frage und Antwort sind eindeutig. Ereignisse ohne Antwort (Notruf, Akku) planen wir später als Topic. Änderungen am Vertrag erfordern Build, `source` und Neustart von rosbridge und Node.
