# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 12:31:26 2019

@author: Saignol

Création  d'un script convertissant du CSV en PDF.

"""
import config
import os
import shutil
import glob
import pandas as pd
from datetime import date

#from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape,A4
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.colors import HexColor
from reportlab.lib import colors

# Fonction créant un fichier
def createDir(path):
  if os.path.exists(path):
  	shutil.rmtree(path)
  os.mkdir(path)

# Création du dossier de sortie
createDir(config.outputDir)

# Liste des fichiers
path = os.path.join(config.inputDir, "*.csv")
fileList = glob.glob(path)

# Parcourir les fcihiers
for file in fileList:
  
  # Nom du fichier
  fileName = os.path.splitext(os.path.basename(file))[0]
  
  # Nouveau dossier
  newDir = os.path.join(config.outputDir, fileName)
  createDir(newDir)
  
  # Lecture du fichier
  df = pd.read_csv(file, sep=config.inputSeparator, header=0)
  
  # Agencement du dataframe
  df.sort_values(by=['Dublin Core:Title'], inplace=True)
  
  # Suppression de la ligne 0
  titre = str(df.iloc[0, 1])
  df = df.drop(df.index[0]) # Ligne à supprimer
  
  # Création du nouveau fichier
  df2 = pd.DataFrame()
  
  # Parcourir les éléments
  for col in config.cols:
    df2[col] = df[col]
  
  # Ajouter une nouvelle ligne
  df2.loc[-1] = config.colsNew  # ajout d'une ligne
  df2.index = df2.index + 1  # arrangement de l'index
  df2 = df2.sort_index()
  
  # Agencement du dataframe
  df2.sort_values(by=['Item Type Metadata:Numéro de la pièce'], inplace=True)
  
  # Remplacement des cases vides qui généraient un bug
  df2 = df2.fillna("!! CASES VIDES !!")
  
  # Création du fichier CSV
  path = os.path.join(config.outputDir, fileName, fileName + ".csv")
  df2.to_csv(path, sep=config.outputSeparator)
  print("Done", fileName, "Export du CSV")
  
  # Date de la création du fichier
  date = date.today()
  dateToday = date.strftime("%d/%m/%Y")
  
  def addPageNumber(canvas, doc):
    # Add the page number
    page_num = canvas.getPageNumber()
    text = "Équipe Joyeuses Inventions ; EMAN (Thalim, CNRS-ENS-Sorbonne nouvelle) ; CC BY-SA 3.0 FR. Date de création du fichier : " + dateToday + " " + " Page %s" % page_num
    canvas.setFont('Vera', 8)
    canvas.drawRightString(25*cm, 0.5*cm, text)
    
  
  # Enregistrement des familles de polices
  pdfmetrics.registerFont(TTFont("Vera", "Vera.ttf"))
  pdfmetrics.registerFont(TTFont("VeraBd", "VeraBd.ttf"))
  pdfmetrics.registerFont(TTFont("VeraIt", "VeraIt.ttf"))
  pdfmetrics.registerFont(TTFont("VeraBI", "VeraBI.ttf"))
  
  # Configuration du PDF
  path = os.path.join(config.outputDir, fileName, fileName + ".pdf")
  docpdf = SimpleDocTemplate(path,
                           pagesize = landscape(A4),
                           rightMargin = 1*cm,
                           leftMargin = 1*cm,
                           topMargin = 1*cm,
                           bottomMargin = 1*cm)
  
  # Création des styles
  style = getSampleStyleSheet()
  
  style.add(ParagraphStyle(name="Titre 1",
                         fontName = "Vera",
                         fontSize = 8,
                         leftIndent = 0,
                         rightIndent = 0,
                         alignment = TA_CENTER,
                         spaceBefore = 0,
                         spaceAfter = 0.25*cm))
  
  style.add(ParagraphStyle(name="titre1URL",
                         fontName = "Vera",
                         textColor = colors.HexColor("#0000FF"),
                         fontSize = 8,
                         leftIndent = 0,
                         rightIndent = 0,
                         alignment = TA_CENTER,
                         spaceBefore = 0,
                         spaceAfter = 0.25*cm))

  # Corps de la pafe
  story = []
  
  # Création des données pour la table
  data = df2.values.tolist()
  
  # Word wrap pour la table
  styles = getSampleStyleSheet()
  styleN = styles['Normal']
  styleN.wordWrap = 'CJK'
  styleN.fontName = "Vera"
  styleN.fontSize = 8
  
  # Paramètre de la table
  data = [[Paragraph(cell, styleN) for cell in row] for row in data]
  colWidths = [8*cm, 2*cm, 7*cm, 7*cm, 5*cm]
  
  # Création de la table
  table = Table(data, colWidths=colWidths)
  
  # Style de la table
  table.setStyle([('BACKGROUND',(0,0),(-1,0),HexColor("#fff5ce")),
                  ("FONTANME", (0,0),(-1,0), "VeraBd"),
                  ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                  ("ALIGN", (0,0), (-1,-1), "LEFT"),
                  ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                  ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ])
  grid = [('GRID', (0,0), (-1,-1), 0.25, colors.black), ('FONTNAME', (0,0), (0,-1), 'Courier-Bold')]
  
  # Corps du document
  story.append(Paragraph(titre, style["Titre 1"]))
  url = "<link href='https://eman-archives.org/joyeuses-inventions/'><u>© Joyeuses Inventions</u></link>"
  story.append(Paragraph(url, style["titre1URL"]))
  story.append(table)
  
  # Création du PDF
  docpdf.build(story, onFirstPage=addPageNumber, onLaterPages=addPageNumber)
  print("Done", fileName, "Export du PDF")
