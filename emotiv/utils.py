# -*- coding: utf-8 -*-
# vim:set et ts=4 sw=4:
#
## Copyright (C) 2012 Ozan Çağlayan <ocaglayan@gsu.edu.tr>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from scipy.io import savemat
import numpy as np

def check_packet_drops(seq_numbers):
    lost = []
    for seq in xrange(len(seq_numbers) - 1):
        cur = int(seq_numbers[seq])
        _next = int(seq_numbers[seq + 1])
        if ((cur + 1) % 128) != _next:
            lost.append((cur + 1) % 128)
    return lost

def get_level(raw_data, bits):
    """Returns signal level from raw_data frame."""
    level = 0
    for i in range(13, -1, -1):
        level <<= 1
        b, o = (bits[i] / 8) + 1, bits[i] % 8
        level |= (ord(raw_data[b]) >> o) & 1
    return level

def save_as_matlab(_buffer, channel_mask, filename, metadata=None):
    """Save as matlab data with optional metadata."""
    matlab_data = {"CTR": _buffer[:, 0]}

    if not filename.endswith(".mat"):
        filename = "%s.mat" % filename

    # Inject metadata
    if metadata:
        for key, value in metadata.items():
            matlab_data[key] = value
    for index, ch_name in enumerate(channel_mask):
        matlab_data[ch_name] = _buffer[:, index + 1].astype(np.float64)
        savemat(filename, matlab_data, oned_as='row')


