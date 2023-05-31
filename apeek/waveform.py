import numpy as np
from pydub import AudioSegment

from enum import Enum
from dataclasses import dataclass
from typing import TypedDict, Optional, cast


class ScalingFactor(Enum):
    LINEAR = 0
    ROOT = 1


class WaveformDataSettings(TypedDict):
    scaling: 'ScalingFactor'
    normalized: bool
    

def default_settings():
    return WaveformDataSettings(scaling=ScalingFactor.ROOT, normalized=True)


@dataclass
class WaveformData:
    """
    Data collected from an AudioSegment to be used for drawing a waveform.
    """
    value_pairs: np.ndarray 
    max_index: int
    max_sample: int
    max_value: float
    full_code_value: float
    samples_per_bin: int

    @classmethod
    def create_waveform_data(cls,
                             audio: AudioSegment, 
                             time_bin_count: Optional[int],
                             bin_length: Optional[int] = None,
                             settings: WaveformDataSettings = default_settings()) -> 'WaveformData':
        """
        Create a numpy array for use in drawing a waveform overview.
     
        """

        samples = audio.get_array_of_samples()
        channel_count = audio.channels
        assert isinstance(channel_count,int)
        
        frame_count = len(samples) // channel_count

        if time_bin_count is not None:
            window_length = (frame_count // time_bin_count) * channel_count
        elif bin_length is not None:
            window_length = bin_length
            time_bin_count = (frame_count // bin_length) * channel_count
        else:
            assert False

        retval = np.zeros((time_bin_count, 2))
        
        max_index = 0
        max_value = 0.0
        max_sample = 0
        for i in range(time_bin_count):
            window = samples[i * window_length : (i + 1) * window_length]
            retval[i] = (np.max(window),np.min(window))
            magnitude = np.max(np.abs(window))
            if magnitude > max_value:
                max_index = i
                max_sample = cast(int, np.argmax(np.abs(window)) + i * window_length)
                max_value = magnitude


        bit_depth = audio.sample_width
        assert isinstance(bit_depth,int) 
        full_code_value = (2 ** (bit_depth * 8 - 1)) 
        retval = retval / full_code_value

        if settings['normalized']:
            sample_max = np.max(retval)
            sample_min = np.min(retval)
            scale_max = max(abs(sample_max), abs(sample_min))
            if scale_max != 0:
                retval = retval / scale_max

        if settings['scaling'] == ScalingFactor.ROOT:
            signs = np.sign(retval)
            absval = np.sqrt(np.fabs(retval))
            retval = absval * signs

        return cls(retval, max_index, max_sample, 
                   max_value, full_code_value, samples_per_bin=window_length)


