import pandas as pd

judges = pd.read_csv("https://raw.githubusercontent.com/christinegu27/State-Sentencing-Project/main/CSV%20Processing/judge_directory.csv")
# Drops n/a and duplicate entries
judges = judges.dropna()
judges = judges.drop_duplicates(subset = ["Judge"])

# Gets the title of each person (Hon, Ms, Mr, etc.)
titles = []
for x in judges["Judge"]:
    titles.append(x[0:3])
judges["Title"] = titles
# Drops all non-judge entries
judges = judges[judges["Title"]=="Hon"]

# Remove unecessry characters from judge names
judges['Judge'] =judges['Judge'].str.replace('I','')
judges['Judge'] =judges['Judge'].str.replace('II','')
judges['Judge'] =judges['Judge'].str.replace('III','')
judges['Judge'] =judges['Judge'].str.replace('IV','')
judges['Judge'] =judges['Judge'].str.replace('V','')
judges['Judge'] =judges['Judge'].str.replace('Jr.','')
judges['Judge'] =judges['Judge'].str.replace('Hon','')
judges['Judge'] =judges['Judge'].str.replace('.','')
judges['Judge'] =judges['Judge'].str.replace("'",' ')
judges['Judge'] =judges['Judge'].str.replace("-",' ')

# Creates new column of each judge's initials 
judges["Initials"]=[''.join(i[0] for i in x.split()) for x in judges['Judge']]

judges.to_csv(r'/Users/hinaljajal/Downloads/judge_initials.csv', index = False)