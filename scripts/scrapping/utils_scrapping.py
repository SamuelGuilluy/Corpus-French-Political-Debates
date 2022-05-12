import requests
import bs4
import pandas as pd
import time
from tqdm import tqdm


def get_pages(url, nb):
    """ Create the list of the pages to request."""
    pages = []
    for i in range(1,nb+1):
        j = url + "?page=" + str(i)
        pages.append(j)
    return pages


def extract_url_article_from_pages(url_web_site,pages):
    """ Extraction de la liste des documents (principalement l'url) présents sur la page """ 
    tab_url = []
    for i in tqdm(pages):
        time.sleep(2)
        response = requests.get(i)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        em_box = soup.find_all("div", {"role":"article"})
        for ele in em_box:
            url_article = url_web_site + ele["about"]
            tab_url.append(url_article)
    return tab_url


def extract_label(response):
    """ Extract labels from a discourse of response format """
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    html_tags = soup.find('div', {"class":"thematicBox"}).findAll('a')
    tab_tags = []
    for ele in html_tags:
        label = ele.text
        label = label.replace("\n",'')
        label = " ".join(label.split())
        tab_tags.append(label)
    return tab_tags


def extract_intervenant(response):
    """ Extract a dict of all the intervenant of the discourse """
    tab_intervenant = []
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    find_intervenant = soup.find("ul",{"class":"line-intervenant"})
    
    if (soup.find("ul",{"class":"line-intervenant"}) is not None):
      all_intervenant_web = soup.find("ul",{"class":"line-intervenant"}).findAll('li')
      for ele in all_intervenant_web:
          dic_info_intervenant = dict()
          balise_a = ele.a
          if(balise_a is not None):
            name = ele.a.text
            name = " ".join(name.split())
            ele.a.decompose()
            title = ele.text
            title = title.replace("-"," ")
            title = " ".join(title.split())
            dic_info_intervenant["name"] = name
            dic_info_intervenant["title"] = title
            tab_intervenant.append(dic_info_intervenant)
    return tab_intervenant


def extract_title_genre(response):
    """ Extract title from response of a request """
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    title = soup.find("div" ,{"class":"discour--desc"}).find("h1").text
    title = title.replace("\n","")
    
    title = title.split()
    genre = title[0]
    title = " ".join(title)
    
    return title, genre


def extract_conversation(soup):
    """ Extract the conversation from the integral text"""
    Texte_Integral = soup.find("span" ,{"class":"clearfix text-formatted field field--name-field-texte-integral field--type-text-long field--label-hidden field__item"})
    tab_with_out_br = []
    for ele in Texte_Integral.contents:
        string = str(ele)
        string = string.replace("\x85","")
        tring = string.replace("\x80","")
        if(string != "<br/>" and string != "- Jingle -"):
            tab_with_out_br.append(string)
    return tab_with_out_br


def extract_conversation_pour_annotation(soup):
    """ Extract the conversation from the integral text"""
    Texte_Integral = soup.find("span" ,{"class":"clearfix text-formatted field field--name-field-texte-integral field--type-text-long field--label-hidden field__item"})
    tab_with_out_br = []
    actual_string = ""
    for ele in Texte_Integral.contents:
        string = str(ele)
        string = string.replace("\x85","")
        string = string.replace("\x80","")
        if(string != "<br/>"):
            actual_string += string
        else:
            #print(actual_string)
            #print('\n')
            tab_with_out_br.append(actual_string)
            actual_string = ""
            
    return tab_with_out_br


def construct_dataframes_from_urls(tab_url):
    """ Construct the dataframe containing the information about the discourse. """
    list_dic = []

    for i in tqdm(tab_url):
        time.sleep(2)
        response = requests.get(i)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        
        labels = extract_label(response)
        date = soup.find("time")["datetime"]
        intervenant = extract_intervenant(response)
        
        conversation = extract_conversation(soup)
        title, genre = extract_title_genre(response)
        
        tab_ele = {
                    "Date" : date,
                    "Intervenant" : intervenant,
                    "Labels" : labels,
                    "Genre" : genre,
                    "Title" : title,
                    "Conversation" : conversation,
                    "Url":i
                  }

        list_dic.append(tab_ele)

    # Creates DataFrame.
    df = pd.DataFrame(list_dic)
    return df