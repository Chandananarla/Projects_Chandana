#!/usr/bin/env python
# coding: utf-8

# # AIT-590 : INTRO TO NLP
# 
# # FINAL PROJECT - RESUME SCREENING
# 
# By: 
#    01 - TEAM 01 (SHRAVYA GADDAM,CHANDANA NARLA, ANIRUDH TUNUGUNTLA)

# In[169]:


import sys
import re
import requests
import bs4
import csv
import os
import datetime
import math
import nltk

from bs4 import BeautifulSoup
from nltk import ngrams
from nltk.corpus import stopwords  
from gensim import similarities
from gensim import models
from gensim import corpora
from datetime import datetime
from nltk.tokenize import word_tokenize, sent_tokenize, WordPunctTokenizer


# In[170]:


#This function takes skills of a role in corpus as input , and returns them in form of list of tuples
# ex: input :"<Skills>(HTML,Hypertext Markup Language), (Cascading Style Sheets,CSS), (SQL, Structured Query Language)</Skills>"
#    output :[(HTML,Hypertext Markup Language), (Cascading Style Sheets,CSS), (SQL, Structured Query Language)]
# Regular expression and string functions like: split(), strip(), replace(), lower() are used to achieve this conversion
def format_skills_corpus(job_skills):
    match = re.search(r'\((\.|\s|\w+)?\,(\.|\s|\w+)*?\)',job_skills,re.M|re.I)
    if match is None:
        job_skills = job_skills.strip('\n').strip().split(',')
    else:    
        job_skills = job_skills.strip('\n').strip().split('),')
    job_skills = [skill.strip().replace('(','').replace(')','') for skill in job_skills]
    job_skills = [skill.lower().split(',') for skill in job_skills]
    return job_skills

#This function takes other tags data of a role in corpus as input and returns them in form of list 
# ex: input: "Computer Science, Computer Programming, Computer Engineering" 
#     output: ['Computer Science', ' Computer Programming', ' Computer Engineering']
def format_corpus(file_data):
    formated_data = file_data.string.strip('\n').strip().split(',')
    return formated_data

# This function takes the formated corpus data and required job_role as input
# and returns the formatted data of Skills, Education and Work Experience for the given job role in form of dictionary
def get_jobrole_corpus(corpus_data,job_role):
    role_data_dic = dict()
    roledata = corpus_data.find(job_role)
    print("role",job_role)
    role_skill_data = roledata.find('Skills')
    print(role_skill_data)
    role_skills = format_skills_corpus(role_skill_data.string)
    role_education = roledata.find('Education')
    role_education = format_corpus(role_education.string)
    role_experience = roledata.find('Experience')
    role_experience = format_corpus(role_experience.string)
    role_data_dic['Skills'] = role_skills
    role_data_dic['Education'] = role_education
    role_data_dic['Experience'] = role_experience
    return role_data_dic
# This function reads the corpus file and returns a dictionary containing require dcorpus data for each role
def get_corpus_data():
    JObRole = open("job_roles.xml","r",encoding="utf8")
    jobdata= JObRole.read()
    jobrole_data = bs4.BeautifulSoup(jobdata, 'lxml-xml')
    job_roles = jobrole_data.corpus.children
    corpus_data_dic = dict()
    for role in job_roles:
        if role.name!=None:
            #print("role name-",role.name)
            role_dic = get_jobrole_corpus(jobrole_data,role.name)
            corpus_data_dic[role.name] = role_dic
    return corpus_data_dic
    


# In[171]:


# this function gets the url of the candidate and returns it.
# this the link to the candidates resume
# it taks th eurl object as input
def get_candidate_url(url):
    resumeurls=url.get('href')
    return resumeurls
# this function takes the bs4 object for the candidates page as input 
# and returns the candidates Name 
def get_candidate_name(indvisoup):
    CandidateName=[]
    d1=indvisoup.find('div')
    CandidateName=d1.find("h1").get_text()
    return CandidateName

# this function takes the bs4 object for the candidates page as input 
# and returns the candidates skills/keywords in form of a list
def get_candidate_skills(indvisoup):
    SkillsSet = []
    for d1 in indvisoup.find_all('li'): 
        Skill=d1.get_text()
        if(Skill=='FAQ'):
            break;
        SkillsSet.append(Skill)
        #print(SkillsSet)
    return SkillsSet

# this function takes the bs4 object for the candidates page as input 
# and returns the candidates work experience in form of list of tuples containing, role & duration details
def get_candidate_experience(indvisoup):
    WorkExperience=[]
    for d1 in indvisoup.find_all(id='work_experience'):
        for d2 in d1.find_all('tr'):
            row = []
            for c2 in d2.find_all('td'):
                if c2 is not None:
                    d3=c2.get_text().strip()
                    row.append(d3)
            WorkExperience.append(tuple(row))
    return WorkExperience

# this function takes the bs4 object for the candidates page as input 
# and returns the education details in form of list of tuples containing program name, year and type of degree 
def get_candidate_education(indvisoup):
    Education=[]
    for d1 in indvisoup.find_all(id='education'): 
        for d2 in d1.find_all('tr'):
            row = []
            for c2 in d2.find_all('td'):
                if c2 is not None:
                    d3=c2.get_text().strip()
                    row.append(d3)
            Education.append(tuple(row))
    return Education

# this function takes the bs4 object for the candidates page as input 
# and returns the candidates details like current occupaltion , location, willing to relocate etc.,
# in form of dictionary
def get_candidate_profile_data(indvisoup):
    profile_data = dict()
    d1 = indvisoup.select("table.resume_module_table > tr")
    if len(d1)==0:
        return profile_data
    data = d1[0].get_text().strip().replace(' ','').replace('\r','').replace('\n',' ')
    data = data.split('  ')
    print(data)
    for ele in data:
        match = re.match(r'(.*):(.*)',ele,re.M|re.I)
        if match is not None:
            try:
                key = match.group(1)
                val = match.group(2)
                profile_data[key.strip()]=val.strip()
            except:
                continue
    return profile_data
                    
    
        


# In[172]:


# This function takes the skills of a role from corpus and list of skills of the user
# and returns score for the user by checking the similarty between the given lists of skills
# Here the corpus dictionary is built based on the user skills,
# which is converted into bag of words using gensim corpora dictionary & dictionary's doc2bow function.
# Then tfidf model is built using gensim models - TfidfModel function based on the bowcorpus built earlier.
# Then using SparseMatrixSimilarity function if gensim similarities module index is built using the tfidf model & feature_count of the dictionary
# Also a base dictionary with skills from required as keys and values as False is created,
# for which the value is set to True if the similarity % obtained using the above created index is matched,
# this way any duplicate matches are eliminated while calculating the score
# Count of the skills which of Trues is noted and then divided by the total number of required skills
# and the obtained value is returned as the skills score for the user for the given role.

def get_skill_score(userSkills, roleReqSkills):
    processd_corpus = [[word for word in document.lower().split()]
         for document in userSkills]
    #print(processd_corpus)
    similarity_dict = dict()
    for req_skill in roleReqSkills:
        temp = ','.join(req_skill)
        similarity_dict[temp] = False
        
    dictionary = corpora.Dictionary(processd_corpus)
    feature_count = len(dictionary.token2id)
    bow_corpus = [dictionary.doc2bow(text) for text in processd_corpus]
    tfidf = models.TfidfModel(bow_corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=feature_count)
    for reqSkill in roleReqSkills:
        query_bow = dictionary.doc2bow(reqSkill)
        sims = index[tfidf[query_bow]]
        sorted_similarity = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
        if sorted_similarity[0][1]>=0.70:
            temp = ','.join(reqSkill)
            similarity_dict[temp] = True
    count = 0
    for reqskill in similarity_dict.keys():
        if similarity_dict[reqskill]:
            count += 1
    return count/len(roleReqSkills)


# In[173]:


# this function takes list of job roles accepted for a specific role and the work experience details of the user
# Using gensim corpora for dictionary, doc2bow and gensims models -> tfidfmodel a model is built
# on which gensim similarities -> sparse similarity matrix is applied , which is used to look for similarities
# between required job roles & user's job role.
# if the job role of user's experience is similar to the required ones, 
# then the duration of the particular experience is calculated by using the start & and end dates given
# duration of all these relevant experiences is summed up to get the user's total relevant experience
# then score is assigned to user based on this duration.
# if the total experience is betweeon 0-3 years then a score of 1 is assigned,
# if the experience is between 3-5 years then a score of 2 is assigned,
# if the experience is between 5-10 years then a score of 3 is assigned, 
# if the experience is > 10 years then a score of 4 is assigned,
# if the user has no relevant experience then a score of 0 is assigned.
# and this score divided by the highest possible score of 4 is returned.
def get_work_experience_score(jobroles, user_experience):
    processd_corpus = [[word for word in document.lower().split()] for document in jobroles]
    dictionary = corpora.Dictionary(processd_corpus)
    feature_count = len(dictionary.token2id)
    bow_corpus = [dictionary.doc2bow(text) for text in processd_corpus]
    tfidf = models.TfidfModel(bow_corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=feature_count)
    master_count = 0
    bachelor_count = 0
    phd_count = 0
    total_expr = 0
    for work_expr in user_experience:
        if(len(work_expr)<2):
            continue
        jobrole = work_expr[0].lower().split()
        job_duration = work_expr[1]
        query_bow = dictionary.doc2bow(jobrole)
        sims = index[tfidf[query_bow]]
        sorted_similarity = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
        if sorted_similarity[0][1]>=0.70:
            job_duration = job_duration.strip()
            dates = job_duration.strip().split('-')
            dates = [date.strip() for date in dates]
            try:
                startdate = datetime.strptime(dates[0],'%m/%Y')
            except:
                try:
                    startdate = datetime.strptime(dates[0],'/%Y')
                except:
                    startdate = ''
            enddate = dates[1]
            if enddate !='Present':
                try:
                    enddate = datetime.strptime(enddate,'%m/%Y')
                except:
                    try:
                        enddate = datetime.strptime(enddate,'/%Y')
                    except:
                        enddate = ''
            else:
                enddate = datetime.now()
            if enddate=='' or startdate=='':
                total_expr = 0
            else:
                duration = enddate-startdate
                total_expr = duration.days/365
    work_score = 0
    if(total_expr>0 and total_expr<3):
        work_score = 1
    elif total_expr>=3 and total_expr<5:
        work_score = 2
    elif total_expr>=5 and total_expr<10:
        work_score = 3
    elif total_expr>10:
        work_score = 4
    else:
        work_score = 0
    return work_score/4
        
          


# In[174]:


# This function takes related education majors from corpus and candidates education details as input
# and returns candidate's education score.
# If the major of the candidate's degree matches with atleast one given in the corpus then it is considered
# For the matched educaton, then degree level counts are calculated. it maintain 3 count variables for each degree level (PHD, Masters, Bachelors)
# i.e., suppose a candidate has total 4 degrees.
# 2 masters degrees, 1 PHD and 1 bachelors degree
# And suppose of these degrees , 1 masters , 1 phd are relevent to the job role and remaining are not relevant
# In such case the count variables are updated only with the count of relevant degrees ie.,
# bachelor_count = 0, master_count = 1, phd_count = 1 will be assigned
# After all the degrees of candidate are verfied for specific role then , 
# score is allocated to candidate based on these counts:
# First the candidate's phdcount is checked, if it is greater than 1 then score of 5 is assigned (hihghest)
# else if the candidate has only 1 phd degree then a score of 4 is assigned, 
# if the candidate's phd_count is 0 then the candidates master_scount is considered.
# Here if the candidate has master_count>1 then score of 3 assigned , 
# else if the candidate has only 1 masters degree then a score of 2 is assigned,
# else if the candidate master_count is 0, then bachelor_count is checked.
# if the candidate has atleast one bachelor degree then score of 1 is assigned 
# else the score of the candidate remains 0
# Only the highest degree level of relevant education is considered.
# Here the highest score possible for a user is 5.
# Finally the percentage of the education score is returned as the education score. ie., 
# the value of the score assigned divided by the max score - 5 is returned.
def get_education_score(jobrole_majors, user_education):
    processd_corpus = [[word for word in document.lower().split()] for document in jobrole_majors]
    dictionary = corpora.Dictionary(processd_corpus)
    feature_count = len(dictionary.token2id)
    bow_corpus = [dictionary.doc2bow(text) for text in processd_corpus]
    tfidf = models.TfidfModel(bow_corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=feature_count)
    master_count = 0
    bachelor_count = 0
    phd_count = 0
    for education in user_education:
        if(len(education)<3):
            continue
        major = education[0].lower().split()
        degree_level = education[2]
        query_bow = dictionary.doc2bow(major)
        sims = index[tfidf[query_bow]]
        sorted_similarity = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
        if sorted_similarity[0][1]>=0.70:
            if 'Master' in degree_level:
                master_count += 1
            elif 'Bachelor' in degree_level:
                bachelor_count += 1
            elif 'PHD' in degree_level or 'Post Graduation' in degree_level or 'Doctorate' in degree_level:
                phd_count += 1
            else:
                sc = 0
                
    edu_score = 0
    if phd_count>0:
        if phd_count>1:
            edu_score = 5
        else:
            edu_score = 4
    else:
        if master_count>0:
            if master_count > 1:
                edu_score = 3
            else:
                edu_score = 2
        elif bachelor_count > 0:
            edu_score = 1
    return edu_score/5
        
     
            
    


# In[175]:


# This function takes, each role required data from corpus and the candidate's data as input arguments
# And returns the overall score of the candidate for given role.
# get_skill_score, get_education_score, get_work_experience_score are used to get the respective scores.
# these 3 scores are used to calculate the overall score for given role for the candidate,
# Overall score is the sum of weighted score of these individual scores.
# Overall score = 55% of skill score, 30% workexperience score & 15% education score
# This calculated value percent is returned ad the candidate's score for the given role.
def get_role_score(role_corpus,candidate_details):
    role_skills_corpus= role_corpus['Skills']
    role_education_corpus = role_corpus['Education']
    role_experience_corpus = role_corpus['Experience']
    candidate_SkillsSet= candidate_details['Skills']
    candidate_education = candidate_details['Education']
    candidate_experience = candidate_details['Experience']
    if len(candidate_SkillsSet)!=0:
        skills_score = get_skill_score(candidate_SkillsSet,role_skills_corpus)
    else:
        skills_score = 0.0
    if len(candidate_education)!=0:
        education_score = get_education_score(role_education_corpus,candidate_education)
    else:
        education_score = 0
    if len(candidate_experience)!=0:
        experience_score = get_work_experience_score(role_experience_corpus,candidate_experience)
    else:
        experience_score = 0
    total_score = 0.55*skills_score+0.15*education_score+0.30*experience_score
    total_score_percentage = total_score*100
    return total_score_percentage                    


# In[176]:


# This block of code is the main part of the project. 
# This is where the actual execution starts.

# Here the get_corpus_data function is used to get the required skillset, education & workexperience details for each role in corpus.
corpus_data_dic = get_corpus_data()
# Here a csv file is created to write all the results into it and header of the file is set based on the roles in the corpus file
# Also result_writer object is created using which the result for each candidate are wriiten into the csv file.
result_file = open('Candidate_Resume_scores.csv','w',newline='')
Columns = ['Name','Occupation','WillRelocate','Location','EducationLevel','Resume_Link']
for key in corpus_data_dic.keys():
    temp = key+'_score'
    Columns.append(temp)
    temp = key+'_picked'
    Columns.append(temp)
result_writer = csv.DictWriter(result_file, fieldnames = Columns)
result_writer.writeheader()

for key in corpus_data_dic.keys():
    print(key,":",corpus_data_dic[key])
    
total_role_sum_dic = dict()
try:
    # here using requests we get the url content of climbers site in which resumes are listed.
    resumesource=requests.get("https://members.climber.com/online-resumes/pdf-doc-txt-rtf-resume/i/Information-Technology")
    # the url content obtained is then parsed using Beautiful soup
    # this page contains links to list of resumes of different roles
    resumesoup=BeautifulSoup(resumesource.text,'html.parser')
    for url in resumesoup.find_all('td'):
        url=url.find('h3')
        if url is not None:
            for department_url in url.find_all('a'):
                urlcount=department_url.get_text()
                resumeurls=department_url.get('href')
                # here the page content of each job role in the website is retrieved.
                # it contains list of candidate resumes of that particular dept/role/occupation
                department_source=requests.get(resumeurls)
                # here also we use beautofu soup get links of each candidate's resume
                department_soup=BeautifulSoup(department_source.text,'html.parser')
                # we iterate for each candidate, extract details from candidate's resume,
                # calculate scores and write the result into a temporary file
                for values in department_soup.find_all('h2'):
                    for url1 in values.find_all('a'):
                        print('*********')
                        candidate_details = dict()
                        score_details = dict()
                        # here url - link to canidate's resume is stored.
                        ResumeDetails = get_candidate_url(url1)
                        print(ResumeDetails)
                        candidate_details['Resume_Link']=ResumeDetails
                        indvisource=requests.get(ResumeDetails)
                        indvisoup=BeautifulSoup(indvisource.text,'html.parser')
                        #here Candidate Name is extracted 
                        CandidateName=get_candidate_name(indvisoup)
                        print(CandidateName)
                        candidate_details['Name']=CandidateName
                        #Here the candidate's profile data like currect location, occupation, willing to relocate are extracted
                        profile_data = get_candidate_profile_data(indvisoup)
                        candidate_details.update(profile_data)
                        #here the candidate's skillset/keywords are extracted
                        SkillsSet = get_candidate_skills(indvisoup)
                        score_details['Skills']=SkillsSet
                        #here the candidate's Work Experience details are extracted
                        WorkExperience=get_candidate_experience(indvisoup)
                        score_details['Experience']=WorkExperience
                        #here the candidate's Education details are extracted         
                        Education=get_candidate_education(indvisoup)
                        # all the candidate's details extracted are stored in from of dictionary
                        score_details['Education']=Education                
                        candidate_rolewise_scores = dict()
                        # for each role in the corpus, candidat'e overall score's are calculated and stored            
                        for corpus_role in corpus_data_dic.keys():
                            role_corpus = corpus_data_dic[corpus_role]
                            total_role_score = get_role_score(role_corpus,score_details)
                            candidate_rolewise_scores[corpus_role] = total_role_score
                            print("role:",corpus_role,",score:",total_role_score)
                            key = corpus_role+'_score'
                            # here the sum of scores of all the candidates for each role is calculated and stored
                            # this is later used to find average score which is later used inorder set the cutoff.
                            candidate_details[key]=total_role_score
                            try:
                                if profile_data['Occupation']==corpus_role:
                                    if corpus_role in total_role_sum_dic.keys():
                                        tempsum = total_role_sum_dic[corpus_role][0]+total_role_score
                                        count = total_role_sum_dic[corpus_role][1] + 1
                                        total_role_sum_dic[corpus_role] = (tempsum,count) 
                                    else:
                                        total_role_sum_dic[corpus_role] = (total_role_score,1)
                            except KeyError:
                                continue
                                
                        # here the candidate's details along with his scores and whether screened for the given roles is written into the csv file    
                        result_writer.writerow(candidate_details)

finally:
    # in this block of code, based on the previously calculated scores,
    # each resume is screened based of the cutoff calculated, 
    # which is about 1.5 times the overall average score.
    # if the candidate's core is greater than this value then his resume is selected
    # which is represented by 'YES' value in the picked column of perticular role
    # This selection is updated into the csv file
    result_file.close()
    total_role_avg = dict()
    try:
        read_file = open('Candidate_Resume_Scores.csv','r')
        result_file = open('Candidate_Resume_Screened.csv','w',newline='')
        
        reader = csv.DictReader(read_file)
        writer = csv.DictWriter(result_file, fieldnames=Columns)
        writer.writeheader()
        for role in total_role_sum_dic.keys():
            total_role_avg[role] =  total_role_sum_dic[corpus_role][0]/total_role_sum_dic[corpus_role][1] 
        for row in reader:
            data_row = row
            for role in total_role_sum_dic.keys():
                key = role+'_score'
                act_key = role+'_picked'
                if float(row[key])>=total_role_avg[role]*1.5:
                    data_row[act_key] = 'YES'
                else:
                    data_row[act_key] = 'NO'
            writer.writerow(data_row)
        
    finally:
        #finally the resultant file is closed so the results are saved.
        read_file.close()
        os.remove('Candidate_Resume_Scores.csv')
        result_file.close()


# In[ ]:




