#
# Copyright (C) 2016 Shang Yuanchun <idealities@gmail.com>
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# drummer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with drummer. If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#

import struct
import StringIO

OPCODE_CONT  = 0x0
OPCODE_TEXT  = 0x1
OPCODE_BIN   = 0x2
# 0x3 - 0x7 reserved
OPCODE_CLOSE = 0x8
OPCODE_PING  = 0x9
OPCODE_PONG  = 0xA
# 0xB - 0xF reserved

def encode(**args):
    """
    Encode data into a valid websocket frame.

    Valid args:

    fin: 0 or 1, indicates whether or not this is final fragment
    opCode: type of payloadData
    payloadData: the real data to send
    needMask: true, or false, default true, whether not this frame need mask

    For more information, please refer to: https://tools.ietf.org/html/rfc6455

    """
    mask = (0 if 'needMask' in args and args['needMask'] == False else 1)
    buf = StringIO.StringIO()
    buf.write(struct.pack('B', (args['fin'] << 7) + args['opCode']))

    length = len(args['payloadData'])
    if length < 126:
        buf.write(struct.pack('B', (mask << 7) + length))
    elif (length < 0x10000):
        buf.write(struct.pack('B', (mask << 7) + 126))
        buf.write(struct.pack('>H', length))
    else:
        buf.write(struct.pack('B', (mask << 7) + 127))
        buf.write(struct.pack('>Q', length))

    if mask:
        import random
        maskList = [ random.randint(0, 255) for i in range(4) ]
        maskList = [ 0x37, 0xfa, 0x21, 0x3d ]
        for m in maskList:
            buf.write(struct.pack('B', m))
        i = 0
        while i < length:
            buf.write(struct.pack('B',
                struct.unpack('B', args['payloadData'][i])[0] ^ maskList[i % 4]))
            i += 1
    else:
        buf.write(args['payloadData'])

    buf.seek(0)
    content = buf.read()
    buf.close()

    return content

def decode(data):
    pass

