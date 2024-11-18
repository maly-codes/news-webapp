#This app uses thenewsapi to retrieve news from around the world. (source: https://www.thenewsapi.com/)
from flask import Flask, request, render_template, url_for # import the Flask class to create an app
import requests
import toml 

secrets = toml.load('secrets.toml')
api_key = secrets.get("API_KEY")

# shows news from around the world, api has a limit of 3, so only 3 articles are displayed
def get_default_news():
    news_url = f'https://api.thenewsapi.com/v1/news/top?api_token={api_key}&limit=3'
    response = requests.get(news_url)
    
    if response.status_code == 200:  # Check if the request was successful
        msg = response.json()
        return msg  # Return the parsed JSON response
    else:
        print(f"Error: {response.status_code}")
        return None   
        
#shows news from a specific location
def get_news_by_locale(location):
    news_url = f'https://api.thenewsapi.com/v1/news/top?api_token={api_key}&limit=3&locale={location}'
    response = requests.get(news_url)
    
    if response.status_code == 200:  # Check if the request was successful
        msg = response.json()
        return msg  # Return the parsed JSON response
    else:
        print(f"Error: {response.status_code}")
        return None 
        
#shows news from a specific category
def get_news_by_category(category):
    news_url = f'https://api.thenewsapi.com/v1/news/top?api_token={api_key}&limit=3&categories={category}'
    response = requests.get(news_url)
    
    if response.status_code == 200:  # Check if the request was successful
        msg = response.json()
        return msg  # Return the parsed JSON response
    else:
        print(f"Error: {response.status_code}")
        return None 
        
app = Flask(__name__) # invoke the Flask class

@app.route('/',methods = ["GET","POST"])
def index():   
    news_data = get_default_news()  # Fetch the news data
    
    if news_data:  # Check if data was successfully retrieved
        news_articles = news_data['data']  # Extract titles        
    else:
        print("No news data available.")
       
    return render_template('index.html', news_articles=news_articles)
    

@app.route("/country",methods=["GET"])
def choose_country():
    return render_template('country.html')

@app.route("/category",methods=["GET"])
def choose_category():
    return render_template('category.html')
                           
@app.route("/data/country",methods=["POST"])
def show_news_by_country():
    if request.method == "POST":
        form_data = request.form
        selected_locale = form_data.to_dict()['country']
        result = get_news_by_locale(selected_locale)
        print (result)
        if result:  # Check if data was successfully retrieved
            news_articles = result['data']  # Extract titles        
        else:
            print("No news data available.")
        return render_template('data.html',form_data = form_data,news_articles = news_articles)   
        
@app.route("/data/category",methods=["POST"])
def show_news_by_category():
    if request.method == "POST":
        form_data = request.form
        selected_category = form_data.to_dict()['category']
        result = get_news_by_category(selected_category)
        print (result)
        if result:  # Check if data was successfully retrieved
            news_articles = result['data']  # Extract titles        
        else:
            print("No news data available.")
        return render_template('data.html',form_data = form_data,news_articles = news_articles)   

if __name__ == '__main__':
    app.run() 

