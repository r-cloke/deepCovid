# -*- coding: utf-8 -*-
"""
Created on Sat May  2 08:57:23 2020

@author: rcloke
"""
from rdkit.Chem.Draw import IPythonConsole
from IPython.display import SVG
from rdkit.Chem.Draw import rdMolDraw2D 
from rdkit.Chem import AllChem
from rdkit import Chem

counter = 0
with open('emol_10M_output_hits.csv','r') as fin:
    fin.readline()
    for aline in fin:
        counter+=1
        smiles = aline.split(',')[3]
        mol = rdkit.Chem.MolFromSmiles(smiles)
        filename = 'mol'+str(counter)+'.png'
        Chem.Draw.MolToFile(mol,filename)