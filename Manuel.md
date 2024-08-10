
# 📘 Manuel Utilisateur - EcoFacker Protection Script

## Table des matières
1. [Introduction](#Introduction)
2. [Prérequis](#prérequis)
3. [Installation](#installation)
4. [Configuration Initiale](#configuration-initiale)
5. [Utilisation du Script](#utilisation-du-script)
    - 5.1 [Commandes de Base](#commandes-de-base)
    - 5.2 [Options CLI](#options-cli)
    - 5.3 [Exemples d'Utilisation](#exemples-dutilisation)
6. [Fonctionnalités Avancées](#fonctionnalités-avancées)
    - 6.1 [Rotation des Proxies](#rotation-des-proxies)
    - 6.2 [Chiffrement des Données](#chiffrement-des-données)
    - 6.3 [Surveillance et Bannissement Automatique](#surveillance-et-bannissement-automatique)
7. [Gestion des Logs et Surveillance](#gestion-des-logs-et-surveillance)
8. [Dépannage](#dépannage)
9. [FAQ](#faq)
10. [Support](#support)

---

## 1. Introduction

**EcoFacker** est un script Python conçu pour offrir une protection avancée de la vie privée et de la sécurité en ligne. 
Ce script permet de masquer votre identité réseau en modifiant l'adresse MAC et IP, de chiffrer vos communications, et de protéger vos connexions grâce à des règles strictes de pare-feu. 
Il est également capable de surveiller les connexions en temps réel et de bannir automatiquement les IP suspectes.

---

## 2. Prérequis

### Système d'exploitation

- **Linux** (Debian, Ubuntu, CentOS, etc.)

### Logiciels et outils nécessaires

- **Python 3.x**
- **Privilèges Root** pour exécuter certaines commandes.

### Modules Python requis

- `requests`
- `pycryptodome`

Pour installer les modules requis, exécutez :

```
pip install requests pycryptodome
```

---

## 3. Installation

### 3.1. Cloner le dépôt

Clonez le dépôt GitHub contenant le script :

```
git clone https://github.com/votre-repo/ecofacker.git
```

### 3.2. Accéder au répertoire du projet

```
cd ecofacker
```

### 3.3. Configuration des permissions

Assurez-vous que le script dispose des permissions d'exécution :

```
chmod +x ecofacker.py
```

---

## 4. Configuration Initiale

### 4.1. Vérification des privilèges Root

Le script nécessite des privilèges root pour fonctionner correctement. Assurez-vous de l'exécuter avec `sudo` ou en tant que super-utilisateur.

### 4.2. Configuration du script

Le script ne nécessite pas de configuration préalable spécifique. Cependant, vous pouvez modifier la liste des proxies dans le script si vous souhaitez utiliser des proxys différents.

---

## 5. Utilisation du Script

### 5.1. Commandes de Base

- **Lancer le script avec rotation des proxies :**

```
sudo python3 ecofacker.py --interface eth0 --mot_clef votremotclef --utiliser_proxy
```

- **Lancer le script sans proxy, uniquement avec chiffrement :**

```
sudo python3 ecofacker.py --interface eth0 --mot_clef votremotclef --chiffrement_seul
```

### 5.2. Options CLI

| Option            | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `--interface`     | Spécifiez l'interface réseau à utiliser (ex: `eth0`).                        |
| `--port`          | Définissez le port à utiliser pour les connexions autorisées (par défaut : `8080`). |
| `--mot_clef`      | Fournissez un mot-clé pour chiffrer les communications.                      |
| `--utiliser_proxy`| Active la rotation des proxies pour anonymiser davantage votre connexion.    |
| `--chiffrement_seul`| Active uniquement le chiffrement sans proxy.                 |

### 5.3. Exemples d'Utilisation

- **Chiffrement des communications sur l'interface `eth0` en utilisant le port 8080, avec rotation des proxies :**

```
sudo python3 ecofacker.py --interface eth0 --port 8080 --mot_clef monSecret --utiliser_proxy
```

- **Chiffrement sans rotation de proxy :**

```
sudo python3 ecofacker.py --interface eth0 --mot_clef monSecret --chiffrement_seul
```

---

## 6. Fonctionnalités Avancées

### 6.1. Rotation des Proxies

Le script permet de changer régulièrement de proxy pour assurer une anonymisation renforcée. 
La rotation se fait toutes les 10 minutes par défaut, mais ce paramètre peut être modifié dans le script.

### 6.2. Chiffrement des Données

Les communications sont chiffrées en utilisant AES avec une clé dérivée d'un mot-clé fourni par l'utilisateur. 
Cette fonctionnalité assure que les données sensibles ne peuvent pas être interceptées ou lues par des tiers non autorisés.

### 6.3. Surveillance et Bannissement Automatique

Le script surveille en temps réel les connexions réseau et détecte les comportements suspects. Si une adresse IP tente des connexions non autorisées, elle est automatiquement bannie après trois tentatives infructueuses.

---

## 7. Gestion des Logs et Surveillance

### 7.1. Logs

Tous les événements importants sont enregistrés dans un fichier de logs situé dans le même répertoire que le script sous le nom `ecofacker_protect.log`.

### 7.2. Surveillance en temps réel

Le script peut être configuré pour surveiller en permanence les connexions réseau, bannissant les IPs suspectes et traçant les routes pour mieux comprendre les éventuelles attaques.

---

## 8. Dépannage

### 8.1. Erreur : "Ce script doit être exécuté avec des privilèges root."

- **Solution**:
 Assurez-vous d'exécuter le script avec `sudo` ou en tant que super-utilisateur.

### 8.2. Problème de connectivité réseau après exécution du script

- **Solution**:
 Vérifiez que l'adresse IP et l'adresse MAC ont été correctement modifiées.
 Vous pouvez essayer de redémarrer l'interface réseau avec `sudo ifconfig eth0 down` suivi de `sudo ifconfig eth0 up`.

### 8.3. Impossible de se connecter via un proxy

- **Solution**:
 Vérifiez les logs pour voir si le proxy est fonctionnel. Si un proxy spécifique échoue, modifiez la liste des proxies dans le script.

---

## 9. FAQ

### Q1 : 

Puis-je ajouter mes propres proxies à la liste ?

**Oui.** 

Modifiez simplement la liste `proxies` dans le script pour inclure vos propres adresses IP et ports de proxy.

### Q2 : 

Le script fonctionne-t-il sur Windows ?

**Non.** 

Ce script est conçu pour les systèmes basés sur Linux.

### Q3 : 

Que faire si je souhaite désactiver la rotation des proxies après avoir lancé le script ?

**Le script doit être redémarré** sans l'option `--utiliser_proxy` pour désactiver la rotation des proxies.

---

## 10. Support

Pour toute assistance ou question, veuillez contacter notre équipe de support à l'adresse suivante : `admin@pctamalou.fr`. 
Nous sommes là pour vous aider avec l'installation, la configuration et l'utilisation du script.

---

## Remerciements

Merci d'utiliser **EcoFacker** ! 

Nous espérons que ce script vous aidera à protéger votre vie privée en ligne. 

Votre sécurité est notre priorité.
