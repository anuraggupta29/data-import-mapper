import pandas as pd
import numpy as np
import re

#globals-----------------------------------------------------
df_map_names = {
  'Name' : None,
  'First Name' : None,
  'Middle Name' : None,
  'Last Name' : None,
}

df_map = {
  'Company' : None,
  'Designation' : None,
  'City' : None,
  'Zip' : None,
  'Date of Birth' : None,
  'Start Date' : None,
  'End Date' : None
}

newDf = None
df = None
newDf_names = None
df_sampled = None

def findZipCode():
    global df_sampled
    zipCodeColumn = None

    int_columns = [i for i in df_sampled.columns if df_sampled[i].dtype == np.int64]

    for col in int_columns:
        len_values = df_sampled[col].apply(str).str.len().mode()[0]
        if len_values == 6:
            zipCodeColumn = col
            break

    return zipCodeColumn

def orderDates():
    global df_sampled
    dob = None
    startDate = None
    endDate = None

    date_list = []
    date_columns = df.select_dtypes(include=[np.datetime64]).columns

    if len(date_columns) == 3:
        for col in date_columns:
            df_sampled[col] = df_sampled[col].astype('int64')//1e12
            date_list.append((col, df_sampled[col].mean()))

        date_list = sorted(date_list, key=lambda x: x[1])
        dob = date_list[0][0]
        startDate = date_list[1][0]
        endDate = date_list[2][0]

    return dob, startDate, endDate

def orderNames():
    global df_sampled
    name = None
    fName = None
    mName = None
    lName = None
    nameList = ['personal', 'real', 'actual', 'individual']
    firstNameList = ['f', 'first', 'fore', 'forename', 'firstname', 'fname', 'given', 'givenname']
    lastNameList = ['l', 'last', 'lastname', 'lname', 'namelast', 'surname', 'family', 'familyname']
    middleNameList = ['m', 'middle', 'middlename']

    str_columns = [i for i in df_sampled.columns if df_sampled[i].dtype == object]
    #print(str_columns)

    for col in str_columns:
        colWords = re.split('_|-|\s+', col.lower())
        if len([i for i in colWords if i in firstNameList]) > 0:
            fName = col

        elif len([i for i in colWords if i in lastNameList]) > 0:
            lName = col

        elif len([i for i in colWords if i in middleNameList]) > 0:
            mName = col

    for col in str_columns:
        if col.lower() == 'name':
            name = col
            break
        else:
            colWords = re.split('_|-|\s+', col.lower())
            if 'name' in colWords:
                if len([i for i in colWords if i in nameList]) > 0:
                    name = col

    return name, fName, mName, lName

def findDesignation():
    global df_sampled
    designation = None

    designationList = ['designation', 'design', 'job', 'work', 'profession', 'professional']
    str_columns = [i for i in df_sampled.columns if df_sampled[i].dtype == object and i not in [i for i in df_map.values() if i is not None]]

    for col in str_columns:
        colWords = re.split(',|_|-|!|:', col.lower())
        if len([i for i in colWords if i in designationList]) > 0:
            designation = col
            break

    return designation

def findCity():
    global df_sampled
    city = None

    cityList = ['city', 'location', 'town', 'place', 'home', 'located', 'metropolis']
    str_columns = [i for i in df_sampled.columns if df_sampled[i].dtype == object and i not in [i for i in df_map.values() if i is not None]]

    for col in str_columns:
        colWords = re.split(',|_|-|!|:', col.lower())
        if len([i for i in colWords if i in cityList]) > 0:
            city = col
            break

    return city

def findCompany():
    global df_sampled
    company = None

    companyList = ['company', 'organisation', 'organization', 'corporation', 'firm', 'establishment', 'agency' 'enterprise']
    str_columns = [i for i in df_sampled.columns if df_sampled[i].dtype == object and i not in [i for i in df_map.values() if i is not None]]

    for col in str_columns:
        colWords = re.split(',|_|-|!|:', col.lower())
        if len([i for i in colWords if i in companyList]) > 0:
            company = col
            break

    return company

def getCorrectColumns():
    global df_map

    df_map['City'] = findCity()
    if df_map['City'] is None:
        return False


    df_map['Company'] = findCompany()
    if df_map['Company'] is None:
        return False

    df_map['Zip'] = findZipCode()
    if df_map['Zip'] is None:
        return False

    df_map['Date of Birth'], df_map['Start Date'], df_map['End Date'] = orderDates()
    if df_map['Date of Birth'] is None or df_map['Start Date'] is None or df_map['End Date'] is None:
        return False


    df_map_names['Name'], df_map_names['First Name'], df_map_names['Middle Name'], df_map_names['Last Name'] = orderNames()
    if df_map_names['Name'] is None and df_map_names['First Name'] is None:
        return False

    df_map['Designation'] = findDesignation()
    if df_map['Designation'] is None:
        return False

    return True

def createNewDf():
    global df
    global df_map
    global newDf

    newDf[list(df_map.keys())] = df[list(df_map.values())]

def datetimeToDate():
    global newDf
    date_columns = newDf.select_dtypes(include=[np.datetime64]).columns
    for col in date_columns:
        newDf[col] = newDf[col].dt.strftime('%Y-%m-%d')

def correctNames():
    global newDf_names
    global df
    #print(df_map_names)

    if df_map_names['Name'] is not None:
        newDf_names['Name'] = df[df_map_names['Name']]

        if df_map_names['First Name'] is None:
            newDf_names['First Name'] = df[df_map_names['Name']].apply(lambda x: x.split()[0])
        else:
            newDf_names['First Name'] = df[df_map_names['First Name']]

        if df_map_names['Last Name'] is None:
            newDf_names['Last Name'] = df[df_map_names['Name']].apply(lambda x: x.split()[-1] if len(x.split()) > 0 else '')
        else:
            newDf_names['Last Name'] = df[df_map_names['Last Name']]

        if df_map_names['Middle Name'] is None:
            newDf_names['Middle Name'] = ''
        else:
            newDf_names['Middle Name'] = df[df_map_names['Middle Name']]

    elif df_map_names['Name'] is None:
        newDf_names['First Name'] = df[df_map_names['First Name']]

        if df_map_names['Middle Name'] is None:
            newDf_names['Middle Name'] = ''
        else:
            newDf_names['Middle Name'] = df[df_map_names['Middle Name']]

        if df_map_names['Last Name'] is None:
            newDf_names['Last Name'] = ''
        else:
            newDf_names['Last Name'] = df[df_map_names['Last Name']]

        if df_map_names['Middle Name'] is None:
            newDf_names['Name'] = newDf_names['First Name'] + ' ' + newDf_names['Last Name']
        else:
            newDf_names['Name'] = newDf_names['First Name'] + ' ' + newDf_names['Middle Name'] + ' ' + newDf_names['Last Name']


#--------------------------------------------------------------

def mapExcelMain(filename):
    global newDf
    global df
    global newDf_names
    global df_map
    global df_map_names
    global df_sampled

    df_map_names = {
      'Name' : None,
      'First Name' : None,
      'Middle Name' : None,
      'Last Name' : None,
    }

    df_map = {
      'Company' : None,
      'Designation' : None,
      'City' : None,
      'Zip' : None,
      'Date of Birth' : None,
      'Start Date' : None,
      'End Date' : None
    }

    newDf = None
    df = None
    newDf_names = None
    df_sampled = None

    try:
        df = pd.read_excel(filename, sheet_name=0)

        date_columns = df.select_dtypes(include=[np.datetime64]).columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], format="%Y-%m-%d")

        newDf = pd.DataFrame(columns=df_map.keys())
        newDf_names = pd.DataFrame(columns=df_map_names.keys())

        df_sampled = pd.DataFrame()

        if len(df) < 50:
            df_sampled = df.copy().reset_index(drop=True)
        else:
            df_sampled = df.sample(n = 50).reset_index(drop=True)

        getCorrectColumns()
        createNewDf()
        datetimeToDate()
        correctNames()

        newDf = newDf_names.join(newDf)
        #print(newDf)
        #print(newDf.head())

        return newDf.to_json(orient='records')

    except:
        return 'Error'
