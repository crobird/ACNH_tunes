#!/usr/bin/env python

import re
import readline
import musicalbeeps

DESCRIPTION = """
    This script plays island tunes for Animal Crossing New Horizons. The tunes can
    be passed in via a file, directly as an argument, or entered in through the
    interactive mode.

    The valid tune characters are: gabcdefGABCDE-x

    The '-' will extend the previous notes duration for an addition note length.

    The 'x' will play no note for that duration.

    Lower cased letters will play the lower octave version of the note and
    upper cased letters will play the upper octave version.
"""

DEFAULT_TUNES = {
    "TMBG - Ana Ng": 'GGG-deG-ddd-c-b-',
    "TMBG - Don't Let's Start": 'D-D-CCG-xeGGA-e-',
    "White Stripes - Seven Nation Army": 'e--eGe-dc--xb--x',
    "ABBA - Dancing Queen": 'cdee-f-f--e-f-f-',
    "ABBA - Lay All Your Love On Me": 'f-GAG-G-f---xxxx',
    "Mii": 'g-ce-c-agggxxxxx',
    "Gravity Falls": 'fffAAGFxAAAGAGf',
    "Howl's Theme": 'e-A-C-E-EDCB-C--',
    "Wii Sports": 'e-f-efGCBCGecded',
    "X Files": 'a-e-d-e-G-e--xxx'
}

DEFAULT_VOLUME = 0.3
DEFAULT_NOTE_DURATION = .1
VALID_CHARS = 'gabcdefGABCDE-x'

class TunePlayer(object):
    NOTE_MAP = dict(
        E = 'E5',
        D = 'D5',
        C = 'C5',
        B = 'B4',
        A = 'A4',
        G = 'G4',
        f = 'F4', F = 'F4',
        e = 'E4',
        d = 'D4',
        c = 'C4',
        b = 'B3',
        a = 'A3',
        g = 'G3',
    )

    def __init__(self, tune_str=None,
        volume=DEFAULT_VOLUME, 
        note_duration=DEFAULT_NOTE_DURATION,
        verbose=False
        ):
        self.tune_str = tune_str
        self.verbose = verbose
        self.note_duration = note_duration
        self.player = musicalbeeps.Player(volume=volume, mute_output=not(verbose))
        if tune_str:
            self.load_tune(tune_str)

    def __repr__(self):
        return str(self.notes)

    def get_note_duration(self, extend_by):
        return self.note_duration + (self.note_duration * extend_by)

    def is_valid_tune(self, tune_str=None):
        tune = tune_str if tune_str else self.tune_str
        if not set(tune_str.lower()).issubset(set(VALID_CHARS.lower())):
            return False
        return True

    def load_tune(self, tune_str):
        if not self.is_valid_tune(tune_str):
            raise Exception(f"tune '{tune_str}' contains illegal characters, valid chars are '{VALID_CHARS}'")

        self.notes = []
        i = 0
        while i < len(tune_str):
            c = TunePlayer.NOTE_MAP.get(tune_str[i], 'pause')

            # Figure out how long this note should be
            if i == len(tune_str) - 1:
                extend_by = 0
            else:
                m = re.match(r'(-*)', tune_str[i+1:])
                dashes = m.group(1)
                extend_by = len(dashes)

            # Add note + note duration
            self.notes.append((c, self.get_note_duration(extend_by)))
            i += 1 + extend_by

    def play(self):
        if self.verbose:
            print(f"Playing tune: {self.tune_str}")
        for note, duration in self.notes:
            self.player.play_note(note, duration)

def main(args):
    player = TunePlayer(volume=args.volume, note_duration=args.duration, verbose=args.verbose)

    tune = None
    if args.file:
        with open(args.file, 'r') as fh:
            tune = fh.read().strip()
    elif args.tune:
        tune = args.tune

    if tune:
        player.load_tune(tune)
        player.play()
        exit(0)

    # Interactive mode    
    tune_names = sorted(list(DEFAULT_TUNES.keys()))
    while True:
        tune = None
        for i, name in enumerate(tune_names):
            print(f'{i+1:2}. {name}')
        choice = input(f'Enter a number (type q to quit): ')
        if choice.strip() in ['q', 'quit']:
            exit(0)
        if choice.isdigit():
            n = int(choice) - 1
            chosen_tune = tune_names[n]
            tune = DEFAULT_TUNES[chosen_tune]
        else:
            if not player.is_valid_tune(choice):
                print("-- That's not valid tune syntax. See help docs for more info. --")
                continue
            tune = choice
        player.load_tune(tune)
        player.play()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f', '--file', help='file')
    parser.add_argument('-t', '--tune', help='Tune to play')
    parser.add_argument('-D', '--duration', default=DEFAULT_NOTE_DURATION, type=float, help=f"Base note duration, default: {DEFAULT_NOTE_DURATION}")
    parser.add_argument('-V', '--volume', default=DEFAULT_VOLUME, type=float, help=f"Volume setting, default: {DEFAULT_VOLUME}")
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='verbose output')
    args = parser.parse_args()

    main(args)