#!/bin/bash
# Zeigt die Präferenz-Tabelle live (für die Demo). Benötigt: sudo apt install sqlite3
DB="${ASSISTANT_DB:-$HOME/.assistant/assistant.db}"
watch -n 1 "sqlite3 -header -column '$DB' 'SELECT * FROM preferences;'"
