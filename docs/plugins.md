# Creating a PromptBot with Plugins

In this section, we will explore how to create a promptBot with plugins.

Plugins are modules that contain specific functionality that can be integrated into a promptBot. 
By using plugins, you can extend the capabilities of your promptBot and tailor it to your specific needs. 
Additionally, you can use other promptBots as plugins, which allows for even greater flexibility.

Here's an example code snippet that demonstrates how to create a promptBot with plugins:

```
def app():
    file_lines_get = FileLinesGet()
    file_lines_replace = FileLinesReplace()
    docstring = DocstringBot()

    # Example output for demonstration purposes only
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

    # Creating a promptBot with plugins
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


if __name__ == "__main__":
    # Run the bot
    app()
```

**In this example:**
- we have created a promptBot named "CodeEnrichBot" with three 
plugins: `file_lines_get`, `docstring`, and `file_lines_replace`. 
- We have also defined several commands and rules for our promptBot.

To use another promptBot as a plugin, you can simply import the promptBot module and add it to your bot 
like any other plugin. For example, if you had a promptBot named "DocBot" that you wanted to use as a 
plugin, you could add it to your bot like this:

```
from DocBot import DocBot

...

bot = (
    PromptBot("CodeEnrichBot", execute_output=True)
    .add_cmd("I enrich projects with supporting data like docstrings and documentation.")
    .add_cmd("I use only plugins to gather info and can't invent ways to do so.")
    .add_cmd("I always ensure my output can be executed in a python runtime. I use code to save files.")
    .add_rule("I can't provide any dialog or request additional info. I must give python code. Nothing else.")
    .add_plugin(DocBot())
    .add_plugin(file_lines_get)
    .add_plugin(file_lines_replace)
    .set_example_output(example_output)
)

``` 

By following these steps, you can easily create a promptBot with plugins that will allow you to automate tasks 
and generate output based on user input. 

# Writing a Plugin in Python

In this section, we will explore how to write a plugin in Python.

Here's an example code snippet of a base class for creating plugins:

`Plugin` is a simple abstract base class that all plugins should inherit from. 
It contains two class attributes, `EXPLAIN` and `NAME`, 
which are used to provide information about the plugin. 
It also defines an abstract method `run()` that should be implemented in the plugin.

To write a plugin, you can create a new class that inherits from the `Plugin` base class 
and implements the `run()` method. Here's an example code snippet of a plugin that gets 
lines of a file between two line numbers:
```
class FileLinesGet(Plugin):
    NAME = "file_lines_get"
    EXPLAIN = "This plugin gets lines of a file between two line numbers."

    def run(self, file: str, start: int, end: int) -> str:
        with open(file, "r") as f:
            lines = f.readlines()
        lines = lines[start - 1:end]
        lines = "".join(lines)
        log.info(f"{Fore.BLUE}============= LINES =============")
        log.info(lines)
        log.info(f"============= /LINES ============={Fore.RESET}")

        return lines
```

**In this example:**
- we have created a new class `FileLinesGet` that inherits from the `Plugin` base class
- We have defined two class attributes, `NAME` and `EXPLAIN`, which provide information about the plugin. 
- We have also implemented the `run()` method, which takes in the file path, 
start line number, and end line number as arguments. The method reads the file, extracts the lines 
between the specified line numbers, logs the lines to the console, and returns the lines as a string.


Once you have written your plugin, you can add it to your promptBot by importing the module
and creating an instance of the plugin class. For example, if you had a plugin named "MyPlugin" 
in a module named "myplugin.py", you could add it to your bot like this:

```
from myplugin import MyPlugin

...

bot = (
    PromptBot("MyBot")
    .add_plugin(MyPlugin())
    ...
)
```