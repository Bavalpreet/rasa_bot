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
