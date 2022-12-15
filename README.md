# Salaries in the Data Science Field

This project shows the projected salary of employers in the data science field for large companies in the United States. A linear regression algorithm was used to calculate the projected salary in 2023 with data provided from 2020, 2021, and 2022. This data can be run on any operating system but the provided information below is based off a Windows device, which how our group processed the data.

## Requirements and Installation (windows OS)
1) Make sure python is installed on your device, you can check this by typing `python --version` in the command prompt.

2) For an accurate representation of the data pip was used, you can check this by typing `pip --version` in the command prompt.

3) Make sure all necessary imports are installed through pip.

4) Once `datasciencesalaries.py` and `ds_salaries_worklevel.csv` are downloaded to your device, you will need to change the path of the file to when you saved it. For example my path is: `E:\\School\\DataScience\\DataScienceSalaries\\ds_salaries_worklevel.csv')`

## Data Manipulation
We used multiple different methods do calculate and display the data for this report. Some of these were `.mean()` to calculate the average for the years 2020 through 2022, `.loc()` used to gather specific columns necessary for the averages, and `.replace()` to replace the titles of careers so we can properly gather data. We were able to count the number of words using map reduce in Hadoop. Hadoop was an important factor in this project. It let us know the most abundant job titles, locations, experience level, remote work status, and company size. 

## Linear Regression 
For this project it was decided best to go with the statistical route. The equation for linear regression is `Y = mX + b`. The equation to find m is `m=(sum(x_num*y_num))/(sum(x_num*x_num))` where `x_num` and `y_num` is the mean of `x` and `y`. The equation for b is `b=y_mean-(m*x_mean)`. When all the values are combined the output is the coordinates for the average salary in the data science field for the year 2023. The coordinates are `Y = 12,412.86X + 92,369.96`. 

## Resources Used
- Python
    - Readable, understandable language especially for data analysis
- Hadoop
    - Used to run the .jar file through for the wordcount map reduce
- Excel
    - Where the data is listed and then turned into a .csv file
- Visual Studio Code
    - Text editor of choice
- Kaggle
    - Informative website for data science. Where our data is from