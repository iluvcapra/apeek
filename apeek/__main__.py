"""
apeek main
"""

import pydub
import apeek

import sys
import shutil

def main():
    console_width = shutil.get_terminal_size((80,20))[0]
    for file in sys.argv[1:]:
        audio = pydub.AudioSegment.from_file(file)
        result = apeek.create_waveform_data(audio, length=console_width)
        text = apeek.rectified_ascii_waveform(result, height=4)
        print(file)
        print(text)

if __name__ == "__main__":
    main()
