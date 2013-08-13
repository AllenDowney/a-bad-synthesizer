""" Code example from Think DSP by Allen B. Downey

Based mididump, a script that is part of python-midi:
https://github.com/vishnubob/python-midi

Copyright 2013 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import midi
import sys

def print_table(self, name, values):
    """Prints values as a table in C syntax.

    name: string variable name
    valeus: sequence of int
    """
    print 'int %s[] = {' % name
    for value in values:
        print '%d, ' % value,
    print '};'


def write_track(track):
    for event in track:
        if event.name.startswith("Note"):
            tick = event.tick
            note, velocity = event.data
            print tick, note, velocity


def main(script, midifile):

    pattern = midi.read_midifile(midifile)

    track = pattern[0]
    write_track(track)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: {0} <midifile>".format(sys.argv[0])
        sys.exit(2)


    main(*sys.argv)
