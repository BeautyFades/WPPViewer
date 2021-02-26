import time, datetime
import csv
import matplotlib as mpl
import pandas as pd
import emoji
import operator
import string
import numpy as np


### GLOBAL SETTINGS ###
# name of WhatsApp chat history CSV file to open:
filename = 'myhalfcsv.csv'
user = 'Fellipe'
partner = 'Isabela'

date_format = "%d/%m/%Y, %H:%M:%S"

### GLOBAL VARS ###
#Total messages in file
results = pd.read_csv(filename)
totalMessages = (len(results))

### FUNCTIONS ###

def convertToTimezone(t):
    #Cutting the milisseconds off of CSV file and converting to int
    t = t[0:-3]
    t = int(t)

    #Conversion to readable time
    convertedTime = datetime.datetime.fromtimestamp(t).strftime(date_format)
    return convertedTime

def grabNumber(n):
    messageNumber = int(n)
    return messageNumber

def whoSent(w):
    person = int(w)
    if person == 0:
        return (f"{partner} enviou")
    else:
        return (f"{user} enviou")

def grabData(d):
    return d

### TEXTS PER DAY FUNCTION ###

def textsPerDay():
    with open(filename, mode = 'r+', encoding="utf8") as csv_file:
        csvReader = csv.DictReader(csv_file)
        lineCount = 0
        for row in csvReader:
            if lineCount == 0:
                print(f'Column names are {", ".join(row)}')
                lineCount += 1
            else:
                #currentNumber = row['number']
                #currentKey = row['key_from_me']
                #currentData = row['data']
                currentTime = row['timestamp']
                # print(grabNumber(currentNumber))
                # print(convertToTimezone(currentTime))
                # print(whoSent(currentKey))
                # print(grabData(currentData))
                # print('\n')
                # If we're on first line, grab date from first message
                if lineCount == 1:
                    d0 = convertToTimezone(currentTime)
                    d0day = int(d0[0:2])
                    d0month = int(d0[3:5])
                    d0year = int(d0[6:10])
                    d0 = datetime.date(d0year, d0month, d0day)
                    #print(d0)

                lineCount += 1

                #Get time from last message
                if lineCount == totalMessages-1:
                    d1 = convertToTimezone(currentTime)
                    d1day = int(d1[0:2])
                    d1month = int(d1[3:5])
                    d1year = int(d1[6:10])
                    d1 = datetime.date(d1year, d1month, d1day)
                    #print(d1)

        #Calculating
        delta = d1 - d0
        perDay = round(totalMessages/delta.days,2)
        print(f"You've been texting for {delta.days} days, for a total of {totalMessages} messages, which averages out to {perDay} messages a day.")

### WHO TEXTS MORE FUNCTION ###

def textsPerPerson():
    with open(filename, mode = 'r+', encoding="utf8") as csv_file:
        csvReader = csv.DictReader(csv_file)
        listUser = []
        listPartner = []
        for row in csvReader:
                currentNumber = row['number']
                currentKey = row['key_from_me']
                if currentKey == "number":
                    print(f'Column names are {", ".join(row)}')

                # Append list of messages sorted by who sent them
                if currentKey == "0":
                    listPartner.append(currentNumber)
                if currentKey == "1":
                    listUser.append(currentNumber)

        #print(listPartner)
        #print(listUser)
        lenU = len(listUser)
        userPercentage = round((lenU/totalMessages)*100,2)
        partnerPercentage = 100-userPercentage
        #print(userPercentage, partnerPercentage)


        print(f'{user} sent a total of {len(listUser)} messages and {partner} send a total of {len(listPartner)} messages. That equates to {userPercentage}% sent by {user} and {partnerPercentage}% sent by {partner}.')

### MOST COMMON WORDS BY PERSON ###

def WordsByPerson():
    with open(filename, mode = 'r+', encoding="utf8") as csv_file:
        csvReader = csv.DictReader(csv_file)
        DataUser = []
        DataPartner = []
        wordsUser = []
        wordsPartner = []
        for row in csvReader:
                currentKey = row['key_from_me']
                currentData = row['data']
                if currentKey == "number":
                    print(f'Column names are {", ".join(row)}')

                # Append list of messages sorted by who sent them
                if currentKey == "0":
                    DataPartner.append(currentData)
                if currentKey == "1":
                    DataUser.append(currentData)

        #print(DataPartner)
        #print('\n')
        #print(DataUser)
        for elem in DataUser:
            s = elem.split()
            wordsUser.append(s)

        for elem in DataPartner:
            s = elem.split()
            wordsPartner.append(s)

        # Flattening list so all words are in a single list
        flatUser = [item for sublist in wordsUser for item in sublist]
        flatPartner = [item for sublist in wordsPartner for item in sublist]
        #print(flatUser[0])
        #print(flatPartner[0])

        # Calculating
        wordsTextedbyUser = len(flatUser)
        wordsTextedbyPartner = len(flatPartner)
        totalWordsMessaged = wordsTextedbyPartner + wordsTextedbyUser
        textedByUserPercent = round(wordsTextedbyUser/totalWordsMessaged*100, 2)
        textedByPartnerPercent = round(100-textedByUserPercent, 2)
        print(f"{user} texted a total of {wordsTextedbyUser} words, and {partner} has texted a total of {wordsTextedbyPartner} words. This means that {textedByUserPercent}% of all words were from {user} and {textedByPartnerPercent}% of all words were from {partner}")



### RUNNING ###
textsPerDay()
textsPerPerson()
WordsByPerson()



