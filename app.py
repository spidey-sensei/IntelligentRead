import pandas as pd
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from urllib.parse import unquote


app = Flask(__name__)

df = pd.read_csv('books.csv')
df['description'] = df['description'].fillna('No Description')
df['categories'] = df['categories'].fillna('')
df['lookup_key'] = df['title'] + " by " + df['authors']
df = df.drop_duplicates(subset=['lookup_key'], keep='first')
df = df.reset_index(drop=True)
df['thumbnail_url'] = 'https://covers.openlibrary.org/b/isbn/' + df['isbn13'].astype(str) + '-L.jpg'

df['similarity'] = df['description'] + ' ' + df['categories']
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['similarity'])

cosine_simi = linear_kernel(tfidf_matrix, tfidf_matrix)

ind = pd.Series(df.index, index=df['lookup_key']).drop_duplicates()

# ind = pd.Series(df.index, index=df['title']).drop_duplicates()

#BOOK_RECOMMENDATION_SYSTEM_FUNCTION

def book_recommendations(title, top_n=6):
    indx = ind.get(title)
    # if indx is None or isinstance(indx, pd.Series):
    #     return pd.DataFrame()
    # print(df[df['lookup_key'] == "Proof by David Auburn"])
    if indx is None:
        print("DEBUG: ❌ Title not found.")
        return pd.DataFrame()
    if isinstance(indx, pd.Series):
        print("DEBUG: ⚠️ Title is duplicated in index.")
        return pd.DataFrame()
    
    #Calculate the cosine similarity of all books with the given book.
    sim = list(enumerate(cosine_simi[indx]))
    sim = sorted(sim, key=lambda x: x[1], reverse=True)
    sim = sim[1: top_n+1]
    book_ind = [i[0] for i in sim if i[0] < len(df)]  # ✅ prevent out-of-bounds

    if not book_ind:
        return pd.DataFrame()

    print("Searched title:", title)
    print(indx, title)
    print("DEBUG: index lookup for", title, "->", indx, "| Type:", type(indx))

    # print(df[df['lookup_key'] == "Proof by David Auburn"])

    # print(df[['title', 'thumbnail']].head())
    recommended_books = df.iloc[book_ind].sort_values(by='average_rating', ascending=False)
    return recommended_books[['title', 'authors', 'average_rating', 'categories', 'description', 'thumbnail_url']]




@app.route("/", methods=["GET", "POST"])
def home():
    books = df.to_dict(orient="records") 
    random_books = df.sample(n=20)
    return render_template("index.html", books=books, random_books=random_books)

@app.route("/recommend", methods=["POST"])
def recommend():
    input_str = request.form.get("book").strip()
    if " by " in input_str:
        title, author = input_str.split(" by ", 1)
    else:
        title, author = input_str, ""

    
    
    num_recs = int(request.form.get("num_recs", 5))
    lookup_key = f"{title} by {author}"
    recs = book_recommendations(lookup_key, num_recs)
    return render_template("recommendations.html", book_title=title, book_author=author, recommendations=recs)


@app.route("/genre/<genre>")
def genre_page(genre):
    genre_books = df[df['categories'].str.contains(genre, case=False, na=False)]
    top_books = genre_books.sort_values(by = 'average_rating', ascending=False).head(10)
    return render_template("genre.html", genre=genre, books=top_books)

@app.route('/book/<title>')
def book_detail(title):
    book_data = df[df['title'] == title]
    book = book_data.iloc[0]
    previous_url = request.referrer or "/"
    random_books = df[df['title'] != title].sample(n=10)

    return render_template('book_detail.html', book=book, previous_url=previous_url, random_books=random_books)





if __name__ == "__main__":
    app.run(debug=True)

