#See README for more
#Set up needed packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

emsi_link = 'https://www.economicmodeling.com/'

#set driver
driver = webdriver.Chrome(executable_path=r'C:\Users\Suraj.Thapa\Downloads\chromedriver\chromedriver.exe')
driver.get(emsi_link)

#Go to the required page using Selinium
about = driver.find_element_by_xpath('//nav/ul/li/div/span[contains(text(), "About")]')
about.click()
content = driver.find_element_by_xpath('//p[contains(text(), "Browse current job openings")]')
content.click()
html_page = driver.page_source

#columns for our final dataframe
columns = ['position_title', 'Position_category', 'Part_or_Full_time', 'Location', 'description', 'core_responsibilities',
           'Organizational Relationships', 'Knowledge, Skills, and Abilities', 'Key Skills', 'preferred_skills',
           'Traits','Credentials and Experience', 'application_requirements', 'optional_application_requirements',
           'Physical Requirements / Work Environment', 'link_to_apply' ]

#Aggregate similar columns
responsibilities_columns = ['Daily Responsibilities', 'Core Responsibilities', 'Responsibilities', 'Job Responsibilities',
                           'Job Duties and Responsibilities']
knowledge_columns = ['Knowledge, Skills and Abilities', 'Knowledge, Skills, and Abilities',
                    'Knowledge, Skills & Abilities', 'Knowledge, Skills, and Abilites']
key_skills_columns = ['Key Skills', 'Candidates must have', 'Qualifications', 'Basic Qualifictions',
                      'In terms of technical ability, candidates must have…', 'Requirements']
application_requirements_columns = ['Application Requirements']
optional_app_materials_columns = ['Optional Application Materials (submit if available)']
preferred_skills_columns = ['Great candidates also have', 'Preferred Qualification', 'Preferred Skills',
                            'Great candidates also have…', 'Specific Qualifications']
traits_columns = ['People who succeed in this position are', 'Traits', 'People who succeed in this position are...']
work_env_columns = ['Physical Requirment/Work Environment', 'Physical Requirements / Work Environment']

#build function to scrape
def insert_html(html_page_input):
    soup = BeautifulSoup(html_page_input)
    all_jobs = soup.find_all('div', class_='job')
    job_links = list(map(lambda x: x.a['href'], all_jobs))
    job_links = job_links[0:-1] #Getting rid of last link as it is not a job page
    #job_links = job_links[17:18]
    dataframe = pd.DataFrame()

    for links in job_links:
        #print(links, '\n')
        data_dic = {}
        page_soup = BeautifulSoup(requests.get(links).content)
        data_dic['position_title'] = page_soup.find(class_='posting-headline').find('h2').text
        data_dic['loc_type_position_time'] = (page_soup.find(class_='posting-categories').text)
        data_dic['description'] = (page_soup.find(class_='section page-centered').text)

        #Getting column names
        for i in page_soup.find_all(class_='section page-centered'):
            if i.find('h3') != None:
                heading = i.find('h3').text.strip()
            else:
                try:
                    heading = i.find('b').text.strip()
                except:
                    heading = ''
            #print(heading)

            #Get all texts within a div of headings or a description
            if len(i.find_all('li'))>0:
                value = i.find_all('li')
                value = list(map(lambda x: x.text, value))
                value = "; ".join(value)
            else:
                value = i.text[len(heading):]

            #Creating columns if they exist (according to our columns above)
            if heading.strip(':') in responsibilities_columns:
                data_dic['core_responsibilities'] = value

            if heading.strip(':') == 'Organizational Relationships':
                data_dic['Organizational Relationships'] = value

            if heading.strip(':') == 'Position Overview':
                 data_dic['description'] = value

            if heading.strip(':') in knowledge_columns:
                data_dic['Knowledge, Skills, and Abilities'] = value

            if heading.strip(':') in key_skills_columns:
                data_dic['Key Skills'] = value

            if heading.strip(':') in preferred_skills_columns:
                data_dic['preferred_skills'] = value

            if heading.strip(':') in traits_columns:
                data_dic['Traits'] = value

            if heading.strip(':') == 'Credentials and Experience':
                data_dic['Credentials and Experience'] = value

            if heading.strip(':') in work_env_columns:
                data_dic['Physical Requirements / Work Environment'] = value

            if heading.strip(':') in application_requirements_columns:
                data_dic['application_requirements'] = value

            if heading in optional_app_materials_columns:
                data_dic['optional_application_requirements'] = value

        data_dic['link_to_apply'] = (page_soup.find(class_='section page-centered last-section-apply').find('a').get('href'))
        dataframe = dataframe.append(data_dic, ignore_index=True)

    #Split Location, position, and full or part time position column
    dataframe[['Location','Position_category', 'Part_or_Full_time']] = dataframe['loc_type_position_time'].str.split("/", expand=True)
    dataframe.drop(columns={'loc_type_position_time'}, inplace=True)
    print(dataframe.columns)

    #Reorder columns and replace one of the error manyally
    dataframe = dataframe[columns]
    dataframe.iloc[7,4] = dataframe.iloc[7,4].replace('Location: Moscow, ID', "")

    #Save it to json (string) format
    dataframe.to_json('emsi_job_lists.json')

    return data_dic, dataframe


if __name__ == "__main__":
    dictionary, df = insert_html(html_page)
