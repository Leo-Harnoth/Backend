"""Web-Interface für Betreuungspersonen: Sprache des Roboters einstellen.

Start:   python3 app.py                (verbindet sich mit rosbridge auf localhost:9090)
Demo:    MOCK=1 python3 app.py         (ohne ROS, Wert nur im Speicher)
Optional: ROSBRIDGE_HOST, ROSBRIDGE_PORT, ACCESS_PIN, PORT

Erwartete ROS-Services (Vorschlag, mit den Teams abstimmen):
  /assistant/get_preferences  assistant_interfaces/srv/GetPreferences
      int32 user_id --- string language
  /assistant/set_preferences  assistant_interfaces/srv/SetPreferences
      int32 user_id, string language --- bool success, string message
"""
import os
import roslibpy
from flask import Flask, render_template_string, request

HOST = os.environ.get("ROSBRIDGE_HOST", "localhost")
ROS_PORT = int(os.environ.get("ROSBRIDGE_PORT", "9090"))
PIN = os.environ.get("ACCESS_PIN", "")  # leer = kein Schutz (nur für Tests!)
LANGUAGES = {"de": "Deutsch", "en": "English"}
USER_ID = 1  # PI-1: ein Nutzer
DEFAULT_LANGUAGE = "de"

app = Flask(__name__)
_mock_language = DEFAULT_LANGUAGE
client = None
mock = os.environ.get("MOCK") == "1"

if not mock:
    try:
        client = roslibpy.Ros(host=HOST, port=ROS_PORT)
        client.run(timeout=5)
    except Exception as e:  # rosbridge nicht erreichbar -> Demo-Modus
        print("rosbridge nicht erreichbar, Demo-Modus:", e)
        mock = True


def _service(name, typ):
    return roslibpy.Service(client, f"/assistant/{name}", f"assistant_interfaces/srv/{typ}")


def get_language():
    if mock:
        return _mock_language
    r = _service("get_preferences", "GetPreferences").call(
        roslibpy.ServiceRequest({"user_id": USER_ID}), timeout=5)
    return r["language"]


def set_language(lang):
    global _mock_language
    if mock:
        _mock_language = lang
        return True, "Gespeichert (Demo-Modus)"
    r = _service("set_preferences", "SetPreferences").call(
        roslibpy.ServiceRequest({"user_id": USER_ID, "language": lang}), timeout=5)
    return bool(r["success"]), r.get("message", "")


PAGE = """<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Roboter einrichten</title>
<style>
 body{font:18px/1.5 system-ui,sans-serif;max-width:34rem;margin:2rem auto;padding:0 1rem;color:#111;background:#fff}
 label{display:block;margin-top:1.2rem;font-weight:600}
 select,input{width:100%;font-size:1rem;padding:.6rem;margin-top:.3rem;border:2px solid #333;border-radius:6px;box-sizing:border-box}
 button{margin-top:1.5rem;font-size:1.1rem;padding:.8rem 1.4rem;background:#0b4f9c;color:#fff;border:0;border-radius:6px;cursor:pointer}
 button:focus,select:focus,input:focus{outline:3px solid #f5a300}
 .msg{padding:.8rem;border-radius:6px;margin:1rem 0}.ok{background:#d9f2dd}.err{background:#fde0e0}
 .demo{background:#fff3cd;padding:.5rem;border-radius:6px}
</style></head><body>
<h1>Roboter einrichten</h1>
{% if mock %}<p class="demo">Demo-Modus: keine Verbindung zum Roboter, Wert nur im Speicher.</p>{% endif %}
{% for m in errors %}<div class="msg err" role="alert">{{ m }}</div>{% endfor %}
{% if saved %}<div class="msg ok" role="status">{{ saved }}</div>{% endif %}
<form method="post">
 <label for="language">Sprache des Roboters</label>
 <select id="language" name="language">
 {% for k,v in languages.items() %}<option value="{{k}}" {{'selected' if language==k}}>{{v}}</option>{% endfor %}
 </select>
 {% if pin_required %}<label for="pin">PIN</label><input id="pin" name="pin" type="password" autocomplete="off">{% endif %}
 <button type="submit">Speichern</button>
</form></body></html>"""


@app.route("/", methods=["GET", "POST"])
def index():
    errors, saved = [], ""
    if request.method == "POST":
        lang = request.form.get("language", "")
        if lang not in LANGUAGES:
            errors.append("Bitte eine gültige Sprache wählen.")
        elif PIN and request.form.get("pin", "") != PIN:
            errors.append("Die PIN ist falsch.")
        else:
            try:
                ok, msg = set_language(lang)
                if ok:
                    saved = msg or "Gespeichert."
                else:
                    errors.append(msg or "Speichern fehlgeschlagen.")
            except Exception as e:
                errors.append(f"Keine Verbindung zum Roboter: {e}")
    try:
        language = get_language()
    except Exception as e:
        language = DEFAULT_LANGUAGE
        errors.append(f"Wert konnte nicht geladen werden: {e}")
    return render_template_string(PAGE, language=language, errors=errors, saved=saved, mock=mock,
                                  languages=LANGUAGES, pin_required=bool(PIN))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
