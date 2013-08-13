"""
"""


import bisect
import serial
import sys
import redis
import numpy

from math import log


class Redis(object):
    """Encapsulates a Redis database.
    """
    def __init__(self):
        """Opens the database.
        """
        self.rdb = redis.Redis(host='localhost', port=6379, db=0)

    def append(self, key, val):
        """Appends a value to the list for a given key.

        key: pot level pair
        val: half pulse width in usecs
        """
        self.rdb.append(key, val + ' ')

    def get(self, key):
        """Looks up a given key.

        key: pot level pair

        returns: string repr of a list of half pulse widths
        """
        return self.rdb.get(key)

    def keys(self, pattern='*'):
        """Returns all keys that match pattern.

        pattern: string regular expression

        returns: sequence of keys
        """
        return self.rdb.keys(pattern)

    def clear(self, pattern='*'):
        """Deletes all keys that match pattern.

        pattern: string regular expression
        """
        for key in self.keys(pattern):
            print key
            self.rdb.delete(key)
        

class Table(object):
    def __init__(self, filename='tuner.db'):
        """Reads measurements and builds the frequency lookup table.

        initializes:
        self.freqs: sorted list of measured frequencies
        self.levels: list of corresponding pot levels
        """
        rdb = Redis()
        keys = rdb.keys()

        pairs = []
        for key in rdb.keys():
            levels = [int(x) for x in eval(key)]
            t = rdb.get(key).split()
            usecs = [float(x) for x in t]
            usec = trimmed_mean(usecs)
            freq = 0.5e6 / usec
            pairs.append((freq, levels))

        pairs.sort()

        self.freqs, self.levels = zip(*pairs)

    def make_table(self):
        """Prints pot levels in C syntax.
        """
        levels = []
        for i in range(128):
            target = midi_to_freq(i)
            freq, level, diff = self.lookup(target)
            levels.append(level)

        self.print_levels(levels, 0)
        self.print_levels(levels, 1)

    def print_levels(self, levels, index=0):
        """Prints pot levels in C syntax.

        levels: list of pot level pairs
        index: which element of the pair to print
        """
        print 'int level%d_table[] = {' % index
        for level in levels:
            print '%d, ' % level[index],
        print '};'

    def lookup(self, target):
        """Finds the best settings for a give target frequency.

        target: float frequency

        returns: actual frequency, pot levels, error in cents
        """
        i = bisect.bisect(self.freqs, target)

        #if i == 0:
        #    diff2 = cents(target, self.freqs[i])
        #    return self.freqs[i], self.levels[i], diff2

        diff1 = cents(target, self.freqs[i-1])

        if i == len(self.freqs):
            return self.freqs[i-1], self.levels[i-1], diff1
        
        diff2 = cents(target, self.freqs[i])

        if abs(diff1) < abs(diff2):
            return self.freqs[i-1], self.levels[i-1], diff1
        else:
            return self.freqs[i], self.levels[i], diff2


def trimmed_mean(t):
    n = len(t) / 5
    t.sort()
    return numpy.mean(t[n:-n])


def log2(x, denom=log(2)):
    return log(x)/denom


def cents(f1, f2):
    semitones = 12 * (log2(f1) - log2(f2))
    cents = semitones * 100
    return cents


def midi_to_freq(num):
    semitones = num - 69.0
    factor = 2 ** (semitones/12)
    return 440.0 * factor


def clear(filename='tuner.db'):
    rdb = Redis()
    rdb.clear()


def collect(filename='tuner.db'):
    ser = serial.Serial('/dev/ttyACM1', 38400)
    #shelf = shelve.open('filename')
    rdb = Redis()

    try:
        i = 0
        while True:
            collect_one(ser, rdb, i>100)
            i += 1
    finally:
        #shelf.close()
        pass


def collect_one(ser, rdb, flag=True):
    try:
        p1, p2, usec = ser.readline().split()
    except ValueError:
        return

    if not p1.startswith('+'):
        return            

    setting = p1, p2
    if flag:
        rdb.append(setting, usec)
        print setting, usec


def main(script, command='table'):
    if command == 'collect':
        collect()
    elif command == 'table':
        table = Table()
        table.make_table()
    elif command == 'clear':
        clear()


if __name__ == '__main__':
    main(*sys.argv)
