# SEO Content Quality & Duplicate Detector

## 1. Project Overview
This project is a complete machine learning pipeline built to analyze web content for SEO (Search Engine Optimization) quality. The system parses raw HTML from a provided dataset, engineers a set of NLP features, detects near-duplicate content, and finally trains a classification model to score content quality as 'High', 'Medium', or 'Low'. The entire pipeline is built in a single Jupyter Notebook (`seo_pipeline.ipynb`) as required.

## 2. Setup Instructions
To run this project, first clone the repository and set up the Python environment.

```bash
# 1. Clone the repository
git clone [https://github.com/your-username/seo-content-detector](https://github.com/your-username/seo-content-detector)
cd seo-content-detector

# 2. Create and activate a virtual environment
python -m venv venv
# On Mac/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# 3. Install the required dependencies
pip install -r requirements.txt
```

You will also need to download the 'punkt' tokenizer from NLTK:

```python
import nltk
nltk.download('punkt')
```

## 3. Quick Start
The entire analysis can be run from top to bottom using the main Jupyter Notebook.

1.  Place the provided `data.csv` file into the `data/` folder.
2.  Launch the Jupyter Notebook:
    ```bash
    jupyter notebook notebooks/seo_pipeline.ipynb
    ```
3.  Inside the notebook, click **"Cell" > "Run All"**.

This will execute the full pipeline, generating the following output files in the `data/` folder:
* `extracted_content.csv`
* `features.csv`
* `duplicates.csv`

It will also compare two models, save the best one to `models/quality_model.pkl`, and save the confusion matrix plot as `confusion_matrix.png`.

## 4. Key Decisions
This project involved several key technical decisions to meet the assignment requirements:

* **HTML Parsing:** Used **`BeautifulSoup`** to parse HTML. To isolate meaningful content, common non-text tags (`script`, `style`, `nav`, `header`, `footer`) were explicitly removed before text extraction.
* **Feature Engineering:** Utilized **`textstat`** for the `flesch_reading_ease` score and **`scikit-learn`'s `TfidfVectorizer`** for keyword extraction. The resulting TF-IDF vectors were also efficiently reused as the 'embeddings' for similarity calculation.
* **Duplicate Detection:** Implemented **`cosine_similarity`** on the TF-IDF vectors. A threshold of **`0.80`** was chosen as a balance to identify near-duplicates without flagging articles that are only topically related.
* **Model Selection:** Both a **`RandomForestClassifier`** and a **`LogisticRegression`** model were trained and compared. The `RandomForestClassifier` was chosen as the final model due to its significantly higher accuracy (90.5% vs 76.2%).

## 5. Results Summary
The final `RandomForestClassifier` model performed exceptionally well on the test set and substantially outperformed the rule-based baseline.

* **Model Performance Comparison:**
    * **Winning Model (Random Forest): 90.5% Accuracy**
    * Logistic Regression: 76.2% Accuracy
    * Word Count Baseline: 47.6% Accuracy

* **Winning Model Metrics (Random Forest):**
    * **Overall Accuracy:** 90.5%
    * **Weighted Avg F1-Score:** 0.90
    * The model is **perfect at identifying `Low` quality content** (1.00 recall).
    * The primary source of error was one `High` page being misclassified as `Medium` and one `Medium` page as `Low`.

* **Top Features:** Readability was the most significant predictor of quality.
    1.  **`flesch_reading_ease`** (Importance: 0.508)
    2.  **`word_count`** (Importance: 0.262)
    3.  **`sentence_count`** (Importance: 0.231)
* **Duplicates Found:** [
* Total pages analyzed: 69
* Duplicate pairs found (>80.0%): 13
* Thin content pages (<500 words): 14 (20.29%)
]

## 6. Limitations
* **Synthetic Labels:** The model is trained on "synthetic" labels based on simple rules (word count, readability). Real-world SEO quality is far more nuanced and would require a human-labeled dataset to capture concepts like "user intent" or "expertise."
* **Small Dataset:** The model's performance, especially for the `High` quality class (which only had 3 test samples), is based on a very small dataset. Its ability to generalize to a wider variety of web pages is unproven.
* **Static HTML Parsing:** The `BeautifulSoup` parser only works on the static HTML provided. It would fail to extract content from modern, JavaScript-heavy websites that load their content dynamically.