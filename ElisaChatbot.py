#!/usr/bin/env python
# coding: utf-8


#001-Team1
#TemaMates: Shravya Gaddam, Chandana Narla , Anirudh Tunuguntla
#Date: 15th Sept, 2020

#This Elisa Chatbot works with few special instructions:
#the User must intorduce himself using phrases (am or Is) so the Chat bot could be interactive
#Example: Doctor: Good Afternoon, I am Eliza - Your psychotherpist.May I know your name please?
         # User: Good Afternoon, I am Chandana.
        #Eliza: Hi Chandana! How can I help you?
        #User: so....
#This chatbot prefers to deal with the User choices, likes ,wants, needs etc., information only.
#Hence the conversations start with I.
#Example: #User: I love books
        #Eliza: Did you not love books at any point in your life?
#Example: #User: I feel pain
        #Eliza: What do you think about these feelings?
        #User: I feel glad
        #Eliza: What do you do when your happy?        
#Also If the user wants to exit the chatsession ith Elisa,
        #User: bye
        #Elizaa: Hope the session was helpful!!
        #ElizaTake care. Good Bye
#Adding to them, If the user doesnot respond to Eliza, the chatbot tries to build interaction by using statements:
        #Eliza: You need to talk to me, For me to be able to help you
        #Eliza: I cannot help you, if you refuse to talk
#We have tried to identify and deal with words including like, love, hate, enjoy,fancy which help us understanding the user interests.
#We have tried to identify and deal with words including want, Need, require, wish which help us understanding the user requirements.
#We have tried to identify and deal with words including Because, Since, As which help us identify the user reasoning.
#We have tried to identify and deal with words including Lonely, alone which help us identify the users mindset.
#We have tried to identify and deal with synonyms of workds like Happy, Sad, Angry, Disappoinment,Anxiety for understanding the user emotions
#We have tried to identify and deal with words including feel, feelings which help us identify other emotions of the user..

#We have tried to identify emotions by extracting verbs and adjectives from the user input using wordnet and pos_tag
import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from datetime import datetime
import random
import time
import sys
from threading import Thread

responseList_FeelingQuestion = [r"How are you feeling?",r"Tell me how you are feeling today?", r"Lets start with basics first, How are you?"]
responseList_FeelingResponse = [r"Since when are you feeling this way?", r"Do you thnk it is normal to feel this way?", r"Do you want to talk about it?",r"Why do you feel this way?",r"What makes you feel this way?",r"You can talk to me about your feelings..",r"What do you exactly feel?",r"What do you think about these feelings?",r"Can you talk more about this?",r"Tell me more about these feelings?"]
responseList_ForUncomprhensibleReply = [r"Tell me more..", r"Please ellaborate", r"Please go on..", r"I am listening , please continue"]
responseList_Timeout = [r"You need to talk to me, For me to be able to help you", r"I cannot help you, if you refuse to talk"]
responseList_Books= [r"Do you read books?",r"What kind of books do you read?",r"What is the last book that you have read...Did you enjoy it?",r"Does reading books excite you?",r"How often do you read books?",r"Can you talk more about this?"]
responseList_Happy=[r"What makes you happy?",r"What gives you happiness",r"What do you do when your happy?",r"what do you love the most?"]
responseList_Excitement=[r"What excites you?",r"Can you talk more about this?"]
responseList_Lonely=[r"What made you feel lonely?",r"What did you do when you felt lonely?",r"How did you react on being alone?",r"How often do you feel lonely",r"Can you talk more about this?"]
responseList_ContinutionQuestion=[r"Do you want to talk about it?",r"Are you comfortable talking about it?",r"How did it impact you?",r"How do you know?",r"Why does it impact you?",r"Can you talk more about this?",r"Tell me more about this"]
responseList_Anxiety=[r"How often do you get anxiety?", r"What do you think the reason for your anxiety is?", r" How long have you been getting anxiety?", r"Did you come to me because you are getting anxiety?", r"Tell me more…", r"Do you believe it is normal to get anxeity?"]
responseList_Sad= [r"How often are you sad?", r"Why do you think you are sad?", r" How long have you been sad?", r"Did you come to me because you are sad?", r"Tell me more…", r"Do you believe it is normal to be sad?"]
responseList_Because=[r"Are there any other reasons?", r"Do you think it is the only reason?"]
responseList_Disappointment=[r"Why do you feel disappointed?",r"What disappoints you?",r"How often do you get disappointed?",r"What has been the greatest disappointment in your life?",r"How do you deal with disappointment?"]
responseList_Anger=[r"What is the reason for your anger?",r"What makes you angry?",r"How so you deal with anger issues?",r"What do you do when you are angry?",r"How often do you get angry?"]

answer = None
# waits for response and prompts user to reply 
def check():
    time.sleep(250)
    global answer
    if answer != None:
        return
    print("Eliza: "+str(random.choice(responseList_Timeout)))

# prompts user for input waits for response and returns it    
def getUserInput():
    global answer
    answer = None
    Thread(target = check).start()
    answer = input("User: \b")
    return answer

# Returns list of synonyms for given argument 'word' 
def GetSynonyms(word):
    synList = list()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synList.append(lemma.name())
    return synList

Happy_SynonymList= GetSynonyms('Happy')
Sad_SynonymList= GetSynonyms('Sad')
Anger_SynonymList= GetSynonyms('Angry')
Disappointment_SynonymList= GetSynonyms('Disappointment')
Anxiety_SynonymList= GetSynonyms('Anxiety')
Exit= False

def ExtractKeywordFromResponse(txt, pos):
    # getting list of stopwords in nltk library
    stop_words = set(stopwords.words('english'))
    # removing punctuation from user input
    punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
    for ele in txt:
        if ele in punc:
            txt = txt.replace(ele, " ")
    # tokenises given sentence into words
    tokenized = sent_tokenize(txt)
    for i in tokenized:
        wordsList = nltk.word_tokenize(i)
        
    wordsList =list()
    # removing stop words from wordList
    for word in wordsList:
        if not word in stop_words:
            wordsList.append(word)
            
    #  pos_tagger, tags each word with its repsective parts of speech
    tagged = nltk.pos_tag(wordsList)
    # converting to dictionary format for accessing parts of speech values
    taggedDic = dict(tagged)
    keys = taggedDic.keys()
    # loops through all the words and returns the word with given parts of speech 'pos'
    for key in keys:
        if(pos in taggedDic[key]):
            return key
    return None

# greet the user based on time of the day
TimeNow = datetime.now()
HourOfDay = int(TimeNow.strftime("%H"))
while(True):
    if(HourOfDay<12):
        print("Doctor: Good Morning, I am Eliza - Your psychotherpist.May I know your name please?")
        break
    elif(HourOfDay<16):
        print("Doctor: Good Afternoon, I am Eliza - Your psychotherpist.May I know your name please?")
        break
    else:
        print("Doctor: Good Evening, I am Eliza - Your psychotherpist.May I know your name please?")
        break


# function checks whether the user wants to exit the session
# takes user input as argument and returns boolean value of to exit or not also sets boolean variable 'Exit' value
def checkForExit(UserInput):
    QuitWords = [r"Quit",r"Good Bye",r"Thank you",r"Bye",r"bye",r"quit",r"exit",r"Exit",r"thank you",r"good bye",r"QUIT",r"BYE",r"EXIT"]
    global Exit
    if(UserInput in QuitWords):
        time.sleep(2)
        print("Eliza: Hope the session was helpful!!")
        print("Eliza: Take care. Good Bye")
        Exit= True
        return Exit
    else:
        Exit= False
        return Exit
# gets user input
UserInput = str(getUserInput())
if(checkForExit(UserInput)):
    sys.exit() 
m = re.match( r'(.*)?(am|is)\s?\b(.*)\b', UserInput, re.M|re.I)

NameFlag=True
# Retreives name of the user form input if present, else prompts user to give name
while(NameFlag):
    if(m is not None):
        txt = m.group(3)
        txt = txt.replace('am', "")
        txt= txt.replace('is',"")
        txt = txt.strip()
        print("Eliza: Hi "+txt+"! How can I help you?")
        NameFlag=False
    else:
        print("Eliza: The Converstaion will be fruitful if I get to know your name")
        UserInput = str(getUserInput())
        time.sleep(2)
        if(checkForExit(UserInput)):
            sys.exit()
        m = re.match(r'(.*)?(am|is)\s?\b(.*)\b', UserInput, re.M|re.I)

umcount=0
UserMessage=''
# initially Exit is False so enters the loop
while(not(Exit)):
    # retrieves user input
    UserInput = str(getUserInput())
    time.sleep(2)
    # checks with previous input of user, if it is same then updates the counter
    if(UserMessage==UserInput):
        umcount= umcount+1
    # checks if counter is more than 2 (it means user is repeating same thing)
    if(umcount>2):
        print("I cannot help you, If you keep repeating yourself")
        umcount=0
        continue
    UserMessage=UserInput
    #checks and ends the session if user wants to
    if(checkForExit(UserInput)):
        break
    # checks and corrects if user is talking about Eliza instead of himself
    elif('you' in UserInput):
        print("Eliza: We were discussing about you not me")
        continue
    else:
        #retrieves verb from the user input
        getVB= ExtractKeywordFromResponse(UserInput,'VB')
        #retrievs adjective from the user input
        getJJ= ExtractKeywordFromResponse(UserInput,'JJ')
        #if the verb or adjective in the input means happy then corresponding response is printed.
        if(getJJ in Happy_SynonymList or getVB in Happy_SynonymList):
            print("Eliza: "+str(random.choice(responseList_Happy)))
            continue
         #if the verb or adjective in the input means sad then corresponding response is printed.
        elif(getJJ in Sad_SynonymList or getVB in Sad_SynonymList):
            print("Eliza: "+str(random.choice(responseList_Sad)))
            continue
         #if the verb or adjective in the input means angry then corresponding response is printed.
        elif(getJJ in Anger_SynonymList or getVB in Anger_SynonymList):
            print("Eliza: "+str(random.choice(responseList_Anger)))
            continue
         #if the verb or adjective in the input means disappointment then corresponding response is printed.
        elif(getJJ in Disappointment_SynonymList or getVB in Disappointment_SynonymList):
            print("Eliza: "+str(random.choice(responseList_Disappointment)))
            continue
         #if the verb or adjective in the input means anxiety then corresponding response is printed.
        elif(getJJ in Anxiety_SynonymList or getVB in Anxiety_SynonymList):
            print("Eliza: "+str(random.choice(responseList_Anxiety)))
            continue
         #if input contains words like alone, lonely then corresponding response is printed.
        elif(re.match(r".*?\s?a?lone(ly)?.*?", UserInput, flags=re.IGNORECASE)):
            print("Eliza: "+str(random.choice(responseList_Lonely)))
            continue
        #if input contains words like feel, feeling, feels then corresponding response is printed.
        elif('feel' in UserInput):
            print("Eliza: "+str(random.choice(responseList_FeelingResponse)))
            continue
        #if input matches sentence like 'I want money', 'I wish to travel', 'I need time'etc., then corresponding response is printed.
        elif(re.match(r"\s?I?\s?(want|wish|need|require)s?\s?\w*",UserInput,flags=re.IGNORECASE)):
            imsg=re.match(r"\s?I?\s?(want|wish|need|require)s?\s?\w*",UserInput,flags=re.IGNORECASE)
            mpart1 = imsg.group(1)
            msgpart1 = mpart1.replace('I','')
            msgpart1 = msgpart1.strip()
            msgpart2 = imsg.group(0)
            msgpart2 = msgpart2.replace(mpart1,'')
            msgpart2 = msgpart2.replace('I','')
            msgpart2 = msgpart2.strip()
            print("Eliza: Why do you think you "+msgpart1+" "+msgpart2+"?"+str(random.choice(responseList_ForUncomprhensibleReply)))
            continue
        #if input matches sentence like 'I love books', 'I adore beauty', 'I hate waiting'etc., then corresponding response is printed.
        elif(re.match(r"\s?I?\s?(like|love|adore|enjoy|fancy|hate)s?\s?(to)?\s(\w*)",UserInput,flags=re.IGNORECASE)):
            imsg=re.match(r"\s?I?\s?(like|love|adore|enjoy|fancy|hate)s?\s?(to)?\s(\w*)",UserInput,flags=re.IGNORECASE)
            mpart1 = imsg.group(1)
            msgpart1 = mpart1.replace('I','')
            msgpart1 = msgpart1.strip()
            msgpart2 = imsg.group(3)
            msgpart2 = msgpart2.strip()
            rlist=[r"Eliza: Why do you "+msgpart1+" "+msgpart2+"?",r"Eliza: Why do you think you "+msgpart1+" "+msgpart2+"?",r"Eliza: Did you not "+msgpart1+" "+msgpart2+" at any point in your life?"]
            print(str(random.choice(rlist)))
            continue
        #if input matches sentence like 'Because, books are expensive', 'As they are boring etc.,' then corresponding response is printed
        elif(re.match(r"(.*)?(because|since|as).*?",UserInput,flags=re.IGNORECASE)):
            print("Eliza: "+str(random.choice(responseList_Because)))
            continue
        #if user replies with Yes, then appropriate response is printed
        elif(re.match(r"(Y|y)es(.*)?",UserInput,flags=re.IGNORECASE)):
            print("Eliza: You seem really confident! "+str(random.choice(responseList_ForUncomprhensibleReply)))
            continue
        #if any uncomprehensible input is given then user is prompted to ellaborate further.
        else:
            print("Eliza: '"+UserInput+"' "+str(random.choice(responseList_ForUncomprhensibleReply)))
            continue

quit()






