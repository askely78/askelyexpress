import os
import psycopg2
from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Connexion PostgreSQL
DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

# Page d’accueil
@app.route("/")
def accueil():
    return """
    <html>
    <head><title>Askely Express</title></head>
    <body>
        <h2>Bienvenue sur Askely Express</h2>
        <p>Veuillez choisir une action :</p>
        <ul>
            <li><a href="/colis">📦 Voir les colis</a></li>
            <li><a href="/transporteurs">🚗 Voir les transporteurs</a></li>
            <li><a href="https://wa.me/212XXXXXXXXX">✉️ Contacter Askely sur WhatsApp</a></li>
        </ul>
    </body>
    </html>
    """

# Page liste des colis
@app.route("/colis")
def liste_colis():
    cursor.execute("SELECT id, expediteur, destinataire, ville_depart, ville_arrivee FROM colis ORDER BY id DESC")
    resultats = cursor.fetchall()
    return render_template("liste_colis.html", colis=resultats)

# Page liste des transporteurs
@app.route("/transporteurs")
def liste_transporteurs():
    cursor.execute("SELECT id, nom, telephone, ville FROM transporteurs ORDER BY id DESC")
    resultats = cursor.fetchall()
    return render_template("liste_transporteurs.html", transporteurs=resultats)

# Webhook WhatsApp
@app.route("/webhook/whatsapp", methods=["POST"])
def whatsapp():
    msg = request.form.get("Body", "").strip().lower()
    resp = MessagingResponse()
    message = resp.message()

    if "colis" in msg:
        message.body("📦 Pour voir la liste des colis : https://projetcomplet.onrender.com/colis")
    elif "transporteur" in msg:
        message.body("🚗 Pour voir la liste des transporteurs : https://projetcomplet.onrender.com/transporteurs")
    elif "bonjour" in msg or "salut" in msg:
        message.body("👋 Bonjour ! Tape 'colis' ou 'transporteur' pour commencer.")
    else:
        message.body("❓ Je ne comprends pas. Tape 'colis' ou 'transporteur'.")

    return str(resp)

# ⚠️ Ne pas ajouter app.run() pour gunicorn

