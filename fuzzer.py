from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List, ArrayList

import random

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        callbacks.registerIntruderPayloadGeneratorFactory(self)

    def getGeneratorName(self):
        return "Payload Generator"

    def createNewInstance(self, attack):
        return Fuzzer(self, attack)

def Fuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self._extender = extender
        self._helpers = extender._helpers
        self._attack = attack
        self.maxPayloads = 10
        self.numIterations = 0

        return

    def hasMorePayloads(self):
        if self.numIterations == self.maxPayloads:
            return False
        else:
            return True

    def getNextPayload(self, currentPayload):
        payload = "".join(chr(x) for x in currentPayload)
        payload = self.mutatePayload(payload)

        self.numIterations += 1

        return payload

    def reset(self):
        self.numIterations = 0
        return

    def mutatePayload(self, originalPayload):
        picker = random.randint(1, 3)

        offset = random.randint(0, len(originalPayload) - 1)
        payload = originalPayload[:offset]
        
        if picker == 1:
            payload += "'"
        
        if picker == 2:
            payload += "<script>alert('Hello, world!');</script>"
        
        if picker == 3:
            chunkLength = random.randint(len(payload[offset:]), len(payload) - 1)
            repeater = random.randint(1, 10)
            
            for i in range(repeater):
                payload += originalPayload[offset:offset + chunkLength]
                
        payload += originalPayload[offset:]
        return payload
