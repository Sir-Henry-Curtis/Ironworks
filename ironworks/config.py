# -*- coding: utf-8 -*-
import os
import sys

import ironworks.db
from flask import g
from ironworks import preferences, tools


def configRootPath():
    if sys.platform == "darwin":
            return os.path.expanduser("~/Library/Application Support/ironworks")
    elif sys.platform.startswith("win"):
            return os.path.join(os.environ['APPDATA'], "ironworks")
    else:
            return os.path.expanduser("~/.ironworks")


class Config():

    def __init__(self):
        # Check for ~/.ironworks
        if not os.path.isdir(configRootPath()):
                os.mkdir(configRootPath())

        tools.setDb()
        self.db = g.get('db')
        self.prefs = preferences.Prefs()

        self.configDb = ironworks.db.Db(os.path.join(configRootPath(), "config.db"))

        self.db.beginTransaction()

        self.db.checkTable("iw_plugins", [
            {"name": "plugin_k", "type": "INT PRIMARY KEY AUTO_INCREMENT"},
            {"name": "name", "type": "varchar(200)"},
            {"name": "description", "type": "text"},
            {"name": "label", "type": "varchar(255)"},
            {"name": "settings", "type": "text"},
            {"name": "poll", "type": "int"},
            {"name": "delay", "type": "int"}])

        self.db.checkTable("iw_plugin_settings", [
            {"name": "setting_k", "type": "INT PRIMARY KEY AUTO_INCREMENT"},
            {"name": "plugin_k", "type": "int"},
            {"name": "key", "type": "text"},
            {"name": "value", "type": "text"},
            {"name": "description", "type": "text"},
            {"name": "options", "type": "text"},
            {"name": "type", "type": "text"},
            {"name": "link", "type": "text"},
            {"name": "xbmc_servers", "type": "text"}])

        self.db.checkTable("iw_server_settings", [
            {"name": "name", "type": "text"},
            {"name": "value", "type": "text"}])

        self.db.checkTable("iw_misc_settings", [
            {"name": "key", "type": "int"},
            {"name": "value", "type": "text"},
            {"name": "type", "type": "text"},
            {"name": "options", "type": "text"}])

        self.db.checkTable("iw_search_settings", [
            {"name": "key", "type": "int"},
            {"name": "value", "type": "text"},
            {"name": "type", "type": "text"},
            {"name": "options", "type": "text"}])

        # Check ironworks server defaults
        self.checkDefaults("iw_server_settings", "timesRun", "0")
        self.checkDefaults("iw_server_settings", "daemon", "False")
        self.checkDefaults("iw_server_settings", "pidfile", "False")
        self.checkDefaults("iw_server_settings", "pidFileName", "")
        self.checkDefaults("iw_server_settings", "port", 7000)
        self.checkDefaults("iw_server_settings", "verbose", "True")
        self.checkDefaults("iw_server_settings", "development", "True")
        self.checkDefaults("iw_server_settings", "kiosk", "False")
        self.checkDefaults("iw_server_settings", "noupdate", "True")
        self.checkDefaults("iw_server_settings", "webroot", "")
        self.checkDefaults("iw_server_settings", "ironworks_username", "")
        self.checkDefaults("iw_server_settings", "ironworks_password", "")

        # Check ironworks misc defaults
        self.checkDefaults("iw_misc_settings", data={'key': 'show_currently_playing',
                                                     'value': '1',
                                                     'description': 'Show currently playing bar',
                                                     'type': 'select',
                                                     'options': "{'1': 'Yes', '2': 'Minimized', '0': 'No'}"})
        self.checkDefaults("iw_misc_settings", data={'key': 'fanart_backgrounds',
                                                     'value': '0',
                                                     'description': 'Show fanart backgrounds when watching media',
                                                     'type': 'bool'})

        # Check ironworks search defaults
        self.checkDefaults("iw_search_settings", data={'key': 'search',
                                                        'value': '0',
                                                        'description': 'Enable search feature',
                                                        'type': 'bool'})
        self.checkDefaults("iw_search_settings", data={'key': 'search_retention',
                                                        'value': '',
                                                        'description': 'Usenet retention'})
        self.checkDefaults("iw_search_settings", data={'key': 'search_ssl',
                                                        'value': '0',
                                                        'description': 'Prefer SSL',
                                                        'type': 'bool'})
        self.checkDefaults("iw_search_settings", data={'key': 'search_english',
                                                        'value': '0',
                                                        'description': 'Prefer English only',
                                                        'type': 'bool'})

        # Check ironworks plugin defaults
        self.checkDefaults("iw_plugins", data={'name': 'applications',
                                              'label': 'Applications',
                                              'description': 'Allows you to link to whatever applications you want (SabNZBd, SickBeard, etc.)',
                                              'static': True,
                                              'poll': 0,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'couchpotato',
                                              'label': 'CouchPotato Manager',
                                              'description': 'Manage CouchPotato from within IRONWORKS',
                                              'static': True,
                                              'poll': 0,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'diskspace',
                                              'label': 'Disk space',
                                              'description': 'Shows you available disk space on your various drives.',
                                              'static': False,
                                              'poll': 350,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'headphones',
                                              'label': 'Headphones Manager',
                                              'description': 'Manage Headphones from within IRONWORKS',
                                              'static': True,
                                              'poll': 0,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'library',
                                              'label': 'XBMC Library',
                                              'description': 'Allows you to browse your XBMC library and select items to play in XBMC.',
                                              'static': True,
                                              'poll': 0,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'nzbget',
                                              'label': 'NZBGet',
                                              'description': 'Shows you information about your NZBGet downloads.',
                                              'static': False,
                                              'poll': 10,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'recently_added',
                                              'label': 'Recently added episodes',
                                              'description': 'Shows you TV Episodes recently added to your library.',
                                              'static': False,
                                              'poll': 350,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'recently_added_movies',
                                              'label': 'Recently added movies',
                                              'description': 'Shows you Movies recently added to your library.',
                                              'static': False,
                                              'poll': 350,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'recently_added_albums',
                                              'label': 'Recently added albums',
                                              'description': 'Shows you Albums recently added to your library.',
                                              'static': False,
                                              'poll': 350,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'sabnzbd',
                                              'label': 'SABnzbd+',
                                              'description': 'Shows you information about your SABnzbd+ downloads.',
                                              'static': False,
                                              'poll': 10,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'script_launcher',
                                              'label': 'Script Launcher',
                                              'description': 'Runs scripts on same system IRONWORKS is located.',
                                              'static': False,
                                              'poll': 350,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'synopsis',
                                              'label': 'Synopsis',
                                              'description': 'Shows you a plot synopsis of what you are currently watching.',
                                              'static': True,
                                              'poll': 0,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'trakt',
                                              'label': 'trakt.tv Shouts',
                                              'description': 'Shows you what people are saying about what you are watching and allows you to add your own comments.',
                                              'static': True,
                                              'poll': 0,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'traktplus',
                                              'label': 'trakt.tv',
                                              'description': 'trakt.tv module',
                                              'static': False,
                                              'poll': 0,
                                              'delay': 10})

        self.checkDefaults("iw_plugins", data={'name': 'transmission',
                                              'label': 'Transmission',
                                              'description': 'Shows you information about your Transmission downloads.',
                                              'static': False,
                                              'poll': 10,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'utorrent',
                                              'label': 'uTorrent',
                                              'description': 'Shows information about uTorrent downloads',
                                              'static': False,
                                              'poll': 10,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'sickbeard',
                                              'label': 'Sickbeard Manager',
                                              'description': 'Manage Sickbeard from within IRONWORKS',
                                              'static': True,
                                              'poll': 0,
                                              'delay': 0})

        self.checkDefaults("iw_plugins", data={'name': 'weather',
                                              'label': 'Weather',
                                              'description': 'Weather details.',
                                              'static': False,
                                              'poll': 350,
                                              'delay': 0})

        res = self.db.select("iw_plugins", where={"name": "applications"}, what="plugin_k")
        print res

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'app_new_tab',
                                                        'value': '0',
                                                        'description': 'Open application in new tab.',
                                                        'type': 'bool'})

        res = self.db.select("iw_plugins", where={"name": "couchpotato"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'couchpotato_api',
                                                        'value': '',
                                                        'description': 'CouchPotato API Key'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'couchpotato_user',
                                                        'value': '',
                                                        'description': 'CouchPotato Username'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'couchpotato_password',
                                                        'value': '',
                                                        'description': 'CouchPotato Password'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'couchpotato_ip',
                                                        'value': '',
                                                        'description': 'CouchPotato Hostname'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'couchpotato_port',
                                                        'value': '',
                                                        'description': 'CouchPotato Port'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'couchpotato_webroot',
                                                        'value': '',
                                                        'description': 'CouchPotato Webroot'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'couchpotato_https',
                                                        'value': '0',
                                                        'description': 'Use HTTPS',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'couchpotato_compact',
                                                        'value': '0',
                                                        'description': 'Compact view',
                                                        'type': 'bool'})

        res = self.db.select("iw_plugins", where={"name": "diskspace"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'show_grouped_disks',
                                                        'value': '0',
                                                        'description': 'Show grouped disks outside of group.',
                                                        'type': 'bool'})

        res = self.db.select("iw_plugins", where={"name": "headphones"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'headphones_host',
                                                        'value': '',
                                                        'description': 'Headphones Hostname'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'headphones_port',
                                                        'value': '',
                                                        'description': 'Headphones Port'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'headphones_webroot',
                                                        'value': '',
                                                        'description': 'Headphones Webroot'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'headphones_user',
                                                        'value': '',
                                                        'description': 'Headphones Username'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'headphones_password',
                                                        'value': '',
                                                        'description': 'Headphones Password'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'headphones_api',
                                                        'value': '',
                                                        'description': 'Headphones API Key'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'headphones_https',
                                                        'value': '0',
                                                        'description': 'Use HTTPS',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'headphones_compact',
                                                        'value': '0',
                                                        'description': 'Compact view',
                                                        'type': 'bool'})

        res = self.db.select("iw_plugins", where={"name": "library"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'library_show_info',
                                                        'value': '0',
                                                        'description': 'Show media information by default',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'library_ignore_the',
                                                        'value': '1',
                                                        'description': 'Ignore "The" in titles',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'library_show_power_buttons',
                                                        'value': '1',
                                                        'description': 'Show Power Controls',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'library_show_music',
                                                        'value': '1',
                                                        'description': 'Show music',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'library_show_pvr',
                                                        'value': '0',
                                                        'description': 'Show PVR (XBMC 12+ only)',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'library_show_files',
                                                        'value': '1',
                                                        'description': 'Show files',
                                                        'type': 'bool'})

        res = self.db.select("iw_plugins", where={"name": "nzbget"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'nzbget_host',
                                                        'value': '',
                                                        'description': 'Hostname'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'nzbget_port',
                                                        'value': '',
                                                        'description': 'Port'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'nzbget_password',
                                                        'value': '',
                                                        'description': 'Password'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'nzbget_https',
                                                        'value': '0',
                                                        'description': 'Use HTTPS',
                                                        'type': 'bool'})

        res = self.db.select("iw_plugins", where={"name": "recently_added"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'num_recent_episodes',
                                                        'value': 1,
                                                        'description': 'Number of episodes to display'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'recently_added_compact',
                                                        'value': '0',
                                                        'description': 'Compact view',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'recently_added_watched_episodes',
                                                        'value': '1',
                                                        'description': 'Show Watched Episodes',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'recently_added_info',
                                                        'value': '0',
                                                        'description': 'View information when selecting episode',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'recently_added_server',
                                                        'value': '',
                                                        'description': 'XBMC server',
                                                        'type': 'select',
                                                        'options': None,
                                                        'xbmc_servers': True})

        res = self.db.select("iw_plugins", where={"name": "recently_added_movies"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'num_recent_movies',
                                                        'value': 3,
                                                        'description': 'Number of movies to display'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'recently_added_movies_compact',
                                                        'value': '0',
                                                        'description': 'Compact view',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'recently_added_watched_movies',
                                                        'value': '1',
                                                        'description': 'Show Watched Movies',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'recently_added_movies_info',
                                                        'value': '0',
                                                        'description': 'View information when selecting movie',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'recently_added_movies_server',
                                                        'value': '',
                                                        'description': 'XBMC server',
                                                        'type': 'select',
                                                        'options': None,
                                                        'xbmc_servers': True})

        res = self.db.select("iw_plugins", where={"name": "recently_added_albums"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'num_recent_albums',
                                                        'value': 3,
                                                        'description': 'Number of albums to display'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'recently_added_albums_compact',
                                                        'value': '0',
                                                        'description': 'Compact view',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'recently_added_albums_info',
                                                        'value': '0',
                                                        'description': 'View information when selecting album',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'recently_added_albums_server',
                                                        'value': '',
                                                        'description': 'XBMC server',
                                                        'type': 'select',
                                                        'options': None,
                                                        'xbmc_servers': True})

        res = self.db.select("iw_plugins", where={"name": "sabnzbd"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sabnzbd_host',
                                                        'value': '',
                                                        'description': 'Hostname'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sabnzbd_port',
                                                        'value': '',
                                                        'description': 'Port'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sabnzbd_webroot',
                                                        'value': '',
                                                        'description': 'Webroot'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sabnzbd_api',
                                                        'value': '',
                                                        'description': 'API Key'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sabnzbd_https',
                                                        'value': '0',
                                                        'description': 'Use HTTPS',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sabnzbd_show_empty',
                                                        'value': '1',
                                                        'description': 'Show module when queue is empty',
                                                        'type': 'bool'})

        res = self.db.select("iw_plugins", where={"name": "tract"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'trakt_api_key',
                                                        'value': '',
                                                        'description': 'Trakt API Key',
                                                        'link': 'http://trakt.tv/settings/api'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'trakt_username',
                                                        'value': '',
                                                        'description': 'Trakt Username'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'trakt_password',
                                                        'value': '',
                                                        'description': 'Trakt Password'})

        res = self.db.select("iw_plugins", where={"name": "tractplus"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'trakt_api_key',
                                                        'value': '',
                                                        'description': 'Trakt API Key',
                                                        'link': 'http://trakt.tv/settings/api'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'trakt_username',
                                                        'value': '',
                                                        'description': 'Trakt Username'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'trakt_password',
                                                        'value': '',
                                                        'description': 'Trakt Password'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'trakt_default_view',
                                                        'value': 'trending',
                                                        'description': 'Default view',
                                                        'type': 'select',
                                                        'options': [{'value': 'trending_shows', 'label': 'Trending (TV Shows)'},
                                                                    {'value': 'trending_movies', 'label': 'Trending (Movies)'},
                                                                    {'value': 'activity_friends', 'label': 'Activity (Friends)'},
                                                                    {'value': 'activity_community', 'label': 'Activity (Community)'},
                                                                    {'value': 'friends', 'label': 'Friends'},
                                                                    {'value': 'calendar', 'label': 'Calendar'},
                                                                    {'value': 'recommendations_shows', 'label': 'Recommendations (TV Shows)'},
                                                                    {'value': 'recommendations_movies', 'label': 'Recommendations (Movies)'},
                                                                    {'value': 'profile', 'label': 'My profile'}]})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'trakt_default_media',
                                                        'value': 'shows',
                                                        'description': 'Default media type',
                                                        'type': 'select',
                                                        'options': [{'value': 'shows', 'label': 'Shows'},
                                                                    {'value': 'movies', 'label': 'Movies'}]})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'trakt_trending_limit',
                                                        'value': '20',
                                                        'description': 'How many trending items to display',
                                                        'type': 'select',
                                                        'options': [{'value': '20', 'label': '20'},
                                                                    {'value': '40', 'label': '40'},
                                                                    {'value': '60', 'label': '60'}]})

        res = self.db.select("iw_plugins", where={"name": "transmission"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'transmission_ip',
                                                        'value': '',
                                                        'description': 'Transmission Hostname'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'transmission_port',
                                                        'value': '9091',
                                                        'description': 'Transmission Port'})
        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'transmission_user',
                                                        'value': '',
                                                        'description': 'Transmission Username'})
        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'transmission_password',
                                                        'value': '',
                                                        'description': 'Transmission Password'})
        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'transmission_show_empty',
                                                        'value': '1',
                                                        'description': 'Show module with no active torrents',
                                                        'type': 'bool'})

        res = self.db.select("iw_plugins", where={"name": "utorrent"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'utorrent_ip',
                                                        'value': '',
                                                        'description': 'uTorrent Hostname'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'utorrent_port',
                                                        'value': '8080',
                                                        'description': 'uTorrent Port'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'utorrent_user',
                                                        'value': '',
                                                        'description': 'uTorrent Username'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'utorrent_password',
                                                        'value': '',
                                                        'description': 'uTorrent Password'})

        res = self.db.select("iw_plugins", where={"name": "sickbeard"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sickbeard_api',
                                                        'value': '',
                                                        'description': 'Sickbeard API Key'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sickbeard_user',
                                                        'value': '',
                                                        'description': 'Sickbeard Username'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sickbeard_password',
                                                        'value': '',
                                                        'description': 'Sickbeard Password'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sickbeard_ip',
                                                        'value': '',
                                                        'description': 'Sickbeard Hostname'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sickbeard_port',
                                                        'value': '',
                                                        'description': 'Sickbeard Port'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sickbeard_webroot',
                                                        'value': '',
                                                        'description': 'Sickbeard Webroot'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sickbeard_https',
                                                        'value': '0',
                                                        'description': 'Use HTTPS',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sickbeard_compact',
                                                        'value': '0',
                                                        'description': 'Compact view',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'sickbeard_airdate',
                                                        'value': '0',
                                                        'description': 'Show air date',
                                                        'type': 'bool'})

        res = self.db.select("iw_plugins", where={"name": "weather"}, what="plugin_k")

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'weather_location',
                                                        'value': '',
                                                        'description': 'weather.com area ID',
                                                        'link': 'http://edg3.co.uk/snippets/weather-location-codes/'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'weather_use_celcius',
                                                        'value': '0',
                                                        'description': 'Temperature in C',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'weather_use_kilometers',
                                                        'value': '0',
                                                        'description': 'Wind Speed in Km',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'weather_time',
                                                        'value': '0',
                                                        'description': '24 hour time',
                                                        'type': 'bool'})

        self.checkDefaults("iw_plugin_settings", data={"plugin_k": "",
                                                        'key': 'weather_compact',
                                                        'value': '0',
                                                        'description': 'Compact view',
                                                        'type': 'bool'})

    def getDb(self):
        return self.configDb

    def checkDefaults(self, table, data):
        cursor = self.db.select(table, where=data)
        if not cursor:
            self.db.beginTransaction()
            self.db.insert(table, data)
            self.db.commitTransaction()
