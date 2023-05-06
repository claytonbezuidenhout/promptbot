from colorama import Fore

from promptbot.plugin import Plugin
from promptbot.tools.input_mixin import InputMixin
from promptbot.tools.logger import get_logger

log = get_logger()


class FileLinesReplace(Plugin, InputMixin):
    """
    This plugin replaces lines of a file between two line numbers.
    """
    NAME: str = "file_lines_replace"
    EXPLAIN = "This plugin replaces lines of a file between two line numbers."

    def run(self, file: str, start: int, end: int, lines: list) -> str:
        """
        :param file: The file to operate on
        :param start: The line number to start replacing from
        :param end: The line number to stop replacing at
        :param lines: A list of lines to replace with, can be empty to delete lines
        :return: A string indicating success or failure
        """
        with open(file, "r") as f:
            file_lines = f.readlines()
        part_1, part_2 = file_lines[:start - 1], file_lines[end:]
        file_lines = part_1 + lines + part_2

        log.info(f"{Fore.YELLOW}============= REPLACE =============")
        log.info("\n".join(file_lines))
        log.info(f"============= /REPLACE ============={Fore.RESET}")

        if self.check_execute(prompt="Replace? (y/n): "):
            with open(file, "w") as f:
                file_lines = "\n".join(file_lines).replace("\n\n", "\n")
                f.writelines(file_lines)
            return f"Replaced lines {start} to {end} in {file}."
        else:
            return f"No replacement done."
