#!/usr/bin/python3
from models.state import State
from models import storage


state = State()
state_id = state.id
print(state_id)
obj = storage.get(State, state_id)
print(obj)
