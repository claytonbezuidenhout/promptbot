from promptbot import PromptBot


class SentimentBot(PromptBot):

    def __init__(self):
        super().__init__("SentimentBot")
        self.add_cmd("I can determine the sentiment of a list of sentences.")
        self.add_rule("I must output a dictionary containing the sentiments of each sentence.")
        self.add_rule("I cannot provide any dialog or request additional info. Just the JSON output.")
        self.set_example_output('[\n{"input": "{sentence}", "sentiment": "Positive" or "Negative" or "Neutral"]}\n]')

    def start(self, list_of_sentences):
        text = f"Analyze the following -> \n{list_of_sentences}"
        self.set_goal(text)
        return self.run_ai()


if __name__ == "__main__":
    bot = SentimentBot()
    data = [
        "I love this product",
        "I hate this product",
        "I don't care about this product",
        "I don't know how I feel about this product",
        "Seems great to me",
        "Somewhat of a drag at times, but generally good",
    ]
    bot.start(data)
    print(bot.result)
    bot.start_improvements()
    with open("____sentiment_result.json", "w") as f:
        f.write(bot.result)

    # Example output:
    # [
    #     {"input": "I love this product", "sentiment": "Positive"},
    #     {"input": "I hate this product", "sentiment": "Negative"},
    #     {"input": "I don't care about this product", "sentiment": "Neutral"},
    #     {"input": "I don't know how I feel about this product", "sentiment": "Neutral"},
    #     {"input": "Seems great to me", "sentiment": "Positive"},
    #     {"input": "Somewhat of a drag at times, but generally good", "sentiment": "Neutral"}
    # ]
