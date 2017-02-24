#!/usr/bin/env python

import datetime
import binparse

def ignore(val):
    return "ignored"

def convertFILETIME(val):

    microseconds = val / 10
    seconds, microseconds = divmod(microseconds, 1000000)
    days, seconds = divmod(seconds, 86400)

    windows_zero_date = datetime.datetime(1601, 1, 1)
    myDateTime = windows_zero_date + datetime.timedelta(days, seconds, microseconds)
    return str(myDateTime)

def dump_type(val):
    if val == 1:
        return "Full dump"
    if val == 2:
        return "Kernel dump"
    if val == 5:
        return "Bitmap dump"
    return "Unknown dump type", val

def valid_dump(val):
    if val == "DU64":
        return "64-bit"
    elif val == "DUMP":
        return "32-bit"
    return "UNKNOWN"

_context64 = ["CONTEXT64", [
    ("Rax",  [ 0x0078, binparse.DWORD64 ], hex),
    ("Rcx",  [ 0x0080, binparse.DWORD64 ], hex),
    ("Rdx",  [ 0x0088, binparse.DWORD64 ], hex),
    ("Rbx",  [ 0x0090, binparse.DWORD64 ], hex),
    ("Rsp",  [ 0x0098, binparse.DWORD64 ], hex),
    ("Rbp",  [ 0x00a0, binparse.DWORD64 ], hex),
    ("Rsi",  [ 0x00a8, binparse.DWORD64 ], hex),
    ("Rdi",  [ 0x00b0, binparse.DWORD64 ], hex)]]

_fields64 = ["CRASHDUMP64", [
    ("Signature",            [0x0000, "4s"], None),
    ("ValidDump",            [0x0004, "4s"], valid_dump),
    ("MajorVersion",         [0x0008, "I"], None),
    ("MinorVersion",         [0x000c, "I"], None),
    ("DirectoryTableBase",   [0x0010, "L"], hex),
    ("PfnDataBase",          [0x0018, "L"], hex),
    ("PsLoadedModuleList",   [0x0020, "L"], hex),
    ("PsActiveProcessHead",  [0x0028, "L"], hex),
    ("MachineImageType",     [0x0030, "I"], None),
    ("NumberProcessors",     [0x0034, "I"], None),
    ("BugCheckCode",         [0x0038, "I"], None),
    ("BugCheckCodeParameter",[0x0040, "4L"], lambda x: map(hex, x)),
    ("KdDebuggerDataBlock",  [0x0080, "L"], hex),
    ("ContextRecord",        [0x0348, "3000s"], lambda x: binparse.BinParse(x, _context64)),
    ("DumpType",             [0x0f98, "B"], dump_type),
    ("RequiredDumpSpace",    [0x0fa0, "L"], None),
    ("SystemTime",           [0x0fa8, "L"], convertFILETIME),
    ("Comment",              [0x0fb0, "128s"], ignore),
    ("SystemUpTime",         [0x1030, "L"], None)]]


if __name__ == "__main__":
    import sys
    data = open(sys.argv[1]).read()

    cd = binparse.BinParse(data, _fields64)
    print "Type:", cd.name
    print "SystemTime:", cd.SystemTime
    print "DumpType:", cd.DumpType
    print "BugCheckCode:", cd.BugCheckCode
    print "BugCheckParameteres:", cd.BugCheckCodeParameter
    print "Major, Minor version:", cd.MajorVersion, cd.MinorVersion
    print "Rax", cd.ContextRecord.Rax
    print "Rbx", cd.ContextRecord.Rbx
    print "Rcx", cd.ContextRecord.Rcx
    print "Rdx", cd.ContextRecord.Rdx
    print "Rsi", cd.ContextRecord.Rsi
    print "Rsp", cd.ContextRecord.Rsp
