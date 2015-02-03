from core import *

def do_ch5():

    # userID, datumID, kind, dataKind, dataType, originalText, Note, 
    IndexUserId = 0
    IndexDatumId = 1
    IndexAnnoKind = 2
    IndexDataKind = 3
    IndexDatumType = 4

    with open(data_dir + 'PhaseA_Annos.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        first = True
        rows = [x for x in spamreader]

    # remove the header row
    rows.pop(0)
    annoKindFreqs = {}

    from collections import Counter
    print Counter([x[IndexAnnoKind] for x in rows])
    print Counter([x[IndexDataKind] for x in rows])
    #])

    total_gt_datums = 161

    print len(rows)

    annoKindLabels = {
        "DateTime": "Temporal",
        "ImageContent": "Image Content",
        "Location": "Location", 
        "People": "People",
        "SocialEvent": "Social Event",
        "UserStructure": "User Structure"
    }

    pretty_labels = {
        'benblamey.saesneg.model.datums.DatumPhoto': 'Photo',
        'benblamey.saesneg.model.datums.DatumStatusMessage': 'Status Message',
        'benblamey.saesneg.model.datums.DatumCheckin': 'Check-In',
        'benblamey.saesneg.model.datums.DatumEvent': 'Facebook Event',
    }


    for annoKind in ["DateTime", "ImageContent", "Location", "People", "SocialEvent", "UserStructure"]:
        print annoKind
        table_data = (            
            ('Total Datums', total_gt_datums),
            ('Total '+annoKindLabels[annoKind]+' Annotations', len([ x[IndexDatumId] for x in rows if (x[IndexAnnoKind] == annoKind)])),
            ('Datums with $\geq1$ annotation', len(Set([x[IndexDatumId] for x in rows if (x[IndexAnnoKind] == annoKind) ]) )),
            ('Mean annotations / datum', "{0:.2f}".format(float(len([ x for x in rows if (x[IndexAnnoKind] == annoKind)]))
                                                          /float(total_gt_datums) ) )
        )
        t1 = matrix2latex.matrix2latex(
           table_data, 
          filename='C:/work/docs/PHD_work/thesis/images/ch5_table_annores_summary_'+annoKind,
          caption='Summary of '+annoKindLabels[annoKind]+' Annotations.',
          alignment='l r')
        print t1

        # this one is just number of annotations, not number of datums -- basically demonstrates different;y heterogeneous nature of data
        hr = ['Datum Type','Text', 'Metadata', 'Image', 'Total Annotations'] 
        table_data2 = []

        for datumType in pretty_labels.keys():
            table_data2.append((
                pretty_labels[datumType], 
                len([ x[IndexDatumId] for x in rows if (x[IndexAnnoKind]==annoKind)
                     and (x[IndexDatumType]==datumType) and (x[IndexDataKind] == "Text")]),
                len([ x[IndexDatumId] for x in rows if (x[IndexAnnoKind] == annoKind)
                     and (x[IndexDatumType]==datumType) and (x[IndexDataKind] == "Metadata")]),
                len([ x[IndexDatumId] for x in rows if (x[IndexAnnoKind] == annoKind)
                     and (x[IndexDatumType]==datumType) and (x[IndexDataKind] == "Image")]),
                len([ x[IndexDatumId] for x in rows if (x[IndexAnnoKind] == annoKind)
                     and (x[IndexDatumType]==datumType) ])
            ))

        # now append the final row of totals    
        table_data2.append((
                'Total', 
                len([ x[IndexDatumId] for x in rows if (x[IndexAnnoKind]==annoKind)
                         and (x[IndexDataKind] == "Text")]),
                len([ x[IndexDatumId] for x in rows if (x[IndexAnnoKind] == annoKind)
                         and (x[IndexDataKind] == "Metadata")]),
                len([ x[IndexDatumId] for x in rows if (x[IndexAnnoKind] == annoKind)
                         and (x[IndexDataKind] == "Image")]),
                len([ x[IndexDatumId] for x in rows if (x[IndexAnnoKind] == annoKind)])
            ))


        t2 = matrix2latex.matrix2latex(
            table_data2, 
            headerRow = hr,
            filename='C:/work/docs/PHD_work/thesis/images/ch5_table_annores_byType_'+annoKind,
            caption=annoKindLabels[annoKind] + ' Annotations by Source Data Kind and Datum Type.' ,
            alignment='l r r r r')
        print t2

