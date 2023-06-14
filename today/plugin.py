################################################################################
# @file        : plugin.py
# @brief       : Today Plugin for MkDocs
# @author      : Jacques Supcik <jacques.supcik@hefr.ch>
# @date        : 14. June 2023
# ------------------------------------------------------------------------------
# @copyright   : Copyright (c) 2022 HEIA-FR / ISC
#                Haute école d'ingénierie et d'architecture de Fribourg
#                Informatique et Systèmes de Communication
# @attention   : SPDX-License-Identifier: MIT OR Apache-2.0
# ------------------------------------------------------------------------------
# @details
# Today Plugin for MkDocs
################################################################################

import collections.abc
import logging
import os
from datetime import date
from typing import Type

import jinja2
from mkdocs.config.base import Config as BaseConfig
from mkdocs.config.config_options import Type as PluginType
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin

logger = logging.getLogger("mkdocs.plugins." + __name__)
logTag = "[today] - "


class TodayPluginConfig(BaseConfig):
    items = PluginType(list, default=[])


class TodayPlugin(BasePlugin[TodayPluginConfig]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.today = date.today()

    def _fix_item(self, key, config, jinja_env):
        c = config
        path = key.split(".")
        for p in path[:-1]:
            if p not in c:
                logger.warn(f"{logTag} Key '{key}' not found in config... skipping")
                return
            if not isinstance(c[p], collections.abc.Mapping):
                logger.warn(f"[today] - Invalid key '{key}' [{type(c[p])}]... skipping")
                return
            c = c[p]

        if path[-1] not in c:
            logger.warn(f"[today] - Key '{key}' not found in config... skipping")
            return

        orig = c[path[-1]]
        template = jinja_env.from_string(orig)

        try:
            c[path[-1]] = template.render(today=self.today)
        except Exception as e:
            logger.warn(f"[today] - Failed to render '{key}': {e}")
            c[path[-1]] = orig

    def on_config(self, config):
        env = jinja2.Environment()
        config["today"] = self.today
        for key in self.config.items:
            self._fix_item(key, config, env)

        return config
