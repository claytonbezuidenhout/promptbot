from promptbot import PromptBot


def main():
    bot = (
        PromptBot("documentBot")
        .add_cmd("I can create beautiful documentation in markdown format for python code.")
        .add_cmd("I am an expert in Python and writing documentation")
        .add_rule("The output must be in valid markdown format.")
        .add_rule("I cannot change code in any way")
        .add_rule("I cannot provide any dialog or request additional info")
        .set_example_output("""# Function Name \nHere is a brief description of my python code. In this section, 
        I will describe the overall purpose of my code and its main functionalities. \n\n## Function 1\nThis function 
        does X, Y, and Z. Here is how it works: \n\n```python\n def function1(param1, param2):\n    # code block\n 
        ```\n\n## Function 2\nThis function does A, B, and C. Here is how it works: \n\n```python\n def function2(
        param1, param2):\n    # code block\n ```""")
    )
    file_path = input("Enter the path to the Python file you want documented: ")
    with open(file_path, "r") as f:
        code = f.read()
    bot.set_goal(f"Document this code: \n{code}")

    print("Creating documentation for: " + file_path)
    result = bot.run_ai()
    print(result)

    bot.start_improvements()
    base_filename = file_path.split("/")[-1]
    filename, _ = base_filename.split(".")
    bot.save_to_file(f"{filename}.md")


if __name__ == "__main__":
    main()