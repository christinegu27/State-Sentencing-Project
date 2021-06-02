# Spider Tutorial

After cloning the repository, follow these steps for each scrapy project to gather the data.

### The case_info Project

The two spiders that scrape the codes from the Case System can be run normally using `scrapy crawl`, but it's probably better to get the two csv files (courts.csv and detail_codes.csv) directly from the repository since those have already been cleaned up.

The spider used to actually get the case information is run from a script instead of the terminal. In the terminal, navigate to the folder containing the `run_spiders.py` file (/State-Sentencing-Project/Web_Scraping/case_info/case_info/), then run the script like normal with the command "python run_spiders.py" or "python3 run_spiders.py" depending on how many versions of python are installed. One spider for each circuit court will be created, so at the beginning, 119 spiders should be running concurrently, but the smaller courts will finish much faster and close on their own. As each spider runs, it will be yielding data to its own csv file for 119 csv files in total.

### The judgescraper Project


# demo