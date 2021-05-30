## State Sentencing Project: Methodology

##### Data Sources:

The first step in creating a single source containing the cases’ information was identifying sources where we can get this information from. Virginia’s judicial system provides access to a statewide case search portal for cases in general district courts and select circuit courts. We scraped the cases from this portal to create our database. The Virginia Judiciary Online Case Information System is linked here. This portal only had the judges’ initials for the cases and so, we got information about all of Virginia’s circuit court judges from this website. The website only had information about current judges. So, we used WayBack Machine to get the archives from previous years for this website, from which we scraped the judges’ full names for all years from 2005-2021.

##### What does the database include? 
- Demographics of the defendant (when available): age, gender, race 
- Last hearing date
- Name of circuit court 
- Information about the charge: charge code, charge code section, and charge class
- Information about the probation (if applicable): probation type, probation length
- Length of the sentence
- Probation in months
- Judge’s full name and initials (when available)

##### How did we scrape the data?


###### Case information:
First, the terms and conditions are accepted by directing to the link where they are already accepted. Since it is a search portal, we had to send search requests to get all the possible cases. The minimum requirement for a search was two letters. So we send a search request for every possible 2 letter permutation, which returns cases where the first, middle, and/or last name start(s) with the search string given. If there are too many cases for a particular permutation, another letter is added to the search string to limit the results. After getting the search results, we send a request for the case details for each case in the results. Each case has a JSON file which contains this information. Then, we yield the relevant information to a dictionary. 
###### Judges’ information: 
To match the judges’ initials with their full names, we scraped the list of judges for each circuit court in Virginia. This website contains the webpages for each circuit court, which in turn contain that court’s judges for the ongoing year. So, the scraper would loop through the courts and then get all the judge names for each year. 

##### How did we process the data?

###### Converting names to initials: 

We compared the names and the initials to determine a pattern in the determination of initials. No roman numerals in suffixes were used in initials so we removed these. Names like J O’Brian would become JO so we dropped the apostrophe as well. 

###### Matching the cases: 

The matching is done for each court at a time so that it’s easier to match the judges. Since there might be multiple judges with the same initials, we also match the cases according to the year in which the last hearing date was and the year in which the judge was active. 

















