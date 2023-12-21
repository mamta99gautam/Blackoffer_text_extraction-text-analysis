#!/usr/bin/env python
# coding: utf-8

# # Code for Text analysis

# #  Installation and import libraries

# In[ ]:


#Installation required to run this code successfully
get_ipython().system('pip install textstat==0.6.2')
get_ipython().system('pip install textstat textblob')


# In[ ]:


#Import required modules
import os
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from textstat.textstat import textstatistics
from textstat import textstat


# In[ ]:


# Download the punkt tokenizer data
nltk.download('punkt')


# # Define function to read each file of stop words 

# In[ ]:


# Define the function
def load_stop_words(file_paths, encoding='utf-8'):
    stop_words = set()
    for file_path in file_paths:
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            stop_words.update(f.read().splitlines())
    return stop_words


# # Specify the path for all master dictionary text files

# In[ ]:


#define path for master distionary
positive_words=r"C:\Blackoffer\positive-words.txt"
negative_words=r"C:\Blackoffer\negative-words.txt"
StopWords_Names=r"C:\Blackoffer\StopWords_Names.txt"
StopWords_Geographic=r"C:\Blackoffer\StopWords_Geographic.txt"
StopWords_GenericLong=r"C:\Blackoffer\StopWords_GenericLong.txt"
StopWords_Generic=r"C:\Blackoffer\StopWords_GenericLong.txt"
StopWords_DatesandNumbers=r"C:\Blackoffer\StopWords_DatesandNumbers.txt"
StopWords_Currencies=r"C:\Blackoffer\StopWords_Currencies.txt"
StopWords_Auditor=r"C:\Blackoffer\StopWords_Auditor.txt"


# # Load stop,positive and negative words from files

# In[ ]:


# Load positive and negative words
with open(positive_words, 'r') as f:
    positive_words = set(f.read().splitlines())

with open(negative_words, 'r') as f:
    negative_words = set(f.read().splitlines())

# Load stop words from multiple files
stop_words_files = [
    StopWords_Names,
    StopWords_Geographic,
    StopWords_GenericLong,
    StopWords_Generic,
    StopWords_DatesandNumbers,
    StopWords_Currencies,
    StopWords_Auditor,
]


# # Function call to get stop words

# In[ ]:


#Call the function to get the stop words
stop_words = load_stop_words(stop_words_files)


# # Import the path of text files

# In[ ]:


# Specify the directory where your text files are located
texts_directory_path = r"C:\\Blackoffer\\text_files\\"


# # Import the path of Input file

# In[ ]:


# Read URLs from the Excel file
urls_excel_path = r'C:\Blackoffer\Input.xlsx'  # Provide the correct path to your URLs Excel file
urls_df = pd.read_excel(urls_excel_path)


# # Create dataframe to store the final result with column names

# In[ ]:


# Create a DataFrame to store the results
results_df = pd.DataFrame(columns=[
    'URL_ID',
    'URL',
    'POSITIVE SCORE',
    'NEGATIVE SCORE',
    'POLARITY SCORE',
    'SUBJECTIVITY SCORE',
    'AVG SENTENCE LENGTH',
    'PERCENTAGE OF COMPLEX WORDS',
    'FOG INDEX',
    'AVG NUMBER OF WORDS PER SENTENCE',
    'COMPLEX WORD COUNT',
    'WORD COUNT',
    'SYLLABLE PER WORD',
    'PERSONAL PRONOUNS',
    'AVG WORD LENGTH'
])


# # Compute different variables(text analysis) using for loop from each text file

# In[ ]:


# Loop through each URL and perform analysis
for index, row in urls_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    # Load text from the file
    file_name = f'{url_id}.txt'
    file_path = os.path.join(texts_directory_path , file_name)
    
    # Checks if current file_path is present in the text files of texts_directory_path 
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            

        # Tokenize the text
        tokens = word_tokenize(text.lower())

        # Remove stop words
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

        # Calculate positive and negative scores
        positive_score = sum(1 for word in filtered_tokens if word in positive_words)
        negative_score = sum(1 for word in filtered_tokens if word in negative_words)

        # Calculate polarity and subjectivity scores using TextBlob
        blob = TextBlob(text)
        polarity_score = blob.sentiment.polarity
        subjectivity_score = blob.sentiment.subjectivity

        # Calculate additional variables
        word_count = len(filtered_tokens)
        sentence_count = len(sent_tokenize(text))
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

        # Calculate percentage of complex words
        complex_words = [word for word in filtered_tokens if textstat.syllable_count(word) > 2]
        percentage_complex_words = (len(complex_words) / word_count) * 100 if word_count > 0 else 0

        # Flesch-Kincaid Readability Tests
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

        # Personal Pronouns (assuming personal pronouns are 'he', 'him', 'his', 'she', 'her', 'hers', 'I', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours')
        personal_pronouns = ['he', 'him', 'his', 'she', 'her', 'hers', 'I', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']
        personal_pronoun_count = sum(1 for word in filtered_tokens if word.lower() in personal_pronouns)

        # Average word length
        avg_word_length = sum(len(word) for word in filtered_tokens) / word_count if word_count > 0 else 0

        # Average number of words per sentence
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0

        # Calculate syllable per word
        syllable_per_word = sum(textstat.syllable_count(word) for word in filtered_tokens) / word_count if word_count > 0 else 0

        # Append the results to the DataFrame
        single_result_df = pd.DataFrame({
            'URL_ID': url_id,
            'URL': url,
            'POSITIVE SCORE': positive_score,
            'NEGATIVE SCORE': negative_score,
            'POLARITY SCORE': polarity_score,
            'SUBJECTIVITY SCORE': subjectivity_score,
            'AVG SENTENCE LENGTH': avg_sentence_length,
            'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
            'FOG INDEX': fog_index,
            'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sentence,
            'COMPLEX WORD COUNT': len(complex_words),
            'WORD COUNT': word_count,
            'SYLLABLE PER WORD': syllable_per_word,
            'PERSONAL PRONOUNS': personal_pronoun_count,
            'AVG WORD LENGTH': avg_word_length
        }, index=[0])
        results_df = pd.concat([results_df, single_result_df], ignore_index=True)


# # Specify the directory path to store final output

# In[ ]:


# Specify the path for the output Excel file
output_excel_path = r'C:\Blackoffer\Output.xlsx'

# Save the results DataFrame to an Excel file
results_df.to_excel(output_excel_path, index=False)


# In[ ]:




