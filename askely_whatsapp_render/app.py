from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
import psycopg2
import os

app = Flask(__name__)

# Connexion PostgreSQL
def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

@app.route("/")
def index():
    return "✅ Askely WhatsApp Agent est en ligne."

@app.route("/webhook/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip().lower()
    sender = request.values.get("From", "")
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg in ["bonjour", "salut", "hello"]:
        msg.body("👋 Bienvenue sur *Askely Express* 🇲🇦

Que souhaitez-vous faire ?
"
                 "📦 [1] Envoyer un colis
🚚 [2] Devenir transporteur
🔍 [3] Suivre un colis
"
                 "🖥️ Voir les listes :
👉 https://projetcomplet.onrender.com/transporteurs
👉 https://projetcomplet.onrender.com/colis")
    else:
        msg.body("🤖 Option non reconnue. Envoyez 'bonjour' pour commencer.")

    return str(resp)

@app.route("/transporteurs")
def liste_transporteurs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT nom, ville_depart, ville_arrivee, date_depart FROM transporteurs ORDER BY date_depart")
    transporteurs = cur.fetchall()
    conn.close()
    return render_template("liste_transporteurs.html", transporteurs=transporteurs)

@app.route("/colis")
def liste_colis():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT expediteur, destinataire, date_envoi FROM colis ORDER BY date_envoi DESC")
    colis = cur.fetchall()
    conn.close()
    return render_template("liste_colis.html", colis=colis)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)