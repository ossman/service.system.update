# -*- coding: utf-8 -*-

import time

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
        # (waitForAbort() doesn't account for time spent suspended,
        # so we have to poll)
        start = time.time()
        while time.time() - start < 24 * 60 * 60:
            if monitor.waitForAbort(10):
                # Abort was requested while waiting. We should exit
                break
