import pandas as pd
import urllib.request
import warnings
warnings.filterwarnings('ignore')

#read in courts and judges
court_list = pd.read_csv("https://raw.githubusercontent.com/christinegu27/State-Sentencing-Project/main/CSV%20Processing/courts.csv")
judges = pd.read_csv("https://raw.githubusercontent.com/christinegu27/State-Sentencing-Project/main/CSV%20Processing/judges.csv")
#dictionary for replacing the court id with the court name
court_code = dict(court_list[["Court ID", "Court Name"]].values)

#Replace codes in the dataframe with their actual meaning
#Ex. replace "W" with "White" for defendant race
def map_values(df):
    
    df = df.rename(columns = {'Charge Code':'Case Type'})#renamed for clarity
    #Fill in NaN values 
    df['Race'] = df['Race'].fillna("U")
    df['Sentence Y'] = df['Sentence Y'].fillna(0)
    df['Sentence M'] = df['Sentence M'].fillna(0)
    df['Sentence D'] = df['Sentence D'].fillna(0)
    df['Probation D'] = df['Probation D'].fillna(0)
    df['Probation Y'] = df['Probation Y'].fillna(0)
    df['Probation M'] = df['Probation M'].fillna(0)
    df["Charge Class"] = df['Charge Class'].fillna("Un")
    df['Judge'] = df['Judge'].fillna("N/A") 
    #Opens the csv containing the codes
    f = open(r"/Users/hinaljajal/Downloads/State-Sentencing-Project/CSV Processing/edited_codes.csv")
#     f = open(r"C:\Users\chris\Documents\GitHub\State-Sentencing-Project\CSV Processing\edited_codes.csv")
    for line in f:
        line = line.strip('\n')
        #Returns a list with the first element being the first column's entry and so on
        line = line.split(",")
        #Replaces each code (stored in first entry) with its meaning (in second entry) for each column (stored in third entry)
        df = df.replace({line[2]:{line[0]:line[1]}})
    f.close()
    
    return df

def case_matcher(cases, judges_court):
    """
    Matches each case with its respective judge if known/found according to the judges' initials
    Parameters:
    cases (dataframe): a dataframe of cases for 1 specifc court
    judges_court(dataframe): judges' full names, initials, and year for specific court
    Returns:
    cases(dataframe): dataframe of cases with matched judges
    """
    cases["Year"]=cases["Last Hearing Date"].str[-4:]

    #Merges the columns by the judge and the hearing year
    cases['Year']=cases['Year'].astype(int)
    
    judges_court = judges_court.drop(['Year', 'Court Name'], axis = 1)
    judges_court = judges_court.drop_duplicates(subset = ['Judge'])

    cases = cases.merge(judges_court, how="left", on = ["Judge"])
    
    #dropping the name and second court name column
    cases=cases.drop(['Name'], axis=1)
        
    return cases

import sqlite3
conn = sqlite3.connect("cases.db") # create a database in current directory called cases.db
separate_court_data = []
for court in court_list["Court ID"]:
#     data = pd.read_csv(f"C:/Users/chris/Documents/case data/finished courts 6.7.9.15/{court}.csv")
    data = pd.read_csv(f"/Users/hinaljajal/all_cases_2017-2019/{court}.csv")
    data = map_values(data)
    #Slices the judges for the particular court 
    judges_court = judges[judges["Court Name"]==court_code[court]]
    #replace court code with name, ie "001C" with "Accomack"
    data["Court"] = court_code[court]
    data = case_matcher(data, judges_court)
    data.to_sql("final_cases", conn, if_exists = "append", chunksize = 100000, index = False)
    separate_court_data.append(data) #add to list for concatenation
    
final_cases = pd.concat(separate_court_data, ignore_index = True)
conn.close()

import sqlite3
conn = sqlite3.connect("cases.db")# create a database in current directory called cases.db
final_cases.to_sql("final_cases", conn, if_exists = "replace",index = False)
conn.close()


final_cases["Judge Full Name"].isna().mean() #0.3043542749138131


# This means that we were able to match judges for 70% of the cases, which is great! We could improve this accuracy by looking into the inconsistencies in how some courts record their judges' initials.


file_name = '/Users/hinaljajal/final_cases_2017-19.csv'
final_cases.to_csv(file_name, index = False)

