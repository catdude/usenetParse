#!/usr/bin/python

import nntplib
import signal
import sys
import string, random
import StringIO, rfc822
import quopri

# The following assumes that "creds.py" exists in the current working 
# directory
from creds import SERVICE, SERVER, PORT, GROUP, USER, PASSWD

def sig_handler(signal, frame):
	sys.exit(0)

SERVICE= "giganews"
SERVER = "news.giganews.com"
PORT   = 119
GROUP  = "rec.pets.cats.community"
USER   = "catdude"
PASSWD = "cleo1cat"

OUTFILE= "rpcc.txt.%s.out" % (SERVICE, )

outFile = open(OUTFILE, "a+")

text = ''

# connect to server
server = nntplib.NNTP(SERVER, PORT, USER, PASSWD)

resp, count, first, last, name = server.group(GROUP)

currentMsg = first
endLoop = 0

while endLoop == 0:
    try:
        print "About to get msg %s (last is %s)" % (currentMsg, last )
        resp, id, message_id, text = server.article(str(currentMsg))
    except KeyboardInterrupt:
        sys.exit()
    except (nntplib.error_temp, nntplib.error_perm):
        (r, n, i) = server.next()
        currentMsg = n
        print "Missing msg; next one to try is %s" % (currentMsg,)
        continue
    else:
        #print "Read the message"
        pass # found a message!
    text = string.join(text, "\n")
    file = StringIO.StringIO(text)

    message = rfc822.Message(file)

    for k, v in message.items():
        outFile.write( "%s = %s\n" % (k, v))
    outFile.write("%s\n~~\n" % (message.fp.read(),))
    (r, n, i) = server.next()
    currentMsg = n
    if int(currentMsg) > int(last):
        sys.exit(0)


