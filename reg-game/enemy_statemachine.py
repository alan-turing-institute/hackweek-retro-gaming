class State:
    def __init__(self, name: str):
        self.name: str = name

    def do_actions(self):
        pass

    def check_conditions(self) -> str | None:
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class StateMachine:
    def __init__(self) -> None:
        self.states: dict[str, State] = {}
        self.active_state: State | None = None

    def add_state(self, state: "State"):
        self.states[state.name] = state
