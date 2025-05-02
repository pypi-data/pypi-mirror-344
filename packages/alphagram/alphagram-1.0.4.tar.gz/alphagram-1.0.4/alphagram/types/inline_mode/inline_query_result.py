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

from uuid import uuid4

import alphagram
from alphagram import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~alphagram.types.InlineQueryResultCachedAudio`
    - :obj:`~alphagram.types.InlineQueryResultCachedDocument`
    - :obj:`~alphagram.types.InlineQueryResultCachedAnimation`
    - :obj:`~alphagram.types.InlineQueryResultCachedPhoto`
    - :obj:`~alphagram.types.InlineQueryResultCachedSticker`
    - :obj:`~alphagram.types.InlineQueryResultCachedVideo`
    - :obj:`~alphagram.types.InlineQueryResultCachedVoice`
    - :obj:`~alphagram.types.InlineQueryResultArticle`
    - :obj:`~alphagram.types.InlineQueryResultAudio`
    - :obj:`~alphagram.types.InlineQueryResultContact`
    - :obj:`~alphagram.types.InlineQueryResultDocument`
    - :obj:`~alphagram.types.InlineQueryResultAnimation`
    - :obj:`~alphagram.types.InlineQueryResultLocation`
    - :obj:`~alphagram.types.InlineQueryResultPhoto`
    - :obj:`~alphagram.types.InlineQueryResultVenue`
    - :obj:`~alphagram.types.InlineQueryResultVideo`
    - :obj:`~alphagram.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "alphagram.Client"):
        pass
