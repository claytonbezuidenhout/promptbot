from promptbot import PromptBot
from promptbot.tools.logger import get_logger

log = get_logger()


def main() -> None:
    """
    Runs the PromptBot to create documentation in markdown format for a given Python code file.
    :return: None
    """
    bot = (
        PromptBot("documentBot")
        .add_cmd("I can create beautiful documentation in markdown format for python code.")
        .add_cmd("I am an expert in Python and writing documentation")
        .add_rule("The output must be in valid markdown format.")
        .add_rule("I cannot change code in any way")
        .add_rule("I cannot provide any dialog or request additional info")
        .set_example_output("""# Function Name 
Here is a brief description of the python code. In this section, we will describe the overall purpose of the code and its main functionalities. 
## Function 1
This function does X, Y, and Z. Here is how it works: 
```python
 def function1(param1, param2):
    # code block
```

## Function 2
This function does A, B, and C. Here is how it works: 
```python
 def function2(param1, param2):
    # code block
```""")
    )
    file_path = input("Enter the path to the Python file you want documented: ")
    with open(file_path, "r") as f:
        code = f.read()
    bot.set_goal(f"Document this code: \n{code}")
    log.info(f"Creating documentation for: {file_path}")
    result = bot.run_ai()
    log.info(f"Result: \n{result}")
    bot.start_improvements()
    base_filename = file_path.split("/")[-1]
    filename, _ = base_filename.split(".")
    bot.save_to_file(f"{filename}.md")


if __name__ == "__main__":
    main()
