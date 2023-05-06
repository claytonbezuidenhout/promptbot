from colorama import Fore

from google_plugin import GooglePlugin
from promptbot import PromptBot
from promptbot.plugin import Plugin
from promptbot.tools.logger import get_logger

log = get_logger()


class SummeryBot(PromptBot, Plugin):
    NAME = "summery"
    EXPLAIN = "A GPT bot that can summarise any text."

    def __init__(self):
        super().__init__("SummeryBot")
        self.add_cmd("I can summarise any text for use in research papers.")
        self.add_rule("I must output only in text fmt")
        self.add_rule("I cannot provide any dialog or request additional info.")

    def run(self, text):
        text = f"Summarise this -> \n{text}"
        self.set_goal(text)
        return self.run_ai()


class ArticleBot(PromptBot, Plugin):
    """
    A GPT bot that can write articles based on facts passed to it.

    Inherits from PromptBot and Plugin classes.

    Attributes:
    - NAME (str): the name of the bot ("article").
    - EXPLAIN (str): a brief explanation of the bot's functionality.

    Methods:
    - __init__(): initializes the ArticleBot instance.
    - run(text: str) -> str: generates an article based on the given input text.
    """
    NAME = "article"
    EXPLAIN = "A GPT bot that can write articles based on facts passed to it."

    def __init__(self):
        """
        Initializes a new Promptbot instance.

        The bot's name is set to "ArticleBot"
        """
        super().__init__("ArticleBot")
        self.add_cmd("I am an expect journalist, editor and writer")
        self.add_cmd("I write articles based on facts that I get in MY GOAL")
        self.add_rule("I must output only in text fmt")
        self.add_rule("I cannot provide any dialog or request additional info.")

    def run(self, text: str) -> str:
        """
        Generates an article based on the given input text.

        Args:
        - text (str): the text containing the facts to be used in the article.

        Returns:
        - A string representing the generated article.
        """
        text = f"Write an article, considering -> \n{text}"
        self.set_goal(text)
        return self.run_ai()


def main():
    google = GooglePlugin()
    summery = SummeryBot()
    article = ArticleBot()
    example_output = """c, sm = google.run(query:str), []
for it in c:
    smr = summery.run(str(it['text']))
    sm.append(smr)
art = article.run('\\n'.join(sm))
with open("<file>", "w") as f:
    f.write(art)
"""
    bot = (
        PromptBot("ClusterBot", execute_output=True)
        .add_cmd("I can do research and write on any subject. That is my ultimate task.")
        .add_cmd("I can rewrite google queries to be more suitable for research.")
        .add_cmd("I use only plugins to gather info and can't invent ways to do so.")
        .add_cmd("I always ensure my output can be executed in a python runtime. I use code to save files.")
        .add_rule("I can't provide any dialog or request additional info. I must give python code. Nothing else.")
        .add_plugin(google)
        .add_plugin(summery)
        .add_plugin(article)
        .set_example_output(example_output)
    )
    concept = input(f"{Fore.MAGENTA}Enter the concept you want to research: {Fore.RESET}")

    bot.set_goal(f"Research -> \n{concept}")

    log.info(f"Doing research for: {concept}")
    result = bot.run_ai()
    log.info(f"Research result: \n{result}")


if __name__ == "__main__":
    main()
