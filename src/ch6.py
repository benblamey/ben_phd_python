from core import *

headers = ['userId', 'isIntra', 'leftDatumID','rightDatumID','leftDataType','rightDataType','featureID','svmValue','message',]

def do_ch6():

    # userID, datumID, kind, dataKind, dataType, originalText, Note, 
    # userID, (isIntra),leftDatumID,rightDatumID,leftDataType,rightDataType,featureID,svmValue,message,

    with open(data_dir + '/PhaseB_Pair_Annos.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        rows = [x for x in spamreader]

    #remove the header row
    rows.pop(0)

    # don't try to fix the apparent syntax here by adding more parentheses -- it introduces a syntax error.
    rows = [ { headers[i] : row[i] 
        for i in range(len(row)-1) } 
        for row in rows]
        
    for row in rows:
        row['svmValue'] = float(row['svmValue'])

    # for the time being, invent a intra-/not intra label.
    #for row in rows:
    #    row['isIntra'] = random.choice([True, False, False, False])

    print('Example row:')
    print(rows[0])

    


    totalEdge = len(rows)
    intraEdge = len([row for row in rows if row['isIntra'] == 'true'])
    interEdge = len([row for row in rows if not row['isIntra'] == 'true'])

    ch6_table_data = (            
        ('Total Datums', total_gt_datums, ''),
        ('Total Edges', totalEdge, '{:.2f}\%'.format(100.0) ),
        ('Intra-Event Edges', intraEdge, '{:.2f}\\%'.format(100*float(intraEdge)/totalEdge) ),
        ('Intra-Event Edges', interEdge, '{:.2f}\\%'.format(100*float(interEdge)/totalEdge) )
    )

    t1 = matrix2latex.matrix2latex(
          ch6_table_data, 
          filename='C:/work/docs/PHD_work/thesis/images/ch6_table_edge_summary.tex',
          caption='Datum Edge Summary',
          alignment='l r r')
    print(t1)



    for featureID in set([row['featureID'] for row in rows]):
        print ("Plotting feature value histogram for " + featureID);
        # we skip the Kind_ features
        if (featureID.startswith('Kind_')):
            print("...Skipping")
            continue;
        x = [row['svmValue'] for row in rows if ((row['featureID'] == featureID) and row['isIntra'] == 'true') ]
        y = [row['svmValue'] for row in rows if ((row['featureID'] == featureID) and not (row['isIntra']) == 'true') ]

        xmin = -1.0
        if featureID == 'Scene_ColorLayout':
            xmin = 0
        matplotlib.pyplot.clf()
        matplotlib.pyplot.hist(x, 100, range=(-1.0, 1.0), label='Intra-Event Edges', alpha=0.5)
        matplotlib.pyplot.hist(y, 100, range=(-1.0, 1.0), label='Inter-Event Edges', alpha=0.5)
        matplotlib.pyplot.legend(loc='upper right')
        #matplotlib.pyplot.ax.set_yscale('log')
        matplotlib.pyplot.yscale('log', nonposy='clip')
        matplotlib.pyplot.savefig("../output/ch6_gen_features_"+featureID+".png", dpi=600, figsize=(8, 6))
        #savefig("../output/ch6_gen_freqGTevents.eps", dpi=600, figsize=(8, 6))
        #matplotlib.pyplot.savefig()

    
