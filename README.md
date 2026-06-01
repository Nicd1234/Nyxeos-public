# Nyxeos

Nyxeos est un projet d'architecture IA locale, modulaire et distribuée, conçu pour fonctionner sur une infrastructure Raspberry Pi/Pironman et pour évoluer vers un système autonome de génération, test, mémoire, surveillance et orchestration de modules.

Ce dépôt public sert de point de synchronisation GitHub pour documenter le projet, rendre son architecture lisible par Codex/ChatGPT/Grok et conserver une base claire pour les prochaines étapes de développement.

## Objectif général

Nyxeos vise à construire progressivement un environnement logiciel local capable de :

- analyser des fichiers et modules existants ;
- générer ou améliorer du code sans écraser les originaux ;
- maintenir une mémoire persistante du projet ;
- coordonner plusieurs machines Raspberry Pi ;
- surveiller l'état matériel et logiciel ;
- documenter automatiquement les décisions, modules, chemins et rôles ;
- préparer une base pour des agents locaux plus autonomes.

## Infrastructure connue

L'architecture matérielle retenue repose principalement sur trois unités Raspberry Pi/Pironman :

| Unité | Rôle logique | Informations connues |
|---|---|---|
| Pironman principal | Poste maître / manipulation directe / orchestration | IP locale connue : `192.168.0.37` |
| Pironman secondaire | Serveur mémoire central / data core / coopération | IP locale connue : `192.168.0.51`, utilisateur souvent `nic2` |
| Pironman 5 MAX | Banc d'essai et unité avancée avec SSD + Hailo | IP locale connue : `192.168.0.50`, Raspberry Pi 5 16 Go, SSD NVMe, Hailo AI M.2 |

Les appareils sont connectés via un switch central HPE OfficeConnect 1920S Series. L'objectif est de garder les traitements et données dans l'architecture locale autant que possible.

## Chemins importants

Chemins mentionnés et à préserver dans la documentation opérationnelle :

```text
/home/nic/nyxeos_pi5/nyxeos_pi
/home/nic/nyxeos_pi5/nyxeos_pi/modules
/home/nic2/pironman5/pironman5
/home/nic/Auto-GPT/
/home/nic/Auto-GPT/auto_gpt_workspace
/home/nic/Downloads/input.yaml
~/nyxeos_local/inbox_from_max/
```

## Principes de développement

Les règles de travail importantes sont :

1. Ne pas écraser les originaux sans sauvegarde.
2. Créer des versions annotées (`_updated`, `_v2`, etc.) lorsque les modules sont modifiés.
3. Maintenir un journal clair des actions.
4. Utiliser une mémoire persistante de progression, idéalement JSON ou SQLite.
5. Éviter les boucles de réanalyse : les fichiers déjà traités doivent être marqués.
6. Tester localement avant réplication.
7. Préserver la synergie entre modules : une modification isolée ne doit pas casser les autres composants.
8. Documenter les décisions, chemins, dépendances et rôles.

## Modules et concepts centraux

### `nyx_comprehender.py`

Dernier module structuré identifié avant une perte de mémoire du projet. Il est considéré comme l'un des noyaux de compréhension et d'interface naturelle. Il doit être relié au noyau central (`nyx_brain_core`) et à la mémoire (`nyx_memory`).

### `nyx_brain_core.py`

Noyau logique et décisionnel. Il doit recevoir les éléments compris par `nyx_comprehender`, organiser les intentions et déclencher les modules appropriés.

### `nyx_memory.py`

Module prévu pour gérer la mémoire court/moyen terme. Formats envisagés : JSON ou SQLite. À intégrer passivement dans `nyx_comprehender` et activement dans le noyau.

### `nyx_logger.py`

Journalisation uniforme des actions, erreurs, tests, analyses et décisions.

### `nyx_monitor.py`, `nyx_guard.py`

Surveillance continue des modules critiques, redémarrage automatique et détection de panne.

### `nyxbrain_analyseur.py`

Analyse nocturne prévue des modules tiers, avec journalisation dans `/logs/brain_analysis.log`.

### `nyx_pironman_monitor.py`

Module de diagnostic et monitoring matériel pour les Pironman : température CPU, RAM, usage système, état des ventilateurs/OLED selon support matériel.

### `nyx_prompt_assist.py`

Module envisagé pour intégrer des structures de prompting comme R-T-F, T-A-G, B-A-B, C-A-R-E et R-I-S-E, afin d'améliorer la génération d'instructions internes.

### `nyx_hivemind_sync.py`

Module de synchronisation inter-nœuds, notamment vers le Pi secondaire ou le MAX.

### `nyx_auto_uploader.py`

Upload/synchronisation automatique après modification locale validée.

### `NyxPulse`

Protocole de communication compressée par pulses/dictionnaire. Utilisable pour communication inter-machines, rovers, environnements à bande passante limitée ou transmission symbolique compacte.

### `NyxCode`

Concept de coeur auto-codeur : composant destiné à remplacer progressivement le rôle d'un codeur humain dans la génération, l'amélioration et la validation de modules.

## Plan opérationnel actuel en 5 étapes

### Étape 1 — Consolidation du noyau central

- Vérifier le lien `nyx_comprehender` → `nyx_brain_core`.
- Ajouter ou renforcer les logs via `nyx_logger`.
- Tester localement avec input simulé.

### Étape 2 — Création et branchement de `nyx_memory.py`

- Mémoire court/moyen terme.
- Intégration passive dans le comprehender.
- Stockage JSON ou SQLite.

### Étape 3 — Diagnostic nocturne

- `nyxbrain_analyseur.py`.
- Cron à 3 h du matin.
- Analyse des modules tiers.
- Log dans `/logs/brain_analysis.log`.

### Étape 4 — Surveillance continue

- `nyx_monitor`.
- `nyx_guard`.
- `nyx_logger`.
- Vérification des modules critiques et redémarrage automatique.

### Étape 5 — Résilience, nettoyage, diffusion

- Automatisation de nettoyage avec `cleanser` et `deep_cleanser_forceur`.
- Synchronisation via `nyx_hivemind_sync`.
- Upload automatique via `nyx_auto_uploader.py`.

## Pironman 5 / Pironman MAX

Le projet inclut le remplacement ou l'amélioration du service officiel `pironman5.service` par une version plus stable, lisible et orientée Nyxeos.

Fonctions visées :

- écran OLED lisible ;
- ventilateurs ;
- température CPU ;
- usage CPU/RAM ;
- IP locale ;
- diagnostic matériel ;
- affichage dynamique sobre ;
- éviter tout effet visuel qui nuit au texte OLED.

## Hailo AI M.2

Le Pironman MAX contient une puce Hailo AI M.2. Les paquets Debian Hailo à considérer comme référence incluent notamment :

- `hailo-all` ;
- `hailo-dkms` ;
- `hailort` ;
- `python3-hailort` ;
- `hailo-tappas-core`.

## Auto-GPT local

Une piste importante est l'utilisation d'Auto-GPT en local, sans Docker, sans dépendance payante et sans `gpt-3.5-turbo`, avec modèles locaux possibles via `llama.cpp`, Mistral, Phi ou équivalent.

Exigences :

- analyse des modules sans retraiter les fichiers déjà traités ;
- mémoire persistante de progression ;
- accès lecture/écriture local ;
- backup automatique avant modification ;
- fichiers améliorés annotés sans écrasement ;
- journal de progression ;
- exécution de séquences de commandes, pas une seule commande vague.

## Documentation prévue dans ce dépôt

Ce dépôt doit idéalement contenir :

```text
README.md
/docs/ARCHITECTURE.md
/docs/MODULES.md
/docs/ROADMAP.md
/docs/INFRASTRUCTURE.md
/docs/NYXPULSE.md
/docs/PIRONMAN.md
/docs/AUTOGPT_LOCAL.md
/docs/OPERATING_RULES.md
```

Ces fichiers doivent permettre à Codex ou à un agent local de reprendre le projet sans dépendre uniquement de la mémoire conversationnelle.

## État de cette documentation

Cette documentation a été générée à partir de la mémoire consolidée du projet Nyxeos disponible dans les conversations ChatGPT du projet. Elle doit être enrichie progressivement avec les vrais fichiers du dépôt, les scripts locaux et les résultats de tests réels.
