from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.parser import parse
import shutil



path_base = "/Volumes/GoogleDrive-111652351013091046884/Shared drives/LITERA/Android/data/phone/"
onlyfiles = [f for f in listdir(path_base + "HTML") if isfile(join(path_base + "HTML", f))]

for file_name in onlyfiles:
    print("File: " + file_name[:-5] )

    shutil.copyfile(join(path_base + "HTML" , file_name), join(path_base + "TXT" , file_name[:-5] + ".txt"))

    with open(join(path_base + "TXT" , file_name[:-5] + ".txt"),'r') as file:
        data = file.readlines()

    actdat = data[32]
    # Hotfix in case dates are expressed in Spanish
    actdat = actdat.replace(" ene ", " jan ")
    actdat = actdat.replace(" abr ", " apr ")
    actdat = actdat.replace(" ago ", " aug ")
    actdat = actdat.replace(" dic ", " dec ")
    actdat = actdat.replace(" ene. ", " jan ")
    actdat = actdat.replace(" abr. ", " apr ")
    actdat = actdat.replace(" ago. ", " aug ")
    actdat = actdat.replace(" dic. ", " dec ")

    preapp = [app.end(0) for app in re.finditer('<p class="mdl-typography--title">', actdat)] 
    postapp = [app.start(0) for app in re.finditer('<br></p></div><div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">', actdat)]
    posttime = [time.start(0) for time in re.finditer('</div><div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1 mdl-typography--text-right">', actdat)]

    ID = []
    appname = []
    datetime = []
    timezone = []

    for i in range(len(posttime)):

        appname += [actdat[preapp[i]:postapp[i]]]

        stamp = actdat[posttime[i]-30:posttime[i]]
        idx = [app.end(0) for app in re.finditer('>', stamp)]
        if len(idx) > 0:
            stamp = stamp[idx[-1]:]

        datetime += [parse(stamp[:-4])]
        timezone += [stamp[-3:]]
        ID += [file_name[:-5]]

    dataframe = pd.DataFrame(list(zip(ID,appname,datetime,timezone)),columns = ['ID','App','Timestamp','TimeZone'])

    #dataframe.loc[dataframe['App'].str.contains('clock', case=False), 'App'] = 'clock'
    #dataframe.loc[dataframe['App'] != "clock", "App"] = "app"

    print(dataframe.head())

    dataframe.to_csv(join(path_base + "CSV" , file_name[:-5] + ".csv"), index=False)