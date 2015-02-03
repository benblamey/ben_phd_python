from core import *

headers = ['userId', 
#'isIntra',  <<< NEED TO RE-ENABLE!!!
'leftDatumID','rightDatumID','leftDataType','rightDataType','featureID','svmValue','message',
]

def do_ch6():

    # userID, datumID, kind, dataKind, dataType, originalText, Note, 
    # userID, (isIntra),leftDatumID,rightDatumID,leftDataType,rightDataType,featureID,svmValue,message,

    with open(data_dir + '/PhaseB_Pair_Annos.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        first = True
        rows = [x for x in spamreader]

    #remove the header row
    rows.pop(0)



    newRows = []
    rows = [ { headers[i] : row[i] for i in range(len(row)-1) } for row in rows]
    for row in rows:
        row['svmValue'] = float(row['svmValue'])

    # for the time being, invent a intra-/not intra label.
    for row in rows:
        row['isIntra'] = random.choice([True, False, False, False])

    print 'Example row:'
    print rows[0]


    # In[3]:

    total_gt_datums = 161

    totalEdge = len(rows)
    intraEdge = len([row for row in rows if row['isIntra']])
    interEdge = len([row for row in rows if not row['isIntra']])

    ch6_table_data = (            
        ('Total Datums', total_gt_datums, ''),
        ('Total Edges', totalEdge, '{:.2f}\%'.format(100.0) ),
        ('Intra-Event Edges', intraEdge, '{:.2f}\\%'.format(100*float(intraEdge)/totalEdge) ),
        ('Intra-Event Edges', interEdge, '{:.2f}\\%'.format(100*float(interEdge)/totalEdge) )
    )

    t1 = matrix2latex.matrix2latex(
          ch6_table_data, 
          filename='C:/work/docs/PHD_work/thesis/images/ch6_table_summary.tex',
          caption='Summary of Phase B Annotations.',
          alignment='l r r')
    print t1


    # In[4]:

    x = [row['svmValue'] for row in rows if ((row['featureID'] == 'Friends_InCommon') and row['isIntra']) ]
    y = [row['svmValue'] for row in rows if ((row['featureID'] == 'Friends_InCommon') and not (row['isIntra'])) ]

    matplotlib.pyplot.hist(x, 100, range=(1.0), label='Intra-Event Edges', alpha=0.5)
    matplotlib.pyplot.hist(y, 100, range=(1.0), label='Inter-Event Edges', alpha=0.5)
    matplotlib.pyplot.legend(loc='upper right')
    savefig("output/ch4_gen_freqGTevents.pdf", dpi=600, figsize=(8, 6))
    savefig("output/ch4_gen_freqGTevents.eps", dpi=600, figsize=(8, 6))
    matplotlib.pyplot.show()


