import flask
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = flask.Flask(__name__, template_folder='templates')

df = pd.read_csv('./model/newData3.csv')

#Create a function to combine the values of the important columns into a single string
def get_important_features(data):
  important_features = []
  for i in range(0, data.shape[0]):
    important_features.append(data['title'][i])
  return important_features

df['important_features'] = get_important_features(df)

#Convert the text to a matrix of token counts
cm = CountVectorizer().fit_transform(df['important_features'].values.astype('U'))
#Get the cosine similarity matrix from the count matrix 
cs = cosine_similarity(cm)

# df2 = df2.reset_index()
indices = pd.Series(df.index, index=df['title'])
all_titles = [df['title'][i] for i in range(len(df['title']))]

# Set up the main route
@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
            
    if flask.request.method == 'POST':
        m_name = flask.request.form['smartwatch_name']
        title = m_name.title()
   
        #Get the title of the smartwatch that the user likes
        # title = 'BT01 Smart Watch Body IP68 Waterproof Heart Rate Fitness Tracker'
    
        if title not in all_titles:
              return(flask.render_template('negative.html',name=m_name))
        else:  
            smartwatch_id = df[df.title == title]['smartwatch_id'].values[0]
            print(smartwatch_id)
            #Create a list of enumerations for the similarity score (list of tuples) [(smartwatch_id, similarity score), (...)]
            scores =  list(enumerate(cs[smartwatch_id]))
            #Sort the list
            sorted_scores = sorted(scores, key = lambda x:x[1], reverse=True)
            sorted_scores = sorted_scores[1:]
            #Create a loop to print the first 7 similar 
            j=0
            titles=[]
            urls=[]
            prices=[]
            for item in sorted_scores:
                sm_title = df[df.smartwatch_id == item[0]]['title'].values[0]
                sm_url =  df[df.smartwatch_id == item[0]]['url'].values[0]
                sm_price =  df[df.smartwatch_id == item[0]]['price'].values[0]
                # print(j+1, sm_title)
                j = j + 1
                smt_name = titles.append(sm_title)
                smt_url = urls.append(sm_url)
                smt_price = prices.append(sm_price)
                if j>6:
                    break

        return flask.render_template('positive.html',smartwatch_names=titles, smartwatch_url=urls, smartwatch_price=prices, search_name=m_name)



if __name__ == '__main__':
    app.run()