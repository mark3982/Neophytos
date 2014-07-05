'''
    This is designed to run tests to verify correct operation.
'''
import random
import subprocess
import os
import sys

from lib.client import Client2

def unitTestHashKmc():
    c = Client2(None, None, None, None)

    for lcnt in range(0, 1000):
        h1 = None
        h2 = None
        h3 = None

        # produce test data
        maxsz = 1024 * 1024 * 16
        sz = random.randint(0, maxsz)
        hsz = random.randint(0, maxsz)
        data = []
        for x in range(0, sz):
            data.append(random.randint(0, 255))
        data = bytes(data)

        # test pure python implementation
        _hentry = c.hentry
        c.hentry = None
        #h1 = c.HashKmc(data, hsz)
        # test native implementation (if exists)
        h2 = None
        if _hentry is not None:
            c.hentry = _hentry
            _data = bytes(list(data))
            print('getting H2')
            h2 = c.HashKmc(_data, hsz)
        cwd = os.getcwd()
        cwd = '%s/goserver/src'
        #p = subprocess.Popen(['go build main'], cwd = cwd, shell = True)
        #p.wait()
        cwd = os.getcwd()
        cwd = '%s/goserver/src/' % cwd
        print('--------------------------')
        p = subprocess.Popen(['%ssrc' % cwd, 'testunit-hash'], cwd = cwd, shell = False, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
        bin = []
        bin.append(hsz >> 16 & 0xff)
        bin.append(hsz >> 8 & 0xff)
        bin.append(hsz & 0xff)
        bin.append(sz >> 16 & 0xff)
        bin.append(sz >> 8 & 0xff)
        bin.append(sz & 0xff)
        bin = bytes(bin) + data
        print('getting H3')
        out = p.communicate(bin)
        h3 = out[0]
        if out[1] is not None and len(out[1]) > 0:
            print(out[1])
            exit()
        p.wait()
        if h1: print('h1', len(h1), h1[0:10])
        if h2: print('h2', len(h2), h2[0:10])
        if h3: print('h3', len(h3), h3[0:10])

        if h2 != h3:
            print('FAILED AT HASH TEST')
            return False
            
            return False
    return True

def main():
    unitTestHashKmc()

main()