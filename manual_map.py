import pandas as pd
import numpy as np
import re

#globals-----------------------------------------------------
newDf = None
df = None

name_list = ['Name','First Name', 'Middle Name', 'Last Name', 'Company', 'Designation', 'City', 'Zip', 'Date of Birth', 'Start Date', 'End Date']


#--------------------------------------------------------------
def datetimeToDate():
    global newDf
    date_columns = newDf.select_dtypes(include=[np.datetime64]).columns
    for col in date_columns:
        newDf[col] = newDf[col].dt.strftime('%Y-%m-%d')

def manualMapExcel(file, headers):
    global newDf
    global df
    global name_list

    newDf = None
    df = None

    try:
        newDf = pd.DataFrame()

        df = pd.read_excel(file, sheet_name=0)
        headerlist = headers.split(',')
        #print(headerlist)
        #print(df.head())

        for i in range(4,len(headerlist)):
            if headerlist[i] == 'Empty String':
                newDf[name_list[i]] = ''
            else:
                newDf[name_list[i]] = df[headerlist[i]]

        for i in range(0,4):
            if headerlist[i] == 'Empty String':
                newDf[name_list[i]] = ''

            elif headerlist[i] not in ['Empty String', 'Get From Name', 'First + Last Name']:
                newDf[name_list[i]] = df[headerlist[i]]

            elif headerlist[i] == 'Get From Name':
                if headerlist[0] in ['Empty String', 'First + Last Name']:
                    newDf[name_list[i]] = ''
                else:
                    if i == 1:
                        newDf[name_list[i]] = df[headerlist[0]].apply(lambda x: x.split()[0])
                    if i == 3:
                        newDf[name_list[i]] = df[headerlist[0]].apply(lambda x: x.split()[-1] if len(x.split()) > 0 else '')

            elif headerlist[i] == 'First + Last Name':
                if headerlist[1] in ['Empty String', 'Get From Name']:
                    newDf[name_list[i]] = ''
                else:
                    if headerlist[3] in ['Empty String', 'Get From Name']:
                        newDf[name_list[i]] = df[headerlist[1]]
                    else:
                        newDf[name_list[i]] = df[headerlist[1]] + ' ' + df[headerlist[3]]

        newDf = newDf[name_list]
        datetimeToDate()

        return newDf.to_json(orient='records')

    except:
        return 'Error'
