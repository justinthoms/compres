#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) PublicLeech Author(s)
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from bot.get_cfg import get_config


class Command:
    START = get_config(
        "COMMAND_START",
        "start"
    )
    COMPRESS = get_config(
        "COMMAND_COMPRESS",
        "compress"
    )
   # CANCEL = get_config(
    #    "COMMAND_CANCEL",
     #   "cancel"
    #)
    ABOUT = get_config(
        "COMMAND_ABOUT",
        "about"
    )
    WARN = get_config(
        "COMMAND_WARN",
        "warn"
    )
    BAN = get_config(
        "COMMAND_BAN",
        "ban"
    )
    UNBAN = get_config(
        "COMMAND_UNBAN",
        "unban"
    )
    STATUS = get_config(
        "COMMAND_STATUS",
        "status"
    )
    RESET = get_config(
        "COMMAND_RESET",
        "reset"
    )
    EXEC = get_config(
        "COMMAND_EXEC",
        "exec"
    )
    HELP = get_config(
        "COMMAND_HELP",
        "help"
    )
    DONATE = get_config(
        "COMMAND_DONATE",
        "donate"
    )
    UPLOAD_LOG_FILE = get_config(
        "COMMAND_UPLOAD_LOG_FILE",
        "log"
    )
