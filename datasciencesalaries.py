import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import country_converter as coco

theme_colors = ['#FF1654', '#20A4F3', '#14A073', '#F9C846', '#4C5760']
df = pd.read_csv('E:\\School\\DataScience\\DataScienceSalaries\\ds_salaries_worklevel.csv')

# Remove all values greater then 599000
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df = df[df['salary_in_usd'] < 599000]
#df.info()

# Replaced values in array
df['remote_ratio'] = df['remote_ratio'].astype('str')
df['remote_ratio'] = df['remote_ratio'].replace(['0'],'On Site')
df['remote_ratio'] = df['remote_ratio'].replace(['50'],'Hybrid')
df['remote_ratio'] = df['remote_ratio'].replace(['100'],'Remote')
print(df['remote_ratio'].value_counts())

# Grouping specific columns
experience_level_df = df.groupby(['experience_level']).size().reset_index().rename(columns={0: 'count'})
company_size_df = df.groupby(['company_size']).size().reset_index().rename(columns={0: 'count'})
work_year_df = df.groupby(['work_year']).size().reset_index().rename(columns={0: 'count'})
remote_ratio_df = df.groupby(['remote_ratio']).size().reset_index().rename(columns={0: 'count'})

fig = make_subplots(rows=2, cols=2,
                    specs=[[{'type':'domain'}, {'type':'domain'}],
                           [{'type':'domain'}, {'type':'domain'}]
                          ])

## Experience Level Donut Chart
fig.add_trace(
    go.Pie(
        labels=experience_level_df['experience_level'],
        values=experience_level_df['count'],
        hole=.6,
        title='Experience',
        titlefont={'color':None, 'size': 24},
        ),
    row=1,col=1
    )

## Company Size Donut Chart
fig.add_trace(
    go.Pie(
        labels=company_size_df['company_size'],
        values=company_size_df['count'],
        hole=.6,
        title='Company Size',
        titlefont={'color':None, 'size': 24},       
        ),
    row=1,col=2
    )

## Work Year Donut Chart
fig.add_trace(
    go.Pie(
        labels=work_year_df['work_year'],
        values=work_year_df['count'],
        hole=.6,
        title='Work Year',
        titlefont={'color':None, 'size': 24},
        ),
    row=2,col=1
    )


## Remote Ratio Donut Chart
fig.add_trace(
    go.Pie(
        labels=remote_ratio_df['remote_ratio'],
        values=remote_ratio_df['count'],
        hole=.6,
        title='Remote Ratio',
        titlefont={'color':None, 'size': 24},
        ),
    row=2,col=2
    )
fig.update_traces(
    hoverinfo='label+value',
    textinfo='label+percent',
    textfont_size=12,
    marker=dict(
        colors=theme_colors,
        line=dict(color='#EEEEEE',
                  width=2)
        )
    )

# Layout for donut chart  
fig.layout.update(title="<b> Categorical Features Donut Charts <b>",
                  titlefont={'color':None, 'size': 28, 'family': 'Courier New'},
                  showlegend=False, 
                  height=800, 
                  width=800,
                  template='plotly_dark',
                  title_x=0.5
                  )
fig.show()


usa_df = df[df['company_location'] == 'US']

# Creates box and whisker chart  
fig=make_subplots(rows=3,cols=1,subplot_titles=('<i>World Salaries', '<i>US Salaries'))
fig.add_trace(go.Histogram(x=df['salary_in_usd'],name='World'),row=1,col=1)
fig.add_trace(go.Histogram(x=usa_df['salary_in_usd'],name='US'),row=2,col=1)
fig.update_layout(height=600, width=800, title_text='<b>Salary Comparison', font_size=20)
fig.update_layout(template='plotly_dark', title_x=0.5, font_family='Courier New', showlegend=False)
fig=make_subplots(rows=4,cols=1,subplot_titles=('<i>Experience Level', '<i>Remote Ratio', '<i>Company Size', '<i>Year'))
fig.add_trace(go.Box(x=df['experience_level'] ,y=df['salary_in_usd'], boxpoints='all'),row=1,col=1)
fig.add_trace(go.Box(x=df['remote_ratio'] ,y=df['salary_in_usd'], boxpoints='all'),row=2,col=1)
fig.add_trace(go.Box(x=df['company_size'] ,y=df['salary_in_usd'], boxpoints='all'),row=3,col=1)
fig.add_trace(go.Box(x=df['work_year'] ,y=df['salary_in_usd'], boxpoints='all'),row=4,col=1)
fig.update_layout(height=1000, width=800, title_text='<b>Salaries WRT', font_size=20)
fig.update_layout(template='plotly_dark', title_x=0.5, font_family='Courier New', showlegend=False)

job_title_list = ['Data Scientist', 'Data Engineer', 'Data Analyst', 'Machine Learning Engineer',
                 'Research Scientist', 'Data Science Manager', 'Data Architect', 'Big Data Engineer']
temp_job_df = df[df['job_title'].isin(job_title_list)]
fig = px.box(temp_job_df, x="job_title", y="salary_in_usd", color="job_title",
             notched=True, points='all',

             title="Salaries as per Job Title",
             hover_data=["job_title"], template='plotly_dark'
            )
fig.show()

# Create box whisker chart 
location_list = ['United States', 'Great Britain', 'Canada', 'Germany', 'India', 'France', 'Spain', 'Greece']
df = df.replace({
    'US':'United States',
    'FR':'France',
    'IN':'India',
    'DE':'Germany',
    'GB':'Great Britain',
    'ES':'Spain',
    'CA':'Canada',
    'GR':'Greece'
})
temp_location_df = df[df['company_location'].isin(location_list)]
fig = px.box(temp_location_df, x= "company_location", y="salary_in_usd", color="company_location",
             notched=True, points='all',
             title="Salaries as per Company Locations",
             hover_data=["company_location"], template='plotly_dark'
            )
fig.show()

# Map for company locations
country_names = coco.convert(names=df['company_location'], to="ISO3")
df['company_location'] = country_names
salary_location_df = df.groupby(['salary_in_usd', 'company_location']).size().reset_index()
average_salary = salary_location_df.groupby('company_location').mean().reset_index()
fig = px.choropleth(locations=average_salary['company_location'],
                    color=average_salary['salary_in_usd'],
                    color_continuous_scale=px.colors.sequential.RdBu,
                    template='plotly_dark')
fig.update_layout(font = dict(size=17,family="Courier new"))
fig.update_layout(
    title="Average Salary by Company Location", title_x=0.5,
    font=dict(
        family="Rubik",
        size=18
    )
)
fig.show()

# Bar graph for Experience vs salary------------------------------------------------
avgEN = df.groupby('experience_level').mean().loc['EN', 'salary_in_usd']
avgMI = df.groupby('experience_level').mean().loc['MI', 'salary_in_usd']
avgSE = df.groupby('experience_level').mean().loc['SE', 'salary_in_usd']
avgEX = df.groupby('experience_level').mean().loc['EX', 'salary_in_usd']
data = {'EN':avgEN, 'MI':avgMI, 'SE':avgSE, 'EX':avgEX}
courses = list(data.keys())
values = list(data.values())  
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(courses, values, color ='blue', width = 0.4)
plt.xlabel("Level of Experience")
plt.ylabel("Salary in USD")
plt.title("Experience vs Salary")
plt.show()

# Salvery verse company size Bar graph --------------------------------------
avgSm = df.groupby('company_size').mean().loc['S', 'salary_in_usd']
avgMed = df.groupby('company_size').mean().loc['M', 'salary_in_usd']
avgLg = df.groupby('company_size').mean().loc['L', 'salary_in_usd']
data = {'Small':avgSm, 'Medium':avgMed, 'Large':avgLg}
courses = list(data.keys())
values = list(data.values())  
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(courses, values, color ='blue', width = 0.4) 
plt.xlabel("Company Size")
plt.ylabel("Salary in USD")
plt.title("Company Size vs Salary")
plt.show()


# Salary verse remote work status-------------------------------------
avgNone = df.groupby('remote_ratio').mean().loc['On Site', 'salary_in_usd']
avgPartial = df.groupby('remote_ratio').mean().loc['Hybrid', 'salary_in_usd']
avgFull = df.groupby('remote_ratio').mean().loc['Remote', 'salary_in_usd']
data = {'On Site':avgNone, 'Hybrid':avgPartial, 'Remote':avgFull}
courses = list(data.keys())
values = list(data.values())
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(courses, values, color ='blue', width = 0.4)
plt.xlabel("Remote Work Status")
plt.ylabel("Salary in USD")
plt.title("Remote Work Status vs Salary")
plt.show()

# Changed job titles to 3 catagories
df = df.replace({  'ML Engineer': 'Data Engineer', 
                   'BI Data Analyst' : 'Data Analyst', 
                   'Data Analytics Engineer': 'Data Analyst', 
                   'Head of Machine Learning':'Data Engineer', 
                   'Lead Machine Learning Engineer':'Data Engineer',
                   'Staff Data Scientist':'Data Scientist',
                   'Big Data Architect':'Data Engineer',
                   'Data Analytics Lead':'Data Analyst', 
                   'Lead Data Scientist':'Data Scientist',
                   'Machine Learning Infrastructure Engineer':'Data Engineer',
                   'Data Specialist':'Data Scientist',
                   'Marketing Data Analyst':'Data Analyst',
                   'Finance Data Analyst':'Data Analyst',
                   'Financial Data Analyst':'Data Analyst',
                   'Product Data Analyst':'Data Analyst',
                   '3D Computer Vision Researcher':'Data Engineer',
                   'Computer Vision Software Engineer':'Data Engineer',
                   'NLP Engineer':'Data Engineer',
                   'Applied Machine Learning Scientist': 'Data Scientist', 
                   'ETL Developer':'Data Engineer',
                   'Principal Data Analyst':'Data Analyst',
                   'Data Science Consultant':'Data Analyst',
                   'Research Scientist':'Data Scientist',
                   'Business Data Analyst':'Data Analyst',
                   'Big Data Engineer':'Data Engineer',
                   'Machine Learning Engineer':'Data Engineer',
                   'AI Scientist':'Data Scientist',
                   'Machine Learning Scientist':'Data Scientist',
                   'Applied Data Scientist':'Data Scientist',
                   'Machine Learning Engineer':'Data Engineer',
                   'Machine Learning Developer':'Data Engineer',
                   'Computer Vision Engineer':'Data Engineer',
                   'Business Data Analyst':'Data Analyst',
                   'Lead Data Analyst':'Data Analyst',
                   'Lead Data Engineer':'Data Engineer',
                   'Cloud Data Engineer':'Data Engineer',
                   'Principal Data Scientist':'Data Scientist',
                   'Head of Data Science':'Data Scientist',
                   'Data Science Manager':'Data Scientist',
                   'Director of Data Engineering':'Data Engineer',
                   'Principal Data Engineer':'Data Engineer',
                   'Data Engineering Manager':'Data Engineer',
                   'Director of Data Science':'Data Scientist',
                   'Data Science Engineer':'Data Engineer',
                   'Data Analytics Manager':'Data Analyst',
                   'Head of Data':'Data Analyst',
                   'Data Architect':'Data Engineer',
                   'Analytics Engineer':'Data Engineer',
                   'Machine Learning Manager':'Data Engineer'
                })

# Created a csv file to make text file 
df.to_csv('basic_info.csv')
with open('basic_info.csv', 'r') as f_in, open('sample.txt', 'w') as f_out:
    # 2. Read the CSV file and store in variable
    content = f_in.read()
    # 3. Write the content into the TXT file
    f_out.write(content)

# Bar graph for Job_Title vs Salary
# Get the mean for the three job titles in our file
DS = df.groupby('job_title').mean().loc['Data Scientist', 'salary_in_usd']
DE = df.groupby('job_title').mean().loc['Data Engineer', 'salary_in_usd']
DA = df.groupby('job_title').mean().loc['Data Analyst', 'salary_in_usd']
data = {'Data Scientist':DS, 'Data Engineer':DE, 'Data Analyst':DA}
courses = list(data.keys())
values = list(data.values())
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(courses, values, color ='blue', width = 0.4)
plt.xlabel("Job Title")
plt.ylabel("Salary in USD")
plt.title("Job Title VS Salary")
plt.show()

# pinpointing large comanpies in the United States 
USA_df = df[df['company_location'] == "USA"]
lgUSA_df = df[df['company_size'] == "L"]

# Getting the mean for each work year
avgUS20 = lgUSA_df.groupby('work_year').mean().loc[2020, 'salary_in_usd']
avgUS21 = lgUSA_df.groupby('work_year').mean().loc[2021, 'salary_in_usd']
avgUS22 = lgUSA_df.groupby('work_year').mean().loc[2022, 'salary_in_usd']

# values set to be put into graph
avg = [1,2,3,4] # this represents the years on the x axis
avg2023 = 142021.39135645324 # this number was figured out by using the code in the last line of the file
avgarray = [avgUS20, avgUS21, avgUS22, avg2023] # Array of each mean for the years 2020, 2021, 2022

#These are the steps we took to solve for linear regression  
x = avg
y = avgarray
x_mean=np.mean(x) # Took the mean of x
y_mean=np.mean(y) # took the mean of y

x_num = x-x_mean # took the x values and subracted each of them to the mean
y_num = y-y_mean # took the y values and subracted each of them to the mean

m=(sum(x_num*y_num))/(sum(x_num*x_num)) # takes the sum of the values in the parentheses 
b=y_mean-(m*x_mean) # subract the y mean by the slope which is m times the x mean

x = np.linspace(1,4,4) # this is to set the line length 
y1 = m*x+b # values plugged into the formula

# This fills out the graph information and plots the scattered points with the best fit line
xAxis = ["2020", "2021","2022","2023"]
plt.plot(x, y1, '-r',label='Best Fit Line')
x = avg
plt.scatter(x, y)
plt.xticks(x, xAxis, rotation='vertical')
plt.xlabel("Work year")
plt.ylabel("Salary in USD")
plt.title('Salaries For Large Companies In US')
plt.show()

# x = 1 represents 2020 while 4 2023 for data
print("Equation------------------------------")
print(m*3+b)
print(m*4+b)