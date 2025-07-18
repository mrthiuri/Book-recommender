# dependencies
import gradio as gr
import json

# data files
with open(r"data\find_title.json",'r') as file:
    book_find_title = json.load(file) # hash-map -> key=id value=book title

with open(r"data\retreive_id.json",'r') as ret:
    book_retreive_id = json.load(ret) # hash-map -> value=id key=book title

with open(r"data\all_books.json",'r') as all:
    all_books = list(json.load(all)) # list -> titles of all supported books

with open(r"data\gallery.json",'r') as gal:
    gallery_images = json.load(gal) # list -> hash-map elements -> key='label'-->value=book title -> key='image'-->value=url for cover page

with open(r"data\images.json",'r') as img:
    book_images = json.load(img) # hash-map -> key=book title value=url for cover page

# similarity matrix
with open(r"data\sim_matrix.json",'r') as sim:
    sim_matrix = json.load(sim) # has-map -> key=book id value=list or most similar books ordered in desc

# recommendation functions
def recommend_n_titles(book_read,retreive_map=book_retreive_id, matrix=sim_matrix, n=10):
    """
    Retreives the titles of the most similar books to a title previously read

    Args:
        - book_read(str): title of a book previously read
        - retreive_map(dict): key-value pairs of book id and title respectively
        - matrix(dict): key-value pairs of book id and list of 100 most similar book ids

    Returns:
        - sim_ntitles_ids(list): an array of n most similar titles ids
    """
    book_id = str(retreive_map[book_read])
    sim_ntitles_ids = matrix[book_id][:n]
    return sim_ntitles_ids

def get_recommendations(selected_book):
    """
    Retrieves the cover page images of recommended books
    """
    recoms = recommend_n_titles(selected_book)
    rec_images = [(book_images[str(title)], book_find_title[str(title)]) for title in recoms]
    return rec_images

# css
custom_css = """
/* Remove grey background and improve styling */
.gradio-container {
    background: black !important;
}

/* Style the main container */
.container {
    background: black !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding: 20px !important;
}

/* Remove grey backgrounds from groups */
.gr-group {
    background: black !important;
    border: none !important;
    box-shadow: none !important;
}

/* Style the gallery to prevent file upload prompts */
.gr-gallery {
    background: white !important;
}

/* Disable gallery file upload */
.gr-gallery .gr-file-upload {
    display: none !important;
}

/* Style buttons */
.gr-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.gr-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
}

/* Style the dropdown */
.gr-dropdown {
    border-radius: 10px !important;
    border: 2px solid #e1e5e9 !important;
}

/* Style markdown headers */
.gr-markdown h1 {
    color: #2d3748 !important;
    text-align: center !important;
    margin-bottom: 30px !important;
}

.gr-markdown h4 {
    color: #4a5568 !important;
    text-align: center !important;
    margin-bottom: 20px !important;
}

/* Gallery styling */
.gr-gallery img {
    border-radius: 10px !important;
    transition: transform 0.3s ease !important;
}

.gr-gallery img:hover {
    transform: scale(1.05) !important;
}

/* Remove any upload areas from gallery */
.gr-gallery .upload-container {
    display: none !important;
}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:

    with gr.Column() as page_1:
        gr.Markdown("# **📖Book Recommender System📖**")
        gr.Markdown("##### **For us to recommend books fitting your exquisite taste, we need to know some books you've read.**")

        input_book = gr.Dropdown(
            choices=all_books,
            interactive=True,
            label="Choose a book you enjoyed reading😊",
            container=True
        )

        get_recs_button = gr.Button("Get recommendations📚", variant="primary")

        gr.Markdown("##### **Didn't find what you were looking for😞**")
        gr.Markdown("##### **You can choose a book from some of our best rated books😊**")

        gallery = gr.Gallery(
            value=[(d['image'], d['label']) for d in gallery_images],
            columns=5,
            height="auto",
            interactive=False,
            show_label=False,
            container=True,
            allow_preview=False,
            show_share_button=False,
            show_download_button=False
        )
        gr.Markdown("**Developed by [Morgan Thiuri](https://www.linkedin.com/in/morgan-thiuri-40151327a/)**")
    with gr.Column(visible=False) as page_2:
        gr.Markdown("## **📚Your personalised recommendations📚**")

        book_title_display = gr.Textbox(
            label="Your selected book",
            interactive=False,
            container=True
        )

        gr.Markdown("#### ***Books you'd enjoy reading!❤️***")

        rec_gallery = gr.Gallery(
            height="auto",
            columns=5,
            show_label=False,
            container=True,
            allow_preview=False,
            show_share_button=False,
            show_download_button=False,
            interactive=False
        )

        back_button = gr.Button("🔙 Go back", variant="secondary")
        gr.Markdown("**Developed by [Morgan Thiuri](https://www.linkedin.com/in/morgan-thiuri-40151327a/)**")

    def handle_dropdown(selected):
        if not selected:
            return gr.update(), gr.update(), "", []
        recs = get_recommendations(selected)
        return gr.update(visible=False), gr.update(visible=True), selected, recs

    get_recs_button.click(
        fn=handle_dropdown,
        inputs=input_book,
        outputs=[page_1, page_2, book_title_display, rec_gallery]
    )

    def handle_gallery_selection(evt: gr.SelectData):
        if evt.index >= len(gallery_images):
            return gr.update(), gr.update(), "", []
        selected_label = gallery_images[evt.index]['label']
        recs = get_recommendations(selected_label)
        return gr.update(visible=False), gr.update(visible=True), selected_label, recs

    gallery.select(
        fn=handle_gallery_selection,
        outputs=[page_1, page_2, book_title_display, rec_gallery]
    )

    back_button.click(
        fn=lambda: (gr.update(visible=True), gr.update(visible=False)),
        inputs=None,
        outputs=[page_1, page_2]
    )

demo.launch(favicon_path=r"assets\favicon.png")