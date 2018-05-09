import pandas as pd

df = pd.read_csv("TextBookText_csv.csv")


for index, row in df.iterrows():
	row.to_csv('tb' + str(index) + '.txt', sep = "\n")