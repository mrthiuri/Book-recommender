# 📚 **Book Recommender System**

Book recommender using [Goodreads](https://www.goodreads.com) dataset and cosine similarity with NLP-based content filtering.

## 🚀 **Features**
- 🎯 Smart Content-Based Filtering – Uses cosine similarity on TF-IDF features to deliver personalized book recommendations based on your reading preferences.
- 🎨 Clean Gradio Interface – Intuitive, responsive, and beautifully designed UI that runs in the browser with zero setup.
- 📚 Real Goodreads Dataset – Built on real-world data from thousands of Goodreads users, ensuring meaningful and reliable recommendations.
- ⚡ Lightweight & Fast – Optimized for speed and minimal resource usage, delivering instant recommendations

## 📁 **Dataset**

This recommender system is built using a curated subset of the **Goodreads Books Dataset** (approximately 10,000 books). The dataset is stored in `data/goodbooks-dataset.csv`.

To improve recommendation accuracy, preprocessing and feature engineering were performed on book descriptions, titles and tag lines to generate a **TF-IDF matrix**. This sparse matrix forms the basis of the cosine similarity computations.

To ensure fast and smooth functionality, key data structures are precomputed and stored as `.json` files in the `data/` directory:

- `all_books.json` — All supported book titles
- `find_title.json` — Retrieve book titles using book IDs
- `gallery.json` — Maps book IDs to cover page image links
- `images.json` — Retrieve image links for given book IDs
- `most_read.json` — Contains some of the highest-rated books
- `retreive_id.json` — Retrieve book IDs using titles
- `sim_matrix.json` — Contains top 100 similar books (per title) based on cosine similarity scores

## 🧠 How It Works

The system uses **TF-IDF vectorization** on a combination of book titles, descriptions and tag lines to compute **cosine similarity** between them. Given a book the user enjoyed (or selects from top-rated books), the system recommends similar books based on content similarity.

📌 For a more detailed breakdown of the entire process — including data preprocessing, TF-IDF modeling and similarity computation check out the [`book_recommender.ipynb`](assets/book_recommender.ipynb) notebook in the `assets/` directory.

## 🔗 Live Demo

Try the app live on [Hugging Face Spaces](https://huggingface.co/spaces/mrthiuri/book_recommender)

## ▶️ Run the App Locally

```bash
git clone https://github.com/your-username/book-recommender.git
cd book-recommender
pip install -r requirements.txt
python app/recommender.py
