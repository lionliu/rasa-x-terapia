# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
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

import requests
import json
from uuid import uuid4
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType


class ActionJoke(Action):
    def name(self):
        return "action_joke"

    def run(self, dispatcher, tracker, domain):
        request = requests.get(
            'http://api.icndb.com/jokes/random'
        ).json()  # make an api call
        joke = request['value']['joke']  # extract a joke
        dispatcher.utter_message(text=joke)  # send the message back
        return []


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # the session should begin with a `session_started` event
        events = [SessionStarted()]
        events.extend(tracker.slots)

        requests.post("https://terapiabot.herokuapp.com/users",
                      {"conversationId": tracker.sender_id, "name": tracker.sender_id})

        dispatcher.utter_message(
            text="Para sincronizar à sua conta do Todoist digite /action_sync_todoist a qualquer momento durante nossa conversa!")

        return events


class ActionSyncWithTodoist(Action):
    def name(self) -> Text:
        return "action_sync_todoist"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        todoist_state = str(uuid4())
        todoist_sync_url = "https://todoist.com/oauth/authorize?client_id=1164292444224bdeb3de134a34ecf016&scope=data:read&state={}".format(
            todoist_state)
        
        dispatcher.utter_message(
            text="OK! Preciso que você entre neste link e me forneça autorização para saber quando você tiver alguma tarefa:\n {}".format(todoist_sync_url))
        
        return []
