# State Sentencing Project Pitch

### Abstract
With the rise of social justice movements focusing on racial discrimination, attention has been cast on the criminal justice system, where non-white defendants may receive harsher punishments compared to their white counterparts. Unfortunately, there is no single resource containing the information needed to verify this claim at the state-level, where most of the sentencing takes place in the United States. The goal of this project is to gather data from various web sources and consolidate them into one, publicly available dataset detailing court records on the crime, judge, and the demographic information of both the defendant and the judge for a given state.

### Planned Deliverables
The main deliverable of this project will be the completed database of criminal sentencing information for a state (almost definitely Virginia). In this database, each court case will have a record for the convicted crime and associated sentence, the name of the sentencing judge, and demographic data (primarily the ethnicity and gender) of the defendant and judge. Once the data is compiled, it will be organized and presented online to be easily accessible to the public. Creating a database with the information outlined above is the ideal plan, but it is very possible that some of the desired data is not available online. If this is the case, a singular database of records will still be published, but it may be missing court cases, judge identities, or demographic information for the individuals involved.

Regardless of full or partial success, the database will be accompanied by brief report detailing the methodology used during the compilation process. This will explain the various sources where data was collected, as well as the assumptions made and reasoning behind linking together different datasets. The document will also provide a guide on how to navigate through the database to access the data (using basic Python tools).

A final, perhaps less important, goal of ours is to create interactive and interesting data visualizations for people to view and understand the data (similar to the interactive data visualizer that JUSTFAIR had). 

### Resources Required
We expect to be working a lot with web scraping tools such as scrapy. We also want to be cautious about this and not scrape the websites too quickly to avoid being banned, so we might phase the web scraping. 

As for actually dealing with the database, which we will probably do at a later stage, the tools pandas and sqlite are likely to be very helpful. 

As mentioned earlier, one of our goals is also to create interactive data visualizations at the end, but we need to do more research on this. Some tools we’re aware of for creating interactive visualizations include Plotly express, Tableau and JavaScript so we might have to use these.

The main resource that we require is sufficient data. We need a website/a couple of websites where we can get data about the state’s criminal records. Some examples are: https://public.courts.in.gov/mycase/#/vw/Search or https://dw.courts.wa.gov/?fa=home.namesearchTerms. These are freely available but not every state has such a portal, and even those that do have inconsistencies in the stored data. However, we are going to be working on one state -- at least to begin with -- so the inconsistencies shouldn’t be an issue. Our goal is to include data about the demographics of the defendants as well as the judges so we are also looking for ways to gather data about the judges and their biographical information. 
 
The states that we have found to be promising in terms of their data as of now include Virginia  (race, gender, and age for most defendants), Kentucky (race, gender, and age for some defendants), and Minnesota (gender and age). 

Because we tried to search many random states, here are our notes on some states’ data availability:

<details>
  <summary>Expand State notes</summary>
   
   California - not likely: must request record instead of openly access on internet

   Indiana/Oregon/Idaho - does have a search portal but no demographics information

   Washington - does not show court sentencing outcome online

   Alabama - unable to access records

   Florida - no statewide portal. Some counties have info on demographics too

   Pennsylvania - statewide portal is there and contains demographic information for some defendants as well. However, the information is in PDF form 

   Virginia - there is a statewide portal and most, if not all, defendants have demographic information. Just one issue: no judge name (https://eapps.courts.state.va.us/ocis/landing/false) 
   (http://ewsocis1.courts.state.va.us/CJISWeb/Logoff.do)

   Kentucky - statewide portal exists and some defendants have demographic info too. 

   New York - portal exists but no demographic information on defendants. 

   Mississippi - portal for Supreme court cases

   Maine - online portal but no demographic information

   Colorado - no statewide portal - must request individual county

   Arkansas - statewide portal exists, but not all district courts upload their information

   Nevada - online portal for Supreme Court and appeals only - does not contain demographic info or judge

   Arizona - online portal with information for 177 out of 184 courts. Does not have demographic info or judge

   Utah - Appellate cases' information available

   New Mexico - statewide portal exists, but is difficult to search through (requires name/DOB or exact case number)

   Michigan - portal but no demographic information

   Georgia - must register an account to access

   Tennessee - portal exists with judge but no demographic information

   West Virginia -  judges have biographies including pictures for the most part, still looking for court records

   South Carolina - search portal by county, scraping is explicitly banned

   North Carolina - no online portal available

   Maryland - sitewide portal with demographic information and charge, but no sentence or judge

   Delaware - sitewide portal with judge but not demographic information

   New Hampshire - no statewide portal

   Connecticut - sitewide portal very easy to navigate, but lacks demographic information and judge 

   New Jersey - exists, but requires specific searches and a recaptcha

   Rhode Island- sitewide portal with judge but not demographic information

   Ohio - no statewide portal

   Illinois - no statewide portal, some limited courts available but lack demographic information and judge
</details>

### Tools/Skills Required

We expect to be working a lot with web scraping tools such as scrapy. We also want to be cautious about this and not scrape the websites too quickly to avoid being banned, so we might phase the web scraping. 

As for actually dealing with the database, which we will probably do at a later stage, the tools pandas and sqlite are likely to be very helpful. 

As mentioned earlier, one of our goals is also to create interactive data visualizations at the end, but we need to do more research on this. Some tools we’re aware of for creating interactive visualizations include Plotly express, Tableau and JavaScript so we might have to use these.

### Risks
 Some states are more transparent than others when publishing their public court records. While we will be researching the data available for multiple states, it is possible that there is incomplete data, or even just data that is incompatible with web-scraping, for the state that will eventually be selected. This will lead to a “partial success” project detailed above. Since we will be managing and joining data from multiple sources that are very different from one another, it is also possible that we will be unable to merge them together.

### Ethics
The main problem we can foresee with our project is its potential use for political gain. The concern is that our project will be used to present misleading information and draw incorrect conclusions that will harm marginalized communities. With the current style of news sharing -- namely through clickbaity titles and shocking stories -- media companies or politicians may find the database, manipulate the data in a way that furthers their political biases, then present their findings online/on air as the absolute facts without nuance or full transparency. Another concern of ours is that some states have data about demographics only about some defendants; could this be because of potential bias and/or could it lead to potential inaccuracy and bias in our results? Virginia is our top option primarily for this reason -- because it contains demographic information about most defendants.

### Tentative Timeline

Week 4: A concrete decision on a state and consolidating (links to) resources, begin web scraping. (This is what we had originally planned, but we have pretty much decided our state now -- Virginia. So, we’re hoping to get started web scraping very soon!)

Week 6: Finish web scraping of crime records (including defendants’ demographics), possibly get information on judges, either personal or aggregate statistics. Should have by this time: somewhat readable/organized CSV file of court records.

Week 8: Compiled dataset of sentencing information with connections to have available for writing reports.

What we have achieved till now: We have done our preliminary research, which includes reading JUSTFAIR’s paper and their methodology, checking and searching for states that have usable data, and are currently trying to learn about potential web scraping tools we can use to scrape search portals. 
