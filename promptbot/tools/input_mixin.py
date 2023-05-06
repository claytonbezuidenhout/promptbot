
class InputMixin:
    """ Provides input methods to the implementing class. """

    @staticmethod
    def get_input(prompt: str = "") -> str:
        """ Gets input from the user. """
        return input(prompt)

    @staticmethod
    def _yes_or_no(answer):
        answer = answer.lower()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            raise ValueError("Invalid input. Please try again. Enter 'y' or 'n'.")

    @classmethod
    def start_prompt_loop(cls, prompt):
        while True:
            answer = cls.get_input(prompt)
            try:
                return cls._yes_or_no(answer)
            except ValueError as e:
                print(e)

    @classmethod
    def check_continue(cls, prompt: str = "Continue? (y/n): ") -> bool:
        """ Checks if the user wants to continue. """
        return cls.start_prompt_loop(prompt)

    @classmethod
    def check_execute(cls, prompt: str = "Execute? (y/n): ") -> bool:
        """ Checks if the user wants to execute the output. """
        return cls.start_prompt_loop(prompt)

    @classmethod
    def check_improve(cls, prompt: str = "Improve? (y/n): ") -> bool:
        """ Checks if the user wants to execute the output. """
        return cls.start_prompt_loop(prompt)
