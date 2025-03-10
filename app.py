from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('E:\\Semisterss\\FInal Year Project\\My FYP Project\\StarGazer FInal Version of Project\\My try\\Complete_Dataset.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    # Get query parameters
    movie_search = request.args.get('movies', '').lower()
    rating = request.args.get('rating', type=float)
    genre = request.args.get('genre', '').lower()
    emotion = request.args.get('emotion', '').lower()
    sentiment = request.args.get('sentiment', '').lower()

    # Filter the DataFrame based on input
    filtered_df = df

    if movie_search:
        filtered_df = filtered_df[filtered_df['title'].str.lower().str.contains(movie_search)]
    
    # filtered_df = filtered_df[pd.to_numeric(filtered_df['rating'], errors='coerce').notnull()]

    if rating is not None:
            # filtered_df['rating'] = pd.to_numeric(filtered_df['rating'])  # Convert ratings to numeric, invalid entries will become NaN
            filtered_df = filtered_df[filtered_df['rating'] > rating]

    if genre:
        filtered_df = filtered_df[filtered_df['genres'].str.lower().str.contains(genre)]

    if emotion:
        filtered_df = filtered_df[filtered_df['emotion'].str.lower() == emotion]

    if sentiment:
        filtered_df = filtered_df[filtered_df['sentiment'].str.lower() == sentiment]
        
    filtered_df = filtered_df.drop_duplicates(subset='title')
        
        # Limit to top 6 movies (based on the existing order)
    filtered_df = filtered_df.head(8)

    # Convert results to a list of dictionaries for rendering
    recommendations_list = filtered_df.to_dict('records')
    

    

    # Render results
    return render_template('recommendations.html', recommendations=recommendations_list,
        movie_search= movie_search,
        rating=rating,
        genre=genre,
        emotion=emotion,
        sentiment=sentiment)


if __name__ == '__main__':
    app.run(debug=True)