#!/usr/bin/env python

"""\
ELOADMENU
"""

from __future__ import print_function

import logging, sys, time

PORT = '/dev/tty.usbserial-1444D'
BAUDRATE = 115200
PIN = None # SIM card PIN (if any)

from gsmmodem.modem import GsmModem

def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))
    # print('Replying to SMS...')
    # sms.reply(u'SMS received: "{0}{1}"'.format(sms.text[:20], '...' if len(sms.text) > 20 else ''))
    # print('SMS sent.\n')
    return


def main():
    phone = "0123456789"
    amount = 10
    print('Initializing modem...')
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    else:
        PORT = '/dev/tty.usbserial-1444D'
    print("ARGV: {0}".format(PORT))

    # logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
    modem.smsTextMode = True
    modem.connect(PIN)
    modem.waitForNetworkCoverage(10)

    reply = modem.write('AT+CPAS')
    STINresponse = [];
    while(len(STINresponse) < 1):
        STINresponse = modem.write('AT')
        print('Reply for STIN: {0}'.format(STINresponse))


    print ('Reply for CPAS: {0}'.format(reply))
    if format(reply[1]) == 'OK':
        print("OK")
    #
    # print ('Reply for STIN=?: {0}'.format(modem.write('AT+STIN=?')))
    # print ('Reply for STIN=?: {0}'.format(modem.write('AT+CFUN')))

    print ('Reply for STGR=98: {0}'.format(modem.write('AT+STGR=98',parseError=False)))
    print ('Reply for STGR=98: {0}'.format(modem.write('AT+STGR=98',parseError=False)))
    print ('Reply for CFUN=0: {0}'.format(modem.write('AT+CFUN=0')))
    print ('Reply for CFUN=1: {0}'.format(modem.write('AT+CFUN=1')))
    print ('Reply for STGI=?: {0}'.format(modem.write('AT+STGI=?')))
    print ('Reply for STGI=0: {0}'.format(modem.write('AT+STGI=0')))
    print ('Reply for STGR=0,1,129: {0}'.format(modem.write('AT+STGR=0,1,129',waitForResponse=True,timeout=10,parseError=False)))
    time.sleep(2)
    # STINresponse = [];
    # while(len(STINresponse) < 1):
    #     STINresponse = modem.write('AT+STIN=?')
    #     print('Reply for STIN: {0}'.format(STINresponse))

    print ('Reply for STGI=6: {0}'.format(modem.write('AT+STGI=6',waitForResponse=True,parseError=False)))
    print ('Reply for STGR=6,1,1: {0}'.format(modem.write('AT+STGR=6,1,1',waitForResponse=True,parseError=False)))
    time.sleep(2)
    # STINresponse = modem.write('AT+STIN=?')
    # print('Reply for STIN: {0}'.format(STINresponse))

    print ('Reply for STGI=3: {0}'.format(modem.write('AT+STGI=3',waitForResponse=True,parseError=False)))
    print ('Reply for STGR=3,1 - input phone number: {0}'.format(modem.write('AT+STGR=3,1\n{}\x1a'.format(phone),waitForResponse=False,parseError=False)))
    time.sleep(2)
    # STINresponse = [];
    # while(len(STINresponse) < 1):
    #     STINresponse = modem.write('AT',parseError=False)
    #     print('Reply for STIN: {0}'.format(STINresponse))
    # print ('Reply for input number: {0}'.format(modem.write('01248474242'+'\x1a',waitForResponse=True,timeout=30,parseError=False)))
    print ('Reply for STGI=6: {0}'.format(modem.write('AT+STGI=6',waitForResponse=True,parseError=False)))
    print ('Reply for STGR=6,1,8: {0}'.format(modem.write('AT+STGR=6,1,8',waitForResponse=True,parseError=False)))
    time.sleep(2)

    print ('Reply for STGI=3: {0}'.format(modem.write('AT+STGI=3',waitForResponse=True,parseError=False)))
    print ('Reply for STGR=3,1 - input amount: {0}'.format(modem.write('AT+STGR=3,1\n{}\x1a'.format(amount),waitForResponse=False,parseError=False)))
    time.sleep(2)

    print ('Reply for STGI=1: {0}'.format(modem.write('AT+STGI=1',waitForResponse=True,parseError=False)))
    print ('Reply for STGR=1,1,1: {0}'.format(modem.write('AT+STGR=1,1,1',waitForResponse=True,parseError=False)))
    time.sleep(2)
    # STINresponse = [];
    # while(len(STINresponse) < 1):
    #     STINresponse = modem.write('AT',parseError=False)
    #     print('Reply for STIN: {0}'.format(STINresponse))
    # print ('Reply for CNMI?: {0}'.format(modem.write('AT+CNMI?',waitForResponse=True,parseError=False)))
    time.sleep(2)
    print ('Reply for STGI=1: {0}'.format(modem.write('AT+STGI=1',waitForResponse=True,parseError=False)))



    STINresponse = [];
    while(len(STINresponse) < 1):
        STINresponse = modem.write('AT')
        print('Reply for STIN: {0}'.format(STINresponse))






        time.sleep(10)
    modem.close()

if __name__ == '__main__':
    main()
