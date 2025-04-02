# Overall goals of this project
## Streamline data collection from the multiple sources I am currently using to track, plan and acheive certain fitness goals.
## Data extrapolation to find representitive body statistics
## Thus we have the data to consistently find a tailored changing TDEE and BMR
    - Even if some calculations are not specifically correct.
## Reduce personal cognitive load by automating this process
# Modules

MFP Web scraping tool \
_Create a scrpit that scraps my a food diary from MFP's printable diary report._
* Pyhton Scrapy and SCrapyselinium did not work. Possible causes are dynamically loaded pages.
    * Using Selenium seems to circumvent this issue.
* Need auth and login cookies from actual browser so there is no need for a login check. browser_cookie3 Issues#180,#210 
    * Using firefox with its repsective driver _GeckoDriver_, as a work around.  

Google sheets intergration \
_Create a script to edit/ create a google sheet. That coalesces all the data that I gather._
* This needs to handle, input depending on date, google sheet functions and creating a new sheet once one _"Mesocycle"_ (phase) has finished.  
    * **Possible Solutions:**
        * Python: Gspread, google cloud project
        * Directly creating google sheets api scripts
    * **Further options**
        * add in scripts for data visualisation on a gsheet document tree.

Google fit/Health connect/ Other health app (undecided) \
 _Pull exercise data from the exsisting tools used_ 
* Have not yet decided which platfrom to extract data from. \
    **Current Options** 
    * Health Sync: It creates a CSV document that is uploaded to google drive daily. It is well annotated and does have some older data accessible.
    * Health connect/Google Fit: Unsure on which API google is currently supporting. This seems 

### Pulling data from MFP
As mfp loads content dynamically, and does its best to block web scraping. We can use Selenium with emulates an actual browser. \

By passing session and login status using browser_cookie3, we do not need to set-up login credentials within our script.
- Current behaviour:
    - Created a selenium mfp.com class
    - uses a Selenium driver for functionality 
    - Create start date(optional) end date
    - Pass username, end date and start date
    - Returns a dicitonary with dates as the keys and macro nutrient information as the values

- Potential additions:
    - Handling login
    - Not quitting after one query
    - breaking up bigger date queries
    - packaging queries into week long dictionaries
    - create logger class as a subclas of selenium driver?

### Adding exercise data from health sync?   
Health Sync is a syncing app created for huawei smart devices. \
Both Health sync and health connect have access to daily step count from my step tracker. \
 \
Currently health sync is creating a .csv document daily with step counts, hr in seperate drive folders
- Options:
    - Daily downloads of the CSV to summate step count and calculate calories burned
    - Try to gain access to health connect api 
    - Syncing to google fit and then using google fit api for data.

### Adding data and managing data in google drive/sheets

We want to manipulate and visualise data on a google sheets document for tracking and clarification

