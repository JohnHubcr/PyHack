import sys
import struct
import volatility.conf as conf
import volatility.registry as registry

memFile = "WindowsXPSP2.vmem"
sys.path.append("/Users/justin/Downloads/volatility")

registry.PluginImporter()
config = conf.ConfObject()

import volatility.commands as commands
import volatility.addrspace as addrspace

config.parse_options()
config.PROFILE = "WinXPSP2x86"
config.LOCATION = "file://%s" % memFile

registry.register_global_options(config, commands.Command)
registry.register_global_options(config, addrspace.BaseAddressSpace)

from volatility.plugins.registry.registryapi import RegistryApi
from volatility.plugins.registry.lsadump import HashDump

registry = RegistryApi(config)
registry.populate_offsets()

samOffset = None
sysOffset = None

for offset in registry.all_offsets:
    if registry.all_offsets[offset].endswith("\\SAM"):
        samOffset = offset
        print "[*] SAM: 0x%08x" % offset

    if registry.all_offsets[offset].endswith("\\system"):
        sysOffset = offset
        print "[*] System: 0x%08x" % offset

    if samOffset is not None and sysOffset is not None:
        config.sysOffset = sysOffset
        config.samOffset = samOffset

        hashDump = HashDump(config)

        for hash in hashDump.caculate():
            print hash

        break

    if samOffset is None and sysOffset is None:
        print "[*] Failed to find the system or SAM offset"
