import numpy as np
from pydub import AudioSegment

from math import sqrt
from enum import Enum
from dataclasses import dataclass
from typing import Tuple, TypedDict, Optional


class ScalingFactor(Enum):
    LINEAR = 0
    ROOT = 1


class WaveformDataSettings(TypedDict):
    scaling: 'ScalingFactor'
    normalized: bool

    @classmethod
    def default(cls):
        return cls(scaling=ScalingFactor.ROOT, normalized=True)


@dataclass
class WaveformData:
    """
    Data collected from an AudioSegment to be used for drawing a waveform.
    """
    value_pairs: np.array
    max_index: int
    max_sample: int
    max_value: float
    full_code_value: float
    samples_per_bin: int

    @classmethod
    def create_waveform_data(cls,
                             audio: AudioSegment, 
                             time_bins: Optional[int],
                             bin_length: Optional[int] = None,
                             settings: WaveformDataSettings = WaveformDataSettings.default()) -> 'WaveformData':
        """
        Create a numpy array for use in drawing a waveform overview.
     
        """
        assert(time_bins or bin_length)

        if time_bins is not None:
            samples = audio.get_array_of_samples()
            bit_depth = audio.sample_width
            window_length = int(len(samples) / time_bins)
        else:
            window_length = bin_length

        retval = np.zeros((time_bins, 2))
        
        max_index = 0
        max_value = 0.0
        max_sample = 0
        for i in range(time_bins):
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

        return cls(retval, max_index, max_sample, max_value, full_code_value, samples_per_bin=window_length)


