import streamlit as st
import pandas as pd
import altair as alt
import random 

from urllib.error import URLError
from data.list_debat import liste_debates, dict_annotated_debates

from annotated_text import annotated_text
from scripts.data_analysis.convert_annotated_to_tuple import construct_the_list_of_annotated_tuple

try:
    st.markdown("# Analyse des débats d'entre deux tours de l'élections présidentielles")
    
    st.markdown("Cette outil permet d'analyser les débats entre deux tours de l'élection présidentielle française.")
    
    with st.sidebar:
        st.markdown("## Choix du débat")

        kind_of_data = st.radio(
            "Select the type of data to show",
            ("Annotated data", "all the data"))

        if (kind_of_data == "Annotated data"):
            debat = st.selectbox(
                "Choose the annotated debate", dict_annotated_debates
            )
        else:
            debat = st.selectbox(
                "Choose the debate", liste_debates
            )
    
    path_directory = "data/annotated_data/"
    object_list = construct_the_list_of_annotated_tuple(dict_annotated_debates[debat]["path"], path_directory)
    # print(object_list)

    for i in range(20):
        annotated_text(*object_list[50+i])
        st.markdown("\n")
       


except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )