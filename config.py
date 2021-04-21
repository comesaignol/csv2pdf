# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 12:31:26 2019

@author: Saignol

Création  d'un script convertissant du CSV en PDF.

"""

import os

# Paramètre du dossier d'entrée
inputDir = os.path.abspath("input")
inputSeparator = ","

# Colonnes
cols = ["Dublin Core:Title", "Item Type Metadata:Numéro de la pièce", "Item Type Metadata:Titre de la pièce", "Item Type Metadata:Incipit non modernisé", "Item Type Metadata:Foliotation"]
colsNew = ["Identifiant", "Rang", "Titre de la pièce", "Incipit non modernisé", "Foliotation"]

# Paramètre du dossier de sortie
outputDir = os.path.abspath("output")
outputSeparator = ","