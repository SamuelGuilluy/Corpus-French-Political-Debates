# Corpus-French-Political-Debates

## Data Analysis of the political debates

The library used to implement the visual aspect of the site is streamlit. A description of its use can be found at the following link: - https://streamlit.io

The main file used to run the site is "tableau_streamlit.py".

You can launch the site with the command :

> streamlit run .\tableau_streamlit.py

## Fonctionalités 

### Terminé

- [x] Faire la présentation "WordCloud" des candidats --> comment le présenter ? faire une carte d'identité des candidats comme sur l'autre site ?

### En cours

- [ ] Ajouter une recherche par sujet en entrant une phrase : on renvoit tous les extraits parlant de ce sujet

### TO DO

- [ ] Ajouter les onglets d'explications de qu'est ce qu'un argument dans notre cas
- [ ] Ajouter les pages de présentations des modèles utilisés et aussi un lien vers un article
- [ ] Utiliser l'outil speech to text streamlit ? (ne semble pas marcher avec l'ordi du boulot)
- [ ] Utiliser d'autres méthodes d'identification d'arguments ? Revoir les modèles des étudiants + ajouter le modèle développé soit même

<!-- 
## Annotate the data

- To download the prodigy package, use the command : 
> pip install prodigy -f /path/to/wheels 

### Launch Prodigy on our dataset.

As mentioned in the annotation guidelines, the two labels are : RAISON,PREUVE, the five span label are : REFERENCE,TEMOIGNAGE,FAIT,VALEUR,POLITIQUE.

The command to use prodigy on our data is : 

> python -m prodigy rel.manual ner_rels_test_3 blank:fr ./data/raw_data/data_Valéry_Giscard_dEstaing_François_Mitterrand.jsonl --label RAISON,PREUVE --span-label REFERENCE,TEMOIGNAGE,FAIT,VALEUR,POLITIQUE --wrap --add-ents
    

### Review annotations from two different annotators.

The command to compare annotations in datasets dataset_1 and dataset_2 is : 

> python -m prodigy review merged_dataset dataset_1,dataset_2 --label RAISON,PREUVE --span-label REFERENCE,TEMOIGNAGE,FAIT,VALEUR,POLITIQUE -v ner_manual --auto-accept
  
--auto-accept : Automatically accept annotations with no conflicts and add them to the merged dataset.

### Export the annotations :

> python -m prodigy db-out macron_lepen | Out-File ./annotation_demonstrateur.jsonl -encoding ASCII -->