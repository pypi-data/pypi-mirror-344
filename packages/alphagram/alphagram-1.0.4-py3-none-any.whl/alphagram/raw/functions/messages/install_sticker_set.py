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


class InstallStickerSet(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``158``
        - ID: ``C78FE460``

    Parameters:
        stickerset (:obj:`InputStickerSet <alphagram.raw.base.InputStickerSet>`):
            N/A

        archived (``bool``):
            N/A

    Returns:
        :obj:`messages.StickerSetInstallResult <alphagram.raw.base.messages.StickerSetInstallResult>`
    """

    __slots__: List[str] = ["stickerset", "archived"]

    ID = 0xc78fe460
    QUALNAME = "functions.messages.InstallStickerSet"

    def __init__(self, *, stickerset: "raw.base.InputStickerSet", archived: bool) -> None:
        self.stickerset = stickerset  # InputStickerSet
        self.archived = archived  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InstallStickerSet":
        # No flags
        
        stickerset = TLObject.read(b)
        
        archived = Bool.read(b)
        
        return InstallStickerSet(stickerset=stickerset, archived=archived)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.stickerset.write())
        
        b.write(Bool(self.archived))
        
        return b.getvalue()
