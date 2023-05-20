import unittest

import pydub
import numpy
from apeek import WaveformData, WaveformDataSettings, ScalingFactor

class TestWaveformData(unittest.TestCase):
    def setUp(self):
        self.hi_audio = pydub.AudioSegment.from_wav("test/media/hi.wav") 

    def tearDown(self):
        pass
        # self.hi_audio = None

    def test_normalize(self):
        settings = WaveformDataSettings()
        settings['scaling'] = ScalingFactor.LINEAR
        settings['normalized'] = True
        result = WaveformData.create_waveform_data(self.hi_audio, 100, settings=settings)

        transposed = result.value_pairs.transpose()
        max_v, min_v = numpy.max(transposed[0]) , abs(numpy.min(transposed[1]))
        self.assertLessEqual(max(max_v, min_v), 1.0)




