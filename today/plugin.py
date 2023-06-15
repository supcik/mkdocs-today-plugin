################################################################################
# @brief       : Today Plugin for MkDocs
# @author      : Jacques Supcik <jacques.supcik@hefr.ch>
# @date        : 14. June 2023
# ------------------------------------------------------------------------------
# @copyright   : Copyright (c) 2022 HEIA-FR / ISC
#                Haute école d'ingénierie et d'architecture de Fribourg
#                Informatique et Systèmes de Communication
# @attention   : SPDX-License-Identifier: MIT OR Apache-2.0
################################################################################

"""Today Plugin for MkDocs"""

import collections.abc
import logging
from datetime import date

import jinja2
from mkdocs.config.base import Config as BaseConfig
from mkdocs.config.config_options import Type as PluginType
from mkdocs.plugins import BasePlugin

logger = logging.getLogger("mkdocs.plugins." + __name__)
TAG = "[today] -"


class TodayPluginConfig(BaseConfig):
    """Configuration options for the Today plugin"""

    items = PluginType(list, default=[])


# pylint: disable-next=too-few-public-methods
class TodayPlugin(BasePlugin[TodayPluginConfig]):
    """Today Plugin for MkDocs"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.today = date.today()

    def _fix_item(self, key, config, jinja_env):
        subconfig = config
        path = key.split(".")
        for stem in path[:-1]:
            if stem not in subconfig:
                logger.warning("%s Key '%s' not found in config... skipping", TAG, key)
                return
            if not isinstance(subconfig[stem], collections.abc.Mapping):
                logger.warning(
                    "%s - Invalid key '{%s}' [%s]... skipping",
                    TAG,
                    key,
                    type(subconfig[stem]),
                )
                return
            subconfig = subconfig[stem]

        if path[-1] not in subconfig:
            logger.warning("%s - Key '{%s}' not found in config... skipping", TAG, key)
            return

        orig = subconfig[path[-1]]
        template = jinja_env.from_string(orig)

        try:
            subconfig[path[-1]] = template.render(today=self.today)
        except jinja2.TemplateError as e:  # pylint: disable=invalid-name
            logger.warning("%s - Failed to render '%s': %s", TAG, key, e)
            subconfig[path[-1]] = orig

    def on_config(self, config):
        """define the today configuration and render the templated options"""
        env = jinja2.Environment()
        config["today"] = self.today
        for key in self.config.items:
            self._fix_item(key, config, env)

        return config
