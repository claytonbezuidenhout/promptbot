from promptbot import PromptBot


def main():
    bot = (
        PromptBot("DocstringBot")
        .add_cmd("I can enrich python code with exceptional docstrings. I can explain what a function does.")
        .add_rule("I must output only in Python file format")
        .add_rule("I cannot change the code in any way")
        .add_rule("I must not move any imports or declarations")
        .add_rule("I cannot provide any dialog or request additional info")

    )

    file = input("Enter the path to a python file: ")
    with open(file, "r") as f:
        data = f.read()
    bot.set_goal(data)
    bot.run_ai()
    print(bot.result)
    bot.start_improvements()
    with open(f"__improved__.{file}", "w") as f:
        f.write(bot.result)


if __name__ == "__main__":
    main()
