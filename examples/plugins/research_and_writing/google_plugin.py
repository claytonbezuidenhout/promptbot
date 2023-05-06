import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from promptbot.plugin import Plugin
from promptbot.tools.config_manager import config

import tiktoken

from promptbot.tools.logger import get_logger

log = get_logger()


def count_tokens(text):
    enc = tiktoken.encoding_for_model(config.get("openai", {}).get("model"))
    token_grid = enc.encode(text)
    return len(token_grid)


def trim_text_sentences(text, count=1):
    sentences = text.split('.')
    if len(sentences) <= 1:
        return text
    else:
        return '.'.join(sentences[:-count])


class GooglePlugin(Plugin):
    NAME = "google"
    EXPLAIN = "This plugin uses the Google Custom Search API to get the top results for a query."

    def __init__(self):
        self.api_key = config.get("google", {}).get("api_key")
        self.cse_id = config.get("google", {}).get("cse_id")
        self.service = build('customsearch', 'v1', developerKey=self.api_key)

    def remove_excessive_linebreaks(self, text):
        if '\n\n' not in text:
            return text
        else:
            new_string = text.replace('\n\n', '\n')
            return self.remove_excessive_linebreaks(new_string)

    def remove_tabs(self, text):
        if '\t' not in text:
            return text
        else:
            new_string = text.replace('\t', '')
            return self.remove_tabs(new_string)

    @staticmethod
    def remove_short_lines(text, cuttoff=50):
        lines = text.split('\n')
        long_lines = filter(lambda line: len(line) >= cuttoff, lines)
        return '\n'.join(long_lines)

    def extract_text(self, data):
        data = data["items"]
        for item in data:
            title = item.get("title")
            link = item.get("link")
            log.info(f"Fetching {title}...")
            log.info(f"Link: {link}")
            response = requests.get(link)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            text = self.remove_excessive_linebreaks(soup.get_text())
            text = self.remove_tabs(text)
            text = text.replace("  ", " ").replace("  ", " ")
            text = self.remove_short_lines(text)
            while True:
                if count_tokens(text) <= 1024:
                    break
                text = trim_text_sentences(text)
            item['text'] = text
        return data

    def run(self, query, limit=3):
        try:
            data = self.service.cse().list(q=query, cx=self.cse_id, fields="items(title,link)", num=limit).execute()
            result = self.extract_text(data)
            return result
        except HttpError as error:
            log.error(f'An HTTP error occurred: {error}')
