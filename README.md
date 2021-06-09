# Spider Tutorial

Before any spiders can be run, Scrapy must be installed in the environment. After cloning the repository, follow these steps for each scrapy project to gather the data.

### The case_info Project

The two spiders that scrape the codes used in the Virginia Case Information System can be run with "scrapy crawl" in the terminal. Make sure to be in the right folder (/State-Sentencing-Project/Web_Scraping/case_info), then write "scrapy crawl {spider name} -o {ouput file name}.csv". However it's probably better to just use the codes already in the repository since the csv files have already been edited for later use.

The spider used to actually get the case information is run from a script instead of "scrapy crawl". In the terminal, navigate to the folder containing the `run_spiders.py` file (.../case_info/case_info), then run the script like normal with the command "python run_spiders.py" or "python3 run_spiders.py" depending on how many versions of python are installed. 

![run case spiders](images/run_spiders.PNG)

One spider for each circuit court will be created, so at the beginning, 119 spiders should be running concurrently, but the smaller courts will finish much faster and close on their own. As each spider runs, it will be yielding data to its own csv file for 119 csv files in total. Once all the courts are done, which will probably takes about 2 weeks, run the `case_matcher.py` script located in the CSV Processing folder to format the cases and create a database file.

### The judgescraper Project

The spiders in the judgescraper project can be run with "scrapy crawl" as seen below. 

![run judge spiders](images/scrapy_crawl.PNG)

The "judges" spider will get judges for most of the courts, and the "judges_missing" spider will get the remaining ~20 courts that were missing. Once the two spiders are done running, `process_judges.py` will convert the judge names into their IDs and combine the separate list from each spider into one judges.csv file.

# Demo

The database file is too large to actually include in this repository, so here's a quick demo using it instead.

```python
import sqlite3 
import seaborn as sns 
import pandas as pd
```
```python
conn = sqlite3.connect("cases.db")
cursor = conn.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type = 'table'")

#will print out the variable names in the database
for result in cursor.fetchall():
    print(result[0])
```

    CREATE TABLE "final_cases" (
    "Case Number" TEXT,
      "Court" TEXT,
      "Last Hearing Date" TEXT,
      "Charge" TEXT,
      "Case Type" TEXT,
      "Charge Class" TEXT,
      "Charge Code Section" TEXT,
      "Concluded By" TEXT,
      "Sentence Y" REAL,
      "Sentence M" REAL,
      "Sentence D" REAL,
      "Probation Type" TEXT,
      "Probation Y" REAL,
      "Probation M" REAL,
      "Probation D" REAL,
      "Race" TEXT,
      "Gender" TEXT,
      "Judge" TEXT,
      "Year" INTEGER,
      "Judge Full Name" TEXT
    )
    
This is the complete list of variables that are included in the database. For this graphing demo, the only three columns needed will be the Case Number to identify each case, the Race of the defendant, and the Year of the final hearing associated with the case. The Chesterfield County Circuit Court is used as the example since it's the last circuit that completely finished scraping as of 6/8.
```python
s = """
SELECT `case number`, race, year 
FROM final_cases
WHERE court = 'Chesterfield'
"""
chester = pd.read_sql_query(s, conn)
chester.shape
```
    (100241, 3)

Chesterfield is currently the court with the third most cases included in the database, which has about 2,400,000 cases in total. However this is not the actual amount of cases in Virginia in the online system because only cases concluding in some type of sentence were included.

This function will plot the amount of cases over time for one court, separated by the race of the defendant.
```python
def data_visualizer(df):
    #A new dataframe with the number of cases with the defendant of a particular race every year
    df = df.groupby(["Race","Year"]).count()["Case Number"]
    df = df.reset_index()
    df = df.rename(columns={"Case Number": "Number of Cases"})
    sns.set_theme(style="darkgrid")
    #Plots a timeseries with separate lines for each race
    sns.lineplot(x="Year", y="Number of Cases",
                 hue="Race",
                 data=df)
    #Moves the legend outside the plot
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
data_visualizer(chester)
```

![plot](images/demo_graph.PNG)

From this graph, some trends can be found that wouldn't have been possible (at least without some extremely tedious manual searching) with the online case system. The number of sentenced cases appears to be increasing over time in Chesterfield County until dropping very recently, possibly due the closures caused by Covid-19. 

The categories on the legend are taken directly from the codes used by the website to identify each defendant's race. Some values ('R', 'X', 'S', and others not present with Chesterfield cases) didn't have any descriptions attached so it's unclear what they stand for. The codes could have been phased out over time, or the people entering the data made some typos (very possible based on some of the inputs for judge initials).
    
Finally, the database unfortunately does not include information on the demographics of the court judges since this information doesn't seem to be easily available online. However with some basic pandas tools, here are the 10 judges with the most associated cases. (Roughly, since the official website changed how they displayed full judge name over the decades, so cases with John James Smith could be split between J J Smith, John J Smith, J James Smith, and John James Smith). Google has revealed 7 of these judges to be white (with 1 unknown) and all 10 of them as male.

```python
df = pd.read_sql_query( "SELECT `case number`, `judge full name` FROM final_cases", conn)
conn.close()
top_judges = df.groupby("Judge Full Name").count()["Case Number"].sort_values(ascending=False).reset_index()
top_judges.rename(columns = {"Case Number":"Number of Cases"}).head(10)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Judge Full Name</th>
      <th>Number of Cases</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>David Victor Williams</td>
      <td>27985</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Timothy J Hauler</td>
      <td>21274</td>
    </tr>
    <tr>
      <th>2</th>
      <td>J E Wetsel</td>
      <td>20679</td>
    </tr>
    <tr>
      <th>3</th>
      <td>John C Kilgore</td>
      <td>19839</td>
    </tr>
    <tr>
      <th>4</th>
      <td>L A Harris</td>
      <td>19393</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Johnny E Morrison</td>
      <td>17784</td>
    </tr>
    <tr>
      <th>6</th>
      <td>G A Hicks</td>
      <td>17722</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Frederick Gore Rockwell</td>
      <td>16918</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Michael Lee Moore</td>
      <td>16846</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Leslie M Osborn</td>
      <td>16669</td>
    </tr>
  </tbody>
</table>
</div>

