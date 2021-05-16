# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import logging


class Tr_testPlugin(octoprint.plugin.RestartNeedingPlugin):

    def __init__(self):
        # This allows us to store and display our logs with the rest of the OctoPrint logs
        self.logger = logging.getLogger("octoprint.plugins.TR_test")
        return

    ########################
    # Software Update Hook #
    ########################
    # Function to tell OctoPrint how to update the plugin
    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return dict(
            TR_test=dict(
                displayName="Tr_test Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="AlexVerrico",
                repo="Octoprint-TR_test",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/AlexVerrico/Octoprint-TR_test/archive/{target_version}.zip"
            )
        )

    ####################
    # Custom functions #
    ####################
    # Function to be called when any thermal runaway is triggered
    def runaway_triggered(self, heater_id, set_temp, current_temp):
        # Log that a thermal runaway has been triggered
        self.logger.critical("runaway triggered on heater {h}. Current temp is {c}, set temp is {s} "
                             .format(h=heater_id, c=current_temp, s=set_temp))
        return

    # Function to be called when an over temp thermal runaway is triggered
    def over_runaway_triggered(self, heater_id, set_temp, current_temp):
        # Log that an over temp thermal runaway has been triggered
        self.logger.critical("over_temp runaway triggered on heater {h}. Current temp is {c}, set temp is {s} "
                             .format(h=heater_id, c=current_temp, s=set_temp))
        return

    # Function to be called when an under temp thermal runaway is triggered
    def under_runaway_triggered(self, heater_id, set_temp, current_temp):
        # Log that an under temp thermal runaway has been triggered
        self.logger.critical("under_temp runaway triggered on heater {h}. Current temp is {c}, set temp is {s} "
                             .format(h=heater_id, c=current_temp, s=set_temp))
        return


__plugin_pythoncompat__ = ">=3,<4"  # only python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Tr_testPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.plugin.ThermalRunaway.runaway_triggered": __plugin_implementation__.runaway_triggered,
        "octoprint.plugin.ThermalRunaway.over_runaway_triggered": __plugin_implementation__.over_runaway_triggered,
        "octoprint.plugin.ThermalRunaway.under_runaway_triggered": __plugin_implementation__.under_runaway_triggered,
    }
