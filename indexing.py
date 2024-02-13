#-------------------------------------------------------------------------
# AUTHOR: Brandon Diep
# FILENAME: indexing.py
# SPECIFICATION: This program will read the file collection.csv and output the tf-idf document-term matrix
# FOR: CS 4250- Assignment #1
# TIME SPENT: 12 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#Importing some Python libraries
import csv
import math

# holds the sentences or rows in the csv file
documents = []

# holds the list of terms with stoppage removal from each document to be inserted into docTerms
termList = []

# holds the terms of each document with stoppage removal
docTerms = []

# holds the number of documents
numOfDocs = 0

# Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append(row[0])
            numOfDocs += 1

# Conducting stopword removal. Hint: use a set to define your stopwords.
# --> add your Python code here
stopWords = {"I", "and", "She", "her", "They", "their", "and"}
for sentence in documents:
    words = sentence.split()
    termList = []
    for word in words:
        if word not in stopWords and word not in termList:
            termList.append(word)
    docTerms.append(termList)
# print(docTerms)

#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
#--> add your Python code here
stemming = {}

# holds the number of terms in each document in a list
totalDocTerms = []

# holds the number of terms in a specific document
totalTerms = 0
suffix = 's'

# stemming for loop
for docTerm in docTerms:
    totalTerms = 0
    for term in docTerm:
        totalTerms += 1
        if term.endswith(suffix):
            termWithoutSuffix = term[:-len(suffix)]
            if termWithoutSuffix in stemming:
                stemming[termWithoutSuffix].append(term)
            else:
                if term not in stemming:
                    stemming[term] = [term]
        if not term.endswith(suffix):
            if (term + suffix) in stemming:
                stemming[term + suffix].append(term)
            else:
                if term not in stemming:
                    stemming[term] = [term]
    totalDocTerms.append(totalTerms)
# print(stemming)

#Identifying the index terms.
#--> add your Python code here
terms = []
for words in stemming.values():
    terms.append(words)
# print(terms)

# creates the matrix size
columns = 0
for term in stemming.items():
    columns += 1
# holds the occurrence of specific term in each document
numOfSpecificTermInDocs = [[0] * columns for _ in range(columns)]

# matrix counting the occurrence of a term in document
count = 0
for i, docTerm in enumerate(docTerms):
    for term in docTerm:
        for j, words in enumerate(terms):
            if term in words:
                numOfSpecificTermInDocs[i][j] += 1

# print(numOfSpecificTermInDocs)
# print(totalDocTerms)

#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here
docTermMatrix = [[0.0] * columns for _ in range(columns)]
# holds the idf for each term
idfList = []
# holds the tf
tfList = []
# holds the tf for each document
tfListMatrix = []
# holds the number of docs that include this term
numOfDocsWithThisTerm = 0

# calculates tf(t, d) and idf(t, D)
for i, rowTermInDocCount in enumerate(numOfSpecificTermInDocs):
    numOfDocsWithThisTerm = 0
    tfList = []
    for j, count in enumerate(rowTermInDocCount):
        tfList.append(numOfSpecificTermInDocs[j][i] / totalDocTerms[j])
        numOfDocsWithThisTerm += numOfSpecificTermInDocs[j][i]
    tfListMatrix.append(tfList)
    idfList.append(math.log((numOfDocs / numOfDocsWithThisTerm), 10))
# print(tfListMatrix)
# print(idfList)


#Printing the document-term matrix.
#--> add your Python code here

# multiplies tf(t, d) * idf(t, D)
for i, idf in enumerate(idfList):
    for j, tf in enumerate(tfListMatrix):
        docTermMatrix[j][i] = tfListMatrix[i][j] * idf

print("Document Term Matrix: ")
for row in docTermMatrix:
    print('[', end='')
    for i, tf_idf in enumerate(row):
        if i < len(row) - 1:
            print(f'{tf_idf:.5f}, ', end='')
        else:
            print(f'{tf_idf:.5f}', end='')
    print(']')



