from colorama import Fore

from examples.plugins.working_with_files.file_read_plugin import FileLinesGet
from examples.plugins.working_with_files.file_write_plugin import FileLinesReplace
from promptbot import PromptBot
from promptbot.plugin import Plugin
from promptbot.tools.logger import get_logger

log = get_logger()


class DocstringBot(PromptBot, Plugin):
    NAME = "docstring"
    EXPLAIN = "a bot that enriches python code with docstrings"

    def __init__(self):
        super().__init__("DocstringBot")
        self.add_cmd("I can enrich python code with exceptional docstrings. I can explain what a function does.")
        self.add_rule("I can correct docstrings that are mismatched with the code.")
        self.add_rule("I must output only in python code format")
        self.add_rule("I cannot change any logic in the code. I can only add docstrings.")
        self.add_rule("I must strictly adhere to the output format of the example output.")
        self.add_rule("I cannot provide any dialog or request additional info.")
        self.set_example_output("""
def example(data: list[dict] , fields: tuple) -> list:
    \"\"\"
    Returns a list for each product in `products` containing the requested fields
    specified in `fields`.
    :param data: A list of dictionaries representing different products.
    :param fields: A tuple of strings representing the fields to be included in the output list.
    :return: A list of lists containing only the requested fields for each product.
    \"\"\"
    """)

    def run(self, text):
        text = f"Write or correct: \n{text}"
        self.set_goal(text)
        return self.run_ai()


def main():
    file_lines_get = FileLinesGet()
    file_lines_replace = FileLinesReplace()
    docstring = DocstringBot()

    example_output = """
# TRAIN OF THOUGHT:
# 1. get lines 1 to 10
# 2. get docstring for lines 1 to 10
...
lines = [1, 10]
gl = file_lines_get.run("<file>", lines[0], lines[1])
newl = docstring.run(gl).split("\n")
rt = file_lines_replace.run("<file>", lines[0], lines[1], newl)
"""
    log.info(":========: Code Enrich Bot :=========:")
    bot = (
        PromptBot("CodeEnrichBot", execute_output=True)
        .add_cmd("I enrich projects with supporting data like docstrings and documentation.")
        .add_cmd("I use only plugins to gather info and can't invent ways to do so.")
        .add_cmd("I always ensure my output can be executed in a python runtime. I use code to save files.")
        .add_rule("I can't provide any dialog or request additional info. I must give python code. Nothing else.")
        .add_plugin(file_lines_get)
        .add_plugin(docstring)
        .add_plugin(file_lines_replace)
        .set_example_output(example_output)
    )
    while True:
        concept = bot.get_input("Enter the filepath, start and end line numbers: ")

        bot.set_goal(f"Do -> \n{concept}")
        log.info(f"Starting Enrichment: {Fore.CYAN}{concept}{Fore.RESET}")
        bot.run_ai()
        if not bot.check_continue():
            break
    log.info(":========: END :=========:")


if __name__ == "__main__":
    main()
