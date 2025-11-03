# SEO Content Quality & Duplicate Detector

## Project Overview
An advanced machine learning pipeline for analyzing web content quality and detecting duplicates. The system analyzes web pages for SEO quality, computes content similarity, and provides detailed readability metrics. Features a fully functional Streamlit interface for real-time content analysis and a comprehensive Jupyter notebook demonstrating the complete analysis pipeline.

## Live Demo
🔗 [Access the live Streamlit app](https://seo-content-detector.streamlit.app)

## Features
- Real-time web content analysis
- SEO quality scoring using ML models
- Duplicate content detection
- Readability metrics calculation
- Keyword extraction and analysis
- Interactive visualizations
- Content similarity matching

## Project Structure
```
seo-content-detector/
├── data/
│   ├── data.csv                  # Dataset with URLs and content
│   ├── extracted_content.csv     # Parsed and cleaned content
│   ├── features.csv             # Extracted features for analysis
│   └── duplicates.csv           # Identified duplicate pairs
├── notebooks/
│   └── seo_pipeline.ipynb       # Main analysis notebook
├── models/
│   └── tfidf_matrix.npy        # TF-IDF vectorizer model
├── streamlit_app/
│   ├── app.py                   # Main Streamlit application
│   ├── utils/
│   │   ├── parser.py           # HTML parsing utilities
│   │   ├── features.py         # Feature extraction
│   │   └── scorer.py           # Quality scoring and ML models
│   └── models/                  # Saved ML models
├── requirements.txt             # Project dependencies
└── README.md                    # Documentation
```

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/drMy5tery/Lead-Walnut.git
cd Lead-Walnut
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the analysis notebook:
```bash
jupyter notebook notebooks/seo_pipeline.ipynb
```

5. Run the Streamlit app locally:
```bash
cd streamlit_app
streamlit run app.py
```

## Key Technical Decisions

### Libraries and Tools
- **BeautifulSoup4**: Chosen for robust HTML parsing and content extraction
- **NLTK & TextStat**: Used for advanced text analysis and readability scoring
- **Scikit-learn**: Implements ML models and TF-IDF vectorization
- **Streamlit**: Powers the interactive web interface for real-time analysis

### Content Analysis Approach
- **HTML Parsing**: Uses intelligent content extraction focusing on main article content
- **Feature Engineering**: Combines traditional readability metrics with ML-based features
- **Similarity Detection**: TF-IDF vectorization with cosine similarity (threshold: 0.80)
- **Quality Scoring**: Random Forest classifier with manual labeling for supervised learning

## Results Summary

### Model Performance
- **Overall Accuracy**: 78%
- **F1-Score**: 0.77 (weighted average)
- **Baseline Improvement**: +14% over word-count only baseline

### Content Analysis
- Successfully processed 60+ web pages
- Identified 3 sets of duplicate content
- Average processing time: ~2 seconds per URL

### Quality Distribution
- High Quality: 35%
- Medium Quality: 45%
- Low Quality: 20%

## Limitations
- Limited to text content analysis (no image or multimedia evaluation)
- May require adjustments for non-English content
- Processing time increases with page complexity

## Future Enhancements
- Add support for multiple languages
- Implement advanced NLP features (sentiment analysis, topic modeling)
- Enhance duplicate detection with semantic similarity
- Add batch processing capabilities

## Acknowledgments
- Dataset provided via Kaggle: [SEO Content Analysis Dataset](https://www.kaggle.com/datasets/naveen1729/dataset-for-assignment)
- Built as part of the Data Science / AI/ML Engineer assessment

## License
This project is licensed under the MIT License - see the LICENSE file for details.