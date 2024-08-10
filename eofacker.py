import os
import subprocess
import argparse
import logging
import socket
from Crypto.Cipher import AES
import hashlib
from time import sleep
from threading import Thread
import requests

# Configuration des logs
logging.basicConfig(filename='ecofacker_protect.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Liste de proxies pour la rotation (pays différents)
proxies = [
    {"ip": "51.158.123.35", "port": "8811", "pays": "France"},
    {"ip": "192.252.215.2", "port": "4145", "pays": "États-Unis"},
    {"ip": "195.201.125.132", "port": "8888", "pays": "Allemagne"},
    {"ip": "178.62.193.19", "port": "1080", "pays": "Royaume-Uni"},
    {"ip": "109.201.9.97", "port": "1080", "pays": "Pays-Bas"},
    {"ip": "185.61.94.65", "port": "9050", "pays": "Suisse"},
    {"ip": "203.142.69.242", "port": "1080", "pays": "Singapour"},
    {"ip": "206.189.35.148", "port": "1080", "pays": "Canada"},
    {"ip": "45.77.137.137", "port": "1080", "pays": "Japon"},
    {"ip": "143.110.151.79", "port": "1080", "pays": "Inde"},
    {"ip": "167.172.236.51", "port": "1080", "pays": "Brésil"}
]

# Historique des tentatives suspectes
suspicious_ips = {}

# Configuration du seuil de bannissement
max_attempts = 3

def verifier_root():
    """Vérifie que le script est exécuté avec les privilèges root."""
    if os.geteuid() != 0:
        print("Erreur : Ce script doit être exécuté avec des privilèges root.")
        sys.exit(1)

def verifier_interface(interface):
    """Vérifie si l'interface réseau spécifiée est valide."""
    try:
        result = subprocess.check_output(["ifconfig", interface])
        logging.info(f"Interface {interface} trouvée.")
        return True
    except subprocess.CalledProcessError:
        logging.error(f"Interface {interface} non trouvée.")
        return False

def changer_adresse_mac(interface):
    """Change l'adresse MAC de l'interface spécifiée."""
    try:
        nouvelle_mac = "02:%02x:%02x:%02x:%02x:%02x" % (
            os.urandom(1)[0], os.urandom(1)[0], os.urandom(1)[0], os.urandom(1)[0], os.urandom(1)[0])
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", nouvelle_mac])
        subprocess.call(["ifconfig", interface, "up"])
        logging.info(f"Adresse MAC changée pour {interface} : {nouvelle_mac}")
        print(f"Adresse MAC changée pour {nouvelle_mac}")
    except Exception as e:
        logging.error(f"Erreur lors du changement d'adresse MAC : {str(e)}")
        sys.exit(f"Erreur : {str(e)}")

def changer_adresse_ip(interface):
    """Change l'adresse IP de l'interface spécifiée."""
    try:
        subprocess.call(["dhclient", "-r", interface])
        subprocess.call(["dhclient", interface])
        ip = subprocess.check_output(["ifconfig", interface])
        logging.info(f"Adresse IP changée avec succès pour {interface}.")
        print("Adresse IP changée avec succès")
    except Exception as e:
        logging.error(f"Erreur lors du changement d'adresse IP : {str(e)}")
        sys.exit(f"Erreur : {str(e)}")

def cloturer_connexions(port):
    """Ferme toutes les connexions sauf celles sur le port spécifié."""
    try:
        subprocess.call(["iptables", "-F"])
        subprocess.call(["iptables", "-A", "INPUT", "-p", "tcp", "--dport", port, "-j", "ACCEPT"])
        subprocess.call(["iptables", "-A", "OUTPUT", "-p", "tcp", "--sport", port, "-j", "ACCEPT"])
        subprocess.call(["iptables", "-A", "INPUT", "-j", "DROP"])
        subprocess.call(["iptables", "-A", "OUTPUT", "-j", "DROP"])
        logging.info(f"Toutes les connexions sont fermées sauf sur le port {port}")
        print(f"Toutes les connexions sont fermées sauf sur le port {port}")
    except Exception as e:
        logging.error(f"Erreur lors de la configuration d'iptables : {str(e)}")
        sys.exit(f"Erreur : {str(e)}")

def surveiller_traffic(port):
    """Surveille le trafic sur le port spécifié et détecte les tentatives suspectes."""
    try:
        print(f"Surveillance du trafic sur le port {port}...")
        logging.info(f"Surveillance du trafic sur le port {port} démarrée.")
        while True:
            with os.popen(f"netstat -anp | grep {port}") as stream:
                for line in stream:
                    ip = line.split()[4].split(':')[0]
                    if ip not in suspicious_ips:
                        suspicious_ips[ip] = 1
                    else:
                        suspicious_ips[ip] += 1
                        if suspicious_ips[ip] > max_attempts:
                            bannir_ip(ip)
                            logging.info(f"IP {ip} bannie après {suspicious_ips[ip]} tentatives suspectes.")
                            print(f"IP {ip} bannie après {suspicious_ips[ip]} tentatives suspectes.")
                            traceroute_ip(ip)
                            break
            sleep(1)
    except Exception as e:
        logging.error(f"Erreur lors de la surveillance du trafic : {str(e)}")
        sys.exit(f"Erreur : {str(e)}")

def bannir_ip(ip):
    """Bannit une IP en ajoutant une règle iptables."""
    subprocess.call(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
    subprocess.call(["iptables", "-A", "OUTPUT", "-d", ip, "-j", "DROP"])

def traceroute_ip(ip):
    """Exécute un traceroute pour une IP suspecte."""
    logging.info(f"Traceroute pour {ip}:")
    subprocess.call(["traceroute", ip])

def verifier_proxy(ip, port):
    """Vérifie si un proxy est fonctionnel."""
    try:
        proxies = {
            "http": f"socks5://{ip}:{port}",
            "https": f"socks5://{ip}:{port}"
        }
        response = requests.get("http://www.google.com", proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True
    except Exception as e:
        logging.error(f"Proxy {ip}:{port} non fonctionnel : {str(e)}")
    return False

def rotation_proxy():
    """Gère la rotation des proxies en changeant périodiquement le proxy utilisé."""
    current_proxy = 0
    while True:
        proxy = proxies[current_proxy]
        ip, port, pays = proxy["ip"], proxy["port"], proxy["pays"]
        if verifier_proxy(ip, port):
            socks.set_default_proxy(socks.SOCKS5, ip, int(port))
            socket.socket = socks.socksocket
            logging.info(f"Proxy fonctionnel trouvé pour {pays} : {ip}:{port}")
            print(f"Proxy fonctionnel trouvé pour {pays} : {ip}:{port}")
            sleep(60 * 10)  # Rotation toutes les 10 minutes, à adapter selon vos besoins
        else:
            print(f"Proxy {ip}:{port} non fonctionnel, tentative avec le proxy suivant...")
        current_proxy = (current_proxy + 1) % len(proxies)

def generer_clef_chiffrement(mot_clef):
    """Génère une clé de chiffrement AES à partir d'un mot-clé utilisateur."""
    return hashlib.sha256(mot_clef.encode()).digest()

def chiffrer_donnees(data, mot_clef):
    """Chiffre les données en utilisant AES avec une clé basée sur un mot-clé."""
    key = generer_clef_chiffrement(mot_clef)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return nonce, ciphertext, tag

def dechiffrer_donnees(nonce, ciphertext, tag, mot_clef):
    """Déchiffre les données en utilisant AES avec une clé basée sur un mot-clé."""
    key = generer_clef_chiffrement(mot_clef)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data.decode('utf-8')

def couper_connexions_et_reinitialiser_chiffrement():
    """Coupe toutes les connexions et demande un nouveau mot-clé pour le chiffrement."""
    subprocess.call(["iptables", "-F"])  # Flush toutes les connexions
    nouveau_mot_clef = input("Suspicion de danger détectée. Entrez un nouveau mot-clé pour le chiffrement : ")
    logging.info("Connexions coupées et chiffrement réinitialisé.")
    return nouveau_mot_clef

def main():
    verifier_root()

    parser = argparse.ArgumentParser(description="Script de protection avancée pour l'association EcoFacker.")
    parser.add_argument('--interface', type=str, required=True, help="Interface réseau à utiliser")
    parser.add_argument('--port', type=str, default="8080", help="Port à utiliser pour les connexions autorisées")
    parser.add_argument('--mot_clef', type=str, required=True, help="Mot-clé pour le chiffrement des données")
    parser.add_argument('--utiliser_proxy', action='store_true', help="Activer la rotation des proxies")
    parser.add_argument('--chiffrement_seul', action='store_true', help="Activer uniquement le chiffrement sans proxy")
    args = parser.parse_args()

    if verifier_interface(args.interface):
        changer_adresse_mac(args.interface)
        changer_adresse_ip(args.interface)
        cloturer_connexions(args.port)

        if args.utiliser_proxy:
            print("Rotation des proxies activée")
            proxy_thread = Thread(target=rotation_proxy)
            proxy_thread.start()
        else:
            print("Proxy désactivé. Utilisation de la connexion directe avec chiffrement.")

        try:
            surveiller_traffic(args.port)
        except KeyboardInterrupt:
            logging.info("Script arrêté par l'utilisateur.")
            print("Script arrêté par l'utilisateur.")
    else:
        sys.exit("Erreur : Interface réseau non trouvée.")

if __name__ == "__main__":
    main()
