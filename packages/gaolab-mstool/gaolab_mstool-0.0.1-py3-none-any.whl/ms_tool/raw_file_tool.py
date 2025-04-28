from zlib import adler32
import struct
import os


def calc_raw_adler32(filename):
    BLOCKSIZE = 10485760 - 152
    asum = 0
    with open(filename, 'rb') as f:
        header = f.read(152)
        header_list = list(header)
        header_list[-4:] = [0, 0, 0, 0]
        header = bytearray(header_list)
        asum = adler32(header, asum)
        data = f.read(BLOCKSIZE)
        asum = adler32(data, asum)
        if asum < 0:
            asum += 2 ** 32
    rev_asum = struct.unpack('<L', struct.pack('>L', asum))[0]
    return hex(rev_asum)[2:10].zfill(8).upper()


def read_adler32_checksum(filename):
    with open(filename, 'rb') as file_raw:
        file_header = file_raw.read(152)
        signature = file_header[:18]
        checksum = file_header[-4:]
    if signature == b'\x01\xA1\x46\x00\x69\x00\x6E\x00\x6E\x00\x69\x00\x67\x00\x61\x00\x6E\x00':
        return ''.join(format(n, '02X') for n in checksum)
    else:
        return 'Not Thermo Raw File'


class ThermoRAW:
    def __init__(self, filename):
        self.filename = filename
        self.filesize = os.path.getsize(filename)
        self.checksum = read_adler32_checksum(filename)
        self.calculated_checksum = calc_raw_adler32(filename)
        self.valid = True if self.checksum == self.calculated_checksum else False

    def __repr__(self):
        return f"Thermo_RAW(filename='{self.filename}', filesize={self.filesize}, valid={self.valid})"





if __name__ == '__main__':
    # test
    raw_file1 = ThermoRAW(r'D:\PATS\hela\hela8ul.raw')
    print(raw_file1)