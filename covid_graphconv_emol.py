#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 14:45:01 2020

@author: ryan
"""


import pandas as pd
from rdkit.Chem import PandasTools
import seaborn as sns
import deepchem as dc
from deepchem.models import GraphConvModel
import numpy as np

def test_graph_conv_model():
    batch_size = 2000
    model = GraphConvModel(1, batch_size=batch_size,mode="classification",model_dir="/tmp/covid/model_dir")
    dataset_file = "covid_mpro_combined_data_sources.csv"
    tasks = ["isHit"]
    featurizer = dc.feat.ConvMolFeaturizer()
    loader = dc.data.CSVLoader(tasks=tasks,smiles_field="SMILES",featurizer=featurizer)
    dataset = loader.featurize(dataset_file, shard_size=8192)

    metrics = [
        dc.metrics.Metric(dc.metrics.matthews_corrcoef, np.mean, mode="classification")]
    
    
    splitter = dc.splits.RandomSplitter()
   
    train_dataset, valid_dataset, test_dataset = splitter.train_valid_test_split(dataset)
    
    model.fit(train_dataset)
    
    pred = [x.flatten() for x in model.predict(valid_dataset)]
    pred_df = pd.DataFrame(pred,columns=["neg","pos"])
    pred_df["active"] = [int(x) for x in valid_dataset.y]
    pred_df["SMILES"] = valid_dataset.ids
    
    sns.boxplot(pred_df.active,pred_df.pos)
    
    print(model.evaluate(train_dataset, metrics))
    print(model.evaluate(test_dataset, metrics))
    
    metrics = [
        dc.metrics.Metric(dc.metrics.roc_auc_score, np.mean, mode="classification")]
    print(model.evaluate(train_dataset, metrics))
    print(model.evaluate(test_dataset, metrics))
#test_graph_conv_model()

#train the model
batch_size = 2000
model = GraphConvModel(1, batch_size=batch_size,mode="classification",model_dir="/tmp/covid/model_dir")
dataset_file = "covid_mpro_combined_data_sources.csv"
tasks = ["isHit"]
featurizer = dc.feat.ConvMolFeaturizer()
loader = dc.data.CSVLoader(tasks=tasks,smiles_field="SMILES",featurizer=featurizer)
dataset = loader.featurize(dataset_file, shard_size=8192)

model.fit(dataset)


#model = GraphConvModel(1, batch_size=128,mode="classification",model_dir="/tmp/mk01/model_dir")
#model.restore()
#make predictions
featurizer = dc.feat.ConvMolFeaturizer()
df = pd.read_csv("emol_10M.csv",sep=",")
#print('num rows in file',df.size)
#df.columns=["SMILES","Name"]

rows,cols = df.shape
df["Val"] = [0] * rows #just add add a dummy column to keep the featurizer happy
infile_name = "emol_10M_withVal.csv"
df.to_csv(infile_name,index=False)
loader = dc.data.CSVLoader(tasks=['Val'], smiles_field="isosmiles", featurizer=featurizer)
dataset = loader.featurize(infile_name, shard_size=8192)
pred = model.predict(dataset)
pred_df = pd.DataFrame([x.flatten() for x in pred],columns=["Neg","Pos"])
sns.distplot(pred_df.Pos,rug=True)
combo_df = df.join(pred_df,how="outer")
combo_df.sort_values("Pos",inplace=True,ascending=False)
#PandasTools.AddMoleculeColumnToFrame(combo_df,"isosmiles","Mol")

combo_df = combo_df.loc[combo_df['Pos'] >= 0.8]
combo_df.to_csv('emol_10M_output_hits.csv',sep=',')

