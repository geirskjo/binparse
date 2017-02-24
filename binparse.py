# ISC License
#
# Copyright (c) 2017, Geir Skjotskift <geir@underworld.no>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import struct

__all__ = ["BinParse", "BYTE", "WORD", "DWORD", "DWORD64"]

# Simplify working with Windows headers.
BYTE    = "B"
WORD    = "H"
DWORD   = "I"
DWORD64 = "L"

class BinParse(object):

    typeinfo = None
    data = None
    name = "NoneType"

    def __init__(self, data, typeinfo):
        self.typeinfo = typeinfo
        self.data = data
        self.parse()

    def parse(self):
        if not self.typeinfo or not self.data:
            raise ValueError("Empty parse info")

        self.name = self.typeinfo[0]

        for theType in self.typeinfo[1]:
            self._read_type(theType)

    def _read_type(self, theType):

        theStruct = struct.Struct(theType[1][1])
        part = self.data[theType[1][0]:theType[1][0]+theStruct.size]

        d = theStruct.unpack(part)
        attr_name = theType[0]

        attr_fn = theType[2]

        if attr_fn == None:
            attr_fn = lambda x: x # identity function

        if len(d) == 1:
            setattr(self, attr_name, attr_fn(d[0]))
        else:
            setattr(self, attr_name, attr_fn(d))
