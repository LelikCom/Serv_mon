from aiogram.fsm.state import State, StatesGroup

class TerminalState(StatesGroup):
    active = State()
