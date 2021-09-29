from typing import List, Union


class AuthorizationError(Exception):
    def __init__(self, messages: Union[str, List[str]]):
        super().__init__()
        self.messages = [messages] if type(messages) == str else messages
        print(self.messages)
