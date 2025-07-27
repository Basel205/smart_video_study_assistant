# Smart Video Study Assistant

This is a Streamlit web app that allows users to analyze YouTube videos using AI-powered tools. Simply paste a YouTube link and unlock insights such as:

* Full transcript of the video
* ELI5-style (Explain Like I'm 5) explanations
* Summaries (full or timestamped)
* Auto-generated quizzes (MCQs)
* RAG-based Q\&A system
* Downloadable output for all features

---

## How to Run Locally

1. **Clone the repository and install dependencies:**

```bash
git clone https://github.com/your-username/smart_video_study_assistant.git
cd smart_video_study_assistant
python -m venv venv

# Activate virtual environment:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

2. **Create a `.env` file and add your Together API key:**

```
TOGETHER_API_KEY=your_key_here
```

3. **Run the app:**

```bash
streamlit run main_app.py
```

---

## Features

* **Transcript Extraction**: Extracts full transcript from any YouTube video (if captions are available).
* **ELI5 Explanation**: Simplifies complex content using large language models.
* **Summarization**: Choose between timestamped chunked summaries or full context summaries.
* **Quiz Generator**: Creates MCQs with smart chunking and fallback models.
* **RAG-based Q\&A**: Ask natural language questions; system retrieves relevant transcript pieces and answers them.
* **Model Fallback**: Tries multiple free Together AI models in priority order if one fails.
* **Smart Chunking**: Uses sentence embeddings to intelligently chunk long text.
* **Download Options**: Save transcripts, explanations, summaries, and quizzes as `.txt` files.
* **Future Add-ons**: PDF export, text-to-speech reading coming soon!

---

## Project Structure

```
smart_video_study_assistant/
├── main_app.py
├── config.py
├── requirements.txt
├── .env
├── venv/
├── utils/
│   ├── explain.py
│   ├── model_fallback.py
│   ├── quiz.py
│   ├── rag_qa.py
│   ├── smart_chunking.py
│   ├── summary.py
│   └── transcript.py
```

---

## Required Files

Make sure your repo includes:

* `main_app.py` – Main Streamlit app
* `requirements.txt` – All dependencies
* `.env` – Your API key (excluded from GitHub)
* `utils/` – All helper modules

---

## .gitignore (Recommended)

Create a `.gitignore` file and add:

```
venv/
.env
__pycache__/
*.pyc
.DS_Store
```

---


## Example `requirements.txt`

This is the minimum set you need:

```
streamlit
sentence-transformers
faiss-cpu
nltk
torch
scikit-learn
numpy
requests
python-dotenv
youtube-transcript-api
```



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


---

## Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you want to propose.
