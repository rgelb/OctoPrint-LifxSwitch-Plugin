# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import requests
import json
from collections import namedtuple

import flask

class LifxSwitchPlugin(octoprint.plugin.StartupPlugin,
                        octoprint.plugin.SettingsPlugin, 
                        octoprint.plugin.TemplatePlugin,
                        octoprint.plugin.EventHandlerPlugin,
                        octoprint.plugin.SimpleApiPlugin, 
                        octoprint.plugin.AssetPlugin):

    def on_after_startup(self):
        self._logger.info("Hello LifX World!")
        self._logger.info("Getting settings...")
        self._logger.info("access_token! (more: %s)" % self._settings.get(["access_token"]))
        self._logger.info("light_id! (more: %s)" % self._settings.get(["light_id"]))

    def get_settings_defaults(self):
        return dict(access_token="654321", light_id="0987")

    def get_template_vars(self):
        return dict(access_token=self._settings.get(["access_token"]), 
                    light_id=self._settings.get(["light_id"]))        

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    def handleTurnOffLight(self):

        headers = {
            "Authorization": "Bearer %s" % self._settings.get(["access_token"]),
        }

        response = requests.get('https://api.lifx.com/v1/lights/all', headers=headers)
        self._logger.info("Response receive")              

        x = json.loads(response.content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self._logger.info("light_id " + x[0].uuid)              


        payload = {
            "power": "off"
        }

        response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)

        self._logger.info("Turning off light")          

    def handleTurnOnLight(self):

        headers = {
            "Authorization": "Bearer %s" % self._settings.get(["access_token"]),
        }

        response = requests.get('https://api.lifx.com/v1/lights/all', headers=headers)
        self._logger.info("Response receive")              

        x = json.loads(response.content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        self._logger.info("light_id " + x[0].uuid)              


        payload = {
            "power": "on"
        }

        response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)

        self._logger.info("Turning on light")     

    def on_event(self, event, payload):

        if event == octoprint.events.Events.PRINT_STARTED:
            self.handleTurnOnLight()
        elif event == octoprint.events.Events.PRINT_FAILED:
            self.handleTurnOffLight()
        elif event == octoprint.events.Events.PRINT_DONE:
            self.handleTurnOffLight()
        elif event == octoprint.events.Events.PRINT_CANCELLED:
            self.handleTurnOffLight()

        self._logger.info("Event: " + event)   
    

    def get_api_commands(self):
        return dict(
            list_lights=["access_token"]
        )

    def on_api_command(self, command, data):
        self._logger.info("on_api_command Command: " + command)

        if command == "list_lights":

            self._logger.info("on_api_command Reading token: " + command)
            accessToken = data.get("access_token", "")

            headers = {
                "Authorization": "Bearer %s" % self._settings.get(["access_token"]),
            }

            response = requests.get('https://api.lifx.com/v1/lights/all', headers=headers)
            self._logger.info("Response receive")              

            x = json.loads(response.content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            self._logger.info("light_id " + x[0].uuid)    

            #self._logger.info("command1 called, parameter is {parameter}".format(**locals()))

            # return flask.jsonify(response.content)    
            return response.content


            


    def on_api_get(self, request):
        return flask.jsonify(foo="bar")    

    def get_assets(self):
        return dict(
            js=["js/lifxswitch.js"]
        )

    ##~~ Softwareupdate hook
    def get_update_information(self):
        return dict(
            rtmpstreamer=dict(
                displayName="Lifx Switch",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="rgelb",
                repo="OctoPrint-LifxSwitch-Plugin",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/rgelb/OctoPrint-LifxSwitch-Plugin/archive/{target}.zip"
            )
        )


    def __plugin_load__():
        global __plugin_implementation__
        __plugin_implementation__ = LifxSwitchPlugin()

        global __plugin_hooks__
        __plugin_hooks__ = {
            "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
        }

# plugin_identifier = "lifxswitch"
# plugin_package = "octoprint_lifxswitch"
# plugin_name = "Lifx Switch"
# plugin_version = "0.1.0"
# plugin_description = """Turns on the light when the print starts.  Turns it off when it ends."""
# plugin_author = "Robert Gelb"
# plugin_author_email = "rgelb@vbrad.com"

# __plugin_implementation__ = LifxSwitchPlugin()
