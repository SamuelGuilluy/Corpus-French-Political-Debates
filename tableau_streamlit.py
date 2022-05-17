import streamlit as st
import pandas as pd
import altair as alt
import random 

from urllib.error import URLError
from data.list_debat import liste_debates, dict_annotated_debates

from annotated_text import annotated_text


try:
    st.markdown("# Analyse des débats d'entre deux tours de l'élections présidentielles")
    
    st.markdown("Cette outil permet d'analyser les débats entre deux tours de l'élection présidentielle française.")
    
    with st.sidebar:
        st.markdown("## Choix du débat")

        
        debat = st.selectbox(
            "Choose the annotated debate", dict_annotated_debates
        )

        debat = st.selectbox(
            "Choose the debate", liste_debates
        )
    
    object_list = ["This ",
        ("is", "verb"),
        " some ",
        ("annotated", "adj"),
        ("text", "noun"),
        " for those of ",
        ("you", "pronoun"),
        " who ",
        ("like", "verb"),
        " this sort of ",
        ("thing", "noun"),
        "."]
    
    annotated_text(*object)
       


except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )