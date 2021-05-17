# tdm2pdf

## Présentation

tdm2pdf est un outil développé en Python 3 convertissant un fichier CSV dans deux nouveaux fichiers : un fichier CSV corrigé et un fichier PDF. Cet outil a été utilisé dans le cadre du projet Joyeuses Inventions pour mettre à disposition de la communauté scientifique les tables des matières des œuvres poétiques analysées.

tdm2pdf a été conçu pour gérer les fichiers par lots : pour chaque documents en entrée, il crée un dossier de sortie comportant les deux documents.

Il est composé de deux fichiers principaux :

* « tdm2pdf » qui contient le cœur du programme ;
* « config.py » comportant les paramètres d’utilisation.

## Installation

tdm2pdf nécessite une installation Python 3 avec plusieurs packages dont ReportLab.

Pour vérifier les packages installées :
    
    pip freeze

Pour installer les packages manquants :

    pip install -r path\to\requirements.txt
    
avec le chemin absolu correspondant au fichier « requirements.txt » présent dans cet outil.

## Usage

Le fichier « config.py » comporte plusieurs paramètres à configurer suivant les besoins du projet. En particulier les paramètres « inputSeparator » et « outputSeparator » configure les séparateurs utilisés dans les fichiers CSV d’entrée et de sortie.

Insérer les fichiers désirés dans le répertoire « Input ».

Exécuter le programme « tdm2pdf.py ».