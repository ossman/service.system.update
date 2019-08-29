# -*- coding: utf-8 -*-

from resources.lib import kodiutils
from resources.lib import kodilogging
from resources.lib.update import check_updates
import logging
import xbmc
import xbmcaddon
import xbmcgui


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))


def run():
    monitor = xbmc.Monitor()

    while not monitor.abortRequested():
        if check_updates():
            if xbmcgui.Dialog().yesno("System Updates Ready",
"""System updates have been downloaded and are ready to be installed.
Do you wish to reboot and install them now?"""):
                xbmc.restart()

        # Recheck every day
        if monitor.waitForAbort(24 * 60 * 60):
            # Abort was requested while waiting. We should exit
            break
