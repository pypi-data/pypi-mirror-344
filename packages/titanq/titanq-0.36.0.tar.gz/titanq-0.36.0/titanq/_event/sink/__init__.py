# Copyright (c) 2025, InfinityQ Technology, Inc.

from abc import ABC, abstractmethod


class ContentBuilder(ABC):
    """
    This class acts as a context manager to ensure that any necessary
    output build logic is properly executed at the end of content building.

    Usage example:
        with ConcreteContentBuilder() as cb:
                cb.add_emoji("👋")
                cb.add_text("Hello")
    """

    def __enter__(self) -> 'ContentBuilder':
        return self

    def __exit__(self, ex_type, ex_value, ex_trace_back):
        self.end()

    @abstractmethod
    def add_emoji(self, emoji: str) -> None:
        """Add an emoji to the content."""

    @abstractmethod
    def add_text(self, text: str) -> None:
        """Add a text to the content."""

    @abstractmethod
    def add_whitespace(self) -> None:
        """Add a whitespace to the content"""

    @abstractmethod
    def end(self) -> None:
        """Finalize the content building process."""


class Sink(ABC):
    """
    Abstract class of a Sink type object. A Sink is any output type that you could
    use to transfer information from somewhere to another destination.

    As an example, a logger is a Sink.
    """

    @abstractmethod
    def content_builder(self) -> ContentBuilder:
        """Returns a content builder to be able to build an output."""