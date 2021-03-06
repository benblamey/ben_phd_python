from __future__ import division # use 3.x behaviour for division -- / for float, // for int.

from core import *

prettyExpNames = {
     #'Full': 'All (Dist. Tempex.)',
    'Full_ClassicTempex': 'All',
    
    'None': 'None',
    
    'FriendsStrat_Only': 'Friends',
    'EventsStrat_Only': 'Events',
    'SpatialStrat_Only': 'Spatial',
    'TemporalStrat_Only': 'Temporal (dist.)',
    'UserHelpStrat_Only': 'User Help',
    'SceneStrat_Only': 'Scene',
    'KindStrat_Only': 'Kind',
    'OldSkoolTempex': 'Temporal',
    
    'SceneAStrat_Only': 'Scene', # old typo.
}

def do_ch7_b():
    # This JSON file contains results about the performance of various experiments in the experiment set.
    clusteringResultsJSON=open(data_dir+'../clusteringResults.json')
    clusteringResults = json.load(clusteringResultsJSON)
    clusteringResultsJSON.close()
    # Print a summary of the JSON in the file.
    #pprint.pprint(clusteringResults)
    
    nmisums = {}
    accIntrasByExp = {}
    accIntersByExp = {}
    exp_names = []
    
    i = 0
    for experiment in clusteringResults['exps']: # for each experiment.
        print(experiment['name'])
        if (experiment['name'] == 'Full'):
            continue
        if (experiment['name'] == 'TemporalStrat_Only'): # Corrections -- exclude result for distributed tempex.
            continue
        
        # mean the NMISums across the users for each exp.
        nmisumsforexp_byuser = []
        for nmiResultsForUser in experiment['results']['OnmiResults'].values(): # for each user.
            print nmiResultsForUser
            nmiOutputForUser = nmiResultsForUser['Output']
            if 'NMISum' in nmiOutputForUser:
                nmisum = nmiOutputForUser['NMISum']
                if nmisum == 'NAN': # In the case of a perfect match in the trivial case (A)->(A), Onmi returns NAN. We interpret this as 1.
                    nmisum = 1
                nmisumsforexp_byuser.append(nmisum)
            else:
                # In the case of a correct trivial mapping (1)->(1) -- the NMI tool returns "NaN".
                # For consistency with other perfect scores, we simply use 1.
                nmisumsforexp_byuser.append(1.0)
        print nmisumsforexp_byuser
        nmisums[i] = numpy.mean(nmisumsforexp_byuser)
        
        pairIntraCorrect = 0
        pairIntraIncorrect = 0
        pairInterCorrect = 0
        pairInterIncorrect = 0

        for pairResultsForUser in experiment['results']['PairwiseResults'].values(): # for each user
            # For each experiment:
            pprint.pprint(pairResultsForUser);
            pairIntraCorrect = pairIntraCorrect +       pairResultsForUser['pairIntraCorrect']
            pairIntraIncorrect = pairIntraIncorrect +   pairResultsForUser['pairIntraIncorrect']
            pairInterCorrect = pairInterCorrect +       pairResultsForUser['pairInterCorrect']
            pairInterIncorrect = pairInterIncorrect +   pairResultsForUser['pairInterIncorrect']
            
            #f1 = 2 * prec * recall / (prec + recall)
        accIntrasByExp[i] = pairIntraCorrect  / (pairIntraCorrect + pairIntraIncorrect)
        accIntersByExp[i] = pairInterCorrect  / (pairInterCorrect + pairInterIncorrect)
        
        # append the name of the experiment.
        exp_names.append(prettyExpNames[experiment['name']])
        i += 1
    
    print(nmisums)
    print(exp_names)
    
    
    hr = ['Strategy Set', 'Accuracy (Intra-Event Edges)', 'Accuracy (Inter-Event Edges)', 'Mean NMI']
    table_data = []
    
    i = 0
    for exp_name in exp_names:
        row = (
            exp_name,
            '%.2f' % accIntrasByExp[i],
            '%.2f' % accIntersByExp[i],
            '%.2f' % nmisums[i]
        )
        table_data.append(row)
        i += 1

    tFoo = matrix2latex.matrix2latex(
        table_data, 
        headerRow = hr,
        filename='C:/work/docs/LATEX/thesis/images/ch7_table_expset.tex',
        caption='Performance According to Strategy Selection' ,
        alignment='l r r r r')

    
    
    
    # import matplotlib.pyplot as plt
    
    #fig, ax = subplots()
    #ax.set_xticks([0.15, 0.68, 0.97])
    #ax.set_yticks([0.2, 0.55, 0.76])
    #ax.set_xticklabels( exp_names )
    
    clf()
    
    print "nmisums: "
    print nmisums.keys()
    print nmisums.values()
    bar(nmisums.keys(), nmisums.values())
    xticks( 
        list(xtickloc + 0.5 for xtickloc in numpy.arange(len(nmisums))), 
        exp_names, 
        rotation=90 )    
    tight_layout()
    savefig("C:/work/docs/LATEX/thesis/images/ch7_expset_nmisum.png", dpi=600, figsize=(8, 6))
    clf()
    
    
    bar(accIntrasByExp.keys(), accIntrasByExp.values())
    xticks( 
        list(xtickloc + 0.5 for xtickloc in numpy.arange(len(accIntrasByExp))), 
        exp_names, 
        rotation=90 )    
    tight_layout()
    savefig("C:/work/docs/LATEX/thesis/images/ch7_expset_accIntrasByExp.png", dpi=600, figsize=(8, 6))
    clf()
    
    bar(accIntersByExp.keys(), accIntersByExp.values())
    xticks( 
        list(xtickloc + 0.5 for xtickloc in numpy.arange(len(accIntersByExp))), 
        exp_names, 
        rotation=90 )    
    tight_layout()
    savefig("C:/work/docs/LATEX/thesis/images/ch7_expset_accIntersByExp.png", dpi=600, figsize=(8, 6))
    clf()
    
    
    
    
    #N = 5
    #menMeans = (20, 35, 30, 35, 27)
    #menStd =   (2, 3, 4, 1, 2)

    #ind = np.arange(N)  # the x locations for the groups
    #width = 0.35       # the width of the bars

    #fig, ax = plt.subplots()
    #rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)

    #womenMeans = (25, 32, 34, 20, 25)
    #womenStd =   (3, 5, 2, 3, 3)
    #rects2 = ax.bar(ind+width, womenMeans, width, color='y', yerr=womenStd)
    

    # add some text for labels, title and axes ticks
    #ax.set_ylabel('Scores')
    #ax.set_title('Scores by group and gender')
    #ax.set_xticks(ind+width)
    #ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )

    #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )

    #def autolabel(rects):
    #        # attach some text labels
    #        for rect in rects:
    #            height = rect.get_height()
    #            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
    #                    ha='center', va='bottom')

    #autolabel(rects1)
    #autolabel(rects2)

    
    
    
