# Copyright (c) 2025, InfinityQ Technology, Inc.

from abc import ABC, abstractmethod
from typing import List, Union

from titanq._event.sink import Sink
from titanq._event.sink.pretty_text import PrettyTextSink
from titanq._event.sink.text import TextSink
from titanq._version import __version__ as titanq_version


class Event(ABC):

    @abstractmethod
    def output(self, sink: Sink):
        """Output self to the sink."""


class EventEmitter():
    """
    A class responsible for emitting events to subscribed output sinks.
    """

    def __init__(self):
        self._sinks: List[Sink] = []

    def subscribe(self, sink: Sink) -> None:
        """subscribe a sink to the events."""
        self._sinks.append(sink)

    def emit(self, event: Event) -> None:
        """Emit an event to the subscribed sinks."""
        for sink in self._sinks:
            event.output(sink)


class EventEmitterFactory():
    """
    Creates an EventEmitter.
    None, on or multiple sinks will be subscribed based on the `log_mode`.
    """

    def __init__(self):
        self._event_emitter = EventEmitter()

    def create(self, log_mode: Union[str, List[str], None]) -> EventEmitter:
        """Setup all sinks based on the given mode and returns the EventEmitter"""

        if log_mode is None or log_mode == "off":
            return self._event_emitter

        elif isinstance(log_mode, str):
            self._event_emitter.subscribe(self._new_sink(log_mode))

        elif isinstance(log_mode, list):
            for mode in log_mode:
                self._event_emitter.subscribe(self._new_sink(mode))

        else:
            raise ValueError("log_mode must be a string, list of strings, or None")

        return self._event_emitter

    def _new_sink(self, type: str) -> Sink:
        if type == "pretty":
            return PrettyTextSink(titanq_version)
        elif type == "text":
            return TextSink(f"Using TitanQ SDK {titanq_version}")
        else:
            raise ValueError(f"got an unknown log_mode type: {type}")