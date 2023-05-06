from promptbot import PromptBot
from promptbot.tools.logger import get_logger

log = get_logger()


class BreakdownBot(PromptBot):
    def __init__(self):
        """
        Initializes a BreakdownBot instance. Inherits from the PromptBot class.
        """
        super().__init__("BreakdownBot")
        self.add_cmd("I can breakdown any complex task into smaller tasks.")
        self.add_rule("I must output only a data structure in JSON format")
        self.add_rule("I cannot provide any dialog or request additional info")
        self.add_rule("I must output only in the example format.")
        self.set_example_output(f'[{{ "step": "1", "task": "The 1st task I create"}},'
                                f'{{ "step": "2", "task": "The 2nd task I create"}}]')

    def start(self, text: str) -> str:
        """
        Takes in a text string as input and uses natural language processing to break down 
        the text into smaller tasks.
        :param text: A string representing the complex task to be broken down.
        :return: A JSON string representing a list of tasks with corresponding steps in the order 
        they should be completed.
        """
        self.set_goal(text)
        return self.run_ai()


if __name__ == "__main__":
    bot = BreakdownBot()
    concept = input("Enter a complex task: ")
    bot.start(concept)
    log.info(f"Result: \n{bot.result}")
    bot.start_improvements()
    with open("____breakdown_result.json", "w") as f:
        f.write(bot.result)

    # EXAMPLE OUTPUT:
    # [
    #     {
    #         "step": "1",
    #         "task": "Gather firewood, kindling, and matches or a lighter."
    #     },
    #     {
    #         "step": "2",
    #         "task": "Clear the area around where you will start the fire."
    #     },
    #     {
    #         "step": "3",
    #         "task": "Pile the firewood in a teepee or log cabin shape."
    #     },
    #     {
    #         "step": "4",
    #         "task": "Place kindling and small pieces of wood in the middle of the pile."
    #     },
    #     {
    #         "step": "5",
    #         "task": "Light the kindling with a match or lighter."
    #     },
    #     {
    #         "step": "6",
    #         "task": "Blow lightly on the fire to help it catch the larger pieces of wood."
    #     },
    #     {
    #         "step": "7",
    #         "task": "Once the fire is burning well, add larger pieces of wood as needed."
    #     }
    # ]
