from typing import List

class CLI:

    DEFAULT_SIGIL = "-"

    def __init__(self, required_args: int, allowed_kwargs: List[str]) -> None:
        self._required_args = required_args
        self._allowed_kwargs = allowed_kwargs

    def verify_valid_input(self, input: List[str]) -> None:
        if len(input) == 0:
            raise Exception("Missing title")
        if len(input) == 1:
            raise Exception(f'Missing command for title "{input[0]}"')
        if len(input) < self._required_args:
            raise Exception(f"{input[1:]}\nMissing arguments")

    def parse(
        self,
        prompt: str | List[str],
        sigil: str=None,
    ) -> None:

        def get_args(prompt) -> List[str]:
            return prompt[:self._required_args+1]

        def get_kwargs(prompt) -> dict:
            kwargs = {}
            for i in range(0, len(prompt), 2):
                key = prompt[i]
                value = prompt[i + 1]

                if key[0] != sigil:
                    raise Exception(
                        f"{prompt}\nKey at index {i}: '{key[0]}' is not a valid sigil. Expected '{sigil}'"
                    )
                if key[1:] not in self._allowed_kwargs:
                    raise Exception(
                        f"""{prompt}\nKey at index {i}: "{key}" not recognized"""
                    )
                for char in value:
                    if not char.isalpha:
                        raise Exception(
                            f"{prompt}\nValue at index {i+1}: Not alphanumeric"
                        )
                kwargs[key[1:]] = value
            return kwargs

        if type(prompt) is str:
            prompt = prompt.split(" ")
        if len(prompt) % 2:
            raise Exception(f"{prompt}\nInvalid amount of arguments")
        if sigil is None:
            sigil = CLI.DEFAULT_SIGIL
        elif not isinstance(sigil, str):
            raise Exception("Sigil must be string")

        self.args = get_args(prompt[:self._required_args+1])
        self.kwargs = get_kwargs(prompt[self._required_args:])

    @staticmethod
    def print_(str_) -> None:
        print(f"> {str_}")
            
