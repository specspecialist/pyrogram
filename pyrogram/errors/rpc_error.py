# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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

import re
from datetime import datetime
from importlib import import_module
from typing import Type

from pyrogram.api.core import TLObject
from pyrogram.api.types import RpcError as RawRPCError
from .exceptions.all import exceptions


class RPCError(Exception):
    ID = None
    CODE = None
    NAME = None
    MESSAGE = "{x}"

    def __init__(self, x: int or RawRPCError = None, rpc_name: str = None, is_unknown: bool = False):
        super().__init__("[{} {}]: {} {}".format(
            self.CODE,
            self.ID or self.NAME,
            self.MESSAGE.format(x=x),
            '(caused by "{}")'.format(rpc_name) if rpc_name else ""
        ))

        try:
            self.x = int(x)
        except (ValueError, TypeError):
            self.x = x

        if is_unknown:
            with open("unknown_errors.txt", "a", encoding="utf-8") as f:
                f.write("{}\t{}\t{}\n".format(datetime.now(), x, rpc_name))

    @staticmethod
    def raise_it(rpc_error: RawRPCError, rpc_type: Type[TLObject]):
        error_code = rpc_error.error_code
        error_message = rpc_error.error_message
        rpc_name = ".".join(rpc_type.QUALNAME.split(".")[1:])

        if error_code not in exceptions:
            raise UnknownError(
                x="[{} {}]".format(error_code, error_message),
                rpc_name=rpc_name,
                is_unknown=True
            )

        error_id = re.sub(r"_\d+", "_X", error_message)

        if error_id not in exceptions[error_code]:
            raise getattr(
                import_module("pyrogram.errors"),
                exceptions[error_code]["_"]
            )(x="[{} {}]".format(error_code, error_message),
              rpc_name=rpc_name,
              is_unknown=True)

        x = re.search(r"_(\d+)", error_message)
        x = x.group(1) if x is not None else x

        raise getattr(
            import_module("pyrogram.errors"),
            exceptions[error_code][error_id]
        )(x=x,
          rpc_name=rpc_name,
          is_unknown=False)


class UnknownError(RPCError):
    CODE = 520
    """:obj:`int`: Error code"""
    NAME = "Unknown error"
