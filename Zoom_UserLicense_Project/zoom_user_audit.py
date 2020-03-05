import csv
import datetime
import os
import re
# # # 
# 
# The 4 March @ 11:43am EST push has a working script for two of the requirements. I've hand-checked the data to verify.
#
# One other small issue is the amount of editing required to make the CSVs work. Blank lines need be removed
# and the header line needs be removed. That should be easy enough to manipulate at the top of this script. 
# For the time being, I've included the neccessary files in this directory.
#
# Here's the plan: 
# Make a list of users who have the licensed version of zoom (done)
# Make a list of users with meetings over 45 minutes (done)
# Make a list of users with meetings that have 4+ participants (done)
# If a licensed user does not fall into either of the two requirement groups, they are not using the 
# functionality (excl outside users, still have to figure that out)
#
# To do:
# Define a function to edit the incoming CSV and remove blank lines (done)
# Ignore the header on CSVs (done)
# I also want to explore using the Zoom API to further automate this, so nobody has to plop scripts in a directory for this to run.
# Find a better way to input files rather than hardcoding the names in the script. (done)
#
# # # 

# Importing files

# This block checks through the current directory and locates any fies beginning with "meetinglistdetails", then assigns it to the meeting_data variable.
# The user_file does not need this treatment as it's consistently named.
folder_content = os.listdir(".")
regex_pattern = 'meetinglistdetails_*'
regex = re.compile(regex_pattern)

res = ''
for path in folder_content:
    if regex.search(path):
        res = path
        break #only finds the first file, preventing this script from breaking if there is more than one report present. Looks like it always grabs the oldest report.

meeting_data = res
user_file = 'zoomus_users.csv'
cleaned_meeting_data = 'cleaned_data.csv'

# Convert the meeting_data csv into the cleaned_meeting_data csv, which removes all blank lines. This also
# preserves the original CSV in case you need it for some reason.

with open(meeting_data) as in_file:
    with open(cleaned_meeting_data, 'w') as out_file:
        writer = csv.writer(out_file)
        for row in csv.reader(in_file):
            if row:
                writer.writerow(row)

# Grab the users and their licenses from a zoom output
# Luckily this report doesn't have a header or blank lines, so I don't have to edit it.
with open(user_file) as csvfile:
    usersCSV = csv.reader(csvfile, delimiter=',')
    userslic = {}
    liccount = 0
    for col in usersCSV:
        userslic.update( {col[0] : col[10]} ) #Column 0 is email, Column 10 is license type
        if col[10] == "Licensed":
            liccount += 1

# Grab a list of users and the duration of their zoom meeting.
# Skip the first row (headers)
# Find any meeting longer than 45 minutes and create a dict with them and the user's email.

with open(cleaned_meeting_data) as csvfile:
    meetingCSV = csv.reader(csvfile, delimiter=',')
    next(meetingCSV)
    meetings_over_45 = {}
    users_this_month = []
    for col in meetingCSV:
        if int(col[10]) > 45:
            meetings_over_45[col[3]] = col[10]
        users_this_month.append(col[3]) # List of everybody who used Zoom during the report period
        users_this_month = list( dict.fromkeys(users_this_month)) # Janky way to remove duplicates

# Similar to the above block, check the meeting list and see if a user has meetings with over 3 people. 
# Skip the first row (headers)
# If they DO, add them to the usersparts dictionary.

with open(cleaned_meeting_data) as csvfile:
    usersCSV = csv.reader(csvfile, delimiter=',')
    usersparts = {}
    next(usersCSV)
    for col in usersCSV:
        if int(col[11]) > 3:
            #Column 0 is email, Column 10 is license type
            usersparts.update( {col[3] : col[11]} )


# 
# This block will check the list of user licenses versus the list of meetings over 45 minutes.
# If a user is NOT in the meetings_over_45 dict AND their dict value is Licensed, they are a licensed user
# not using 1 of the requirements for licensed users.
#
# It also prints out the final report, including time and number of licenses used/reclaimable
# 

print("")
start_date = meeting_data.split('_')[1]
end_date = meeting_data.split('_')[2].split('.')[0]
fstart_date = datetime.datetime(int(start_date[0:4]),int(start_date[4:6]),int(start_date[6:])) 
fend_date = datetime.datetime(int(end_date[0:4]),int(end_date[4:6]),int(end_date[6:]))
print("Report covers dates between: ", fstart_date.strftime("%b-%d-%Y"),"to", fend_date.strftime("%b-%d-%Y"))
print("")
print("Licensed Users who do not have any meetings over 45 minutes or with more than 3 participants:")
print("")
reclaimable = []
for i in userslic.keys():
    if i not in meetings_over_45.keys() and userslic[i] == "Licensed" and i not in usersparts and i in users_this_month:
            reclaimable.append(i)
            print(i.split('@')[0])

print("")
print("License users who have not used the product during the report period.")
print("")
for i in userslic.keys():
    if i not in users_this_month and userslic[i] == "Licensed":
        print(i)

#Some extra information for the report.
print("")
print("Total licenses used in this report: ", liccount)
print("Number of licenses that can be reclaimed from this report: ",len(reclaimable))
print("")



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