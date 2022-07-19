"""
linux-like hex-outputed hexdump
e.g.
pi@raspberrypi:~/Desktop/rpi-gpio-python $ hd a.out -n 100
00000000  7f 45 4c 46 01 01 01 00  00 00 00 00 00 00 00 00  |.ELF............|
00000010  02 00 28 00 01 00 00 00  50 0e 01 00 34 00 00 00  |..(.....P...4...|
00000020  98 39 00 00 00 04 00 05  34 00 20 00 09 00 28 00  |.9......4. ...(.|
00000030  1f 00 1e 00 01 00 00 70  08 1c 00 00 08 1c 01 00  |.......p........|
00000040  08 1c 01 00 30 00 00 00  30 00 00 00 04 00 00 00  |....0...0.......|
00000050  04 00 00 00 06 00 00 00  34 00 00 00 34 00 01 00  |........4...4...|
00000060  34 00 01 00                                       |4...|
00000064
pi@raspberrypi:~/Desktop/rpi-gpio-python $
"""

def hexdump(data = b'',caption=''):
    __hd_format = '{0:08X}  {1:<24} {2:<24} |{3}|'
    __hd_format_wo_address = '{1:<24} {2:<24} |{3}|'
    __print_version = lambda b: chr(b) if chr(b).isprintable() else '.'
    try:
        output = caption + '\n'
        for i in range(0,len(data),16):
            output_line = __hd_format.format(
                i,
                " ".join( [ "{:02X}".format(x) for x in data[i:i+8] ] ),
                " ".join( [ "{:02X}".format(x) for x in data[i+8:i+16] ] ),
                ''.join( [ __print_version(x) for x in data[i:i+16] ] )
                )
            output += output_line
            output += '\n'
            pass
    except Exception as e:
        print(__file__,type(e),type(e).__name__,e)
    output += '{:08X}\n'.format(len(data))
    return output

#alias
hd = hexdump

def m_testing():
    #test fn
    import time

    def timespent(func):
        def measure_me(*args,**kwargs):
            s = time.time()
            retval = func(*args,**kwargs)
            report = '{0} time spent: {1:1.3f}'.format(func.__name__,time.time() - s)
            print(report)
            return retval
        return measure_me
    
    @timespent
    def getbytearray():
        return bytes(100 * 4 * list(range(0x100))) + b"??"
    
    @timespent
    def test_of_10kB():
        return hexdump(getbytearray())

    mesg = bytes(list(range(0x100))) + b'nieco naviac'
    o = hexdump(mesg)
    print(o)
    o = test_of_10kB()
    print(len(o))
    #print(o)
    print(hd(b'mato', "Caption")) 
    print(hd('mato')) #will produce type error
    print(hd(b'\x02QS\x1cc500\x1cmEUR\x03x','ecr'))
    print(hd(b"\x02QP\x1cI101\x1cV4.10U\x03",'ecr-device state'))   

if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        with open(sys.argv[1],'rb') as f:            
            print(hexdump(f.read(),f.name))
    else:
        print('usage: hexdump.py <filename>')
        print('running tests')
        m_testing()
