from bs4 import BeautifulSoup
import requests
import csv 

source = requests.get('http://coreyms.com').text

soup = BeautifulSoup(source,'lxml')

csv_file = open('cms_scrape.csv','w') #Open a file for writing
csv_writer = csv.writer(csv_file) #Create a contextwriter. 
csv_writer.writerow(['headline','summary','video_link']) #Initially creates the first rows to be headline, summary, videolink

for article in soup.find_all('article'):
    headline = article.h2.a.text
    print(headline)

    summary = article.find('div',class_="entry-content")
    print(summary.p.text)
    # Now let's extract an embedded youtube link
    # Note that we put everything in a try-expect block in order to make sure that the code still runs if something unexpected happens (such as a page not having the same format as expected, etc.)
    try:
        vid_component = article.find('iframe',class_='youtube-player') # This gives us the tag itself as one would expect, that is the iframe tag.

        #Now, to get the youtube link, we need to get teh src.part of the tag which can be accessed like a dictionary

        vid_src = vid_component['src'] #This gave an embedded youtubeLink. We just want the regular youtube link itself, which means we need to aprse the link

        vid_id = vid_src.split('/')[4].split('?')[0] # The first split splits the URL on all the forward slashes. The fourth element gives the query of the URL. From there, one can split it again on the ?, in which the first part there gives the youtube video ID. THis is how a youtube video query is made. 

        yt_link = f'https://youtube.com/watch?v={vid_id}' # This is the typical youtube link URL 
    except Exception as e:
        yt_link = None

    print(yt_link)
    print()

    csv_writer.writerow([headline,summary,yt_link])

csv_file.close()
#Now, just wrap everything in a find_all by article, loop over each to scrape the entire website on the page. 