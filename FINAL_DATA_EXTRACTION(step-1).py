#!/usr/bin/env python
# coding: utf-8

# # Code for text extraction
# - There are maily two classes which are used here to extract text from URLs<br>
#    1)'td-post-content tagdiv-type'<br>
#    2)'tdb-block-inner td-fix-index'<br>
# - There are two files giving status code error<br>
#    URL_ID:<br>
#    1)blackassign0036<br>
#    2)blackassign0049<br>
# - There are also two files having issue in extracting article text <br>
#    URL_ID:<br>
#    1)blackassign0099<br>
#    2)blackassign0100

# # Import libraries

# In[5]:


#Importing libraries
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


# # Function to extract text

# In[13]:


#Define function  to extract article title and text from url
def extract_article_text(url, article_classes):
    # Make a request to the URL
    response = requests.get(url)

    if response.status_code == 200: #checks whether website gives error or not as in URL_id=36 and 49 gives error
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the article title
        article_title = soup.title.text.strip()

        # Try the first class
        article_body = soup.find('div', class_=article_classes[0])

        # If the first class is not found then try the second class
        if not article_body:
            article_body = soup.find('div', class_=article_classes[1])

        if article_body:
            paragraphs = article_body.find_all(['p'])
            article_text = '\n'.join([paragraph.text.strip() for paragraph in paragraphs])

            return f"{article_title}\n\n{article_text}"
        else:
            print(f"Article body not found in {url} with given class")
            return None
    else:
        print(f"Gives OOOps error 404 from {url}. Status code: {response.status_code}")
        return None


# # Import the Input excel file

# In[7]:


# Read URLs from the Excel file
excel_file_path = r"C:\Blackoffer\Input.xlsx"
df = pd.read_excel(excel_file_path)


# ![image.png](attachment:image.png)

# # Classes used to extract text from url

# In[9]:


# Classes to use in extract_article_text function
article_classes_to_try = ['td-post-content tagdiv-type', 'tdb-block-inner td-fix-index']


# # Path of file where you want to save extracted text files

# In[17]:


# Specify the file path where you want to save the text files
save_file_path = r"C:\Blackoffer\text_files"


# # Function call using for loop to extract text and save it with its url_id

# In[ ]:


# Iterate through the list of URLs
for index, row in df.iterrows():
    url = row['URL'] #'URL' column for current row
    url_id = row['URL_ID'] # assign current url_id for each url so that can use in defining name of text file

    # Extract article title and text for the current URL using the specified classes
    article_content = extract_article_text(url, article_classes_to_try) #function call

    if article_content: #if article_content variable is true then write the path name and sa
        # Save the article content to a text file in the specified directory
        file_path = os.path.join(save_file_path, f'{url_id}.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(article_content)

        print(f"Article content for {url_id} saved to {file_path}.")


# ![image.png](attachment:image.png)
