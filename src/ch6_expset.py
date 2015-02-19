from core import *

def do_ch6_b():
    # This JSON file contains results about the performance of various experiments in the experiment set.
    clusteringResultsJSON=open(data_dir+'../clusteringResults.json')
    clusteringResults = json.load(clusteringResultsJSON)
    clusteringResultsJSON.close()
    # Print a summary of the JSON in the file.
    pprint.pprint(clusteringResults)
    
    for experiment in clusteringResults['exps']:
        print experiment['name']
        print experiment['results']['OnmiResults']['Output']['NMISum']
    