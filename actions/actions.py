# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re
from datetime import datetime

class ActionSetSlot(Action):

    def name(self) -> Text:
        return "action_set_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #dispatcher.utter_message(text=res)
        return [SlotSet("chat_trail", 'l_1'),SlotSet("flag_l4", "0")]

class ActionLevelMenu(Action):

    def name(self) -> Text:
        return "action_level_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        res = "TEST 123"
        flag_l4_set = "0"
        msg = tracker.latest_message.get('text')
        slot_chat_trail = tracker.get_slot('chat_trail')
        lvl_flag = slot_chat_trail
        if slot_chat_trail == 'l_1' and msg in ['yes','y']:
            res = "Have you made an appointment with any of your car dealer yet?"
            lvl_flag = "l_2"
        elif slot_chat_trail == 'l_1' and msg in ['no','n']:
            res = "Would you like to book an appointment to discuss more about this safety recall?"
            lvl_flag = "l_5"

        elif slot_chat_trail == 'l_2' and msg in ['yes','y']:
            res = "Ok Great"
            lvl_flag = "l_0"

        elif slot_chat_trail == 'l_2' and msg in ['no','n']:
            res = "Ok. We have an available slot to book your appointment. Are you interested?"
            lvl_flag = "l_3"

        elif slot_chat_trail == 'l_3' and msg in ['yes','y']:
            res = "What would be the best available time to discuss it?\nDate format -> YYYY-MM-DD"
            lvl_flag = "l_4"

        elif slot_chat_trail == 'l_3' and msg in ['no','n']:
            res = "No Problem. Thanks."
            lvl_flag = "l_0"

        elif slot_chat_trail == 'l_4':
            print('l4444444444444444444444444444444444444444')
            flag_l4 = tracker.get_slot('flag_l4')
            print(flag_l4,'flag_l4flag_l4flag_l4flag_l4flag_l4flag_l4flag_l4')

            try:
                match = re.search(r'\d{4}-\d{2}-\d{2}', msg)
                date = datetime.strptime(match.group(), '%Y-%m-%d').date()
                if date:
                    res = "Ok Thanks We will be in touch with you."
                else:
                    res = "Ok Thanks We will be in touch with you during business hours"

                lvl_flag = "l_0"

            except Exception as err:
                if flag_l4 == "2":
                    res = "Ok Thanks We will be in touch with you during business hours"
                else:
                    res = "Please try again with date, Use this date format - YYYY-DD-MM"

                lvl_flag = "l_4"
                flag_l4_set = "2"

        elif slot_chat_trail == 'l_5' and msg in ['yes','y']:
            res = "What would be the best available time to discuss it?\nDate format -> YYYY-MM-DD"
            lvl_flag = "l_4"

        elif slot_chat_trail == 'l_5' and msg in ['no','n']:
            res = "Ok no problem"
            lvl_flag = "l_0"

        else:
            res = "We didn't get you, Would you like to jump over call to discuss more?"
            lvl_flag = "l_5"
        print(msg)
        print('slot_chat_trail_111111111',slot_chat_trail)
        print(lvl_flag,'lvl_flaglvl_flaglvl_flaglvl_flag')


        dispatcher.utter_message(text=res)

        return [SlotSet("chat_trail", lvl_flag),SlotSet("flag_l4", flag_l4_set)]