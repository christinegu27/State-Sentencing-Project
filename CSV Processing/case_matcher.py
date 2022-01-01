import pandas as pd
import urllib.request
import warnings
warnings.filterwarnings('ignore')

#read in courts and judges
court_list = pd.read_csv("https://raw.githubusercontent.com/christinegu27/State-Sentencing-Project/main/CSV%20Processing/courts.csv",dtype={'Court Code': 'str'})
judges = pd.read_csv("https://raw.githubusercontent.com/christinegu27/State-Sentencing-Project/main/CSV%20Processing/judges.csv")
#dictionary for replacing the court id with the court name
court_code = dict(court_list[["Court Code", "Court Name"]].values)

#Replace codes in the dataframe with their actual meaning
#Ex. replace "W" with "White" for defendant race
def map_values(df):
    
    df = df.rename(columns = {'charge_code':'case_type'})#renamed for clarity
    #Fill in NaN values 
    df['race'] = df['race'].fillna("U")
    df['sentence_y'] = df['sentence_y'].fillna(0)
    df['sentence_m'] = df['sentence_m'].fillna(0)
    df['sentence_d'] = df['sentence_d'].fillna(0)
    df['probation_d'] = df['probation_d'].fillna(0)
    df['probation_y'] = df['probation_y'].fillna(0)
    df['probation_m'] = df['probation_m'].fillna(0)
    df["charge_class"] = df['charge_class'].fillna("U")
    df['Judge'] = df['judge'].fillna("N/A") 
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
    cases["year"]=cases["last_hearing_date"].str[-4:]

    #Merges the columns by the judge and the hearing year
    cases['year']=cases['year'].astype(int)
    
    judges_court = judges_court.drop(['Year', 'Court Name'], axis = 1)
    judges_court = judges_court.drop_duplicates(subset = ['Judge'])

    cases = cases.merge(judges_court, how="left", on = ["Judge"])
    
    #dropping the name and second court name column
    cases=cases.drop(['name'], axis=1)
        
    return cases

#import sqlite3
#conn = sqlite3.connect("cases.db") # create a database in current directory called cases.db
separate_court_data = []
#courts_ = ['001']
for court in court_list["Court Code"]:
#for court in courts_:
   # data = pd.read_csv(f"C:/Users/chris/Documents/case data/finished courts 6.7.9.15/{court}.csv",dtype={'court': 'str'})
    data = pd.read_csv(f"/Users/hinaljajal/all_cases_2017-2019/{court}.csv",dtype={'court': 'str'})
    data = map_values(data)
    #Slices the judges for the particular court 
    judges_court = judges[judges["Court Name"]==court_code[court]]
    #replace court code with name, ie "001C" with "Accomack"
    data["court"] = court_code[court]
    data = case_matcher(data, judges_court)
   #data.to_sql("final_cases", conn, if_exists = "append", chunksize = 100000, index = False)
    separate_court_data.append(data) #add to list for concatenation
    
final_cases = pd.concat(separate_court_data, ignore_index = True)
#conn.close()

#import sqlite3
#conn = sqlite3.connect("cases.db")# create a database in current directory called cases.db
#final_cases.to_sql("final_cases", conn, if_exists = "replace",index = False)
#conn.close()


final_cases["Judge Full Name"].isna().mean() #0.3043542749138131


# This means that we were able to match judges for 70% of the cases, which is great! We could improve this accuracy by looking into the inconsistencies in how some courts record their judges' initials.


file_name = '/Users/hinaljajal/final_cases_2017-19.csv'
final_cases.to_csv(file_name, index = False)

