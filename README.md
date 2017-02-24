binparse
=========

simple library to simplify writing of binary parsers.

## Usage

The type is defined in a list of TYPENAME, TYPEDEF

where TYPEDEF is a list of 3-tuples

NAME, PARSEDEF, FORMATFUNCTION

where PARSEDEF is a list of

OFFSET, FORMAT

where FORMAT is a [struct](https://docs.python.org/2/library/struct.html) format string

```python
import datetime
import binparse
import hexdump

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
    ("ValidDump",            [0x0004, "4s"], None),
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
```
<pre>
Type: CRASHDUMP64
SystemTime: 2017-02-19 07:12:23.313370
DumpType: Kernel dump
BugCheckCode: 59
BugCheckParameteres: ['0xc0000005', '0x4204001c', '0xfffff88006599080L', '0x0']
Major, Minor version: 15 7601
Rax 0xfffff880065988c0L
Rbx 0xfffff80002fe1250L
Rcx 0x3b
Rdx 0xc0000005
Rsi 0xfffff80002e1d000L
Rsp 0xfffff880065987b8L
</pre>

## Installation

`% pip install binparse`

or

`% python setup.py install`

## Known issues


## Credits

Inspired by the volatilty vtypes format

## License

binparse is released under the ISC License. See the bundled LICENSE file for
details.
