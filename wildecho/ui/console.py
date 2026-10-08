"""
WildEcho UI Console & Theme Configuration
Centralized Rich Console singleton with forest & nature theme.
"""

from rich.console import Console
from rich.theme import Theme

FOREST_THEME = Theme(
    {
        "forest": "bold green",
        "emerald": "bright_green",
        "biophony": "green",
        "anthrophony": "bright_red",
        "ndsi": "cyan",
        "aci": "magenta",
        "whisper": "bold yellow",
        "forage": "bright_yellow",
        "safety": "bold red",
        "species": "bold cyan",
        "muted": "dim white",
        "accent": "spring_green3",
    }
)

console = Console(theme=FOREST_THEME)
