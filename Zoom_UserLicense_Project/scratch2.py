import csv

# # # 
# 
# The 4 March @ 11:43am EST push has a working script for two of the requirements. I've hand-checked the data to verify.
#
# One other small issue is the amount of editing required to make the CSVs work. Blank lines need be removed
# and the header line needs be removed. That should be easy enough to manipulate at the top of this script. 
# For the time being, I've included the neccessary files in this directory.
#
# Here's the plan: 
# Make a list of users who have the licensed version of zoom (done-ish, see the last block of code)
# Make a list of users with meetings over 45 minutes (done)
# Make a list of users with meetings that have 4+ participants (done)
# If a licensed user does not fall into either of the two requirement groups, they are not using the 
# functionality (excl outside users, still have to figure that out)
#
# To do:
# Define a function to edit the incoming CSV
# I also want to explore using the Zoom API to further automate this, so nobody has to plop scripts in a directory for this to run.
#
# # # 

# Grab the users and their licenses from a zoom output
with open('zoomus_users.csv') as csvfile:
    usersCSV = csv.reader(csvfile, delimiter=',')
    userslic = {}
    for col in usersCSV:
        #Column 0 is email, Column 10 is license type
        userslic.update( {col[0] : col[10]} )

# Grab a list of users and the duration of their zoom meeting.
# Find any meeting longer than 45 minutes and create a dict with them and the user's email
with open('meetinglistdetails_20200201_20200301.csv') as csvfile:
    meetingCSV = csv.reader(csvfile, delimiter=',')
    meetings_over_45 = {}
    for col in meetingCSV:
        if int(col[10]) > 45:
            meetings_over_45[col[3]] = col[10]

# Similar to the above block, check the meeting list and see if a user has meetings with over 3 people. 
# If they DO, add them to the usersparts dictionary.
with open('meetinglistdetails_20200201_20200301.csv') as csvfile:
    usersCSV = csv.reader(csvfile, delimiter=',')
    usersparts = {}
    for col in usersCSV:
        if int(col[11]) > 3:
            #Column 0 is email, Column 10 is license type
            usersparts.update( {col[3] : col[11]} )

# This block will check the list of user licenses versus the list of meetings over 45 minutes.
# If a user is NOT in the meetings_over_45 dict AND their dict value is Licensed, they are a licensed user
# not using 1 of the requirements for licensed users.
#
# Added another check for usersparts to see if they have meetings over 4 users or not
print("Licensed Users who do NOT have meetings over 45 minutes or with more than 3 participants:")
print("")
for i in userslic.keys():
    if i not in meetings_over_45.keys():
        if userslic[i] == "Licensed":
            if i not in usersparts:
                print(i)



#
# This section exists only to comment/uncomment when I want to see how all my dict/lists are outputting.
#
# print("userslic")
# print(userslic)
# print(type(userslic))
# print("")
# #print("license_users")clear
# #print(license_users)
# print("")
# print("meetings_over_45")
# print(meetings_over_45)
# print(type(meetings_over_45))