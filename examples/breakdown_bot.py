from promptbot import PromptBot


class BreakdownBot(PromptBot):
    def __init__(self):
        super().__init__("BreakdownBot")
        self.add_cmd("I can breakdown any complex task into smaller tasks.")
        self.add_rule("I must output only a data structure in JSON format")
        self.add_rule("I cannot provide any dialog or request additional info")
        self.add_rule("I must output only in the example format.")
        self.set_example_output(f'[{{ "step": "1", "task": "The 1st task I create"}},'
                            f'{{ "step": "2", "task": "The 2nd task I create"}}]')

    def start(self, text):
        self.set_goal(text)
        return self.run_ai()


if __name__ == "__main__":
    bot = BreakdownBot()
    bot.start(f"""Creating a BBQ Fire with charcoal.""")
    print(bot.result)
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
