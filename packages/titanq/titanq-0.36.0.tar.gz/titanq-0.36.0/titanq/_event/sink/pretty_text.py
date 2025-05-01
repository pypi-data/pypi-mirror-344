# Copyright (c) 2025, InfinityQ Technology, Inc.

from typing_extensions import override

from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel

from titanq._event import Sink
from titanq._event.sink import ContentBuilder

# if set to true will add the path to the source where it was logged from.
# no useful in this case we do not manage the source and will only lead
# to this file.
_LOG_PATH = False

# if set to true, will repeat timestamps on sequent logs even if the same
_REPEAT_TIMESTAMPS = True

# This option disable the option that forces the logger to be optimized for jupyter.
# Disabling this avoid logs to be split into multiple cells
# which isn't in our case (we will need to use Live feature).
_FORCE_JUPYTER_RENDERING = False


class PrettyTextContentBuilder(ContentBuilder):

    def __init__(self, console: Console):
        self._console = console
        self._content = ""

    @override
    def add_emoji(self, emoji: str) -> None:
        self._content += emoji

    @override
    def add_text(self, text: str) -> None:
        self._content += text

    @override
    def add_whitespace(self) -> None:
        self._content += " "

    @override
    def end(self) -> None:
        self._console.log(self._content)


class PrettyTextSink(Sink):
    """
    The PrettyTextSink utilizes rich library to enhance the output and make it
    as beautiful as possible and pleasing for the end-users.

    It offers features such as Emoji's support, colors and some progress bars.
    """

    def __init__(self, banner_header_text: str):
        """
        Initialize the pretty sink logger.

        :param banner_header_text: Text added to the top of the banner
        """
        self._console = Console(log_path=_LOG_PATH, force_jupyter=_FORCE_JUPYTER_RENDERING)
        self._console._log_render.omit_repeated_times = not _REPEAT_TIMESTAMPS

        self._display_banner(header=banner_header_text)

    @override
    def content_builder(self) -> ContentBuilder:
        return PrettyTextContentBuilder(self._console)

    def _display_banner(self, header: str) -> None:
        """
        Displays a banner.
        """
        #╭───────────────── Version vX.Y.Z ──────────────────╮
        #│      _________________              _______       │
        #│      ___  __/__(_)_  /______ _________  __ \      │
        #│      __  /  __  /_  __/  __ `/_  __ \  / / /      │
        #│      _  /   _  / / /_ / /_/ /_  / / / /_/ /       │
        #│      /_/    /_/  \__/ \__,_/ /_/ /_/\___\_\       │
        #│                                                   │
        #│                                                   │
        #╰───────────────────────────────────────────────────╯
        panel = Panel.fit(
            Figlet(font='speed').renderText("TitanQ"), style="purple",
            title=f"[italic bold purple]{header}[/]",
            padding=(0, 6),  # (top_bottom, left_right)
            border_style="purple",
        )
        self._console.print(panel)