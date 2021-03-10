#!/usr/bin/python
"""

        .______  .________._______ .______  .______  
        : __   \ |    ___/:_.  ___\:      \ :      \ 
        |  \____||___    \|  : |/\ |   .   ||       |
        |   :  \ |       /|    /  \|   :   ||   |   |
        |   |___\|__:___/ |. _____/|___|   ||___|   |
        |___|       :      :/          |___|    |___|
                    : 

      roomscanner is a tool for scanning rooms owned by a person.
      It aims on finding all of one avatar, even private rooms.

      Version: 0.1

      Written by cyberwaste

"""

import sys
import argparse
import os
import requests
import time
import json

def clear():
   os.system("cls" if os.name == "nt" else "clear")


def infoheader(mode):
    clear()
    print("="*50)
    print("=>")
    print("=> RSCAN - 0.1")
    print("=> written by cyberwaste")
    print("=>")
    print("="*50)
    if ( mode == 0 ):
        print("-"*50)
        print("->>  Target: %s" %(options.cid))
        print("->>    From: %d to %d" %(options.begin,options.end))
        print("-"*50)
    elif ( mode == 1):
        parser.print_help()


def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

# needs a big cleanup :o
def checkroom(cid,number):
    room = 'http://client-dynamic.imvu.com/api/rooms/room_info.php?room_id=%s-%d' % (cid,number)
    response = requests.get(room)
    rcontent = response.content
    if rcontent.find(b'Room does not exist') != -1:
        if verb:
            print('[-] %s-%d') % (cid,number)
    elif rcontent.find(b'You have made too many requests recently') != -1:
        print('\n\r\n\r')
        print(' --- too many requests, lets have a break and get a coffee for a bit. waiting 3 minutes ---\n\r')
        time.sleep(180) #3 minutes
    else:
        dict = json.loads(response.content)
        roomname = (dict['name'].encode("utf-8"))
        ownercid = (dict['customers_id'])
        count = len(dict['participants'])
        if ( verb == True ):
            print('CID: %s-%d' % (cid,number))
            print("Name: %s" % (roomname))
            print ("Users: %d" % count)
            cids = extract_values(dict, 'customers_id')
            cids.remove(ownercid)
            names = extract_values(dict, 'avatar_name')
            for x in range(count):
                print ("--- %s - %s" %(names[x],cids[x]))
            print("-"*50)
        elif ( verb == False ):
            if ( peep == True ):
                if( count != 0 ):
                    print('CID: %s-%d' % (cid,number))
                    print("Name: %s" % (roomname))
                    print ("Users: %d" % count)
                    cids = extract_values(dict, 'customers_id')
                    cids.remove(ownercid)
                    names = extract_values(dict, 'avatar_name')
                    for x in range(count):
                        print ("--- %s - %s" %(names[x],cids[x]))
                    print("-"*50)
            elif ( peep == False ):
                print('CID: %s-%d' % (cid,number))
                print("Name: %s" % (roomname))
                if count != 0 :
                    print ("Users: %d" % count)
                    cids = extract_values(dict, 'customers_id')
                    cids.remove(ownercid)
                    names = extract_values(dict, 'avatar_name')
                    for x in range(count):
                        print ("--- %s - %s" %(names[x],cids[x]))
                print("-"*50)

# will be added in next version
def usernametocid(user):
   whatever
   return cid

if __name__=="__main__":
    parser = argparse.ArgumentParser("usage: %prog [options] arg1 arg2")
    parser.add_argument("-c", "--cid", dest="cid",default=00000000,help="specify the cid of a user")
    parser.add_argument("-b", "--begin", dest="begin",type=int,default=1,help="specify the room number to start with")
    parser.add_argument("-e", "--end", dest="end",type=int,default=100,help="specify the room number to end with")
    parser.add_argument("-v", "--verbose",dest="verbose_switch",default=False, action="store_true",help="shows all attempts")
    parser.add_argument("-p", "--people",dest="people_switch",default=False, action="store_true",help="shows only rooms with people inside")
    parser.add_argument("-d", "--delay", dest="delay",type=float,default=0.0,help="specify the delay between each room to scan")
    options = parser.parse_args()
    if len(sys.argv) < 2:
        infoheader(1)
        quit()
    else:
        cid = options.cid
        verb = options.verbose_switch
        peep = options.people_switch
        delay = options.delay
        infoheader(0)
        for x in range(options.begin,options.end):
            checkroom(cid,x)
            time.sleep(delay)
        print(" -- done --")
