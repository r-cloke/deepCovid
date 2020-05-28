# deepCovid
This is a graph convolutional model imported from the DeepChem project to screen 10 million commercially available compounds from emolecules.com for mPro SARS-Cov2 hits.

The input data set for training was made by combining datasets from two sources to provide more training examples:
1) https://www.diamond.ac.uk/covid-19/for-scientists/Main-protease-structure-and-XChem/Downloads.html

2)https://chemrxiv.org/articles/Computational_Models_Identify_Several_FDA_Approved_or_Experimental_Drugs_as_Putative_Agents_Against_SARS-CoV-2/12153594 
https://github.com/alvesvm/sars-cov-mpro/tree/master/datasets

The model performed poorly on both data sets in isolation but the combined datasets produce a decent model.  A ROC-AUC score of 0.86 was achieved on the test set.  The model_test_score.png file shows the distribution of hit probability scores for the test set produced by the model on the y-axis vs the experimental ground truth classification on the x-axis.  All of the compounds that were not hits in the test set were classified correctly (i.e. the model predicts they have hit probabilities less than 0.5).  Whereas some active compounds were predicted to have hit probabilities less than 0.5 (i.e. this model has a low false negative rate and high false positive rate).  Therefore experimental testing of predicted hit compounds is needed to validate their actual potential SARS-Cov2 mPro binding.
