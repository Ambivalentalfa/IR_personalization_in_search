from scipy.stats import kendalltau
import json
import matplotlib.pyplot as plt

#jaccard similarity
def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

def comparison(f1, f2, session_id, bias):
    lw = open(f1)
    rw = open(f2)
    data_lw = json.load(lw)
    data_rw = json.load(rw)
    #avg distances between users
    sum_final = 0
    corr_final = 0

    #for each lw user
    for userid_lw in data_lw.keys():
        # avg distance between queries for a given couple of users
        sum_user = 0
        corr_user = 0
        #look at each rw user
        for userid_rw in data_rw.keys():
            #distance from one query to another query, of the same couple of users
            sum_dist = 0
            corr_dist = 0
            if(bias == 1):
                for query in list(data_lw[userid_lw][session_id].keys())[-5:]:
                       sum_dist += jaccard(data_lw[userid_lw][session_id][query], data_rw[userid_rw][session_id][query])
                       corr_dist += kendalltau(data_lw[userid_lw][session_id][query], data_rw[userid_rw][session_id][query])[0]
                sum_user += sum_dist / 5
                corr_user += corr_dist / 5
            elif(bias == 0):
                for query in list(data_lw[userid_lw][session_id].keys())[:5]:
                       sum_dist += jaccard(data_lw[userid_lw][session_id][query], data_rw[userid_rw][session_id][query])
                       corr_dist += kendalltau(data_lw[userid_lw][session_id][query], data_rw[userid_rw][session_id][query])[0]
                sum_user += sum_dist / 5
                corr_user += corr_dist / 5
            else:
                for query in list(data_lw[userid_lw][session_id].keys()):
                       sum_dist += jaccard(data_lw[userid_lw][session_id][query], data_rw[userid_rw][session_id][query])
                       corr_dist += kendalltau(data_lw[userid_lw][session_id][query], data_rw[userid_rw][session_id][query])[0]
                #and add the mean to the total distance
                sum_user += sum_dist/10
                corr_user += corr_dist/10
        sum_final += sum_user
        corr_final += corr_user
    #return the average distance of the average results distance between different queries
    return (sum_final/100, corr_final/100)

def internal_comparison(f1, session_id, bias):
    w = open(f1)
    data_w = json.load(w)
    #avg distances between users
    sum_final = 0
    corr_final = 0

    #for each lw user
    for userid_w in data_w.keys():
        # avg distance between queries for a given couple of users
        sum_user = 0
        corr_user = 0
        #look at each user except the current one
        users = list(data_w.keys())
        users.remove(userid_w)
        for userid_w1 in users:
            #distance from one query to another query, of the same couple of users
            sum_dist = 0
            corr_dist = 0
            if(bias == 1):
                for query in list(data_w[userid_w][session_id].keys())[-5:]:
                       sum_dist += jaccard(data_w[userid_w][session_id][query], data_w[userid_w1][session_id][query])
                       corr_dist += kendalltau(data_w[userid_w][session_id][query], data_w[userid_w1][session_id][query])[0]
                sum_user += sum_dist / 5
                corr_user += corr_dist / 5
            elif(bias == 0):
                for query in list(data_w[userid_w][session_id].keys())[:5]:
                       sum_dist += jaccard(data_w[userid_w][session_id][query], data_w[userid_w1][session_id][query])
                       corr_dist += kendalltau(data_w[userid_w][session_id][query], data_w[userid_w1][session_id][query])[0]
                sum_user += sum_dist / 5
                corr_user += corr_dist / 5
            else:
                for query in list(data_w[userid_w][session_id].keys()):
                       sum_dist += jaccard(data_w[userid_w][session_id][query], data_w[userid_w1][session_id][query])
                       corr_dist += kendalltau(data_w[userid_w][session_id][query], data_w[userid_w1][session_id][query])[0]
                #and add the mean to the total distance
                sum_user += sum_dist/10
                corr_user += corr_dist/10
        sum_final += sum_user
        corr_final += corr_user
    #return the average distance of the average results distance between different queries
    return (sum_final/90, corr_final/90)

def general():
    jaccard = []
    jaccard_1 = []
    jaccard_2 = []
    tau = []
    tau_1 = []
    tau_2 = []
    sessions = [1,2,3]
    for i in range(1,4):
        jaccard.append(comparison('results_lw_env_' + str(i) + '.json', 'results_rw_env_' + str(i) + '.json', str(i), None)[0])
        tau.append(comparison('results_lw_env_' + str(i) + '.json', 'results_rw_env_' + str(i) + '.json', str(i),None)[1])
        jaccard_1.append(comparison('results_lw_env_' + str(i) + '.json', 'results_rw_env_' + str(i) + '.json', str(i), 0)[0])
        tau_1.append(comparison('results_lw_env_' + str(i) + '.json', 'results_rw_env_' + str(i) + '.json', str(i),0)[1])
        jaccard_2.append(comparison('results_lw_env_' + str(i) + '.json', 'results_rw_env_' + str(i) + '.json', str(i), 1)[0])
        tau_2.append(comparison('results_lw_env_' + str(i) + '.json', 'results_rw_env_' + str(i) + '.json', str(i), 1)[1])
    #FIGURE PARAMETERS
    fig, axs = plt.subplots(1, 2)
    fig.set_figwidth(10)
    fig.set_figheight(4)
    axs[0].grid(True, linestyle='--')
    axs[1].grid(True, linestyle='--')
    axs[0].plot(sessions, jaccard, 'goldenrod')
    axs[0].plot(sessions, jaccard_1, 'darkred')
    axs[0].plot(sessions, jaccard_2, 'black')
    axs[1].plot(sessions, tau, 'goldenrod')
    axs[1].plot(sessions, tau_1, 'darkred')
    axs[1].plot(sessions, tau_2, 'black')
    axs[0].set_xticks([1, 2, 3])
    axs[1].set_xticks([1, 2, 3])
    axs[0].set_yticks([0, 0.5, 1])
    axs[1].set_yticks([-1, -0.5, 0, 0.5, 1])
    axs[0].legend(['all queries', 'non biased', 'biased'])
    axs[1].legend(['all queries', 'non biased', 'biased'])
    axs[0].set_xlabel('sessions')
    axs[0].set_ylabel('Avg.Jaccard')
    axs[1].set_xlabel('sessions')
    axs[1].set_ylabel('Avg.Kendall-Tau')
    #plt.show()
    plt.savefig('leftright.png')

def general_internal(wing):
    jaccard = []
    jaccard_1 = []
    jaccard_2 = []
    tau = []
    tau_1 = []
    tau_2 = []
    sessions = [1,2,3]
    for i in range(1,4):
        jaccard.append(internal_comparison('results_' + wing + '_env_' + str(i) + '.json', str(i), None)[0])
        tau.append(internal_comparison('results_' + wing + '_env_' + str(i) + '.json', str(i), None)[1])
        jaccard_1.append(internal_comparison('results_' + wing + '_env_' + str(i) + '.json', str(i), 0)[0])
        tau_1.append(internal_comparison('results_' + wing + '_env_' + str(i) + '.json', str(i), 0)[1])
        jaccard_2.append(internal_comparison('results_' + wing + '_env_' + str(i) + '.json', str(i), 1)[0])
        tau_2.append(internal_comparison('results_' + wing + '_env_' + str(i) + '.json', str(i), 1)[1])

    #FIGURE PARAMETERS
    fig, axs = plt.subplots(1, 2)
    fig.set_figwidth(10)
    fig.set_figheight(4)
    axs[0].grid(True, linestyle='--')
    axs[1].grid(True, linestyle='--')
    axs[0].plot(sessions, jaccard, 'goldenrod')
    axs[0].plot(sessions, jaccard_1, 'darkred')
    axs[0].plot(sessions, jaccard_2, 'black')
    axs[1].plot(sessions, tau, 'goldenrod')
    axs[1].plot(sessions, tau_1, 'darkred')
    axs[1].plot(sessions, tau_2, 'black')
    axs[0].set_xticks([1, 2, 3])
    axs[1].set_xticks([1, 2, 3])
    axs[0].set_yticks([0, 0.5, 1])
    axs[1].set_yticks([-1, -0.5, 0, 0.5, 1])
    axs[0].legend(['all queries', 'non biased', 'biased'])
    axs[1].legend(['all queries', 'non biased', 'biased'])
    axs[0].set_xlabel('sessions')
    axs[0].set_ylabel('Avg.Jaccard')
    axs[1].set_xlabel('sessions')
    axs[1].set_ylabel('Avg.Kendall-Tau')
    #plt.show()
    plt.savefig('internal'+wing+'.png')

general()
general_internal('rw')
general_internal('lw')
