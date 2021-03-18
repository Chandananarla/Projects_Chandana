Problem Description
    In the past, many studies have been conducted which demonstrated the recommendations. Designing a personalized resume recommendation algorithm which benefits the job seekers by using part-of-speech TF-IDF approach. Classification of various skills based on the job requirement by matching the phrases and segregating them. The existing works recommend resumes helping the employers and potentially discarding 1000 of candidates. To improve the scenario, discarded resumes can be redirected to appropriate departments.
Solution Outline
    Initially, as the first step for the implementation of the project, we will be performing web scrapping, where we are looking at extracting over 400 real-time resumes. This acts as the dataset for our project. 
    After scraping the resumes data, the resume content for each profile is pre-processed. During the pre-processing important information like the skillset, education, work-experience are retained. 
    From this information each resume is given 3 scores: Skill Set, Education and Work Experience based on their relevance to the required role. 
    Relevance of the candidate’s resume is verified using genism’s dictionary built on the candidate’s data, on which Tifidf model is built, and then sparse index matrix is built from which the similarity score between the required role data and candidate’s data is obtained. 
    Based on this similarity and other factors like education degree level and duration of the work experience scores are calculated.
    An overall score based on the above 3 score for each role on each candidate is calculated, then based on the cutoff score, Each resume is screened to be either picked or not for the specific role.
    All these details of the candidates are written into the output csv file, which can be used by the recruiter for further filtering and processing.
Input – Output Examples
   System takes 2 inputs, the Required Job description corpus and link to the resumes.
    The Required Job roles & its details must be in XML file named ‘JobRoles.xml’
Ex: Job role File contents:
[<?xml version="1.0" encoding="UTF-8"?>
<corpus lang="en">
   <WebDeveloper>
       <Skills>(HTML,Hypertext Markup Language), (Cascading Style Sheets,CSS), (SQL, Structured Query Language), (PHP,Hypertext Preprocessor), (Javascript), (Python), (Laravel), (Django), (Angular,AngularJS), (ReactJS, React), (JQuery),(.NET,ASP.NET),(Ruby),(Node.js) </Skills>
       <Education> Computer Science, Computer Programming, Computer Engineering, Information Technology, Software Engineering </Education>
       <Experience> Web Developer, Web Designer, Front End, UI Designer, UX Designer, Full Stack </Experience>
    </WebDeveloper>
   <DataMiningSpecialist>
       <Skills>R, Python, Java, SQL, Scala, SAS, NoSQL, Databox, Zoho Analytics,Google Chart, Tableau, Power BI, Qlikview, Apache Spark, Excel, SAP, TIBCO, Grafana, WEKA, Hadoop,HIVE, HDFS, Highcharts, D3, Fusion chart, Canvas, nltk, pandas, numpy, MATLAB, Logistic Regression,Linear Regression, Gradient Boost, (SVM,Support Vector Machine), Naive Bayes, (K nearest neighbor,KNN), Neural Network, Natural Language Processing, Clustering, Classification, Big Data, MapReduce, Machine Learning, (ETL,Extraction Transformation and Loading) </Skills>
       <Education> Data Science, Data Analytics, Statistical and Data Science, Computer Science, Predictive Analytics, Big Data Analytics </Education>
       <Experience> Data Analyst, Data Scientist, Data Engineer, Business Intelligence Analyst </Experience>
   </DataMiningSpecialist>
</corpus>
]
    Link to the Climbers website containing the resumes to be filtered.
Climber website URL consisting links to resumes of candidates.
[
 URL - https://members.climber.com/online-resumes/pdf-doc-txt-rtf-resume/i/Information-Technology
]
   
   OUTPUT:
    The output of the system is file with name Candidate_Resume_Screened.csv is created in the same folder. It consists the Candidates details along with their scores & whether they are picked or not  for each role specified in the input corpus. Following is and example of the result in csv format. 
   Name,Occupation,WillRelocate,Location,EducationLevel,Resume_Link,WebDeveloper_score,WebDeveloper_picked,DataMiningSpecialist_score,DataMiningSpecialist_picked,DatabaseAdministrator_score,DatabaseAdministrator_picked,Tester_score,Tester_picked,TeamLeader_score,TeamLeader_picked,NetworkAdministrator_score,NetworkAdministrator_picked
Ken K,ApplicationSupport,No,"Bremerton,WA",Bachelor,https://members.climber.com/online-resumes/pdf-doc-txt-rtf-resume/11084684/206/Information-Technology/Sr-Application-Analyst-14-Years-of-Experience-Near-98312,7.857142857142857,YES,7.5,YES,10.0,YES,0.0,NO,3.6666666666666665,NO,0.0,NO
Margaret N,BusinessAnalyst,YES,"Alpharetta,GA",Bachelor,https://members.climber.com/online-resumes/pdf-doc-txt-rtf-resume/10925112/770/Information-Technology/Business-Analyst-15-Years-of-Experience-Near-30009,0.0,NO,22.499999999999996,YES,22.499999999999996,YES,0.0,NO,3.6666666666666665,NO,0.0,NO
One of the results of our execution is being attached as a sample output, which has better readability.

How to run:
    Using Command Prompt:
        Install/ Load all the necessary modules including – bs4 – BeautifulSoup, nltk, genism if not already installed.
        Place ‘resume_screening.py’, ‘job_roles.xml’ files in a single folder.
        To this folder location in the command prompt run the following command: python resume_screening.py
    Using jupyter:
       Open the resume_screening.py/ resume_screening.ipynb file in the jupyter notebook.
       Place ‘resume_screening.py’, ‘job_roles.xml’ files in a single folder.
       And run all the cells.
