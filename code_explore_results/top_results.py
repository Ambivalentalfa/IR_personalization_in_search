import argparse
import json
import itertools
import math

'''
Input:
filename1.json
filename2.json
run (integer: 1, 2 or 3)
Example:
python3 top_results.py results_lw_env.json results_rw_env.json 1
Output:
Jaccard similarity index.
Text file with left wing and right wing top 10 most common links.
'''

#parsing
parser=argparse.ArgumentParser()
parser.add_argument('filename1')
parser.add_argument('filename2')
parser.add_argument('run')
args=parser.parse_args()

#counting link appearance among all users and queries
with open(args.filename1) as json_file1, open(args.filename2) as json_file2:
	f1=json.load(json_file1)
	f2=json.load(json_file2)
	for itm in f1:
		dic1={}
		dic2={}
		links1=f1[itm][args.run].values()
		links2=f2[itm][args.run].values()
		for query_l in links1:
			for l in query_l:
				if l not in dic1:
					dic1[l]=1
				else:
					dic1[l]+=1
		for query_l in links2:
			for l in query_l:
				if l not in dic2:
					dic2[l]=1
				else:
					dic2[l]+=1

dic1_sorted=dict(sorted(dic1.items(), key=lambda item: item[1], reverse=True))
dic2_sorted=dict(sorted(dic2.items(), key=lambda item: item[1], reverse=True))
		
#taking top 10 most common links
def take(n, collection):
	return list(itertools.islice(collection, n))

top10_lw=take(10, dic1_sorted.keys())
top10_rw=take(10, dic2_sorted.keys())

#jaccard
def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))

jc=jaccard_similarity(top10_lw, top10_rw)
print('Jaccard similarity index:', round(jc, 4))

#saving both rankings into a file
with open(f'./top10_env{args.run}.txt', 'w') as f:
	f.write('TOP 10 Left Wing:'+'\n')
	for ele in top10_lw:
		f.write(str(ele)+'\n')
	f.write('\n'+'TOP 10 Right Wing:'+'\n')
	for ele  in top10_rw:
		f.write(str(ele)+'\n')
	f.write('\n'+'Jaccard similarity index: '+str(round(jc, 4)))

#kendall rank coeff
'''
Does not make sense to compute because when doing the most common links among all users and 
queries we loose the rank.
'''
