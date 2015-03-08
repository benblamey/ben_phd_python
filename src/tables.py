import pymongo

client = pymongo.MongoClient("localhost", 1234)
users = client.SocialWorld.users
table_data = [] #data for the latex table.

table_data.append(("Total Participants", users.count()))

import sys
sys.path.append('C:/work/code/3rd_Ben/matrix2latexPython/matrix2latex')
import matrix2latex as foo
import numpy

havedonegroundtruthevents = 0
gteventsizes = [] # list in ints - sizes of everyones ground truth events.

for user in users.find():
	fullname = unicode(user["FACEBOOK_FIRST_NAME"]) + unicode(user["FACEBOOK_LAST_NAME"])
	if fullname == "Ben Blamey":
		continue
	if "GROUND_TRUTH_EVENTS" in user:
		havedonegroundtruthevents += 1
		usergts = user["GROUND_TRUTH_EVENTS"]
		gteventsizes.append(len(usergts))
	

table_data.append(("...who created ground truth event clusters", havedonegroundtruthevents))		

bins = []

hist1 = numpy.histogram(gteventsizes, bins=(1,2,3,4,5)
print(hist1)
		
t = foo.matrix2latex(table_data, filename="table", caption="Summary of participants' ground truth data.", alignment='|r|c|')



print(t)














