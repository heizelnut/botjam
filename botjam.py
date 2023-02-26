#!/usr/local/bin/python3

import os
import re
import time
import json
import subprocess
import traceback
from multiprocessing import Process

class Botjam:
    TABLE = "botjam"
    EXCLUDE = { '127.0.0.1' }
    def __init__(self, config_filename, relax=2):
        self.rules = {}
        pf_proc = subprocess.Popen(["pfctl", "-t", self.TABLE, "-T", "show"],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        banned_ips = pf_proc.stdout.read()
        self.banned = self.EXCLUDE.union({ip.strip()
            for ip in banned_ips.decode('utf-8').split('\n')})
        self.config_filename = config_filename
        self.relax = relax
        self.reload_config()
        self.watch_files()

    def reload_config(self):
        with open(self.config_filename, "r") as rules_file:
            botjam_config = json.load(rules_file)
        if 'relax' in botjam_config:
            self.relax = int(botjam_config['relax'])
            del botjam_config['relax']
        for filename, rules in botjam_config.items():
            self.rules[filename] = []
            for rule in rules:
                try:
                    self.rules[filename].append(re.compile(rule))
                except Exception as e:
                    print("could not compile regex for rule: ", rule)

    def watch_files(self):
        for filename in self.rules.keys():
            # the main process will join all the child processess 
            #  when it's ready to exit
            Process(target=self.watcher_process, args=(filename,)).start()

    def watcher_process(self, filename):
        stamp = os.stat(filename).st_mtime
        while True:
            time.sleep(self.relax)
            newstamp = os.stat(filename).st_mtime
            if (stamp == newstamp): continue
            with open(filename, "r") as f:
                newlog = f.read()
            for rule in self.rules[filename]:
                new_ips = set(rule.findall(newlog)) - self.banned
                self.ban(new_ips)
                self.banned.update(new_ips)
 
    def ban(self, ips):
        for ip in ips:
            print("adding " + ip + " to blacklist")
            subprocess.run(["pfctl", "-t", self.TABLE, "-T", "add", ip])

if __name__ == "__main__":
    try:
        Botjam("/etc/botjam.json")
    except KeyboardInterrupt:
        print("shutting down...")
    except Exception as e:
        print("eggseption!!!")
        traceback.print_exc()
