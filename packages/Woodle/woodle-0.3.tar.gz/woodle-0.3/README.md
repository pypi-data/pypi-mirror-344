# Woodle
Outil pour transformer un fichier de notes Moodle (xlsx) en fichier SNW (csv)

## Installation

### Pré-requis

* Python >=3.5
* pip
* Git

### Installation avec pip

    pip install https://pypi.org/project/Woodle/

## Utilisation

Cet utilitaire permet de passer les notes de Moodle à SNW

Utilisation seule :

```
woodle [option] <fichier moodle> <fichier snw> <colonne>

Options:
  -b BAREME   Barême.
  -h, --help  Affiche ce message d'aide et termine.
```

**Attention : le fichier SNW doit exister et avoir le bon entête (le télécharger depuis SNW avant).**

Exemple :

    woodle "Bilan S4 Notes.xlsx" "Extract_SN_Web.csv" "Admi/Sys/Res CC (Brut)"

## Versions

* 0.1 Version initiale
* 0.2 Améliorations de la gestion des erreurs
* 0.3 Gestion des exports Excel avec un "’" dans la colonne d'identifiants au lieu de "'"
