import streamlit as st
import sys
import os
import json
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.parser import scrape_url, parse_html
from utils.features import extract_features, extract_keywords, get_tfidf_vector
from utils.scorer import (
    load_model, load_encoder, predict_quality, 
    find_similar_content, create_quality_label_manual
)

#setup page
st.set_page_config(
    page_title="SEO Content Quality Analyzer",
    layout="wide"
)

#make it look nice
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .metric-card span {
        font-size: 1.2rem;
        display: block;
        margin-top: 0.5rem;
    }
    .quality-high {
        color: #28a745;
        font-weight: bold;
    }
    .quality-medium {
        color: #ffc107;
        font-weight: bold;
        text-shadow: 0 0 1px rgba(0,0,0,0.3);
    }
    .quality-low {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

#main title
st.markdown('<h1 class="main-header">SEO Content Quality Analyzer</h1>', unsafe_allow_html=True)

st.markdown("""
Check your content's SEO quality and find duplicates.
Just paste a URL below to get started.
""")

# Load models
@st.cache_resource
def load_models():
    model = load_model()
    encoder = load_encoder()
    return model, encoder

model, encoder = load_models()

# Main input
url_input = st.text_input(
    "Enter URL to analyze:",
    placeholder="https://example.com/article",
    help="Enter a complete URL including http:// or https://"
)

analyze_button = st.button("Analyze Content", type="primary")

if analyze_button and url_input:
    if not url_input.startswith(('http://', 'https://')):
        st.error("Please enter a valid URL starting with http:// or https://")
    else:
        with st.spinner("Analyzing content..."):
            #show progress
            progress_bar = st.progress(0)
            
            #get the webpage
            progress_bar.progress(20)
            st.info("Getting webpage content...")
            html_content, error = scrape_url(url_input)
            
            if error:
                st.error(f"Failed to fetch URL: {error}")
                st.stop()
            
            #parse the page
            progress_bar.progress(40)
            st.info("Reading webpage content...")
            title, body_text, word_count = parse_html(html_content)
            
            if body_text.startswith("Error") or word_count == 0:
                st.error("Couldn't read the page content")
                st.stop()
            
            #analyze text
            progress_bar.progress(60)
            st.info("Analyzing content...")
            features = extract_features(body_text)
            keywords = extract_keywords(body_text)
            
            #check quality
            progress_bar.progress(80)
            st.info("Checking content quality...")
            
            if model and encoder:
                quality_label, probabilities = predict_quality(features, model, encoder)
            else:
                quality_label = create_quality_label_manual(
                    features['word_count'], 
                    features['flesch_reading_ease']
                )
                probabilities = {}
            
            #look for similar content
            progress_bar.progress(90)
            st.info("Looking for similar content...")
            vector, _ = get_tfidf_vector(body_text)
            similar_content = []
            if vector is not None:
                similar_content = find_similar_content(vector)
            
            progress_bar.progress(100)
            time.sleep(0.3)
            progress_bar.empty()
            
            #show what we found
            st.success("Analysis Complete!")
            
            # Main metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Word Count", f"{features['word_count']:,}")
            
            with col2:
                st.metric("Sentences", features['sentence_count'])
            
            with col3:
                readability_score = features['flesch_reading_ease']
                st.metric("Readability", f"{readability_score:.1f}")
            
            with col4:
                quality_class = f"quality-{quality_label.lower()}"
                st.markdown(f'<p class="metric-card">Quality<br><span class="{quality_class}">{quality_label}</span></p>', 
                           unsafe_allow_html=True)
            
            # Detailed information
            st.divider()
            
            # Page info
            with st.expander("Page Information", expanded=True):
                st.markdown(f"**Title:** {title}")
                st.markdown(f"**URL:** {url_input}")
                st.markdown(f"**Thin Content:** {'Warning: Yes' if features['is_thin'] else 'No'}")
            
            # Keywords
            with st.expander("Top Keywords"):
                if keywords and not keywords.startswith("Error"):
                    keyword_list = keywords.split('|')
                    st.write(", ".join([f"`{kw}`" for kw in keyword_list]))
                else:
                    st.write("No keywords extracted")
            
            # Quality details
            if probabilities:
                with st.expander("Quality Score Details"):
                    for label, prob in sorted(probabilities.items(), key=lambda x: x[1], reverse=True):
                        st.progress(prob, text=f"{label}: {prob:.1%}")
            
            # Readability interpretation
            with st.expander("Readability Interpretation"):
                score = features['flesch_reading_ease']
                if score >= 90:
                    interpretation = "Very Easy (5th grade level)"
                elif score >= 80:
                    interpretation = "Easy (6th grade level)"
                elif score >= 70:
                    interpretation = "Fairly Easy (7th grade level)"
                elif score >= 60:
                    interpretation = "Standard (8th-9th grade level)"
                elif score >= 50:
                    interpretation = "Fairly Difficult (10th-12th grade level)"
                elif score >= 30:
                    interpretation = "Difficult (College level)"
                else:
                    interpretation = "Very Difficult (Professional level)"
                
                st.markdown(f"**Score:** {score:.1f}/100")
                st.markdown(f"**Level:** {interpretation}")
            
            # Similar content
            if similar_content:
                with st.expander("Similar Content Found", expanded=True):
                    st.warning(f"Found {len(similar_content)} potentially similar pages")
                    for item in similar_content:
                        similarity_pct = item['similarity'] * 100
                        st.markdown(f"**{item.get('title', 'Unknown')}**")
                        st.markdown(f"URL: `{item['url']}`")
                        st.progress(item['similarity'], text=f"Similarity: {similarity_pct:.0f}%")
                        st.divider()
            
            # Export results
            st.divider()
            
            result_json = {
                "url": url_input,
                "title": title,
                "word_count": features['word_count'],
                "sentence_count": features['sentence_count'],
                "readability_score": round(features['flesch_reading_ease'], 2),
                "quality_label": quality_label,
                "is_thin_content": features['is_thin'],
                "top_keywords": keywords,
                "similar_content": similar_content
            }
            
            st.download_button(
                label="Download Results (JSON)",
                data=json.dumps(result_json, indent=2),
                file_name=f"seo_analysis_{int(time.time())}.json",
                mime="application/json"
            )

#sidebar info
with st.sidebar:
    st.header("About")
    st.markdown("""
    This tool analyzes web content for:
    - **Content Quality**: Using ML model
    - **Readability**: Flesch score
    - **Duplicates**: Similar content
    - **SEO Stats**: Word count & structure
    """)
    
    st.divider()
    
    st.header("Quality Levels")
    st.markdown("""
    - **High**: >1500 words, good readability
    - **Medium**: Average content
    - **Low**: <500 words or hard to read
    """)
    
    st.divider()
    
    st.header("Readability Scale")
    st.markdown("""
    - **90-100**: Very Easy
    - **80-89**: Easy
    - **70-79**: Fairly Easy
    - **60-69**: Standard
    - **50-59**: Fairly Hard
    - **30-49**: Hard
    - **0-29**: Very Hard
    """)
    
    st.divider()
    
    st.markdown("---")
    st.markdown("Built with Streamlit")
