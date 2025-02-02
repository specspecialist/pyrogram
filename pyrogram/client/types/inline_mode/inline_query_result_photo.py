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

from typing import Union

from pyrogram.api import types
from .inline_query_result import InlineQueryResult
from ..bots_and_keyboards import InlineKeyboardMarkup
from ..input_message_content import InputMessageContent
from ...parser import Parser


class InlineQueryResultPhoto(InlineQueryResult):
    """Link to a photo.

    By default, this photo will be sent by the user with optional caption.
    Alternatively, you can use *input_message_content* to send a message with the specified content instead of the
    photo.

    Parameters:
        photo_url (``str``):
            A valid URL of the photo.
            Photo must be in jpeg format an must not exceed 5 MB.

        thumb_url (``str``, *optional*):
            URL of the thumbnail for the photo.
            Defaults to the value passed in *photo_url*.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        title (``str``, *optional*):
            Title for the result.

        description (``str``, *optional*):
            Short description of the result.

        caption (``str``, *optional*):
            Caption of the photo to be sent, 0-1024 characters.

        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.

        reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
            An InlineKeyboardMarkup object.

        input_message_content (:obj:`InputMessageContent`):
            Content of the message to be sent instead of the photo.
    """

    __slots__ = [
        "photo_url", "thumb_url", "title", "description", "caption", "parse_mode", "reply_markup",
        "input_message_content"
    ]

    def __init__(
        self,
        photo_url: str,
        thumb_url: str = None,
        id: str = None,
        title: str = None,
        description: str = None,
        caption: str = None,
        parse_mode: Union[str, None] = object,
        reply_markup: InlineKeyboardMarkup = None,
        input_message_content: InputMessageContent = None
    ):
        super().__init__("photo", id, input_message_content, reply_markup)

        self.photo_url = photo_url
        self.thumb_url = thumb_url
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    def write(self):
        photo = types.InputWebDocument(
            url=self.photo_url,
            size=0,
            mime_type="image/jpeg",
            attributes=[]
        )

        if self.thumb_url is None:
            thumb = photo
        else:
            thumb = types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpeg",
                attributes=[]
            )

        return types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            thumb=thumb,
            content=photo,
            send_message=(
                self.input_message_content.write(self.reply_markup)
                if self.input_message_content
                else types.InputBotInlineMessageMediaAuto(
                    reply_markup=self.reply_markup.write() if self.reply_markup else None,
                    **(Parser(None)).parse(self.caption, self.parse_mode)
                )
            )
        )
