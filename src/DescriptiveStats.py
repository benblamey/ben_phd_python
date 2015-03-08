from core import *

# Import Datum Types from CSV file 
def do_descriptiveStats():
    global total_gt_datums
    # See: ExportGroundTruthDatumEventTypes in Java.


    # a table of the different kinds of datums was exported to CSV (for all user lifestories)
    
    # { ID : datum-classname }
    # all the datums -- not just the ground truth datums.
    datum_types = {}

    # Two strategies for life story selection:
    #- Use the latest life story always - recommended for most things - maximizes Ground truth data which "exists" in the life stories (38 missing vs. 104)
    #- Use the life story which matches the gold gate doc -this is the only strategy suitable for gold labelling text eval. */
    with open(data_dir + 'DatumTypesForPython.csv', 'rb') as csvfile: # LATEST
        #- these are slightly older and contain slightly more datums!!!!!!!!!!!!!
         spamreader = csv.reader(csvfile, delimiter=',')
         for row in spamreader:
            datum_types[row[0]] = row[1]
    print set(datum_types.values())
    if (len(set(datum_types.keys())) != total_gt_datums):
        print "Number of GT datums defined in core.py = " + str(total_gt_datums)
        print "Number of GT datums in DatumTypesForPython.csv = " + str(len(set(datum_types.keys())))
#        raise Exception("gt datum count does not match")

    pp = pprint.PrettyPrinter(indent=4)

    client = pymongo.MongoClient("localhost", 27017) # previously using 1234 for tunnel.
    users = client.SocialWorld.users

    print "number of users: " + str(users.count())

    data = []
    excluded_datums = 0

    for user in users.find():
        
        print user["FACEBOOK_USER_ID"]
        
        if (user[u"FACEBOOK_USER_ID"] == u"16457018212"):
            continue # Unknown randomer
        if (user[u"FACEBOOK_USER_ID"] == u"836555706"):
            continue # Muhamed Mustafa
        if (user[u"FACEBOOK_USER_ID"] == u"100005149806497"):
            continue # Felix Smith

        
        fullname = unicode(user[u"FACEBOOK_FIRST_NAME"]) + unicode(user[u"FACEBOOK_LAST_NAME"])
        print "fullname:" + fullname


        if "GROUND_TRUTH_EVENTS" in user:
            print fullname
            usergts = user["GROUND_TRUTH_EVENTS"]

            data_user = []

            for gtec in usergts["events"]:

                data_user_datums = []

                # lookup the datum IDs in the dictionary
                # [3:] #strip off 'fb_' at the start
                for datum in gtec["datums"]:

                    datum_num_id = datum['id']
                    if (datum_num_id.startswith('fb_')):
                        datum_num_id = datum_num_id[3:]

                    # We exclude datums that are missing from the latest life story.
                    if (datum_types.has_key(datum_num_id)):    
                        datumtype = datum_types[datum_num_id]
                        data_user_datums.append((datum_num_id, datumtype))
                    else:
                        excluded_datums += 1

                if (len(data_user_datums) > 0):
                    data_user.append(data_user_datums)

            if (len(data_user)>0):
                data.append(data_user)

    table_data = []
    table_data.append(("Participants", users.count()))
    table_data.append(("...who created ground truth event clusters",len(data)))

    table_data.append(("Total ground truth event clusters", 
                       sum(len(user) for user in data)))

    table_data.append(("Mean clusters per user", 
                       "{:.2f}".format(
    float(sum(len(user) for user in data))/ # no of clusters
                        users.count()) # no of users
                       ))

    total_gt_datums_calc = len(list(chain.from_iterable(chain.from_iterable(data))))
    print "total_gt_datums: "
    print total_gt_datums
    print "total_gt_datums_calc: "
    print total_gt_datums_calc # GT datums from MongoDB
    assert(total_gt_datums == total_gt_datums_calc)
    table_data.append(("Total datums in ground truth clusters", total_gt_datums))

    table_data.append(("Mean datums per cluster", 
                       "{:.2f}".format(
                       float(len(list(chain.from_iterable(chain.from_iterable(data))))) # total datums
                       /sum(len(user) for user in data) # total clusters
                       )
                       ))



    #print "List of Number of Ground Truth Event Clusters per User"
    number_of_gt_events_per_user = list(len(user_events) for user_events in data)
    #pp.pprint(number_of_gt_events_per_user)


    #print "List of Number of Datums per Ground Truth Event Cluster"
    number_of_datums_per_gt_event_cluster = [len(list(gt_cluster)) for gt_cluster in chain.from_iterable(data)]
    #pp.pprint(number_of_datums_per_gt_event_cluster)

    #table_data.append(("Total ground truth event clusters", total_gtecs))
    #table_data.append(("Total ground truth event cluster datums", total_gtecdatums))



    print("#### Excluded Datums: " + str(excluded_datums) + "####") # under latest=38,gold_or_latest=?
    pp.pprint(table_data)

    # Generate Data for Bar Chart
    # Frequency of Number of Ground Truth Event Clusters per User
    # =========

    gteventsizes = number_of_gt_events_per_user


    xvalues = range(1,max(gteventsizes)+1)
    gt_events_per_user_graph_data = [0] * max(gteventsizes)
    print xvalues
    for (x,f) in Counter(gteventsizes).items():
        gt_events_per_user_graph_data[x-1] = f
    print gt_events_per_user_graph_data  

    width = 1

    xlabels = range(0,max(gteventsizes)+2, 2)
    xlabels_positions = [x + 0.5 for x in xlabels]
    xminorformatter = FixedLocator([x - 0.5 for x in xlabels])

    bar(xvalues, gt_events_per_user_graph_data, width=width, linewidth=1)
    yticks(range(0, max(gt_events_per_user_graph_data)+2))
    xticks(xlabels_positions, xlabels)
    xlabel("# Ground Truth Events for User")
    ylabel("Frequency")
    xlim(0, max(xlabels)+1)

    # The function gca() returns the current axes - instance of http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes
    gca().get_xaxis().set_minor_locator(xminorformatter)
    gca().get_xaxis().tick_bottom()
    gca().get_yaxis().tick_left()

    savefig(phd_output_dir+"ch4_gen_freqGTusers.png", dpi=600, figsize=(8, 6))
    savefig(phd_output_dir+"ch4_gen_freqGTusers.pdf", dpi=600, figsize=(8, 6))
    #title("Frequency of Number of Ground Truth Event Clusters per User")


    # Frequency of Number of Datums per Ground Truth Event Cluster
    # ============================================================

    gtecsizes = number_of_datums_per_gt_event_cluster

    xvalues = range(1,max(gtecsizes)+1)
    datums_per_event_cluster_graph_data = [0] * max(gtecsizes)
    print xvalues
    for (x,f) in Counter(gtecsizes).items():
        datums_per_event_cluster_graph_data[x-1] = f
    print datums_per_event_cluster_graph_data  

    #import numpy
    #xlocations = numpy.array(range(len(gteventsizes)))+0.5
    #xlocations = xlocations+ width/2 * 2
    #print xlocations

    width = 1

    xlabels = range(0,max(gtecsizes)+2, 2)
    xlabels_positions = [x + 0.5 for x in xlabels]
    xminorformatter = FixedLocator([x - 0.5 for x in xlabels])

    #print xlocations

    bar(xvalues, datums_per_event_cluster_graph_data, width=width, linewidth=1)
    yticks(range(0, max(datums_per_event_cluster_graph_data)+10, 10))
    xticks(xlabels_positions, xlabels)
    xlim(0, max(xlabels)+1)

    xlabel("# Datums in Ground Truth Event Cluster")
    ylabel("Frequency")

    # The function gca() returns the current axes - instance of http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes
    gca().get_xaxis().set_minor_locator(xminorformatter)
    gca().get_xaxis().tick_bottom()
    gca().get_yaxis().tick_left()

    savefig(phd_output_dir+"ch4_gen_freqGTevents.png", dpi=600, figsize=(8, 6))
    savefig(phd_output_dir+"ch4_gen_freqGTevents.pdf", dpi=600, figsize=(8, 6))
    #title("Frequency of Number of Datums per Ground Truth Event Cluster")


    # Types in GT Event Clusters
    # =======

    # In[6]:

    datum_type_counts = Counter()

    for user in data:
        for gt_event_cluster in user:
            for datum in gt_event_cluster:
                datum_type = datum[1]
                datum_type_counts[datum_type] += 1

    pretty_labels = {
    'benblamey.saesneg.model.datums.DatumPhoto': 'Photo',
    'benblamey.saesneg.model.datums.DatumStatusMessage': 'Status Message',
    'benblamey.saesneg.model.datums.DatumCheckin': 'Check-In',
    'benblamey.saesneg.model.datums.DatumEvent': 'Facebook Event',
    'mixed': '(Mixed)',
    }

    #t = sum(x_list)
    #cluster_type_comp_table_data = zip(label_list, x_list, [("{:.2f}".format(
    #    (float(x)/t) * 100) + "\%") # \% is for latex.
    #                                  for x in x_list ])

    label_list = [pretty_labels[key] for key in datum_type_counts.keys()]
    values = datum_type_counts.values()

    datum_type_table_data = zip(label_list, values)



    #cluster_type_comp_table_data = sorted(cluster_type_comp_table_data, key=lambda x: x[1], reverse=True) # %'s are strings! sort on col.2

    #cluster_type_comp_table_data.reverse()
    #print cluster_type_comp_table_data

    hr = ['Type','Frequency']

    datum_type_table_data.append(("\midrule Total", sum(values)))

    t = matrix2latex.matrix2latex(datum_type_table_data,
                                  headerRow = hr,
                                  filename=phd_output_dir+'ch4_table_gen_datums_by_type', 
                                  caption='Frequency of Datum by Type', 
                                  alignment='r r')
    print t


    # In[7]:

    #Number of types in each gt event cluster
    types_in_gt_clusters = [set([datum[1] for datum in gt_event_cluster]) for gt_event_cluster in list(chain.from_iterable(data))]
    #pp.pprint(types_in_gt_clusters)


    gt_cluster_type_counter = Counter()

    for types in types_in_gt_clusters:
        if (len(types) == 1):
            type = next(iter(types))
        else:
            type = 'mixed'

        gt_cluster_type_counter[type] += 1


    pp.pprint(gt_cluster_type_counter)  


    # In[8]:




    print gt_cluster_type_counter.keys()
    label_list =  [pretty_labels[label] for label in gt_cluster_type_counter.keys()]
    x_list = gt_cluster_type_counter.values()

    axis("equal")
    pie(
    x_list,
    labels=label_list,
    autopct=None,
    #startangle=45
    #autopct="%1.1f%%",
    #pctdistance=0.8
    )



    savefig(phd_output_dir+"ch4_gen_GTtypepie.png", dpi=600, figsize=(8, 6))
    savefig(phd_output_dir+"ch4_gen_GTtypepie.pdf", dpi=600, figsize=(8, 6))


    # In[9]:

    t = sum(x_list)
    cluster_type_comp_table_data = zip(label_list, x_list, [("{:.2f}".format(
        (float(x)/t) * 100) + "\%") # \% is for latex.
                                      for x in x_list ])

    cluster_type_comp_table_data = sorted(cluster_type_comp_table_data, key=lambda x: x[1], reverse=True) # %'s are strings! sort on col.2

    #cluster_type_comp_table_data.reverse()
    print cluster_type_comp_table_data

    hr = ['Type(s) in Event Cluster','Frequency','']

    cluster_type_comp_table_data.append(("\midrule Total", t, ""))

    t = matrix2latex.matrix2latex(cluster_type_comp_table_data,
                                  headerRow = hr,
                                  filename=phd_output_dir+'ch4_table_gen_gt_comp_by_type', 
                                  caption='Ground Truth Cluster Datums by Type', 
                                  alignment='r r r')
    print t


    # X-Type Matrix
    # ====

    # Postive/Intra Cases
    cross_types_matrix = Counter()
    all_types = Set()
    for user in data:
        for gtec in user:
            for x in gtec:
                x_id = x[0]
                x_type = x[1]
                all_types.add(x_type)
                for y in gtec:
                    y_id = y[0]
                    y_type = y[1]
                    if (x_type > y_type):
                        continue
                    if (x_id == y_id):
                        continue
                    types = [x_type,y_type]
                    types.sort()
                    types = tuple(types)
                    cross_types_matrix[types] += 1

    pp.pprint (cross_types_matrix)
    print (all_types)

    # Negative/Inter Cases
    inter_cross_types_matrix = Counter()
    for user in data:
        for cluster_x in user:
            for cluster_y in user:
                if (cluster_x == cluster_y): # this works.
                    continue
                for x_datum in cluster_x:
                    x_type = x_datum[1]
                    for y_datum in cluster_y:
                        y_type = y_datum[1]
                        if (x_type > y_type):
                            continue
                        types = [x_type,y_type]
                        types.sort()
                        types = tuple(types)
                        inter_cross_types_matrix[types] += 1

    # In[12]:

    all_types_sorted = list(all_types)
    all_types_sorted.sort()
    all_types_sorted_reversed = list(all_types_sorted)
    all_types_sorted_reversed.reverse()

    pair_table_data = []

    header_row = list(all_types_sorted)
    header_row = [pretty_labels[typestring] for typestring in header_row]
    header_row.insert(0,"")

    xtype_table_data = [header_row]
    for t1 in all_types_sorted:
        table_row = [pretty_labels[t1]]
        for t2 in all_types_sorted:
            if (t1 <= t2):
                cell = cross_types_matrix[(t1, t2)]
            else:
                cell = "-"
            table_row.append(cell)
        xtype_table_data.append(table_row)

    matrix2latex.matrix2latex(xtype_table_data, 
                              filename=phd_output_dir+"ch6_table_gen_intra_xtype_cluster", 
                              caption="Intra-Cluster Datum Pairs by Type (Positive Cases).", 
                              alignment='r ' * len(header_row))
    pair_table_data.append(
    ("Total intra-cluster (positive) datum pairs", 
     sum(count for count in cross_types_matrix.values())))

    inter_xtype_table_data = [header_row]
    for t1 in all_types_sorted:
        table_row = [pretty_labels[t1]]
        for t2 in all_types_sorted:
            if (t1 <= t2):
                cell = inter_cross_types_matrix[(t1, t2)]
            else:
                cell = "-"
            table_row.append(cell)
        inter_xtype_table_data.append(table_row)

    matrix2latex.matrix2latex(inter_xtype_table_data, 
                              filename=phd_output_dir+"ch6_table_gen_inter_xtype_cluster", 
                              caption="Inter-Cluster Datum Pairs by Type (Negative Cases).", 
                              alignment='r ' * len(header_row))

    pair_table_data.append(
    ("Total inter-cluster (negative) datum pairs", 
     sum(count for count in inter_cross_types_matrix.values())))




    inter_xtype_table_data = [header_row]
    for t1 in all_types_sorted:
        table_row = [pretty_labels[t1]]
        for t2 in all_types_sorted:
            if (t1 <= t2):
                cell = inter_cross_types_matrix[(t1, t2)] + cross_types_matrix[(t1, t2)]
            else:
                cell = "-"
            table_row.append(cell)
        inter_xtype_table_data.append(table_row)

    matrix2latex.matrix2latex(inter_xtype_table_data, 
                              filename=phd_output_dir+"ch6_table_gen_all_xtype_cluster", 
                              caption="Cluster Datum Pairs by Type (All Cases).", 
                              alignment='r ' * len(header_row))

    pair_table_data.append(
    ("\midrule Total cluster datum pairs", 
     sum(count for count in inter_cross_types_matrix.values())
     + sum(count for count in cross_types_matrix.values())))


    # Generate Overview Stats Table
    # ====

    # In[13]:

    t = matrix2latex.matrix2latex(table_data, filename=phd_output_dir+"ch4_table_gen_gt_summary", caption="Summary of participants' ground truth data.", alignment='r r')
    print t


    # In[14]:

    t = matrix2latex.matrix2latex(pair_table_data, 
                                  filename=phd_output_dir+'ch6_table_pair_summary', 
                                  caption='Summary of Ground Truth Datum Pairs.', 
                                  alignment='r r')
    print t

