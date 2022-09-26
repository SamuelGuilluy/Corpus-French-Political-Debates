from ctypes import sizeof
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
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

try:
    
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center; color: black;'>Analyse des débats d'entre deux tours des élections présidentielles françaises.</h1>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("## Choix du débat")

        kind_of_data = st.radio(
            "Choisissez le type de débat à explorer", ["Explication du modèle","Données pré-traîtés"])# "Tous les débats d'entre deux tours")) #"Recherche par mots clés",

        if (kind_of_data == "Données pré-traîtés"):
            debat_int = st.selectbox(
                "Choisissez un débat à analyser", ["Macron vs LePen - 2017"] #"Hollande vs Sarkozy - 2012",
            )
            
            relation_name = {
                "Hollande vs Sarkozy - 2012":"Hollande Sarkozy Antoine",
                "Macron vs LePen - 2017":"Macron Lepen Charles"
            }
            debat = relation_name[debat_int]
          
        elif(kind_of_data == "Tous les débats d'entre deux tours"):
            debat = st.selectbox(
                "Choisisser un débat à analyser", dict_liste_debats
            )

        
        
    if(kind_of_data == "Recherche par mots clés"):
        # search bar
        query = st.text_input("Cherchez des arguments sur le sujet de votre choix!", "")
        st.markdown(query)
        topics = st.multiselect("Sélectionné les sujets d'intérêts", options=["Economie","Opinion","Politique","Societe","Culture","Sport","Environement","Technologie","Education","Justice"])

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

    
    elif (kind_of_data == "Explication du modèle"):

        with st.expander(label = "Schéma argumentaire", expanded=True):
            st.markdown("## Explication du schéma argumentaire.")


            col1_simple, col2_simple, col3_simple = st.columns([2,6,2])
            with col1_simple:
                st.write("")
            with col2_simple:
                st.image("./data/images/meta_model.png")
                st.markdown("<h5 style='text-align: center; color: black;'>Méta modèle du schéma de données.<h5>",unsafe_allow_html=True)
            with col3_simple:
                st.write("")
            

            st.markdown("L'objectif de ce modèle est d'identifier les arguments au sein des débats politiques. Pour cela, nous allons dans un premier temps définir les unités élémentaires ainsi que les supports de relations qui sont les éléments de base qui composents les arguments.")
            st.markdown(" Ce modèle d'étude des arguments est adapté à l'étude des débats politiques est provient d'une étude réalisée par Joonsuk Park en 2015 dans son article : [Toward Machine-assisted Participation in eRulemaking: An Argumentation Model of Evaluability ](https://dl.acm.org/doi/10.1145/2746090.2746118) .",unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<h3 style='text-align: center; color: black;'> Les unités élémentaires.<h3>",unsafe_allow_html=True)

                st.markdown("- Proposition d'un fait non expérimental (FAIT): Il s'agit d'une référence à une proposition objective 'exprimant ou traitant des faits ou des conditions tels qu'ils sont perçus sans être déformés par des sentiments personnels ou des interprétations.' Par définition, une proposition de FAIT a une valeur de vérité qui peut être vérifiée par des preuves objectives. Nous limitons la notion de vérifiabilité aux éléments de preuve qui peuvent être disponibles au moment où l'affirmation est faite. Les prédictions sur l'avenir sont considérées comme invérifiables.")
                st.markdown("- Proposition de fait expérimental (TÉMOIGNAGE): Il s'agit d'une proposition objective sur l'état ou l'expérience personnelle de l'auteur. Une caractéristique majeure de ce type de propositions objectives, par opposition aux contreparties non expérimentales classées comme FAITS, est qu'il est pratiquement impossible de fournir des preuves objectives dans un contexte de débat, sous forme d'URL ou de citation. En d'autres termes, la preuve du TÉMOIGNAGE n'est pas publiquement disponible dans la plupart des cas.")
                st.markdown("- Référence à une ressource (RÉFÉRENCE) : Il s'agit d'une référence à une source de preuves objectives. Dans les débats, une RÉFÉRENCE est généralement une citation d'une personnalité.")
                st.markdown("- Proposition de valeur (VALEUR) : il s'agit d'une proposition contenant des jugements de valeur sans faire de déclarations spécifiques sur ce qui devrait être fait. En raison de la subjectivité des jugements de valeur, une proposition de VALEUR ne peut être prouvée directement par des preuves objectives toutefois, il est possible et approprié de fournir une raison.")
                st.markdown("- Proposition de politique (POLITIQUE) : Il s'agit d'une proposition qui propose une ligne de conduite spécifique à suivre. Elle contient généralement des verbes modaux tels que 'devrait'. Tout comme la VALEUR, une proposition de POLITIQUE ne peut être directement vérifiée par des preuves objectives.")
            with col2: 
                st.markdown("<h3 style='text-align: center; color: black;'> Les supports de relation.<h3>",unsafe_allow_html=True)

                st.markdown("Le support de relation définit la nature de relation pouvant exister entre les différentes unités élémentaires. ")

                st.markdown("- RAISON: Une unité élémentaire X est une raison pour une proposition. Y si X fournit une justification pour Y. ")
                st.markdown("- ÉVIDENCE: Une unité élémentaire X est une preuve pour une proposition Y si elle prouve que la proposition Y est vraie ou non. Les types possibles types de preuves sont limités à TÉMOIGNAGE ou RÉFÉRENCE.")
            
            with col3:
                st.markdown("<h3 style='text-align: center; color: black;'> Définition d'un argument.<h3>",unsafe_allow_html=True)
                st.markdown(" Un argument est un ensemble (R, E, c) où:")
                st.markdown("- R est un ensemble de raisons expliquant que c est vrai, tels que chacun de ces éléments soit une proposition.")
                st.markdown("- E est un ensemble d'évidence confirmant que c est vraie tels que chacun de ces éléments soit du type Évidence.")
                st.markdown("- c est la conclusion de type Proposition.")

                st.markdown("En d'autres termes, un argument peut être constitué de zéro ou plus de raisons et d'évidences, mais il y a quelques restrictions à respecter pour qu'il soit correctement évalué.")
                st.markdown("Lorsque la conclusion est un témoignage, il n'est pas nécessaire de fournir des prémisses explicites pour que l'argument soit évalué. ")
                st.markdown("Les conclusions de tous les autres types nécessitent au moins un type de soutien : la Politique et la Valeur requièrent une prémisse explicite comme soutien, et le Fait peut être étayé par une preuve ou un autre fait.")

        with st.expander(label = "Modèle d'apprentissage.", expanded=True):
            st.markdown("## Description du modèle d'apprentissage.")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h3 style='text-align: center; color: black;'> Identification du sujet du débat. <h3>",unsafe_allow_html=True)

                st.image("./data/images/topic.png")
                st.markdown("<h5 style='text-align: center; color: black;'>Architecture du modèle d'identification des sujets.<h5>",unsafe_allow_html=True)
                
                st.markdown("#### Schéma d'annotation.")

                st.markdown("Identification du thème courant du débat parmi 10 thèmes possibles :")
                st.markdown(" - Culture")
                st.markdown(" - Economie")
                st.markdown(" - Education")
                st.markdown(" - Environnement")
                st.markdown(" - Justice")
                st.markdown(" - Opinion")
                st.markdown(" - Politique")
                st.markdown(" - Société")
                st.markdown(" - Sport")
                st.markdown(" - Technologie")

                st.markdown("Les thèmes ont été choisis afin d’obtenir les meilleurs résultats possibles en se basant sur des modèles pré-existant entraînés sur de large corpus de données. ")

                st.markdown("#### Modèle de classification.")

                st.markdown("Le modèle a été entraîné en partenariat avec trois étudiants de CentraleSupélec lors d'un projet de recherche de 6 mois.")
                st.markdown("[FlauBERT](https://github.com/getalp/Flaubert) est un modèle de NLP basé sur l'architecture BERT entraîné sur un corpus français très large et hétérogène. Des modèles de différentes tailles sont entraînés en utilisant le supercalculateur Jean Zay du CNRS (Centre National de la Recherche Scientifique).")
                st.markdown("Notre modèle est une adaptation d'un modèle de [classification d'articles de presses avec Flaubert](https://huggingface.co/lincoln/flaubert-mlsum-topic-classification) entraîné sur les données de débats politiques ainsi que des données OpenSource du projet [Manifesto](https://manifesto-project.wzb.eu/) ")
                

            with col2:
                st.markdown("<h3 style='text-align: center; color: black;'> Identification des arguments.<h3>",unsafe_allow_html=True)
            
                st.image("./data/images/argument.png")
                st.markdown("<h5 style='text-align: center; color: black;'>Architecture du modèle d'identification des arguments.<h5>",unsafe_allow_html=True)
                
                st.markdown("L'objectif du modèle est d'exploiter la structure syntaxique de la phrase afin d'avoir une segmentation des composants argumentaires cohérente avec la syntaxe de la phrase.")
                st.markdown("Pour cela, nous avons adapté le modèle edc réseaux de Neurones présentée dans l'article [Argument Mining with Structured SVMs and RNNs](https://arxiv.org/pdf/1704.06869.pdf) utilisant un facteur de graphe afin de modéliser le problème.")

                st.markdown("Nous avons utilisé [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) durant la phase de pré-processing afin d'avoir les arbres de constituant associé au texte.")

                st.markdown("L'algorithme de résolution du problème a été présenté dans le papier : [AD3: Alternating Directions Dual Decomposition for MAP Inference in Graphical Models](https://www.jmlr.org/papers/volume16/martins15a/martins15a.pdf)")
                

    elif (kind_of_data == "Données pré-traîtés"):

        col1, col2 = st.columns(2)

        with col2:
            st.markdown("<h2 style='text-align: center; color: black;'>Graphes Argumentifs du débat.</h1>", unsafe_allow_html=True)
    
            final_stopwords_list = stopwords.words('english') + stopwords.words('french')

            path_directory = "./data/preprocessed_data/"
            file_name = dict_annotated_debates[debat]["path"]

            names_intervenant = dict_annotated_debates[debat]["name_intervenant"]

            with open("./data/preprocessed_data/" + file_name[:-6] + "_" + "output_dict", "rb") as fp:   # Unpickling
                dict_output = pickle.load(fp)  

            num_of_element_to_show = st.slider("Sélectionne le nombre de paragraphe à analyser.",0,50, 10)
            
            topics = st.multiselect("Sélectionné les sujets d'intérêts", options=["Economie","Opinion","Politique","Societe","Culture","Sport","Environement","Technologie","Education","Justice"],default="Economie")
            list_word_to_use  = [["Politique"],["Politique"]]
            indice_extrait = 1
            for topic in topics:
                dict_du_topic = dict_output[topic]
                st.markdown("## "+ topic)
                num_element = min(num_of_element_to_show,len(dict_du_topic["graph"]),len(dict_du_topic["debate"]))      

                is_there_any_graph = False
                for i in range(num_element):
                    with st.expander(label = 'Extrait du débat n°' + str(indice_extrait), expanded=True):
                        if(len(list(dict_du_topic["graph"][i].keys())) != 0):
                            indice_extrait += 1 
                            is_there_any_graph = True
                            
                            annotated_text(*dict_du_topic["debate"][i])
                            
                            text_tokens_element = [word_tokenize(ele[0]) for ele in dict_du_topic["debate"][i]]
                            tokens_without_sw = [word for word in text_tokens_element if not word in stopwords.words()]
                            text = (" ").join([word.replace("\x92","") for list_word in tokens_without_sw for word in list_word ])
                            

                            if(dict_du_topic["debate"][i][0][:len(names_intervenant[0])] == names_intervenant[0]):
                                list_word_to_use[0].append(text)
                            elif(dict_du_topic["debate"][i][0][:len(names_intervenant[1])] == names_intervenant[1]):
                                list_word_to_use[1].append(text)

                            # Create a graphlib graph object
                            graph = graphviz.Digraph()
                            # print(dict_du_topic["graph"][i])
                            for key, values in dict_du_topic["graph"][i].items():
                                graph.edge(*values)
                            st.graphviz_chart(graph)

                                                
                
                # text_tokens_element = word_tokenize(text)
                # tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]

                            
        with col1: 

            st.markdown("<h2 style='text-align: center; color: black;'>Nuage de mots clés des candidats.</h1>", unsafe_allow_html=True)
    
        
            list_path_person = dict_annotated_debates[debat]["path_images"]
            path_to_text = "./data/text/"
            path_to_image = "./data/images/"
            list_to_show = []
            for (i,personne_image) in enumerate(list_path_person):
                text = (" ").join(list_word_to_use[i])
                print(list_word_to_use[i])
                melenchon_color = np.array(Image.open(os.path.join(path_to_image, personne_image)))
                melenchon_mask = melenchon_color.copy()
                wc = WordCloud(max_words=250, mask=melenchon_mask, background_color="white")
                wc.generate(text)
                image_colors = ImageColorGenerator(melenchon_color)
                wc.recolor(color_func=image_colors)
                list_to_show.append([wc,personne_image,melenchon_color])

            fig, ax = plt.subplots(nrows=2, ncols=1,figsize = (22, 22))
            plt.subplot(211)
            ax[0] = plt.imshow(list_to_show[0][0], interpolation="bilinear")
            ax[0] = plt.imshow(list_to_show[0][2], alpha=0.4)
            plt.axis('off')
            plt.title(list_to_show[0][1][:-4].capitalize(),loc="center", fontsize=20)
            # plt.figure(figsize = (10, 10))
            plt.subplot(212)
            ax[1] = plt.imshow(list_to_show[1][0], interpolation="bilinear")
            ax[0] = plt.imshow(list_to_show[1][2], alpha=0.4)
            plt.axis('off')
            # plt.figure(figsize = (10, 10))
            plt.title(list_to_show[1][1][:-4].capitalize(),loc="center", fontsize=20)
            st.pyplot(fig)

        

    elif (kind_of_data == "Tous les débats d'entre deux tours"):
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