from bs4 import BeautifulSoup

with open('WebScrapingTutorial/simple.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

#print(soup.prettify()) # This funtion essentially prints out the entire page with a prettified HTML format

#match = soup.title # You can access the tags essentially like attributes 
#print(match.getText()) # The attributes also have getters, so one can get the string value of the title 

match2 = soup.find('div') 
print(match2)
match2 = soup.find('div', class_='footer') #class is a special keyword in python and can be used to find specific compoennets with the class tag in html
print(match2)

#Note that the divs that are found in these two cases are actually different due to the added keyword

for article in soup.find_all('div', class_='article'): # find_all returns a lsit of all the div-components with class article
    headline = (article.h2.a.text) # the headlines were wrapped inside anchor tags within h2 tags, hence this fetch
    print(headline)

    summary = article.p.text # the summary is found in the p tag. 
    print(summary)

    print()

