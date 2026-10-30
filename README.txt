# Harvard Art Museums ETL and Data Analysis Project

## Project Overview
This project uses the Harvard Art Museums API to collect art-related data, validate the extracted records, store the data in Microsoft SQL Server, and analyze it using SQL queries.

## Technologies Used
- Python
- Jupyter Notebook
- Harvard Art Museums API
- Microsoft SQL Server
- pyodbc
- Streamlit

##Project Workflow

- Extract artwork data using the Harvard Art Museums API.

- Clean and preprocess the extracted data.

- Connect Python with SQL Server.

- Create database tables and store the processed data.

- Perform SQL-based data analysis.

- Develop an interactive Streamlit dashboard to display results.


## Database
The project stores data in three SQL Server tables for artifact metadata,media information, and colors.

##Dashboard

The Streamlit dashboard allows users to explore artwork information using classification fliters and SQL-based results.

Project Files 
- 'Harvard_Project.ipynb' - Contains API extraction, record validation, SQL table creation, data insertion, and analysis.
- 'app.py' — Contains the Streamlit dashboard and SQL query results.


## How to Run
1. Open PowerShell in the project folder.
2. Run 'streamlit run app.py'.
3. Open the local URL displayed in PowerShell.
4. Explore the dashboard and its SQL analysis results.

## Notes
- The data is already loaded into SQL Server.
- The Jupyter Notebook contains the original ETL and analysis workflow.
- Keep API keys and database credentials private.