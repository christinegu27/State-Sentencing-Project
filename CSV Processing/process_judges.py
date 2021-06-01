import pandas as pd

judges_original = pd.read_csv(r"C:\Users\chris\Documents\GitHub\State-Sentencing-Project\Web Scraping\judgescraper\judges_ind.csv")
judges_missing = pd.read_csv(r"C:\Users\chris\Documents\GitHub\State-Sentencing-Project\Web Scraping\judgescraper\judges_missing.csv")

#Adds the judges from missing courts to the general file
judges = judges_original.append(judges_missing, ignore_index = True) 

#Removes roman numerals from names because they aren't used in determining initials
judges['Judge'] =judges['Judge'].str.replace('II','')
judges['Judge'] =judges['Judge'].str.replace('III','')
judges['Judge'] =judges['Judge'].str.replace('IV','')
judges['Judge'] =judges['Judge'].str.replace(' V ','')
judges['Judge'] =judges['Judge'].str.replace('Jr.','')
#Removes the title 
judges['Judge'] =judges['Judge'].str.replace('Hon. ','')
judges['Judge'] =judges['Judge'].str.replace('Hon ','')
#Removes punctuation because it isn't used 
judges['Judge'] =judges['Judge'].str.replace('.','')
judges['Judge'] =judges['Judge'].str.replace("'",'')
judges['Judge'] =judges['Judge'].str.replace("-",' ')
judges['Judge'] =judges['Judge'].str.replace("~",'')
judges['Judge'] =judges['Judge'].str.replace("*",'')
judges['Judge'] =judges['Judge'].str.replace(",",'')
#Removes mentions of chief/presiding judges
judges['Judge'] =judges['Judge'].str.replace("Chief Judge",'')
judges['Judge'] =judges['Judge'].str.replace("Presiding Judge",'')

#Finds the initials for all judges
judges["Initials"]=[''.join(i[0] for i in x.split()) for x in judges['Judge'] ]

#Rename columns for merging later on
judges = judges.rename(columns={"Judge": "Judge Full Name", "Initials": "Judge", "Court": "Court Name"})

#Format court name 
judges["Court Name"] = judges["Court Name"].apply(lambda x: x[:-14] if "Circuit Court" in x else x)

judges.to_csv(r"C:\Users\chris\Documents\GitHub\State-Sentencing-Project\CSV Processing\judges.csv", index = False)
