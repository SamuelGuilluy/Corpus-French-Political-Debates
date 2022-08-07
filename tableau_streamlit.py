import streamlit as st
import pandas as pd
import altair as alt
import random 
import graphviz as graphviz
import pickle

import os
from PIL import Image
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator

from urllib.error import URLError
from data.list_debat import dict_liste_debats, dict_annotated_debates

from annotated_text import annotated_text

import matplotlib.pyplot as plt

try:
    st.markdown("# Analyse des débats d'entre deux tours de l'élections présidentielles")
    
    st.markdown("Cette outil permet d'analyser les débats entre deux tours de l'élection présidentielle française.")
    
    with st.sidebar:
        st.markdown("## Choix du débat")

        kind_of_data = st.radio(
            "Choisissez le type de débat à explorer",
            ("Recherche par mots clés","Données annotées", "Tous les débats d'entre deux tours"))

        if (kind_of_data == "Données annotées"):
            debat = st.selectbox(
                "Choisissez un débat annoté à analyser", dict_annotated_debates
            )
        else:
            debat = st.selectbox(
                "Choisisser un débat non annoté à analyser", dict_liste_debats
            )
        
        topics = st.multiselect("Sélectionné les sujets d'intérêts", options=["Economie","Opinion","Politique","Societe","Culture","Sport","Environement","Technologie","Education","Justice"])
    # print(kind_of_data)

    if(kind_of_data == "Recherche par mots clés"):
        # search bar
        query = st.text_input("Cherchez des arguments sur le sujet de votre choix!", "")
        st.markdown(query)

        ## On ittère sur tous les débats annotés
        for debat in dict_annotated_debates:
            st.markdown("### " + debat)

            path_directory = "./data/preprocessed_data/"
            file_name = dict_annotated_debates[debat]["path"]
            with open("./data/preprocessed_data/" + file_name[:-6] + "_" + "output_dict", "rb") as fp:   # Unpickling
                dict_output = pickle.load(fp)

                for topic in topics:
                    is_there_any_graph = False
                    st.markdown("### " + topic )
                    list_debat = dict_output[topic]["debate"]
                    list_graph = dict_output[topic]["graph"]

                    # print(list_debat)
                    # print(list_graph)
                    for debat_text, graph in zip(list_debat,list_graph):
                        # print(debat_text)
                        # print(graph)
                        # st.markdown(debat_text)
                        for ele_list in debat_text:
                            graph = graphviz.Digraph()
                            if(len(ele_list)>1):
                                st.markdown(ele_list)
                        break
                    
                        # if(len(ele_tuple) ==2):
                        
                        for ele in ele_list:
                            print(ele)
                            # if(our_word_in_the_text(query, ele)):
                                # graph.edge(*values)
                                # st.graphviz_chart(graph)
                        break


                    if(is_there_any_graph == False):
                        st.markdown("Ce sujet n'a pas été débatu.")
                    break


    elif (kind_of_data == "Données annotées"):

        list_path_person = dict_annotated_debates[debat]["path_images"]
        path_to_text = "./data/text/"
        path_to_image = "./data/images/"
        for personne_image in list_path_person:
            text = open(path_to_text + 'examples_wiki_rainbow.txt', encoding="utf-8").read()
            melenchon_color = np.array(Image.open(os.path.join(path_to_image, personne_image)))
            melenchon_mask = melenchon_color.copy()
            wc = WordCloud(max_words=250, mask=melenchon_mask, background_color="white")
            wc.generate(text)
            image_colors = ImageColorGenerator(melenchon_color)
            wc.recolor(color_func=image_colors)
            fig, ax = plt.subplots(nrows=1, ncols=2,figsize = (20, 20))
            plt.subplot(121)
            ax[0] = plt.imshow(melenchon_color)
            plt.subplot(122)
            ax[1] = plt.imshow(wc, interpolation="bilinear")
            st.pyplot(fig)

        path_directory = "./data/preprocessed_data/"
        file_name = dict_annotated_debates[debat]["path"]
        with open("./data/preprocessed_data/" + file_name[:-6] + "_" + "output_dict", "rb") as fp:   # Unpickling
            dict_output = pickle.load(fp)        
        
        for topic in topics:
            dict_du_topic = dict_output[topic]
            st.markdown("## "+ topic)

            num_of_element_to_show = st.slider("Choose how many elements to show",0,200, 20)
            num_element = min(num_of_element_to_show,len(dict_du_topic["graph"]),len(dict_du_topic["debate"]))
            
            is_there_any_graph = False
            for i in range(num_element):

                if(len(list(dict_du_topic["graph"][i].keys())) != 0):
                    is_there_any_graph = True
                    
                    st.markdown("### "+ "Graphe argumentatif associé")
                    # Create a graphlib graph object
                    graph = graphviz.Digraph()
                    # print(dict_du_topic["graph"][i])
                    for key, values in dict_du_topic["graph"][i].items():
                        graph.edge(*values)
                    st.graphviz_chart(graph)

                    st.markdown("### "+ "Extrait du débat annoté")
                    annotated_text(*dict_du_topic["debate"][i])
                    st.markdown("\n")
            
            if(is_there_any_graph == False):
                st.markdown("Ce sujet n'a pas été débatu.")

    if (kind_of_data == "Tous les débats d'entre deux tours"):
        st.markdown("## " + debat)
                

        list_path_person = dict_liste_debats[debat]["path_images"]
        path_to_text = "./data/text/"
        path_to_image = "./data/images/"
        for personne_image in list_path_person:
            text = open(path_to_text + 'examples_wiki_rainbow.txt', encoding="utf-8").read()
            melenchon_color = np.array(Image.open(os.path.join(path_to_image, personne_image)))
            melenchon_mask = melenchon_color.copy()
            wc = WordCloud(max_words=250, mask=melenchon_mask, background_color="white")
            wc.generate(text)
            image_colors = ImageColorGenerator(melenchon_color)
            wc.recolor(color_func=image_colors)
            fig, ax = plt.subplots(nrows=1, ncols=2,figsize = (20, 20))
            plt.subplot(121)
            ax[0] = plt.imshow(melenchon_color)
            plt.subplot(122)
            ax[1] = plt.imshow(wc, interpolation="bilinear")
            st.pyplot(fig)


except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )