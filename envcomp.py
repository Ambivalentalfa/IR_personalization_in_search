"""
Environmental session 1 to env sesh 2? compare teh distance between two groups for each. We use both jaccard and kendall 

environment results dictionary:
user_id:{username: .. , password: .. , session_id: {query : [top 10 results ranked]}}
one for left one for right, 60 sec between each other
the first 5 queries are the general the last 5 are the biased

############################
For both left and right:
first compare r2_Xw to r1_Xw  (Xw_change1 ) and then r3_Xw to r1_Xw (Xw_change2). Compare these two. Expect Xw_change2 to be larger than Xw_change1.

compare left and right:
rX_rW to rX_lw, we expect the difference to increase as X increases



"""


import matplotlib.pyplot as plt
import json


def gendic(dic,filename):
    f = open(filename)
    data = json.load(f)
    for k,v in data.items():
        i=0
        for k1,v1 in v.items():
            if i >1: #only want "session id"s value which is another dictionary {query : [top 10 results ranked]}
                for k2,v2 in v1.items():
                    dic[k2]=v2 # {query : [top 10 results ranked]}


            i+=1
    # Closing file
    f.close()

def check_jacsim(dic1,dic2):
    sim_dic={}
    sum_sim=0
    for i in dic1: # keys are the same in all dictionaries
        sim_dic[i]=jaccard_similarity(dic1[i],dic2[i])
    #similarity of the results for each query for the two given sessions 
    for k,v in sim_dic.items():
        sum_sim+=v
    return sim_dic, sum_sim/len(sim_dic) # return dictionary of similarities and the mean similarity

# def check_jacdis(dic1,dic2): #just copied sim remember to change both
    sim_dic={}
    sum_sim=0
    for i in dic1: # keys are the same in all dictionaries
        sim_dic[i]=jaccard_distance(dic1[i],dic2[i])
    #similarity of the results for each query for the two given sessions 
    for k,v in sim_dic:
        sum_sim+=v
    return sim_dic, sum_sim/len(sim_dic) # return dictionary of similarities and the mean similarity

def jaccard_similarity(A, B):
    #Find intersection of two sets
    nominator = intersection(A,B)

    #Find union of two sets
    denominator = Union(A,B)

    #Take the ratio of sizes
    similarity = len(nominator)/len(denominator)
    
    return similarity

# def jaccard_distance(A, B):
#     #Find symmetric difference of two sets
#     nominator = A.symmetric_difference(B)

#     #Find union of two sets
#     denominator = A.union(B)

#     #Take the ratio of sizes
#     distance = len(nominator)/len(denominator)
    
#     return distance

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def Union(lst1, lst2):
    final_list = lst1 + lst2
    return final_list

def main():
    r1_rw={} # query : [top 10 results ranked]
    r2_rw={}
    r3_rw={}

    r1_lw={}
    r2_lw={}
    r3_lw={}
    l_dic=[r1_rw,r2_rw,r3_rw,r1_lw,r2_lw,r3_lw]
    l_fil=["results_rw_env.json","results_rw_env_2.json","results_rw_env_3.json","results_lw_env.json","results_lw_env_2.json","results_lw_env_3.json"]
    for i in range(6):
        gendic(l_dic[i],l_fil[i])

    # For both left and right:
    # first compare r2_Xw to r1_Xw  (Xw_change1 ) and then r3_Xw to r1_Xw (Xw_change2). Compare these two. Expect Xw_change2 to be larger than Xw_change1.
    envcomp_dic=[]
    envcomp_mean=[]
    for i in [0,3]: # 0 and 3
        #envcomp_dic_=[]
        # for j in range(3): # 0,1 and 2
        sim_ch1,simmean_ch1=check_jacsim(l_dic[0+i],l_dic[1+i]) #r1 and r2
        sim_ch2,simmean_ch2=check_jacsim(l_dic[0+i],l_dic[2+i]) #r1 and r3
        envcomp_mean.append(simmean_ch1)
        envcomp_mean.append(simmean_ch2)
        envcomp_dic.append(sim_ch1)
        envcomp_dic.append(sim_ch2)
    # compare left and right:
    # rX_rW to rX_lw, we expect the difference to increase as X increases
    simlist=[]
    simmeanlist=[]
    for i in range(3):
        simd,simmean=check_jacsim(l_dic[i],l_dic[i+3])
        simlist.append(simd)
        simmeanlist.append(simmean)
    
    print("Mean:",envcomp_mean) 
    print(simmeanlist)

###############################################
#FIRST COMPARING CHANGES BETWEEN ENVIRONMENTAL# 
###############################################


rwquery_plot={}
lwquery_plot={}
rwlw=[rwquery_plot,lwquery_plot]
queries=[]

for p in rwlw:
    for k,v in envcomp_dic[1].items():
        if len(queries)<10:
            queries.append(k)
        p[k]=[]
#print(rwlw)

for i,e in enumerate(envcomp_dic):
    if i >1:
        for k,v in e.items():
            lwquery_plot[k].append(v)
    else:
        for k,v in e.items():
            rwquery_plot[k].append(v)
                
#print( "AAAHHH:",lwquery_plot,"rw",rwquery_plot,"QQQQQQq",queries) # {change nr:[query means]}
lbl=["RW", "LW"]
for j,q in enumerate(rwlw):
    for i in queries:
        plt.plot( [1,2 ],q[i], label = i)
    plt.title(f"Change of similarity before and after training, {lbl[j]}.")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #plt.legend()
    plt.show()
            
        



###############################################
#     COMPARING CHANGES BETWEEN LW AND RW     # 
###############################################
#print(simlist) #[[],[],[]] 
env1={}

for q in queries:
    env1[q]=[]
        
for i,e in enumerate(simlist):
    for k,v in e.items():
            env1[k].append(v)
for i in queries:
    plt.plot( [1,2,3], env1[i], label = i)
    
plt.title("Similarity between LW and RW over time.")
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
       
if __name__=="__main__":
    main()