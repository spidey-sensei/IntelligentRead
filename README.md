# IntelligentRead

**IntelligentRead** is a book recommendation system which displays the top-rated books of the selected genre or book-title.

## 🚀 Features

- Search for books by title or select a genre
- Displays book covers 
- Web app powered by Flask 
- Suggests similar books using content-based filtering model

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, Jinja2 (Flask)
- **Backend**: Python, Flask 
- **Data Processing**: pandas, NumPy, scikit-learn
- **Recommender Engine**: Content-based filtering (TF-IDF / cosine similarity)
- **Deployment**: Localhost / Render 

## 📁 Folder Structure

```bash
intelligentread/
│
├── app.py                   # Main application file (Flask entry point)
├──books.csv                 # Dataset used
├── templates/               # HTML templates (for Flask)
│   ├──index.html
│   ├──recommendations.htmt
│   ├──genre.html
│   └──book_detail.html
├── static/                  # Static files (images, CSS)
│   ├──index.jpeg
│   ├──logo.jpg
│   ├──index.css
│   ├──recommendations.css
│   ├──genre.css
│   ├──book_detail.css
│   └──header.css            #common header on all pages 
├── requirements.txt         # Python dependencies
└── README.md                # You're here!
