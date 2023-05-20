"""
apeek is a package for creating audio waveform previews.
"""

__version__ = "0.1.0"

from typing import List

import numpy as np

from .waveform import WaveformData, WaveformDataSettings, ScalingFactor

def rectified_unicode_waveform_charmatrix(data: np.array, height: int, bg: str = "·") -> List[List[str]]:
    """ 
    Create a grid of strs for a rectified waveform bargraph
    """
    BLOCK_CHARS = list(f"{bg}▁▂▃▄▅▆▇")
    FULL_BLOCK = "█"
    levels = height * (len(BLOCK_CHARS))

    retval = []

    for i, sample_pair in enumerate(data):
        rectified_value = max(abs(sample_pair[0]), abs(sample_pair[1]))
        leveled_value = int(rectified_value * levels)
        
        full, partial = divmod(leveled_value, len(BLOCK_CHARS))
        blank = height - full

        retval += [list( FULL_BLOCK * full + BLOCK_CHARS[partial] + BLOCK_CHARS[0] * blank)]

    return retval


def unicode_waveform(data: np.array, height: int) -> str:
    
    char_matrix = rectified_unicode_waveform_charmatrix(data, height)
    
    # transpose
    retval_lines = list()
    for j in reversed(range(height)):
        this_line = ""
        for i in range(len(char_matrix)):
            this_line = this_line + char_matrix[i][j]

        retval_lines += [this_line]

    return "\n".join(retval_lines)


