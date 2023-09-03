import streamlit as st
from similarity_checker import SentenceSimilarityChecker
import summarizer
from get_news_newsapi import get_news
import warnings
warnings.filterwarnings("ignore")
import nltk 

def get_key(d, keyword):
    for i in d.keys():
        if keyword in i:
            return i

def get_text(input_list):
    sentences = []
    d = {}
    for i in input_list:
        desc = i.split(".")[0]
        d[desc] = i 

    for sentence in d.keys():
        sentences += nltk.sent_tokenize(sentence)

    checker = SentenceSimilarityChecker()
    similarity_groups = checker.group_similar_sentences(sentences)
    output_list = [d[get_key(d, list(s)[0].replace(".", ""))] for s in similarity_groups]  # select one sentence from each group
    curated_content = " ".join(output_list)
    return curated_content

center_heading = lambda heading: st.markdown(f"<h1 style='text-align: center;'>{heading}</h1>", unsafe_allow_html=True)

st.set_page_config(layout="wide")

c_1, c_2, _ = st.columns([0.2, 0.6, 0.2])
with c_2:
    center_heading("Content Curation PoC")
    topic = st.text_input("Enter the Topic ")
    getnews = st.button("Get News")

    if getnews:
        st.markdown("---")
        st.success("Collecting News...")
        news_list = get_news(topic)
        text = get_text(news_list) 

        st.success("Curating News...")
        final_result = summarizer.summarize(text)
        #final_result_llm = summarizer.summarize_llm(text)
   


        #c1, _, c2 = st.columns([0.44, 0.02, 0.44])
        
        with st.expander("Summary"):
            center_heading("Summary")
            st.write(final_result)

        #with st.expander("Summary LLM"):
         #   center_heading("Summary with LLM")
         #   st.write(final_result_llm)
        
        
        st.markdown("---")
        with st.expander("Additional logs"):
            get_len = lambda x: len(x.split(" "))
            st.write(f"Extracted news length: {get_len(text)} words")
            st.write(f"Summarized news length: {get_len(final_result)} words")
        #    st.write(f"Summarized news with llm length: {get_len(final_result_llm)} words")

