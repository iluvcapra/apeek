"""
apeek main
"""

import pydub
import apeek

import sys
import shutil
import math
import optparse

def main():
    
    console_width = shutil.get_terminal_size((80,20))[0]

    parser = optparse.OptionParser(version=apeek.__version__)
    parser.add_option("-w","--width", help="Waveform width",
                      type=int,
                      metavar="WIDTH", default=console_width)
    parser.add_option("-l","--lines", help="Waveform height in lines",
                      dest="height", type=int,
                      metavar="HEIGHT", default=4)
    parser.add_option("-i","--info", help="Print statistics", 
                      default=False, 
                      action='store_true')

    (options, args) = parser.parse_args()

    for file in args:
        audio = pydub.AudioSegment.from_file(file)
        settings = apeek.WaveformSettings.default()
        settings['scaling'] = apeek.ScalingFactor.ROOT
        settings['normalized'] = True
        result = apeek.create_waveform_data(audio, length=options.width, settings=settings)
        text = apeek.rectified_ascii_waveform(result.value_pairs, height=options.height)
        if len(args) > 1:
            print(file)

        sys.stdout.write(text)
        if options.info:
            peak_db = 20 * math.log10(result.max_value / result.full_code_value)
            if result.max_index > 6:
                print(" " * (result.max_index - 4) + "max ↑" )
            else:
                print(" " * (result.max_index) + "↑ max" )

            print(f"DUR: {audio.frame_count() / audio.frame_rate:.2f} seconds @ {audio.frame_rate}Fs // " +
            f"Peak: {peak_db:.2f} dBFS at {result.max_sample / audio.frame_count():.2f} secs")

if __name__ == "__main__":
    main()
