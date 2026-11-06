# ADR 0002: Anbindung der Web-App über rosbridge und roslibpy

**Status:** akzeptiert (PI-1)

**Kontext:** Die Web-App braucht Zugriff auf ROS-Services. Optionen: (A) gemeinsame Datenbank, (B) REST-API mit ROS-Client, (C) rosbridge mit roslibpy, (D) Webserver als ROS-Node.

**Entscheidung:** Option C. Sie ist Vorgabe der Aufgabe, bietet eine Live-Verbindung und die Web-App muss kein ROS-Node sein.

**Folgen:** rosbridge hat ab Werk keine Authentifizierung. Betrieb nur im lokalen Netz mit Testdaten. Absicherung ist für PI-2/3 geplant.
