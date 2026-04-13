# 📖 Guide d'Utilisation - SysNarrator pour Débutants

## Pour Quelconque Utilisateur - Comment Utiliser le Système

**SysNarrator** est un outil qui explique l'état de votre ordinateur en **langage humain**, pas en chiffres compliqués.

---

## 📋 Table des Matières

1. [Installation (5 minutes)](#-installation-5-minutes)
2. [Utilisation Basique (2 minutes)](#-utilisation-basique-2-minutes)
3. [Qu'est-ce que Signifie le Rapport](#-que-signifient-les-couleurs-et-les-résultats)
4. [Questions Courantes](#-questions-courantes)
5. [Commandes Utiles](#-commandes-utiles)

---

## 🔧 Installation (5 minutes)

### Étape 1: Ouvrir le Terminal

Appuyez sur `Ctrl + Alt + T` pour ouvrir le terminal.

### Étape 2: Aller au Dossier

Copiez-collez cette commande:
```bash
cd /home/youssef/sysnarrator
```

Puis appuyez sur **Entrée**.

### Étape 3: Vérifier que Tout est Installé

Copiez-collez:
```bash
. venv/bin/activate
```

Vous verrez apparaître `(venv)` avant votre nom d'utilisateur.

C'est bon? Passez à l'étape suivante! ✅

---

## 🚀 Utilisation Basique (2 minutes)

### Commande #1: Voir l'État du Système

Le plus simple pour commencer:

```bash
./sysnarrator-pro.sh --no-color
```

**Qu'est-ce que vous verrez:**
- Score de Santé du Système (0-100)
- État de chaque composant (CPU, RAM, Disque, etc.)
- Les processus qui consomment le plus

### Commande #2: Voir en Couleur (Plus Joli)

```bash
./sysnarrator-pro.sh
```

Vous verrez les mêmes infos mais **avec des couleurs** pour mieux comprendre!

### Commande #3: Voir Juste le CPU et la RAM

```bash
./sysnarrator.sh --only cpu,ram --no-color
```

Seulement les infos importantes.

---

## 🎨 Que Signifient les Couleurs et les Résultats

### Le Score de Santé (HEALTH SCORE)

C'est la note de votre ordinateur de 0 à 100:

| Score | Couleur | Meaning | Quoi Faire |
|-------|---------|---------|-----------|
| **90-100** | 🟢 Vert | EXCELLENT | Rien à faire, tout va bien! |
| **75-89** | 🟢 Vert | BON | Tout fonctionne, petites optimisations possibles |
| **60-74** | 🟡 Orange | MOYEN | Attention, quelque chose ralentit |
| **40-59** | 🟠 Orange-Rouge | FAIBLE | Plusieurs problèmes, action recommandée |
| **0-39** | 🔴 Rouge | CRITIQUE | Urgent! Votre PC ralentit beaucoup |

### Les Barres de Progression

```
CPU Usage: 45%
████████████░░░░░░░░░░░░░░░░░░ 45% - HEALTHY
```

- **Plein (████)** = High usage
- **Vide (░░░░)** = Low usage
- La couleur change:
  - 🟢 **Vert** = OK
  - 🟡 **Orange** = Attention
  - 🔴 **Rouge** = Problème

### CPU (Processeur)

```
CPU Usage: 45%
```

- 0-30% = Normal ✅
- 30-70% = Modéré (OK)
- 70-90% = Élevé (attention)
- 90-100% = SATURÉ (problème!)

**Si trop haut:** Votre PC fait trop de choses en même temps
**Solution:** Fermer des applications

### RAM (Mémoire Vive)

```
RAM Usage: 7.2GB / 16GB (45%)
```

- Cela veut dire: **7.2 Go utilisé sur 16 Go total**
- 0-50% = Bien ✅
- 50-75% = Normal
- 75-90% = Serré (attention)
- 90%+ = CRITIQUE (très lent!)

**Si trop haut:** Vous avez trop d'applications ouvertes
**Solution:** Fermer navigateur, VS Code, Slack, etc.

### DISK (Disque Dur)

```
Disk Usage: 150GB / 256GB (59%)
```

- Cela veut dire: **150 Go utilisé sur 256 Go disponibles**
- 0-70% = Bien ✅
- 70-85% = À surveiller
- 85-95% = Nettoyage recommandé
- 95%+ = CRITIQUE (système instable!)

**Si trop haut:** Votre disque est plein
**Solution:** Supprimer fichiers inutiles, vieux téléchargements

### SWAP (Mémoire Disque)

```
Swap Usage: 0.5GB / 4GB (10%)
```

C'est la mémoire de secours quand la RAM est pleine.

- 0-30% = Normal ✅
- 30%+ = Votre RAM manque
- **Beaucoup d'utilisation SWAP = PC TRÈS LENT**

**Si utilisé beaucoup:** Fermer applications ou ajouter RAM

---

## 💡 Qu'est-ce que Signifie "System Running Optimally"?

Si vous voyez ceci:

```
✓ System running optimally
```

**C'est excellent!** Votre ordinateur:
- N'a pas de problèmes
- Fonctionne normalement
- Ne ralentit pas
- Pas d'action nécessaire ✅

---

## ⚠️ Qu'est-ce que Signifie "Expert Analysis"?

Parfois elle vous montre des avertissements:

```
Expert Analysis:
├─ ⚠️ High CPU Usage (>80%)
   └─ Solutions: Close browser tabs, check processes
├─ ⚠️ High RAM Usage (>85%)
   └─ Solutions: Close heavy apps
```

**Cela veut dire:** SysNarrator a trouvé un problème et vous donne une solution!

---

## 📊 Les Processus (TOP PROCESSES)

```
► TOP PROCESSES
────────────────────────────────────────────────────────────────
chrome: 793MB
code: 738MB
Firefox: 600MB
```

**Cela montre:** Les applications qui utilisent le plus de mémoire (RAM).

- Chrome = 793 MB
- VS Code = 738 MB
- Firefox = 600 MB

**Si un processus utilise beaucoup:** Vous pouvez le fermer pour libérer de la RAM!

---

## ❓ Questions Courantes

### Q1: Pourquoi mon PC ralentit?

**Utiliser SysNarrator pour le découvrir:**

```bash
./sysnarrator-pro.sh --no-color
```

Regardez:
1. Le **Health Score** - Il est bas?
2. La **Expert Analysis** - Elle explique le problème
3. Les **TOP PROCESSES** - Quelles apps consomment le plus

C'est là vos réponses!

### Q2: Quoi faire si la RAM est à 90%?

**Fermer les applications lourdes:**

```bash
# Voir les apps qui consomment le plus de RAM
ps aux --sort=-%mem | head -10
```

Vous verrez quelque chose comme:
```
root       1000  0.5 30.5 5000000 12000000  chrome
user       2000  0.3 25.0 3000000 10000000  firefox
```

Chrome et Firefox consomment beaucoup! Fermez les!

### Q3: Quoi faire si le Disque est à 95%?

**Libérer de l'espace:**

```bash
# Voir les gros fichiers
du -sh ~/* | sort -rh | head -10
```

Supprimez:
- Anciens téléchargements
- Fichiers .iso ou vidéos inutiles
- Dossiers temporaires

### Q4: Comment surveiller tout le temps?

**Afficher le rapport chaque 30 secondes:**

```bash
watch -n 30 './sysnarrator-pro.sh --no-color'
```

Appuyez sur `Ctrl + C` pour arrêter.

### Q5: Je veux voir le rapport en Français?

```bash
./sysnarrator-pro.sh --lang fr --no-color
```

Vous verrez les messages en Français!

### Q6: Je veux garder un historique?

```bash
./sysnarrator-pro.sh --no-color >> mon_rapport.txt
```

Cela ajoute le rapport dans le fichier `mon_rapport.txt`.

---

## 🎯 Commandes Utiles

### Les Plus Courantes

```bash
# Rapport simple
./sysnarrator-pro.sh --no-color

# Rapport avec couleurs
./sysnarrator-pro.sh

# Juste CPU et RAM
./sysnarrator.sh --only cpu,ram --no-color

# Exporter en fichier
./sysnarrator-pro.sh --no-color > rapport.txt

# Voir chaque 30 secondes
watch -n 30 './sysnarrator-pro.sh --no-color'

# En Français
./sysnarrator-pro.sh --lang fr --no-color

# En Arabic
./sysnarrator-pro.sh --lang ar --no-color

# JSON (pour scripts)
./sysnarrator-pro.sh --json
```

### Voir les Applications Lourdes

```bash
# Top 10 applications qui utilisent RAM
ps aux --sort=-%mem | head -11

# Top 10 applications qui utilisent CPU
ps aux --sort=-%cpu | head -11
```

### Nettoyer le Système

```bash
# Nettoyer le cache
sudo apt clean && sudo apt autoclean

# Nettoyer les anciennes logs
sudo journalctl --vacuum=3d

# Nettoyer le téléchargement
rm -rf ~/Téléchargements/*
```

---

## 📱 Scénarios d'Utilisation

### Scénario 1: Mon PC Ralentit, Quoi Faire?

**Étapes:**
1. Ouvrir terminal: `Ctrl + Alt + T`
2. Aller au dossier: `cd /home/youssef/sysnarrator`
3. Activer: `. venv/bin/activate`
4. Voir le rapport: `./sysnarrator-pro.sh --no-color`
5. Lire la "Expert Analysis" - c'est votre réponse!

### Scénario 2: Je Veux Surveiller en Temps Réel

**Étapes:**
1. Terminal: `Ctrl + Alt + T`
2. Aller au dossier + activer (comme au-dessus)
3. Taper: `watch -n 3 './sysnarrator-pro.sh --no-color'`
4. Le rapport se met à jour chaque 3 secondes
5. Appuyer `Ctrl + C` pour arrêter

### Scénario 3: Je Veux Garder un Historique de la Santé

**Étapes:**
1. Créer un dossier: `mkdir -p ~/rapports_sysnarrator`
2. Taper ceci (sur une seule ligne):
```bash
for i in {1..10}; do 
  ./sysnarrator-pro.sh --no-color > ~/rapports_sysnarrator/rapport_$(date +%Y-%m-%d_%H-%M-%S).txt
  sleep 60
done
```
3. Cela va créer 10 rapports avec 1 minute d'intervalle

### Scénario 4: Mon Navigateur Consomme Trop!

**Étapes:**
1. Voir les détails: `ps aux | grep chrome` (ou firefox)
2. Voir combien ça consomme:
```bash
ps aux --sort=-%mem | grep chrome
```
3. Si c'est trop: Fermer le navigateur et le rouvrir
4. Vérifier avec: `./sysnarrator-pro.sh --no-color`

---

## 🎓 Comprendre les Concepts

### CPU (Processeur)

C'est le "cerveau" de votre ordinateur.
- **Bas (0-30%)**  = PC au repos, peu de tâches
- **Moyen (30-70%)** = Normal, tout fonctionne
- **Haut (70-90%)**  = PC travaille dur
- **Saturé (90%+)**  = PC est à la limite

### RAM (Mémoire Vive)

C'est la "table de travail" de l'ordinateur.
Plus elle est pleine, moins vite le PC peut travailler.
- **30-40%** = Bon
- **60% +**   = À surveiller
- **85%+**    = Problème, fermer apps

### SWAP (Mémoire Disque)

Quand la RAM n'est pas suffisante, le PC utilise le disque dur.
Le disque est **très lent** par rapport à la RAM!
- Si SWAP = 0% → Parfait ✅
- Si SWAP > 30% → Problème, ajouter RAM

### Disk (Disque Dur)

C'est le "classeur" qui sauvegarde vos fichiers.
Doit toujours avoir 10% libre minimum.
- **0-70%**  = Bien ✅
- **70-85%** = À surveiller
- **85%+**   = Nettoyer
- **95%+**   = Critique

---

## ✅ Checklist Utilisation Simple

Si vous êtes pressé, voici le **minimum à savoir:**

- [ ] **Ouvrir terminal:** `Ctrl + Alt + T`
- [ ] **Aller au dossier:** `cd /home/youssef/sysnarrator`
- [ ] **Activer:** `. venv/bin/activate`
- [ ] **Voir le rapport:** `./sysnarrator-pro.sh --no-color`
- [ ] **Lire le Health Score:** C'est votre note
- [ ] **Lire Expert Analysis:** C'est la solution
- [ ] **Comprendre:** Green = Good, Red = Bad

---

## 🆘 Besoin d'Aide?

```bash
# Voir toutes les options
./sysnarrator-pro.sh --help

# Voir la documentation complète
cat PROFESSIONAL.md

# Lancer la démo
./demo.sh
```

---

## 📝 Résumé Rapide

| Quoi | Commande | Résultat |
|------|----------|----------|
| Voir la santé | `./sysnarrator-pro.sh --no-color` | Score + détails |
| Voir avec couleurs | `./sysnarrator-pro.sh` | Joli + code couleur |
| Voir en Français | `./sysnarrator-pro.sh --lang fr --no-color` | En Français |
| Sauvegarder rapport | `./sysnarrator-pro.sh > rapport.txt` | Fichier texte |
| Surveiller en temps réel | `watch -n 5 './sysnarrator-pro.sh --no-color'` | Mise à jour chaque 5s |

---

**C'est tout! Vous savez maintenant utiliser SysNarrator!** 🎉

Quelques clics, et vous comprenez l'état de votre ordinateur comme un expert! 💻✨
