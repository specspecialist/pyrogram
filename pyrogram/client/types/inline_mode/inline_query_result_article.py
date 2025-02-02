# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from pyrogram.api import types
from .inline_query_result import InlineQueryResult
from ..bots_and_keyboards import InlineKeyboardMarkup
from ..input_message_content import InputMessageContent


class InlineQueryResultArticle(InlineQueryResult):
    """Link to an article or web page.

    Parameters:
        title (``str``):
            Title for the result.

        input_message_content (:obj:`InputMessageContent`):
            Content of the message to be sent.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        url (``str``, *optional*):
            URL of the result.

        description (``str``, *optional*):
            Short description of the result.

        thumb_url (``str``, *optional*):
            URL of the thumbnail for the result.

        reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.
    """

    __slots__ = ["title", "url", "description", "thumb_url"]

    def __init__(
        self,
        title: str,
        input_message_content: InputMessageContent,
        id: str = None,
        reply_markup: InlineKeyboardMarkup = None,
        url: str = None,
        description: str = None,
        thumb_url: str = None
    ):
        super().__init__("article", id, input_message_content, reply_markup)

        self.title = title
        self.url = url
        self.description = description
        self.thumb_url = thumb_url

    def write(self):
        return types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            send_message=self.input_message_content.write(self.reply_markup),
            title=self.title,
            description=self.description,
            url=self.url,
            thumb=types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpeg",
                attributes=[]
            ) if self.thumb_url else None
        )
