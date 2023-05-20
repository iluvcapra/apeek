"""
apeek is a package for creating audio waveform previews.
"""

__version__ = "0.0.1"

import numpy as np
from pydub import AudioSegment

from math import sqrt
from enum import Enum
from dataclasses import dataclass
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


@dataclass
class WaveformData:
    value_pairs: np.array
    max_index: int
    max_sample: int
    max_value: float
    full_code_value: float


def create_waveform_data(audio: AudioSegment, 
                        length: int, 
                        settings: WaveformSettings = WaveformSettings.default()) -> WaveformData:
    """
    Create a numpy array for use in drawing a waveform overview.
 
    """
    samples = audio.get_array_of_samples()
    bit_depth = audio.sample_width
    window_length = int(len(samples) / length)

    retval = np.zeros((length, 2))
    
    max_index = 0
    max_value = 0.0
    max_sample = 0
    for i in range(length):
        window = samples[i * window_length : (i + 1) * window_length]
        retval[i] = (np.max(window),np.min(window))
        magnitude = np.max(np.abs(window))
        if magnitude > max_value:
            max_index = i
            max_sample = np.argmax(np.abs(window)) + i * window_length
            max_value = magnitude
    
    full_code_value = (2 ** (bit_depth * 8 - 1)) 
    retval = retval / full_code_value

    if settings['normalized']:
        sample_max = np.max(retval)
        sample_min = np.min(retval)
        scale_max = max(abs(sample_max), abs(sample_min))
        retval = retval / scale_max

    if settings['scaling'] == ScalingFactor.ROOT:
        signs = np.sign(retval)
        absval = np.sqrt(np.fabs(retval))
        retval = retval * signs

    return WaveformData(retval, max_index, max_sample, max_value, full_code_value)


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
    retval_lines = list()
    for j in range(height,0,-1):
        this_line = ""
        for i in range(len(accum_array)):
            this_line = this_line + accum_array[i][j]

        retval_lines += [this_line]

    return "\n".join(retval_lines)


