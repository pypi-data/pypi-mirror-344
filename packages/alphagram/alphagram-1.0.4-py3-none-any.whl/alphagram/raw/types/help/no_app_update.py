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


class NoAppUpdate(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~alphagram.raw.base.help.AppUpdate`.

    Details:
        - Layer: ``158``
        - ID: ``C45A6536``

    Parameters:
        No parameters required.

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: alphagram.raw.functions

        .. autosummary::
            :nosignatures:

            help.GetAppUpdate
    """

    __slots__: List[str] = []

    ID = 0xc45a6536
    QUALNAME = "types.help.NoAppUpdate"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "NoAppUpdate":
        # No flags
        
        return NoAppUpdate()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
