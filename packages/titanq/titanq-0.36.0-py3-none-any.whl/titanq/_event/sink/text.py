# Copyright (c) 2025, InfinityQ Technology, Inc.

from typing_extensions import override

import logging

from titanq._event.sink import ContentBuilder, Sink


# Configure the logger
logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)


class TextContentBuilder(ContentBuilder):

    def __init__(self):
        self._content = ""

    @override
    def add_emoji(self, emoji: str) -> None:
        # no emoji for text based output
        pass

    @override
    def add_text(self, text: str) -> None:
        self._content += text

    @override
    def add_whitespace(self) -> None:
        self._content += " "

    @override
    def end(self) -> None:
        logging.info(self._content.strip())


class TextSink(Sink):
    """The TextSink is just a simple python logger."""

    def __init__(self, header_text: str):
        """
        Initialize a simple text sink logger.

        :param header: Text logged when initialising the logger
        """
        logging.info(header_text)

    @override
    def content_builder(self) -> ContentBuilder:
        return TextContentBuilder()