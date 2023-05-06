import inspect
import traceback

from colorama import Fore, Style

from promptbot.tools.api import exec_openai
from promptbot.tools.config_manager import config
from promptbot.tools.input_mixin import InputMixin
from promptbot.tools.logger import get_logger

log = get_logger()


class PromptBot(InputMixin):
    """
    A class for generating a prompt and retrieving a response from GPT OpenAI.

    Attributes
    ----------
    name: str
        name of the promptBot
    execute_output: bool
        boolean value representing whether the output should be executed or not
    version_limit: int
        limit for the versions of output promptBot can have
    goal: str
        the goal of promptBot
    result: str
        the result of the last promptBot execution
    prompt: str
        the prompt for the OpenAI API
    improve_prompt: str
        the prompt for improving the previous output
    improve: str
        the improvement to be made
    rules: list
        a list of promptBot rules
    commands: list
        a list of commands that define promptBots behavior
    versions: list
        a list of promptBot versions, builds automatically as you execute promptBot

    Methods
    -------
    __init__(self, name=None, execute_output=False, version_limit=3)
        Initializes the PromptBot object
    set_goal(self, goal)
        Sets the goal of promptBot
    add_rule(self, rule)
        Adds a rule to the list of promptBot rules
    set_example_output(self, output)
        Sets the example output
    add_cmd(self, command)
        Adds a command to the list of commands promptBot accepts
    get_prompt(self)
        Creates the prompt for the OpenAI API
    _set_and_return_improve_prompt(self)
        Creates the prompt for improving the previous output
    _set_improve(self, improve)
        Sets the improvement made between two different versions
    run_ai(self, improve=False)
        Runs OpenAI API on the prompt and retrieves the result
    start_improvements(self)
        Starts the improvement process
    _execute_code(self)
        Executes the output if execute_output is True
    save_to_file(self, file_name)
        Saves the result to a file
    save_versions(self, file_name)
        Saves all versions of output to a file
    """

    def __init__(self, name=None, execute_output=False, version_limit=3, filter_defaults=True, autonomous=False):
        """
        Initializes the PromptBot object.

        Parameters
        ----------
        name: str, optional
            name of the promptBot
        execute_output: bool, optional
            boolean value representing whether the output should be executed or not
        version_limit: int, optional
            limit for the versions of output promptBot can have
        """
        self.name = name if name else "promptBot"
        self.execute_output = execute_output
        self.version_limit = version_limit
        self.filter_defaults = filter_defaults  # used by plugins to remove parameters with default in the prompt
        self.autonomous = autonomous  # will execute without user input if True

        self.goal = None
        self.result = None
        self.prompt = None
        self.improve_prompt = None
        self.improve = None
        self.rules = []
        self.examples = []
        self.commands = []
        self.versions = []
        self.plugins = {}

        self.add_cmd(f"I am autonomous. There's no users, just {self.name}.")
        if self.execute_output:
            self.add_rule("My output will be executed in Python. I must output only valid Python code.")

    def set_goal(self, goal):
        """
        Sets the goal of promptBot.

        Parameters
        ----------
        goal: str
            the goal of promptBot

        Returns
        -------
        self
        """
        self.goal = goal
        self.prompt = None
        return self

    def add_rule(self, rule):
        """
        Adds a rule to the list of promptBot rules.

        Parameters
        ----------
        rule: str
            the new rule to be added

        Returns
        -------
        self
        """
        self.rules.append(rule)
        return self

    def set_example_input(self, input_data):
        """
        Sets the example input.

        Parameters
        ----------
        input_data: str
            the example input to be set

        Returns
        -------
        self
        """
        self.examples.append(f"EXAMPLE INPUT:\n{input_data}")

        return self

    def set_example_output(self, output_data):
        """
        Sets the example output.

        Parameters
        ----------
        output_data: str
            the example output to be set

        Returns
        -------
        self
        """
        self.examples.append(f"EXAMPLE OUTPUT:\n{output_data}")
        return self

    def add_cmd(self, command):
        """
        Adds a command to the list of commands that defines what PromptBot can do.

        Parameters
        ----------
        command: str
            the new command to be added

        Returns
        -------
        self
        """
        self.commands.append(command)
        return self

    def add_plugin(self, plugin_class):
        if not self.execute_output:
            raise Exception("Cannot add plugins if execute_output is False.")
        self.plugins[plugin_class.NAME] = plugin_class
        return self

    def get_prompt(self):
        """
        Creates the prompt for the OpenAI API.

        Returns
        -------
        prompt: str
            the prompt for the OpenAI API
        """
        if not self.prompt:
            prompt = f"I am {self.name}. I must complete MY GOAL.\n"
            cmds = "\n".join(self.commands)
            rules = "\n".join(self.rules)
            examples = "\n".join(self.examples)
            prompt += f"{cmds}\n" if cmds else ""

            if self.plugins:
                prompt += "I have plugins. Python functions I can use to help finish MY GOAL. I must use them like the example/s below.\n"
                prompt += "MY PLUGINS:\n"
                for plugin_name, plugin in self.plugins.items():
                    signature = inspect.signature(plugin.run)
                    param_list = []
                    for param in signature.parameters:
                        if "=" in param and self.filter_defaults:
                            continue
                        param_list.append(param)
                    param_text = ", ".join([param for param in signature.parameters])
                    prompt += f"- self.plugins['{plugin_name}'].run({param_text}) # {plugin.EXPLAIN}\n"

            prompt += f"MY RULES:\n{rules}\n" if rules else ""
            prompt += f"{examples}\n" if examples else ""
            prompt += f"MY GOAL:\n{self.goal}"
            self.prompt = prompt

        log.debug(f"{Fore.BLUE}ASSEMBLED PROMPT : {self.prompt}{Style.RESET_ALL}")
        return self.prompt

    def run_ai(self, improve=False):
        """
        Runs OpenAI API on the prompt and retrieves the result.

        Parameters
        ----------
        improve: bool
            boolean value representing whether promptBot will improve its output or not

        Returns
        -------
        result: str
            the result of the OpenAI API call
        """
        result = exec_openai(self.get_prompt() if not improve else self._set_and_return_improve_prompt())

        if len(self.versions) > self.version_limit:
            log.debug(f"{Fore.YELLOW}Dropping a version of output due to limit of {self.version_limit}{Style.RESET_ALL}")
            self.versions.pop(0)

        self.versions.append(result)
        self.result = self.versions[-1]
        if not improve:
            self._execute_code()
        return self.result

    def start_improvements(self):
        """
        Starts the improvement process.
        """
        while True:
            if not self.check_improve():
                break

            self._set_improve(self.get_input(Fore.MAGENTA + "How should I improve? "))
            result = self.run_ai(improve=True)
            log.info(f"{Fore.GREEN}============ IMPROVEMENT ============{Style.RESET_ALL}")
            log.info(result)
            log.info(f"{Fore.GREEN}=========== /IMPROVEMENT ============{Style.RESET_ALL}")
            self._execute_code()

    def save_to_file(self, file_name):
        """
        Saves the result to a file.

        Parameters
        ----------
        file_name: str
            the name of the file

        """
        with open(file_name, 'w') as f:
            f.write(self.result)

    def save_versions(self, file_name):
        """
        Saves all versions of output to a file.

        Parameters
        ----------
        file_name: str
            the name of the file
        """
        with open(file_name, 'w') as f:
            f.write("\n".join(self.versions))

    def _set_and_return_improve_prompt(self):
        """
        Creates the prompt for improving the previous output.

        Returns
        -------
        improve_prompt: str
            the prompt for improving the previous output
        """
        self.improve_prompt = f"""{self.prompt}\n I must improve my previous output\nMY PREVIOUS OUTPUT:\n{self.result}\nIMPROVEMENT TO MAKE:\n{self.improve}"""

        log.debug(f"{Fore.BLUE} IMPROVE PROMPT : {self.improve_prompt}{Style.RESET_ALL}")
        return self.improve_prompt

    def _set_improve(self, improve):
        """
        Sets the improvement made between two different versions.

        Parameters
        ----------
        improve: str
            the improvement made between two different versions

        Returns
        -------
        self
        """
        self.improve = improve
        return self

    def _get_fixed_code(self, old_code, traceback_error):
        prompt = f"I must fix my code. \n code I wrote: \n```{old_code}```\n error: \n```{traceback_error}```\n"
        prompt += f"Original Task: {self.goal}\n. GOLDEN RULE: only output the code. " \
                  f"I cannot ask questions or provide dialogue.\n"

        result = exec_openai(prompt)
        return result

    def _execute_code(self, result=None):
        """
        Executes the output if execute_output is True.
        """
        if self.execute_output:
            log.info(f"{Fore.LIGHTGREEN_EX}======== OUTPUT =========")
            log.info(self.result if not result else result)
            log.info(f"======== /OUTPUT ========={Fore.RESET}")
            while True:
                continue_execution = self.check_execute() if not self.autonomous else True
                if not continue_execution:
                    break

                try:
                    log.info(f"{Fore.CYAN}======== EXECUTING =========")
                    exec(self.result if not result else result)
                    log.info(f"======== /EXECUTING ========={Fore.RESET}")
                    break
                except Exception:
                    error = traceback.format_exc()
                    log.error(f"{Fore.RED}======== ERROR =========")
                    log.error(error)
                    log.error(f"======== /ERROR ========={Fore.RESET}")
                    fixed_code = self._get_fixed_code(self.result if not result else result, error)
                    self._execute_code(fixed_code)

