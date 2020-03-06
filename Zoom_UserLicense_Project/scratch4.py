"""
Zoom User License Audit

The goal of this script is to find which Licensed Zoom users are not using the Licensed functionality.
This script will pull all meetinglistdetails_*.csv files from the current working directory, format them into a 
single CSV, and then create lists pairing each user email to:
- Meetings over 45 minutes
- Meetings with >3 participants
It will then produce a report showing users who have not met either of the above requirements.
It will also show licensed users who have not made any meetings during the report period.
After running, it will delete the CSV it created.

"""


import csv, datetime, os, re, time

# Define a few file locations
user_file = "zoomus_users.csv"
cleaned_meeting_data = "cleaned_data.csv"

# Importing files. Looks specifically for the format that the meetinglistdetails csv's come in. Create a list of all of them in the current dir
folder_content = os.listdir(".")
regex_pattern = "meetinglistdetails_*"
regex = re.compile(regex_pattern)
res = []
for path in folder_content:
    if regex.search(path):
        res.append(path)


def clean_csv(incoming_report):
    """
    Go through a list of incoming CSVs. Spin up a new CSV to write to.
    For each incoming CSV, skip the header row and append its contents to the new CSV.
    If a line is blank, skip it.
    """
    for i in incoming_report:
        with open(i) as in_file:
            with open(cleaned_meeting_data, "a") as out_file:
                writer = csv.writer(out_file)
                next(in_file)  # skip the header row
                for row in csv.reader(in_file):
                    if row:
                        writer.writerow(row)


clean_csv(res)
res = sorted(res)

# Generate a dictionary of users and their license type. Also count how many times Licensed appears.
with open(user_file) as csvfile:
    usersCSV = csv.reader(csvfile, delimiter=",")
    userslic = {}
    liccount = 0
    for col in usersCSV:
        userslic.update(
            {col[0]: col[10]}
        )  # Column 0 is email, Column 10 is license type
        if col[10] == "Licensed":
            liccount += 1


# Make a dictionary of all users with meetings OVER 45 minutes. Also create a list of users who have made meetings in the reports.
with open(cleaned_meeting_data) as csvfile:
    meetingCSV = csv.reader(csvfile, delimiter=",")
    meetings_over_45 = {}
    users_this_month = []
    for col in meetingCSV:
        if int(col[10]) > 45:
            meetings_over_45[col[3]] = col[10]
        users_this_month.append(
            col[3]
        )  # List of everybody who used Zoom during the report period
        users_this_month = list(
            dict.fromkeys(users_this_month)
        )  # Janky way to remove duplicates


# Make a dictionary of all users with meetings containing more than 3 people.
with open(cleaned_meeting_data) as csvfile:
    usersCSV = csv.reader(csvfile, delimiter=",")
    usersparts = {}
    for col in usersCSV:
        if int(col[11]) > 3:
            usersparts.update({col[3]: col[11]})


# Create some timestamps.
start_date = res[0].split("_")[1]
end_date = res[(len(res) - 1)].split("_")[2].split(".")[0]
fstart_date = datetime.datetime(
    int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:])
)
fend_date = datetime.datetime(int(end_date[0:4]), int(end_date[4:6]), int(end_date[6:]))
#

# Start the report.

# License file information
print("")
print("## License File Information ##")
print(
    "Using user license information from: ",
    time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime("./zoomus_users.csv"))
    ),
)

# Report file information
print("")
print("## Report file information ##")
print(
    "Report covers dates between: ",
    fstart_date.strftime("%b-%d-%Y"),
    "to",
    fend_date.strftime("%b-%d-%Y"),
)
print("Report generated from the following files: ", res)

# Optional interactive portion, allows the user to see the input before the output
print(input("Press enter to generate report."))
print("")

# Compare the dictionaries to the license file and return only those who do not appear in either 45 minutes/+3 users but DO appear on the details report.
print(
    "Licensed Users who do not have any meetings over 45 minutes or with more than 3 participants:"
)
print("")
reclaimable = []
for email in userslic.keys():
    if (
        email not in meetings_over_45.keys()
        and userslic[email] == "Licensed"
        and email not in usersparts
        and email in users_this_month
    ):
        reclaimable.append(email)
        print("\t", email.split("@")[0])

# Show licensed users who do not appear in the reports
print("")
print("License users who have not used the product during the report period.")
print("")
for email in userslic.keys():
    if email not in users_this_month and userslic[email] == "Licensed":
        print("\t", email.split("@")[0])


# Some extra information for the report.
print("")
print("Total licenses used in this report: ", liccount)
print("Number of licenses that can be reclaimed from this report: ", len(reclaimable))
print("")

# Clean up after yourself so the report can run clean the next time too
os.remove(cleaned_meeting_data)
