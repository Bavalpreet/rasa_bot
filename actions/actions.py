# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
from sentence_transformers import SentenceTransformer, util
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

#inheriting ActionGreet class through predefined action class  
class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"
    
    def run(self ,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:

            dispatcher.utter_message(text="Hi how can i help you with your boat")

            return []

    def loader(self):
        model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
        df=pd.read_csv('/home/bavalpreet/Downloads/boatbox/faq-rasa.csv')
        sentences=df['Questions'].str.replace("\n", "", case = False).tolist()#list of sentences after pickingup from csv
        solutions=df['Answers'].str.replace("\n", "", case = False).tolist()#list of solutions after picking up from csv

        embeddings = model.encode(sentences)#list of embeddings

        return [model,embeddings,solutions]


#inheriting ActionFAQ class from ActionGreet class
class ActionFAQ(ActionGreet):

    def name(self) -> Text:
        return "action_faq"
    
    def run(self ,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]: 


            model,embeddings,solutions = ActionGreet.loader(self)#calling loader function defined in ActionGreet class

            message=tracker.latest_message['text']# extracting text i.e what user has entered

            test=model.encode(message)# creating embeddings for what user has entered

            parts = tracker.get_slot("boat_info") # this is a list slot so we will store all entities 
                                                    # extracted from an user input

            # to search all the strings in a list wthether in column or not                                     
            # https://stackoverflow.com/questions/17972938/check-if-a-string-in-a-pandas-dataframe-column-is-in-a-list-of-strings
            pattern = '|'.join(parts)# basically we are applying or condition to check the presence of all the extracted entities in the csv

           
            sols_temp=pd.DataFrame(solutions) # converting our series to datatframe


            sols_temp.rename(columns = {0:'solutions'},  inplace = True)  # renaming the column

            checker= sols_temp[sols_temp['solutions'].str.contains(pattern,na=False)]  # checking if the extracted entity
            # is present or not and if yes in which answers
            
            checker_index=list(checker.index.values) # storing the indexes of rows that were having our entity

            sols_temp=sols_temp.iloc[checker_index] # now storing only those solutions that are shortlisted

            sols_temp.reset_index(level=0, inplace=True) # setting indexes again to normal

            sols_temp.drop(columns=['index'],inplace=True) # dropping that unnecessary index column


            emb= [embeddings[i] for i in checker_index] # stroing list of only those embeddings of questions 
            # whose corresponding answer had the entity

            cos_sim = util.pytorch_cos_sim(test, emb) #  cosine similarity
                
            cos_sim=cos_sim.tolist()

            print(cos_sim)
            sol_index=cos_sim[0].index(max(cos_sim[0])) # to get the index of maximum cosine similarity

         # to get values from series ( this series conatains answer that was selected on behalf of highest cos similarity)
            solution=sols_temp.iloc[[sol_index]]['solutions'].values[0] 

            dispatcher.utter_message(text=solution)
            return []






'''

class Action_repair_hull(Action):

    def name(self) -> Text:
        return "action_repair_hull"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="There are two scenarios where a boat hull can be damaged – one is when the hull is damaged above the waterline, the second when it is damaged below the waterline.For first scenario take it out and dry it thoroughly.For hull repair, a basic fibreglass repair kit is used, using which the damaged section is removed in a circular cut. The part can be then patched using either fibreglass and the proper adhesives or the putties available.")

        return []


class Action_repair(Action):

    def name(self) -> Text:
        return "action_repair"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        print(entities)

        for e in entities:
            if e['entity'] == 'boat_part':
                name = e['value']

            if name == "hull":
                message = "There are two scenarios where a boat hull can be damaged – one is when the hull is damaged above the waterline, the second when it is damaged below the waterline.For first scenario take it out and dry it thoroughly.For hull repair, a basic fibreglass repair kit is used, using which the damaged section is removed in a circular cut. The part can be then patched using either fibreglass and the proper adhesives or the putties available."

            if name == "core":
                message = "Core damage primarily happens due to the intrusion of water through hull-fittings or deck-fittings"
            
        dispatcher.utter_message(text=message)

        return []

class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"
    
    def run(self ,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:

            dispatcher.utter_message(text="hi boat manufacturer which boat you are using , how may i help you?")

            return []

    def loader(self):
        model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
        df=pd.read_csv('/home/bavalpreet/Downloads/boatbox/faq-rasa.csv')
        sentences=df['Questions'].str.replace("\n", "", case = False).tolist()
        solutions=df['Answers'].str.replace("\n", "", case = False).tolist()

        embeddings = model.encode(sentences)

        return [model,embeddings,solutions]


class ActionDemo(ActionGreet):

    def name(self) -> Text:
        return "action_demo"
    
    def run(self ,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]: 


            model,embeddings,solutions = ActionGreet.loader(self)

            message=tracker.latest_message['text']

            test=model.encode(message)

            for i in range(len(solutions)):
                cos_sim = util.pytorch_cos_sim(test, embeddings)
                
            cos_sim=cos_sim.tolist()
            print(cos_sim)
            sol_index=cos_sim[0].index(max(cos_sim[0]))

            solution=solutions[sol_index]
            print(solution)
            dispatcher.utter_message(text=solution)

            return []
'''