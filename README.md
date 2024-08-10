# 🌐 EcoFacker Protection Script

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Introduction

**EcoFacker** est un script avancé de protection de la vie privée et de la sécurité réseau, conçu pour les utilisateurs soucieux de leur anonymat en ligne. 
Ce script offre une variété de fonctionnalités pour protéger vos connexions réseau, masquer votre identité, et chiffrer vos communications.

## 🎯 Fonctionnalités

- **Changement d'adresse MAC et IP** pour masquer votre identité réseau.
- **Clôture des connexions non autorisées** à l'aide de règles `iptables`.
- **Surveillance en temps réel** des connexions réseau avec bannissement automatique des IPs suspectes.
- **Rotation automatique des proxies** pour une anonymisation avancée.
- **Chiffrement des communications** basé sur un mot-clé utilisateur.
- **Facilité d'utilisation via CLI**, avec options pour personnaliser l'expérience utilisateur.

## 📋 Prérequis

- **Python 3.x**
- Modules Python :
  - `requests`
  - `socket`
  - `subprocess`
  - `hashlib`
  - `Crypto`
  
Pour installer les modules requis, exécutez :

```
pip install requests pycryptodome
```
⚙️ Installation

Clonez le dépôt et accédez au répertoire :

```
git clone https://github.com/votre-repo/ecofacker.git
cd ecofacker
```

Assurez-vous d'avoir les privilèges root pour exécuter le script :

```
sudo python3 ecofacker.py --interface eth0 --mot_clef votremotclef
```
🛠️ Utilisation

Commandes de Base:

  Lancer le script avec proxy activé :

    ```
    sudo python3 ecofacker.py --interface eth0 --mot_clef votremotclef --utiliser_proxy

    ```
Lancer le script sans proxy, uniquement avec chiffrement :

    ```
    sudo python3 ecofacker.py --interface eth0 --mot_clef votremotclef --chiffrement_seul
    ```
Options CLI

    --interface:         Spécifiez l'interface réseau à utiliser (ex: eth0).
    --port:              Définissez le port à utiliser pour les connexions autorisées (par défaut : 8080).
    --mot_clef:          Fournissez un mot-clé pour chiffrer les communications.
    --utiliser_proxy:    Active la rotation des proxies.
    --chiffrement_seul:  Active uniquement le chiffrement sans proxy.

🔍 Surveillance et Logs

    Les événements importants et les erreurs sont enregistrés dans le fichier ecofacker_protect.log.
    Les IPs suspectes sont automatiquement bannies et tracées via traceroute.

🤝 Contribution

Les contributions sont les bienvenues ! Veuillez soumettre un pull request ou ouvrir une issue pour discuter de nouvelles fonctionnalités ou signaler des bogues.

📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE.md pour plus de détails.

📧 Contact

Pour toute question ou suggestion, veuillez contacter notre équipe à admin@pctamalou.fr.

👏 Remerciements

Merci d'utiliser EcoFacker et de contribuer à un internet plus sûr et plus privé pour tous !

