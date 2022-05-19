import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TextClassificationPipeline

dict_sorted_by_topics = {
        "Sport":{
            "graph":[],
            "debate":[]
        },
        "Economie":{
            "graph":[],
            "debate":[]
        },
        "Opinion":{
            "graph":[],
            "debate":[]
        },
        "Politique":{
            "graph":[],
            "debate":[]
        },
        "Societe":{
            "graph":[],
            "debate":[]
        },
        "Culture":{
            "graph":[],
            "debate":[]
        },
        "Environement":{
            "graph":[],
            "debate":[]
        },
        "Technologie":{
            "graph":[],
            "debate":[]
        },
        "Education":{
            "graph":[],
            "debate":[]
        },
        "Justice":{
            "graph":[],
            "debate":[]
        },
    }
    
def construct_the_list_of_annotated_tuple(file_name,path_annotated_data):

    model_name = 'lincoln/flaubert-mlsum-topic-classification'

    loaded_tokenizer = AutoTokenizer.from_pretrained(model_name)
    loaded_model = AutoModelForSequenceClassification.from_pretrained(model_name)

    nlp = TextClassificationPipeline(model=loaded_model, tokenizer=loaded_tokenizer)

    total_name =  path_annotated_data + file_name
    with open(total_name,"r") as f:
        annotated_data = f.readlines()


    for line in annotated_data:
        data_json_format = json.loads(line)
        list_relation = {}
        list_graph_structure = {}

        
        label_topic = nlp(data_json_format["text"][:511])[0]["label"]
        

        for ele in data_json_format["relations"]:

            start_head = ele["head_span"]["start"]
            end_head = ele["head_span"]["end"]
            label_head = ele["head_span"]["label"]

            list_relation[start_head] = (start_head,end_head,label_head)

            start_child = ele["child_span"]["start"]
            end_child = ele["child_span"]["end"]
            label_child = ele["child_span"]["label"]

            list_relation[start_child] = (start_child,end_child,label_child)

            ele_for_graph = (label_head, label_child,  ele["label"] )

            list_graph_structure[start_child] =(ele_for_graph)

        list_keys_sorted = sorted(list(list_relation.keys()))

        list_segment = []
        previous_end_indices = 0

        if(len(list_keys_sorted) == 0):
            list_segment.append(data_json_format["text"])


        for ele in list_keys_sorted:
            ## On ajoute la partie qui n'est pas anotée
            if(previous_end_indices < ele):
                segment_start = data_json_format["text"][previous_end_indices:ele]
                list_segment.append(segment_start)

            ## On s'occupe des parties ayant des arguments
            (start_char,end_char,label_segment) = list_relation[ele]
            segment = data_json_format["text"][start_char:end_char]
            tuple = (segment,label_segment)
            list_segment.append(tuple)

            previous_end_indices = end_char

        # global_debate_to_show.append(list_segment)
        dict_sorted_by_topics[label_topic]["graph"].append(list_graph_structure)
        dict_sorted_by_topics[label_topic]["debate"].append(list_segment)
        # global_graph.append(list_graph_structure)

    return dict_sorted_by_topics