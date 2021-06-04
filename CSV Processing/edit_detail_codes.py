import pandas as pd

#prepares the scraped detail codes to use when matching cases

codes = pd.read_csv("https://raw.githubusercontent.com/christinegu27/State-Sentencing-Project/main/CSV%20Processing/detail_codes.csv")
#renames relevant codes to match with columns of case data
codes=codes.replace({'circuitGender':'Gender',
	'circuitRace':'Race',
	'criminalCaseType':'Case Type',
	'criminalChargeClass':'Charge Class',
	'criminalConcludedBy':'Concluded By',
	'criminalProbationType':'Probation Type'})

#keeps only the relevant codes
codes = codes[(codes['Code Type'] == "Gender") |
 (codes['Code Type'] == "Race") | 
 (codes['Code Type'] == "Case Type") | 
 (codes['Code Type'] == "Charge Class")| 
 (codes['Code Type'] == "Concluded By")| 
 (codes['Code Type'] == "Probation Type")]

file_name = '/Users/hinaljajal/Downloads/edited_codes.csv'
codes.to_csv(file_name, index = False)
