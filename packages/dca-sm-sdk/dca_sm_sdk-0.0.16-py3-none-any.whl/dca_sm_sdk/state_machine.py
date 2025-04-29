import datetime

import nuclio_sdk
from abc import ABC, abstractmethod

from dca_sm_sdk.mts_state import MtsState

from dca_sm_sdk.Exceptions import SM_EXCEPTION


class IState(ABC):
    @abstractmethod
    def Action(self, context : nuclio_sdk.Context ,mts_state: MtsState) -> str:
        pass

class StateMachine:
    def __init__(self, context : nuclio_sdk.Context):
        self.current_state = ""
        self.states = {}
        self.mts_state = MtsState()
        self.context = context


    def RegisterState(self, state_mame: str, state: IState):
        if state_mame in self.states:
            raise Exception(f"State {state_mame} registered")
        self.states[state_mame] = state
        self.context.logger.info(f"State {state_mame} registered")


    def SetStartState(self, state_name: str):
        if state_name not in self.states:
            raise Exception(f"State {state_name} not registered")
        self.current_state = state_name
        self.context.logger.info(f"State {state_name} set start")

    def Execute(self, context : nuclio_sdk.Context, event : nuclio_sdk.Event):
        for eventItem in event.body:
            prev_state = self.current_state
            state = self.states[self.current_state]
            try:
                self.mts_state.UpdateMtsState(eventItem)
                self.current_state = state.Action(context, self.mts_state)
                self.context.logger.info(f"State {prev_state} executed")

            except SM_EXCEPTION as e:
                return nuclio_sdk.Response(body=e, content_type="text/plain", status_code=e.StatusCode())
            except Exception as e:
                context.logger.error_with(f"State {prev_state} failed with exception {e}")
                return nuclio_sdk.Response(body= f"State {prev_state} failed with exception {e}", content_type="text/plain", status_code=SM_EXCEPTION.StatusCode())
        return nuclio_sdk.Response(status_code=200)