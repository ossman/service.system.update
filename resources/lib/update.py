# -*- coding: utf-8 -*-

import os 
import logging
import subprocess

import xbmcaddon
import xbmcgui

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))

def check_updates():
    origin = os.path.dirname(os.path.realpath(__file__))
    helper = os.path.join(origin, "..", "bin", "update")

    p = subprocess.Popen(helper, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    ready = False
    for line in p.stdout:
        (cmd, args) = line.split(":", 1)
        args = args.strip()

        if cmd == "ERROR":
            logger.error(args)
            xbmcgui.Dialog().notification("System Package Update Error",
                                          args,
                                          xbmcgui.NOTIFICATION_ERROR)
        elif cmd == "STATUS":
            if args == "CACHE":
                logger.info("Refreshing package cache...")
            elif args == "UPDATES":
                logger.info("Checking for updates...")
            elif args == "UPTODATE":
                logger.info("No updates found.")
            elif args == "DOWNLOADING":
                logger.info("Downloading packages...")
            elif args == "PREPARING":
                logger.info("Preparing updates for next boot...")
            elif args == "READY":
                ready = True
            else:
                logger.error("Unknown status: %s" % args)
        elif cmd == "UPDATE":
            logger.info("Found update: %s" % args)
        elif cmd == "BLOCKED":
            logger.info("Blocked update: %s (ignoring)" % args)
        elif cmd == "DOWNLOAD":
            logger.info("Downloading: %s" % args)
        else:
            logger.error("Unknown command: %s" % cmd)

    p.wait()

    return ready
