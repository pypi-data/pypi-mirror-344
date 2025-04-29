# SPDX-FileCopyrightText: 2025-present Marceau <git@marceau-h.fr>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from enum import Enum

class Formats(Enum):
    video = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".mpeg", ".mpg", ".3gp", ".3g2"}
    image = {".jpg"}
    audio = {".wav", ".aac", ".mp3"}
    text = {".txt"}
    csv = {".csv"}
    json = {".json"}
    html = {".html"}

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: "Formats") -> bool:
        if isinstance(other, Formats):
            return self.value == other.value
        return False

    def __ne__(self, other: "Formats") -> bool:
        if isinstance(other, Formats):
            return self.value != other.value
        return True

    def __contains__(self, other: str) -> bool:
        if isinstance(other, str):
            return other in self.value
        return False
