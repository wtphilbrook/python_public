import csv, datetime, os, re, time
folder_content = os.listdir(".")
regex_pattern = 'meetinglistdetails_*'
regex = re.compile(regex_pattern)
res = []
for path in folder_content:
    if regex.search(path):
        res.append(path)
print("")
print("")
print("Using user license information from: ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime('./zoomus_users.csv'))))
for i in res:
    meeting_data = i
    user_file = 'zoomus_users.csv'
    cleaned_meeting_data = 'cleaned_data.csv'
    def clean_csv(incoming_report):
        with open(incoming_report) as in_file:
            with open(cleaned_meeting_data, 'w') as out_file:
                writer = csv.writer(out_file)
                for row in csv.reader(in_file):
                    if row:
                        writer.writerow(row)
    clean_csv(meeting_data)
    with open(meeting_data) as in_file:
        with open(cleaned_meeting_data, 'w') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)
    with open(user_file) as csvfile:
        usersCSV = csv.reader(csvfile, delimiter=',')
        userslic = {}
        liccount = 0
        for col in usersCSV:
            userslic.update( {col[0] : col[10]} ) 
            if col[10] == "Licensed":
                liccount += 1
    with open(cleaned_meeting_data) as csvfile:
        meetingCSV = csv.reader(csvfile, delimiter=',')
        next(meetingCSV)
        meetings_over_45 = {}
        users_this_month = []
        for col in meetingCSV:
            if int(col[10]) > 45:
                meetings_over_45[col[3]] = col[10]
            users_this_month.append(col[3]) 
            users_this_month = list( dict.fromkeys(users_this_month)) 
    with open(cleaned_meeting_data) as csvfile:
        usersCSV = csv.reader(csvfile, delimiter=',')
        usersparts = {}
        next(usersCSV)
        for col in usersCSV:
            if int(col[11]) > 3:
                
                usersparts.update( {col[3] : col[11]} )
    start_date = meeting_data.split('_')[1]
    end_date = meeting_data.split('_')[2].split('.')[0]
    fstart_date = datetime.datetime(int(start_date[0:4]),int(start_date[4:6]),int(start_date[6:])) 
    fend_date = datetime.datetime(int(end_date[0:4]),int(end_date[4:6]),int(end_date[6:]))
    print("")
    print("")
    print("Report covers dates between: ", fstart_date.strftime("%b-%d-%Y"),"to", fend_date.strftime("%b-%d-%Y"))
    print("Report generated from the following file: ", i)
    print(input("Press enter to generate report."))
    print("")
    print("Licensed Users who do not have any meetings over 45 minutes or with more than 3 participants:")
    print("")
    reclaimable = []
    for i in userslic.keys():
        if i not in meetings_over_45.keys() and userslic[i] == "Licensed" and i not in usersparts and i in users_this_month:
                reclaimable.append(i)
                print("\t",i.split('@')[0])
    print("")
    print("License users who have not used the product during the report period.")
    print("")
    for i in userslic.keys():
        if i not in users_this_month and userslic[i] == "Licensed":
            print("\t",i.split('@')[0])  
    print("")
    print("Total licenses used in this report: ", liccount)
    print("Number of licenses that can be reclaimed from this report: ",len(reclaimable))
    print("")















