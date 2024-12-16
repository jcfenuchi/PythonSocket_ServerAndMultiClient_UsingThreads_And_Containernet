from flask import Flask, redirect, url_for, request
from os import getenv
import subprocess
import toml

class APP():
    def __init__(self):
        self.environment = {
            "MINION_HOSTNAME":  getenv('USERNAME'),
            "MINION_IP": subprocess.check_output("hostname -I | awk '{print $1}'", shell=True, text=True)[:-1],
            "SWITCH_IP": None,
            "SWITCH_HOSTNAME": None,
            "SWITCH_RUNNINGCONFIG": None,
            "SWITCH_LAST_CONFIG_UPDATE": None,
            "SWITCH_KPI": None,
            "CORE_IP": None,
            "CORE_PORT": None,
        }
        
    def start_app(self):
        self.app = Flask("__APP__")

        @self.app.errorhandler(404)
        def page_not_found(_):
            return redirect(url_for('metrics'))
        
        @self.app.route("/metrics", methods=["GET"])
        def metrics():
            if request.args.get("toml", default='False') in ['True','true']:
                return toml.dumps(self.environment)
            return self.environment
        return self.app

    def run(self, *args, **kwargs):
        self.start_app().run(*args, **kwargs)
    
    def __del__(self):
        ...

        