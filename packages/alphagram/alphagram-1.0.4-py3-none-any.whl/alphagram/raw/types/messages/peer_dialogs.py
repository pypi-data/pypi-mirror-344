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


class PeerDialogs(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~alphagram.raw.base.messages.PeerDialogs`.

    Details:
        - Layer: ``158``
        - ID: ``3371C354``

    Parameters:
        dialogs (List of :obj:`Dialog <alphagram.raw.base.Dialog>`):
            N/A

        messages (List of :obj:`Message <alphagram.raw.base.Message>`):
            N/A

        chats (List of :obj:`Chat <alphagram.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <alphagram.raw.base.User>`):
            N/A

        state (:obj:`updates.State <alphagram.raw.base.updates.State>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: alphagram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetPeerDialogs
            messages.GetPinnedDialogs
    """

    __slots__: List[str] = ["dialogs", "messages", "chats", "users", "state"]

    ID = 0x3371c354
    QUALNAME = "types.messages.PeerDialogs"

    def __init__(self, *, dialogs: List["raw.base.Dialog"], messages: List["raw.base.Message"], chats: List["raw.base.Chat"], users: List["raw.base.User"], state: "raw.base.updates.State") -> None:
        self.dialogs = dialogs  # Vector<Dialog>
        self.messages = messages  # Vector<Message>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.state = state  # updates.State

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PeerDialogs":
        # No flags
        
        dialogs = TLObject.read(b)
        
        messages = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        state = TLObject.read(b)
        
        return PeerDialogs(dialogs=dialogs, messages=messages, chats=chats, users=users, state=state)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.dialogs))
        
        b.write(Vector(self.messages))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        b.write(self.state.write())
        
        return b.getvalue()
