import pandas as pd
# import os

# os.system()

def get_trip(filename, n):
	# read file
	f = filename + str(n) + ".txt"
	data = pd.read_table(f, sep="|", header=None)
	# keep cols that mae up relshp
	data2 = data.iloc[:,[3,8,10]]
	# reset col names
	data2.columns = ["Subject", "Predicate", "Object"]
	# remove rows that are NaNs
	data2.dropna(axis=0, how="any", inplace=True)
	# write to csv ----- change file/folder name!
	data2.to_csv("./sr_ct_triples/output_triples" + str(n) + ".csv", index=False)

def get_trip_batch(base_filename, start, end):
	for i in range(start,end+1):
		get_trip(base_filename, i)

# change file name here
get_trip_batch("./sr_ct_rels/output_rels", 0, 315)

