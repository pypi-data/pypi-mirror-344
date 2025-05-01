# Copyright (c) 2025, InfinityQ Technology, Inc.

"""
Milestone events are some type of events that would just occur at some point.
Nothing special about them, they just happen and something is instantly done.
"""

from typing_extensions import override

from titanq._event import Event
from titanq._event.sink import Sink


class PreparingDataEvent(Event):

    @override
    def output(self, sink: Sink) -> None:
        with sink.content_builder() as cb:
            cb.add_emoji(":wrench:")
            cb.add_whitespace()
            cb.add_text("Preparing data for TitanQ...")


class UploadStartEvent(Event):

    @override
    def output(self, sink: Sink) -> None:
        with sink.content_builder() as cb:
            cb.add_emoji(":outbox_tray:")
            cb.add_whitespace()
            cb.add_text("Starting data upload...")

class UploadEndEvent(Event):

    @override
    def output(self, sink: Sink) -> None:
        with sink.content_builder() as cb:
            cb.add_emoji(":clock1:")
            cb.add_whitespace()
            cb.add_text("Upload completed!")


class SendingRequestEvent(Event):

    @override
    def output(self, sink: Sink) -> None:
        with sink.content_builder() as cb:
            cb.add_emoji(":rocket:")
            cb.add_whitespace()
            cb.add_text("Sending request to the server...")


class OptimizationCompletedEvent(Event):

    @override
    def output(self, sink: Sink) -> None:
        with sink.content_builder() as cb:
            cb.add_emoji(":white_check_mark:")
            cb.add_whitespace()
            cb.add_text("Optimization completed!")