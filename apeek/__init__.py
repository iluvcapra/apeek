"""
apeek is a package for creating audio waveform previews.
"""

__version__ = "0.1.0"

import numpy as np

from .waveform import WaveformData, WaveformDataSettings, ScalingFactor


def rectified_unicode_waveform(data: np.array, height: int = 10) -> str:
    
    BLOCK_CHARS = list(" ▁▂▃▄▅▆▇")
    FULL_BLOCK = "█"
    levels = height * (8)

    accum_array = []

    for i, sample_pair in enumerate(data):
        rectified_value = max(abs(sample_pair[0]), abs(sample_pair[1]))
        leveled_value = int(rectified_value * levels)
        
        full, partial = divmod(leveled_value, 8)
        blank = height - full

        accum_array += [list( FULL_BLOCK * full + BLOCK_CHARS[partial] + " " * blank)]
    
    # transpose
    retval_lines = list()
    for j in reversed(range(height)):
        this_line = ""
        for i in range(len(accum_array)):
            this_line = this_line + accum_array[i][j]

        retval_lines += [this_line]

    return "\n".join(retval_lines)


