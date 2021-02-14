# Scraping EMSI job web page
## This is a scraper to scrape jobs from EMSI job website.

#### There are various columns which are identical, but differnt in wordings. So, I created columns which would mean the same thing. For example, columns "Key Skills" and "Candidates must have" are converted into "Key Skills." the information below shows which columns are merged into the same columns.
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

#### I manually replacing of the position job description. It is on dataframe.iloc[7,4] .
