import re
import zlib
import cv2

from scapy.all import *

picturesDirectory = "/home/neo/picCarver/pictures"
facesDirectory = "/home/neo/picCarver/faces"
pcapFile = "bhp.pcap"

def getHttpHeaders(httpPayload):
    try:
        headersRaw = httpPayload[:httpPayload.index("\r\n\r\n") + 2]
        headers = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", headersRaw))
    except:
        return None

    if "Content-Type" not in headers:
        return None

    return headers

def extractImage(headers, httpPayload):
    image = None
    imageType = None

    try:
        if "image" in headers['Content-Type']:
            imageType = headers['Content-Type'].split('/')[1]
            image = httpPayload[httpPayload.index("\r\n\r\n") + 4:]

        try:
            if "Content-Encoding" in headers.keys():
                if headers["Content-Encoding"] == "gzip":
                    image = zlib.decompress(image, 16 + zlib.MAX_WBITS)
                elif headers['Content-Encoding'] == 'deflate':
                    image = zlib.decompress(image)
        except:
            pass
    except:
        return None, None

def faceDetect(path, fileName):
    img = cv2.read(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR, SCALE_IMAGE, (20, 20))

    if len(rects) == 0:
        return False

    rects[:, 2:] += rects[:, :2]

    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)

    cv2.imwrite("%s/%s-%s" % (facesDirectory, pcapFile, fileName), img)

    return True

def httpAssembler(pcapFile):
    
    carvedImages = 0
    facesDetected = 0

    a = rdpcap(pcapFile)

    sessions = a.sessions()

    for session in sessions:
        httpPayload = ""

        for packet in sessions[session]:
            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    httpPayload += str(packet[TCP].payload)
            except:
                pass

        headers = getHttpHeaders(httpPayload)

        if headers is None:
            continue

        image, imageType = extractImage(headers, httpPayload)

        if image is not None and imageType is not None:
            fileName = "%s-picCarver-%d.%s" % (pcapFile, carvedImages, imageType)
            
            fd = open("%s/%s" % (picturesDirectory, fileName), "wb")
            fd.write(image)
            fd.close()

            carvedImages += 1

            try:
                result = faceDetect("%s/%s" % (picturesDirectory, fileName), fileName)

                if result is True:
                    facesDetected += 1
            except:
                pass

    return carvedImages, facesDetected

carvedImages, facesDetected = httpAssembler(pcapFile)

print "Extracted: %d images" % carvedImages
print "Detected: %d faces" % facesDetected
