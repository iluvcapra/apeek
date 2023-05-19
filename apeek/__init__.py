"""
apeek
"""

__version__ = "0.0.1"

import numpy as np
from pydub import AudioSegment

from math import sqrt
from enum import Enum
from typing import Tuple, TypedDict


class ScalingFactor(Enum):
    LINEAR = 0
    ROOT = 1


class WaveformSettings(TypedDict):
    scaling: ScalingFactor
    normalized: bool

    @classmethod
    def default(cls):
        return cls(scaling=ScalingFactor.ROOT, normalized=True)


def create_waveform_data(audio: AudioSegment, 
                        length: int, 
                        settings: WaveformSettings = WaveformSettings.default()) -> np.array:
    """
    Create a numpy array 
    """
    samples = audio.get_array_of_samples()
    bit_depth = audio.sample_width
    window_length = int(len(samples) / length)

    retval = np.zeros((length, 2))

    for i in range(length):
        window = samples[i * window_length : (i + 1) * window_length]
        retval[i] = (np.max(window),np.min(window))

    retval = retval / (2 ** (bit_depth * 8))

    if settings['normalized']:
        sample_max = np.max(retval)
        sample_min = np.min(retval)
        scale_max = max(abs(sample_max), abs(sample_min))
        retval = retval / scale_max

    if settings['scaling'] == ScalingFactor.ROOT:
        signs = np.sign(retval)
        absval = np.sqrt(np.fabs(retval))
        retval = retval * signs

    return retval


def rectified_ascii_waveform(data: np.array, height: int = 10) -> str:
    
    BLOCK_CHARS = list("▁▂▃▄▅▆▇█")
    levels = height * len(BLOCK_CHARS)

    accum_array = []

    for i, sample_pair in enumerate(data):
        rectified_value = max(abs(sample_pair[0]), abs(sample_pair[1]))
        leveled_value = int(rectified_value * levels)
        
        full, partial = divmod(leveled_value, len(BLOCK_CHARS))
        blank = height - full
        if partial == 0:
            blank += 1

        accum_array += [list(str(BLOCK_CHARS[-1]) * full + BLOCK_CHARS[partial] + " " * blank )]
    
    # transpose
    retval = ""
    for j in range(height,0,-1):
        this_line = ""
        for i in range(len(accum_array)):
            this_line = this_line + accum_array[i][j]

        retval += this_line + "\n"

    return retval 


