# SEO Content Detector

A machine learning pipeline for detecting and analyzing SEO content, including duplicate detection and quality assessment.

## Project Structure

```
seo-content-detector/
├── data/
│   ├── data.csv                    # Input dataset
│   ├── extracted_content.csv       # Parsed content
│   ├── features.csv                # Feature vectors
│   └── duplicates.csv              # Duplicate pairs
├── notebooks/
│   └── seo_pipeline.ipynb          # Main notebook
├── models/
│   └── quality_model.pkl           # Trained model
├── requirements.txt                 # Project dependencies
├── .gitignore                      # Git ignore file
└── README.md                       # This file
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your input data in `data/data.csv`
2. Open `notebooks/seo_pipeline.ipynb`
3. Run the notebook cells sequentially

## Features

- Content extraction and preprocessing
- Feature engineering
- Quality assessment
- Duplicate detection

## License

MIT