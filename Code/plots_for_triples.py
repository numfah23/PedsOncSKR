import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib_venn import venn3
from wordcloud import WordCloud # requires installation
from collections import Counter
import networkx as nx

#######################################################################################
# read data and define different data types
# pubmed
pm = pd.read_csv("pubmed_triples/semmeddb_combined_triples.csv")
# clintrials
ct = pd.read_csv("clinical_trial_triples/clintrials_combined_triples.csv")
# textbook
tb = pd.read_csv("textbook_triples/textbook_combined_triples.csv")

# gold standard pmid clintrials
gs_ct = pd.read_csv("ClinicalTrialGSTriples.csv")
gs_pmid = pd.read_csv("PubMedGSTriples.csv")
gs_tb = pd.read_csv("TextbookGSTriples.csv")
ideal = pd.read_csv("IdealSemanticRelations_csv.csv")

# diff data types
datas = [pm, ct, tb]
gs_datas = [gs_pmid, gs_ct, gs_tb]
inds = ["PMID", "NCT", "Section"]

# subset of data to match gs in 1 df
pm_subset = pm[pm["PMID"].isin(gs_pmid["PMID"])]
ct_subset = ct[ct["NCT"].isin(gs_ct["NCT"])]
tb_subset = pd.read_csv("textbook_triples/textbook_triples_ss.csv")
ss_data = [pm_subset, ct_subset, tb_subset]

# combine subset data from 3 sources
subset_data = pd.concat(ss_data, keys=['PMID','NCT','Section']).reset_index()
subset_data['Source'] = subset_data['PMID'].combine_first(subset_data['NCT'])
subset_data['Source'] = subset_data['Source'].combine_first(subset_data['Section'])
subset_data = subset_data.rename(columns={'level_0':'Source Type'})
subset_data = subset_data[['Source Type', 'Source', 'Subject', 'Object', 'Predicate']]
# subset_data.to_csv("subset_triples.csv", index=False)

# # combine gs into 1 df
all_gs = pd.concat(gs_datas)
all_gs['D_Source'] = all_gs['PMID'].combine_first(all_gs['NCT'])
all_gs['D_Source'] = all_gs['D_Source'].combine_first(all_gs['Section'])

# #######################################################################################
# # single barplot for ss predicates
datas = [subset_data]
inds = ['Source']
i=0
data_unq = datas[i].groupby(["Subject","Object","Predicate"]).count()[inds[i]].reset_index()
pred_unq = data_unq.groupby(["Predicate"]).count()[inds[i]].reset_index()
pred_unq = pred_unq.sort_values(inds[i], ascending=False)
plt.bar(pred_unq["Predicate"], pred_unq[inds[i]])
plt.xticks(rotation=90)
plt.tight_layout()
# plt.savefig("ss_preds_barplot_paper")
plt.show()

# plot for gs
datas = [all_gs]
inds = ['D_Source']
i=0
pred = datas[i].groupby(["Predicate"]).agg({inds[i]: ['count'], "Source": ['first']}).reset_index()
pred = pred.sort_values([(inds[i], 'count')], ascending=False)
fig = plt.figure(figsize=(10,8))
colors = {'UMLS':'C0', 'New':'red', 'NCI Thesaurus':'green'}
plt.bar(pred["Predicate"], pred[(inds[i], 'count')], color=map(lambda x: colors[x], pred[('Source', 'first')]))
plt.xticks(rotation=90)
fig.tight_layout()
red_patch = mpatches.Patch(color='C0', label='UMLS')
blue_patch = mpatches.Patch(color='red', label='New')
green_patch = mpatches.Patch(color='green', label='NCI Thesaurus')
plt.legend(handles=[red_patch, blue_patch, green_patch])
# plt.savefig("gs_preds_barplot_paper")
plt.show()


# #######################################################################################
# double barplot for before and after remove unique
for i in range(len(datas)):
	pred = datas[i].groupby(["Predicate"]).count()[inds[i]].reset_index()
	pred = pred.sort_values(inds[i], ascending=False)
	data_unq = datas[i].groupby(["Subject","Object","Predicate"]).count()[inds[i]].reset_index()
	pred_unq = data_unq.groupby(["Predicate"]).count()[inds[i]].reset_index()
	# combine before and after
	preds_all = pred.merge(pred_unq, left_on="Predicate", right_on="Predicate", how="left")

	# preds_all.to_csv("temp_preds_" + str(i) + ".csv")

	plot
	fig = plt.figure(figsize=(10,10))
	# fig = plt.figure()
	ax = fig.add_subplot(111)
	preds_all = preds_all.set_index(['Predicate'])
	preds_all[inds[i] +"_x"].plot(kind='bar', color='red', ax=ax, position=0, width=0.25)
	preds_all[inds[i] +"_y"].plot(kind='bar', color='blue', ax=ax, position=1, width=0.25)
	fig.tight_layout()
	# plt.savefig(inds[i] + "_preds_with_unq_barplot")
	plt.show()

#######################################################################################
# get total number of triples vs unique number of triples
triples = []
unique_triples = []
for i in range(len(datas)):
	data = datas[i]
	index = inds[i]
	print index 
	# print "total triples"
	print data.shape[0]
	triples.append(data.shape[0])
	data_unq = data.groupby(["Subject","Object","Predicate"]).count()[index].reset_index()
	# print "unqiue triples"
	print data_unq.shape[0]
	unique_triples.append(data_unq.shape[0])

# plot
fig = plt.figure()
ax = fig.add_subplot(111)
all_t = ax.bar([-0.1,0.4,0.9], triples, width=0.2, label="all_triples")
unq_t = ax.bar([0.1,0.6,1.1], unique_triples, width=0.2, label="unique_triples")
ax.set_xticks((0, 0.5, 1))
ax.set_xticklabels(["PubMed", "ClinTrial", "Textbook"])
ax.legend((all_t[0], unq_t[0]), ('All triples', 'Unique triples'))
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.01*height,'%d' % int(height),ha='center', va='bottom')
autolabel(all_t)
autolabel(unq_t)
plt.xlabel("Data source")
plt.ylabel("Number of triples")
fig.tight_layout()
# plt.savefig("all_unique_triples")
plt.show()

######################################################################################
# find intersection between data sources and make venn diagram
all_sources_triples = {'PMID':[], 'NCT':[], 'Section':[]}
for i in range(len(datas)):
	data = datas[i]
	index = inds[i]
	data_unq = data.groupby(["Subject","Object","Predicate"]).count()[index].reset_index()
	all_sources_triples[index] = data_unq

# all compared
# pmid + nct + section
print("PMID + NCT + SECTION")
temp = pd.merge(all_sources_triples['PMID'],all_sources_triples['NCT'], on=["Subject","Object","Predicate"], how="inner")
intersect_3 = pd.merge(temp,all_sources_triples['Section'], on=["Subject","Object","Predicate"], how="inner").shape[0]
print intersect_3

# pairwise comparisons
# pmid + nct
print("PMID + NCT")
pmid_nct = pd.merge(all_sources_triples['PMID'],all_sources_triples['NCT'], on=["Subject","Object","Predicate"], how="inner").shape[0]
print pmid_nct - intersect_3
# pmid + section
print("PMID + Section")
pmid_sect = pd.merge(all_sources_triples['PMID'],all_sources_triples['Section'], on=["Subject","Object","Predicate"], how="inner").shape[0]
print pmid_sect - intersect_3
# nct + section
print("NCT + Section")
nct_sect = pd.merge(all_sources_triples['NCT'],all_sources_triples['Section'], on=["Subject","Object","Predicate"], how="inner").shape[0]
print nct_sect - intersect_3

# single
# pmid
print "PMID"
pmid_t = all_sources_triples['PMID'].shape[0] - pmid_nct - pmid_sect - intersect_3
print pmid_t
# nct
print "NCT"
nct_t = all_sources_triples['NCT'].shape[0] - pmid_nct - nct_sect - intersect_3
print nct_t
# section
print "Section"
sect_t = all_sources_triples['Section'].shape[0] - pmid_nct - nct_sect - intersect_3
print sect_t

venn3(subsets = (pmid_t, nct_t, pmid_nct, sect_t, pmid_sect, nct_sect, intersect_3),
	set_labels = ("PubMed","ClinTrial","Textbook"))
# plt.savefig("venn_diagram_triples")
plt.show()

######################################################################################
# histogram for triple freq

# helper fn for grouping ends
def group_n_or_more(x, n):
	if x > n:
		# manually hard coded this
		if n == 50:
			return "52-2122"
		else:
			return "20-119"
	else:
		return str(x)

# histogram for triple freq
for i in range(len(datas)):
	data = datas[i]
	index = inds[i]
	triples_freq = data.groupby(["Subject","Object","Predicate"]).count().reset_index()
	counts = triples_freq.groupby(index).count()["Subject"].reset_index()
	if i == 2:
		plt.bar(x=counts[index], height=counts["Subject"])
		plt.xlabel("Triple Frequency")
		plt.ylabel("Counts")
		plt.xticks(rotation=90)
		plt.tight_layout()
		# plt.savefig(inds[i] + "_hist_triple_freq")
		plt.show()
	else:
		if i == 0:
			# group ends
			counts['group'] = map(lambda(x): group_n_or_more(x, 50), counts[index])

		else:
			counts['group'] = map(lambda(x): group_n_or_more(x, 20), counts[index])

		counts_grouped = counts.groupby('group', sort=False)['Subject'].apply(list).reset_index()
		counts_grouped['Subject'] = map(lambda(x): sum(x), counts_grouped['Subject'])

		plt.bar(x=counts_grouped['group'], height=counts_grouped["Subject"])
		plt.xlabel("Triple Frequency")
		plt.ylabel("Counts")
		plt.xticks(rotation=90)
		plt.tight_layout()
		# plt.savefig(inds[i] + "_hist_triple_freq")
		plt.show()


#######################################################################################
# # Generate word cloud images
all_text = []
for i in range(len(datas)):
	data = datas[i]
	text = data["Subject"].append(data["Object"]).reset_index()
	all_text.append(text)
	text_freqs = text.groupby([0]).count().reset_index()
	text_freqs_dict = dict(zip(text_freqs[0], text_freqs['index']))
	wc = WordCloud(width=1600, height=800, background_color="white")
	wordcloud = wc.generate_from_frequencies(text_freqs_dict)
	# plt.figure(figsize=(20,10))
	# plt.imshow(wordcloud, interpolation='bilinear')
	# plt.axis("off")
	# plt.savefig(inds[i] + "_word_cloud")
	# plt.show()

# # make wordcloud for 3 sources combined
all_text = pd.concat(all_text)
all_text_freqs = all_text.groupby([0]).count().reset_index()
all_text_freqs_dict = dict(zip(all_text_freqs[0], all_text_freqs['index']))
wc = WordCloud(width=1600, height=800, background_color="white")
wordcloud = wc.generate_from_frequencies(all_text_freqs_dict)
plt.figure(figsize=(20,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
# plt.savefig("all_word_cloud_paper")
plt.show()

# # make wordcloud for gold standards
all_gs_text = []
for i in range(len(gs_datas)):
	gs_data = gs_datas[i]
	gs_text = gs_data["Subject"].append(gs_data["Object"]).reset_index()
	all_gs_text.append(gs_text)
all_gs_text = pd.concat(all_gs_text)
all_gs_freqs = all_gs_text.groupby([0]).count().reset_index()
all_gs_freqs_dict = dict(zip(all_gs_freqs[0], all_gs_freqs['index']))
wc = WordCloud(width=1600, height=800, background_color="white")
wordcloud = wc.generate_from_frequencies(all_gs_freqs_dict)
plt.figure(figsize=(20,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
# plt.savefig("gs_word_cloud_paper")
plt.show()

# # # # make wordcloud for subset semrep to match gs
ss_text = subset_data["Subject"].append(subset_data["Object"]).reset_index()
all_ss_freqs = ss_text.groupby([0]).count().reset_index()
all_ss_freqs_dict = dict(zip(all_ss_freqs[0], all_ss_freqs['index']))
wc = WordCloud(width=1600, height=800, background_color="white")
wordcloud = wc.generate_from_frequencies(all_ss_freqs_dict)
plt.figure(figsize=(20,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
# plt.savefig("ss_word_cloud_paper")
plt.show()

#######################################################################################

# # make knowledge graphs
# # only make graph for one nct: NCT01471782

# ss data
g_data = subset_data[subset_data['Source'] == 'NCT01471782']
edges=zip(g_data['Subject'], g_data['Object'])
G=nx.Graph()
G.add_edges_from(edges)
# pos=nx.circular_layout(G)
pos=nx.spring_layout(G, k=100)
plt.figure(figsize=(10,8))    
nx.draw(G,pos,edge_color='black',width=1,linewidths=1,\
node_size=500,node_color='skyblue',alpha=0.9,\
labels={node:node for node in G.nodes()})
keys = zip(g_data['Subject'], g_data['Object'])
edge_lab=dict(zip(keys,g_data['Predicate']))
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_lab)
plt.axis('off')
# plt.savefig("ss_graph_NCT01471782")
plt.show()


# # gs data
g_data = gs_ct[gs_ct['NCT'] == 'NCT01471782']
edges=zip(g_data['Subject'], g_data['Object'])
edges_to_hl = [('Blinatumomab','Recurrent childhood acute lymphoblastic leukemia'),
('Blinatumomab','Refractory childhood acute lymphoblastic leukemia'),
('Blinatumomab','*Clinical Study (NCT01471782)*'),
('*Clinical Study (NCT01471782)*','Recurrent childhood acute lymphoblastic leukemia'),
('*Clinical Study (NCT01471782)*','Refractory childhood acute lymphoblastic leukemia')]

G=nx.Graph()
G.add_edges_from(edges, color='black')
G.add_edges_from(edges_to_hl, color='red')
# pos=nx.circular_layout(G)
pos=nx.spring_layout(G, k=100)
plt.figure(figsize=(10,8))  
edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]  
nx.draw(G,pos,edges=edges,edge_color=colors,width=1,linewidths=1,\
node_size=50,node_color='skyblue',alpha=0.9,\
labels={node:node for node in G.nodes()}, font_size=10)
keys = zip(g_data['Subject'], g_data['Object'])
edge_lab=dict(zip(keys,g_data['Predicate']))
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_lab, font_size = 10, color=colors)
plt.axis('off')
# plt.savefig("gs_graph_NCT01471782_with_hl2")
plt.show()




knowledge graph for tb prognostic factors + gender

g_data = gs_tb[gs_tb['Section'] == 'Prognostic Factors']
edges=zip(g_data['Subject'], g_data['Object'])
G=nx.Graph()
G.add_edges_from(edges)
# pos=nx.circular_layout(G)
pos=nx.spring_layout(G, k=100)
plt.figure(figsize=(10,8))    
nx.draw(G,pos,edge_color='black',width=1,linewidths=1,\
node_size=50,node_color='skyblue',alpha=0.9,\
labels={node:node for node in G.nodes()}, font_size=8)
keys = zip(g_data['Subject'], g_data['Object'])
edge_lab=dict(zip(keys,g_data['Predicate']))
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_lab, font_size = 8)
plt.axis('off')
# plt.savefig("gs_graph_tb_prog_fact.png")
plt.show()


# knowledge graph for ideal set
g_data = ideal
edges=zip(g_data['Subject'], g_data['Object'])
G=nx.Graph()
G.add_edges_from(edges, color='black')
# pos=nx.circular_layout(G)
pos=nx.spring_layout(G, k=100)
plt.figure(figsize=(10,8))  
edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]  
nx.draw(G,pos,edges=edges,edge_color=colors,width=1,linewidths=1,\
node_size=50,node_color='skyblue',alpha=0.9,\
labels={node:node for node in G.nodes()}, font_size=10)
keys = zip(g_data['Subject'], g_data['Object'])
edge_lab=dict(zip(keys,g_data['Predicate']))
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_lab, font_size = 10, color=colors)
plt.axis('off')
# plt.savefig("gs_graph_NCT01471782_with_hl2")
plt.show()


