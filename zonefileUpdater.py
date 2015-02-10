#!/usr/bin/env python
# author: dfosborne2
# Free for any kind of use. No warranty of any sory implied or to be assumed.
# For use with BIND DNS. Most DNS libraries make the assumption
# that you will not make more than 100 changes to a zone
# on any given day. These methods have shortcomings in the datestamp
# serial method:
# 2015021099  (yyyymmddrn - 2015 Feb 10 revion 99)
# This script will bump the serial number to the next day of the given month, 
# should revision 101 be needed for the day.
# Prerequites: dnspython

import dns.zone
from time import strftime
from calendar import monthrange
import sys
serial_base = strftime('%Y%m%d')
zfile = sys.argv[1]


def updateSerial(zfile):

    """Supply /path/to/zonfile as your zfile object"""

    zname = zfile.split('/')[1]
    zone = dns.zone.from_file(zfile,zname)

    for (name, ttl, rdata) in zone.iterate_rdatas('SOA'):
        old_serial = rdata.serial
        serial = str(old_serial)[:8]
        bump = str(rdata.serial)[8:10]
        if serial < serial_base:
            new_serial = serial_base + '00'
        elif int(bump) == 99:
            if  monthrange(int(yr), int(month.lstrip('0')))[1] == int(day):
                if int(month) == 12:
                    new_serial = str(int(int(yr)) + 1) + '01' + '01' + '00'
            else:
                if len(str(int(int(month) + 1 ))) == 1:
                    month = '0' + str(int(int(month) + 1 ))

                    new_serial = yr + month  + '01' + '00'
                else:
                    new_serial = yr + month + str(int(int(day) + 1 )) + '00'

        elif int(serial + '00') >= int(serial_base + '00') :
            new_serial = rdata.serial + 1
        else:
            new_serial = rdata.serial + 1

    #return str(old_serial), str(new_serial)
    return str(new_serial)


if __name__ == "__main__":

    print updateSerial(zfile) 
