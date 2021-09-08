# Dashboard GOV Challenge

This is a repository for Dashboard-Challenge developed with Python, [rpaframework](https://rpaframework.org/releasenotes.html).
### Features

1. **Automate the process of Scraping the** [IT-Dashboard](https://itdashboard.gov/)
2. It will scrap companies profiles and their investment in IT Technology and stores into an excel file.
3. It will goto one company profile and will scrap the Individual Investments into another excel file.
4. It will scrap the **UII** links available in the investment table data and stores in a list, then it downloads all pdfs into "**OUTPUT**" folder.
5. Can be test on [robocorp](https://cloud.robocorp.com/)
6. All downloaded PDF's and Excel sheets will be land in **output** folder
7. It will read the downloaded PDF files and get the **Section A** from each PDF then it will compare the values "Name of this Investment" with the column "Investment Title", and the value "Unique Investment Identifier (UII)" with the column "UII"
8. If **Investment Title** matches with the pdf`s **Investment Title** and "Unique Investment Identifier (UII)" with the column "UII" it adds two columns in the Investment data excel and add those pdfs names in
which Title and UII got matched

## how to setup (robocorp)

1. [rpaframework](https://rpaframework.org/releasenotes.html)

### Installation Process

1. First create a bot from here [robocorp](https://cloud.robocorp.com/taskoeneg/task/robots)
2. Add repo link in public GIT field.
3. Goto [assistants](https://cloud.robocorp.com/taskoeneg/task/assistants) and add new assistant linked with robot that you had registered above. 
4. Download and install desktop app of robocorp assistant from [there](https://cloud.robocorp.com/taskoeneg/task/assistants) by click on **Download Robocorp Assistant App**
5. Run the assistant you had created above
6. Bot will start performing the task as mentioned above
7. Your output data will be saved in output folder. click on output when task finished.






### [dashboard.py](https://github.com/Us-manArshad/it-dashboard-challenge/blob/master/dashboard.py)
- It will initialize the [ITDashboard](https://github.com/Us-manArshad/it-dashboard-challenge/blob/master/dashboard.py) object and it will call the 
functions that will perform the challenge.
- Have the logic to scrap and create the Excel file for agencies and Investment table,
- Get the uii links and download the PDF's associated with it.
- Read PDF's and compare with "Name of this Investment" with the column "Investment Title", and the value "Unique Investment Identifier (UII)" with the column "UII".

### [conda.yaml](https://github.com/Us-manArshad/it-dashboard-challenge/blob/master/conda.yaml)
Having configuration to set up the environment and [rpaframework](https://rpaframework.org/releasenotes.html) dependencies.

### [robot.yaml](https://github.com/Us-manArshad/it-dashboard-challenge/blob/master/conda.yaml)
Having configuration for robocorp to run the [conda.yaml](https://github.com/Us-manArshad/it-dashboard-challenge/blob/master/conda.yaml) and execute the task.py


You can find more details and a full explanation of the code on [Robocorp documentation](https://robocorp.com/docs/development-guide/browser/rpa-form-challenge)
