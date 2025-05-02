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


class TermsOfServiceUpdate(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~alphagram.raw.base.help.TermsOfServiceUpdate`.

    Details:
        - Layer: ``158``
        - ID: ``28ECF961``

    Parameters:
        expires (``int`` ``32-bit``):
            N/A

        terms_of_service (:obj:`help.TermsOfService <alphagram.raw.base.help.TermsOfService>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: alphagram.raw.functions

        .. autosummary::
            :nosignatures:

            help.GetTermsOfServiceUpdate
    """

    __slots__: List[str] = ["expires", "terms_of_service"]

    ID = 0x28ecf961
    QUALNAME = "types.help.TermsOfServiceUpdate"

    def __init__(self, *, expires: int, terms_of_service: "raw.base.help.TermsOfService") -> None:
        self.expires = expires  # int
        self.terms_of_service = terms_of_service  # help.TermsOfService

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TermsOfServiceUpdate":
        # No flags
        
        expires = Int.read(b)
        
        terms_of_service = TLObject.read(b)
        
        return TermsOfServiceUpdate(expires=expires, terms_of_service=terms_of_service)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.expires))
        
        b.write(self.terms_of_service.write())
        
        return b.getvalue()
