import win32con
import win32api
import win32security

import wmi
import sys
import os

LOG_FILE = "processMonitoryLog.csv"


def getProcessPrivileges(pid):
    try:
        hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFOMATION, False, pid)
        htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)
        privs = win32security.GetTOkenInfomation(htok, win32security.TokenPrivileges)

        privList = []
        for privId, privFlag in privs:
            if privFlag == 3:
                privList.append(win32security.LookupPrivegeName(None, privId))
    except:
        privList.append("N/A")

    return "|".join(privList)


def logToFile(msg):
    fd = open(LOG_FILE, "ab")
    fd.write("%s\r\n" % msg)
    fd.close()

    return

if not os.path.isfile(LOG_FILE):
    logToFile("Time,User,Executable,CommandLine,PID,ParentPID,Privileges")

c = wmi.WMI()

processWatcher = c.Win32_Process.watch_for("creation")

while True:
    try:
        newProcess = processWatcher()

        procOwner = newProcess.GetOwner()
        procOwner = "%s\\%s" % (procOwner[0], procOwner[2])
        createDate = newProcess.CreationDate
        executable = newProcess.ExecutablePath
        cmdline = newProcess.CommandLine
        pid = newProcess.ProcessId
        parentPID = newProcess.ParentProcessId

        privileges = getProcessPrivileges(pid)

        processLogMsg = "%s,%s,%s,%s,%s,%s,%s" % (createDate, procOwner, executable, cmdline, pid, parentPID, privileges)

        print "%s\r\n" % processLogMsg

        logToFile(processLogMsg)
    except:
        pass
