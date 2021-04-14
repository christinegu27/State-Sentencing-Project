# State-Sentencing-Project

hello! 

## Project Pitch

### Abstract
With the rise of social justice movements focusing on racial discrimination, attention has been cast on the criminal justice system, where non-white defendants may receive harsher punishments compared to their white counterparts. Unfortunately, there is no single resource containing the information needed to verify this claim at the state-level, where most of the sentencing takes place in the United States. The goal of this project is to gather data from various web sources and consolidate them into one, publicly available dataset detailing court records on the crime, judge, and the demographic information of both the defendant and the judge for a given state.

### Planned Deliverables
The main deliverable of this project will be the completed database of criminal sentencing information for a state (yet to be determined). In this database, each court case will have a record for the convicted crime and associated sentence, the name of the sentencing judge, and demographic data (primarily the ethnicity and gender) of the defendant and judge. Once the data is compiled, it will be organized and presented online to be easily accessible to the public. Creating a database with the information outlined above is the ideal plan, but it is possible that some of the data is not available online. If this is the case, a singular database of records will still be published, but it may be missing certain court cases or demographic information.

Regardless of full or partial success, the database will be accompanied by a report detailing the methodology used during the compilation process. This will explain the various sources where data was collected, as well as the assumptions made and reasoning behind linking together different datasets. The document will also provide a guide on how to navigate through the database to access the data (using basic Python tools?).

### Risks
 Some states are more transparent than others when publishing their public court records. While we will be researching the data available for multiple states, it is possible that there is incomplete data, or even just data that is incompatible with web-scraping, for the state that will eventually be selected. This will lead to a “partial success” project detailed above. Since we will be managing and merging data from multiple sources that are very different from one another, it is also possible that we will be unable to merge them together.


### Ethics
The main problem we can foresee with our project is its potential use for political gain. The concern is that our project will be used to present misleading information and draw incorrect conclusions that will harm marginalized communities. With the current style of news sharing -- namely through clickbaity titles and shocking stories -- media companies or politicians may find the database, manipulate the data in a way that furthers their political biases, then present their findings online/on air as the absolute facts without nuance or full transparency.
