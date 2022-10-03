from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests
import numpy as np


#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs={'class':'lister-list'})
content = table.find_all("div", attrs={'class':'lister-item-content'})

row_length = len(content)

temp = [] #initiating a list 

for i in range(0, row_length):
    
    # Titles
    titles = content[i].find('a').text
        
    # Ratings and Metascores
    imdb_ratings = content[i].find('strong')
    if imdb_ratings is not None:
        imdb_ratings = imdb_ratings.text
    else: imdb_ratings = np.nan
    imdb_metascores = content[i].find('span', attrs={'class':'Metascore mixed'})
    if imdb_metascores is not None:
        imdb_metascores = imdb_metascores.text
    else: imdb_metascores = np.nan
    
    # Votes
    imdb_votes = content[i].find('span', attrs={'name':'nv'})
    if imdb_votes is not None:
        imdb_votes = imdb_votes.text.replace(',','')
    else: imdb_votes = np.nan
    
    temp.append((titles, imdb_ratings, imdb_metascores, imdb_votes))
    





temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns=['Title', 'Rating', 'Metascore', 'Votes'])
#insert data wrangling here
data[['Rating', 'Metascore', 'Votes']] = data[['Rating', 'Metascore', 'Votes']].astype('float64')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["Metascore"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)