from colorama import Fore

from promptbot.plugin import Plugin
from promptbot.tools.logger import get_logger

log = get_logger()


class FileLinesGet(Plugin):
    NAME = "file_lines_get"
    EXPLAIN = "This plugin gets lines of a file between, two line numbers."

    def run(self, file: str, start: int, end: int) -> str:
        """
        Runs the plugin.

        Args:
            :param file: file path
            :param start: line number to start from
            :param end: line number to end at
        """
        with open(file, "r") as f:
            lines = f.readlines()
        lines = lines[start - 1:end]
        lines = "".join(lines)
        log.info(f"{Fore.BLUE}============= LINES =============")
        log.info(lines)
        log.info(f"============= /LINES ============={Fore.RESET}")

        return lines


if __name__ == '__main__':
    file_lines_get = FileLinesGet()
    print(file_lines_get.run("/Users/cbezui/projects/promptbot/test.py", 3, 10))