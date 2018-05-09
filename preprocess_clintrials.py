import pandas as pd

df = pd.read_csv("ClinicalTrialsTextFinal_csv.csv")


for index, row in df.iterrows():
	row.to_csv('ct_data2/ct' + str(index) + '.txt', sep = "\n")