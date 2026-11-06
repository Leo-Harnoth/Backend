# ADR 0003: SQLite, Logik getrennt von ROS

**Status:** akzeptiert (PI-1)

**Kontext:** Wenige Nutzer, geringes Datenvolumen, geteilter Raspberry Pi.

**Entscheidung:** SQLite (eine Datei, kein Server). Die Logik liegt in `preferences_db.py` ohne ROS-Abhängigkeit, `backend_node.py` ist nur eine dünne ROS-Hülle.

**Folgen:** Logik ist ohne Roboter testbar (siehe `test/`). Bei mehreren gleichzeitigen Schreibzugriffen oder größerem Datenvolumen neu bewerten.
