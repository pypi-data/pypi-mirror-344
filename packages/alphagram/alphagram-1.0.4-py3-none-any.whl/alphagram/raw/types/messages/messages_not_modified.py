#  Alphagram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Alphagram.
#
#  Alphagram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Alphagram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Alphagram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from alphagram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from alphagram.raw.core import TLObject
from alphagram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class MessagesNotModified(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~alphagram.raw.base.messages.Messages`.

    Details:
        - Layer: ``158``
        - ID: ``74535F21``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

    Functions:
        This object can be returned by 13 functions.

        .. currentmodule:: alphagram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetMessages
            messages.GetHistory
            messages.Search
            messages.SearchGlobal
            messages.GetUnreadMentions
            messages.GetRecentLocations
            messages.GetScheduledHistory
            messages.GetScheduledMessages
            messages.GetReplies
            messages.GetUnreadReactions
            messages.SearchSentMedia
            channels.GetMessages
            stats.GetMessagePublicForwards
    """

    __slots__: List[str] = ["count"]

    ID = 0x74535f21
    QUALNAME = "types.messages.MessagesNotModified"

    def __init__(self, *, count: int) -> None:
        self.count = count  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessagesNotModified":
        # No flags
        
        count = Int.read(b)
        
        return MessagesNotModified(count=count)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        return b.getvalue()
