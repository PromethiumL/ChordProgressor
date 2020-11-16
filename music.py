import copy
import playsound as ps
import pprint

_first_C_offset = 3
_highlimit = 87

global _standard_position_chord
_notename_to_int = {
    'C': 0,
    'C#': 1,
    'Db': 1,
    'D': 2,
    'D#': 3,
    'Eb': 3,
    'E': 4,
    'Fb': 4,
    'E#': 5,
    'F': 5,
    'F#': 6,
    'Gb': 6,
    'G': 7,
    'G#': 8,
    'Ab': 8,
    'A': 9,
    'A#': 10,
    'Bb': 10,
    'B': 11,
    'Cb': 11,
    'B#': 11,
}

_int_to_notename = {
    0: ('C', 'C'),
    1: ('C#', 'Db'),
    2: 'D',
    3: ('D#', 'Eb'),
    4: ('E', 'E'),
    5: ('F', 'F'),
    6: ('F#', 'Gb'),
    7: 'G',
    8: ('G#', 'Ab'),
    9: 'A',
    10: ('A#', 'Bb'),
    11: ('B', 'B')
}

_interval_to_offset = {
    'd2': 0,
    'P1': 0,
    'A1': 1,
    'm2': 1,
    'AA1': 2,
    'd3': 2,
    'M2': 2,
    'A2': 3,
    'dd4': 3,
    'm3': 3,
    'd4': 4,
    'M3': 4,
    'A3': 5,
    'dd5': 5,
    'P4': 5,
    'A4': 6,
    'd5': 6,
    'AA4': 7,
    'd6': 7,
    'P5': 7,
    'A5': 8,
    'm6': 8,
    'AA5': 9,
    'd7': 9,
    'M6': 9,
    'A6': 10,
    'dd8': 10,
    'm7': 10,
    'd8': 11,
    'M7': 11,
    'A7': 12,
    'd9': 12,
    'P8': 12,
    'A8': 13,
    'm9': 13,
    'AA8': 14,
    'M9': 14,
    'A9': 15,
    'dd11': 15,
    'd11': 16,
    'P11': 17,
    'A11': 18,
    'AA11': 19,
    'd13': 19,
    'm13': 20,
    'M13': 21,
    'A13': 22,
}

_chord_to_interval = {
    'maj': ['M3', 'P5', 'P8'],

    'min': ['m3', 'P5'],
    'm': ['m3', 'P5'],
    '-': ['m3', 'P5'],

    '(b5)': ['M3', 'd5'],

    'aug': ['M3', 'A5'],
    '+': ['M3', 'A5'],

    'dim': ['m3', 'd5'],
    'o': ['m3', 'd5'],

    'sus2': ['M2', 'P5'],

    'sus4': ['P4', 'P5'],

    '6': ['M3', 'P5', 'M6'],

    'm6': ['M3', 'P5', 'm6'],

    '69': ['M3', 'P5', 'M6', 'M9'],

    '7': ['M3', 'P5', 'm7'],

    #    '7alt': ['M3', 'd5', 'm7'],    ambigious
    '7b5': ['M3', 'd5', 'm7'],
    '7-5': ['M3', 'd5', 'm7'],
    '7#5': ['M3', 'A5', 'm7'],
    '7b5b9': ['M3', 'd5', 'm7', 'm9'],
    '7b5#9': ['M3', 'd5', 'm7', 'A9'],
    'm7-5': ['m3', 'd5', 'm7'],
    'm7b5': ['m3', 'd5', 'm7'],
    'm7b5b9': ['m3', 'd5', 'm7', 'm9'],
    'm7b5#9': ['m3', 'd5', 'm7', 'A9'],

    'maj7': ['M3', 'P5', 'M7'],
    'maj7-5': ['M3', 'd5', 'M7'],
    'maj7b5': ['M3', 'd5', 'M7'],
    'maj7#5': ['M3', 'A5', 'M7'],

    'M7': ['M3', 'P5', 'M7'],
    'M7-5': ['M3', 'd5', 'M7'],
    'M7b5': ['M3', 'd5', 'M7'],
    'M7#5': ['M3', 'A5', 'M7'],

    'm7': ['m3', 'P5', 'm7'],
    '-7': ['m3', 'P5', 'm7'],

    'dim7': ['m3', 'd5', 'd7'],
    'o7': ['m3', 'd5', 'd7'],

    '+7': ['M3', 'A5', 'M7'],
    'aug7': ['M3', 'A5', 'M7'],

    '7sus2': ['M2', 'P5', 'm7'],
    '7sus4': ['P4', 'P5', 'm7'],

    'mM7': ['m3', 'P5', 'M7'],

    '7b9': ['M3', 'P5', 'm7', 'm9'],
    '7#9': ['M3', 'P5', 'm7', 'A9'],

    '7b9#5': ['M3', 'A5', 'm7', 'm9'],
    '7#9#5': ['M3', 'A5', 'm7', 'A9'],

    '(-9)': ['M3', 'P5', 'm9'],
    '(b9)': ['M3', 'P5', 'm9'],
    '(#9)': ['M3', 'P5', 'A9'],

    '9': ['M3', 'P5', 'm7', 'M9'],

    'maj9': ['M3', 'P5', 'M7', 'M9'],

    'm9': ['m3', 'P5', 'm7', 'M9'],

    'add9': ['M3', 'P5', 'M9'],
    '(9)': ['M3', 'P5', 'M9'],

    'madd9': ['m3', 'P5', 'M9'],

    '9sus4': ['P4', 'P5', 'm7', 'M9'],

    '11': ['M3', 'P5', 'm7', 'M9', 'P11'],

    'maj11': ['M3', 'P5', 'M7', 'M9', 'A11'],

    'm11': ['m3', 'P5', 'm7', 'M9', 'P11'],
    '-11': ['m3', 'P5', 'm7', 'M9', 'P11'],

    'mb11': ['m3', 'P5', 'm7', 'd11'],
    'm(b11)': ['m3', 'P5', 'm7', 'd11'],

    '13': ['M3', 'P5', 'm7', 'M9', 'M13'],

    'm13': ['m3', 'P5', 'm7', 'M9', 'P11', 'M13'],

    'maj13': ['M3', 'P5', 'M7', 'M9', 'A11'],

    'add13': ['M3', 'P5', 'M13']
}

_modetable = {
    'Ionion': [0, 2, 4, 5, 7, 9, 11],
    'Dorian': [0, 2, 3, 5, 7, 9, 10],
    'Phrygian': [0, 1, 3, 5, 7, 8, 10],
    'Lydian': [0, 2, 4, 6, 7, 9, 11],
    'Mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'Aeolian': [0, 2, 3, 5, 7, 8, 10],
    'Locrian': [0, 1, 3, 5, 6, 8, 10],
    'ChineseMajor': [0, 2, 4, 7, 9],
    'ChineseMinor': [0, 3, 5, 7, 10],
    'HamoniousMinor': [0, 2, 3, 5, 7, 8, 11],
    'MelodyMinor': [0, 2, 3, 5, 7, 9, 11],
    'TokyoMajor': [0, 4, 5, 9, 11],
    'TokyoMinor': [0, 2, 3, 7, 8],
}


def _is_note_name(name):
    return name in _notename_to_int


def _is_chord_name(name):
    return name in _chord_to_interval


def _have_same_name(i1, i2):
    return i1 % 12 == i2 % 12


def cmp(a, b):
    return (a > b) - (a < b)


class Note:
    """Note is the basic class of the progresser."""
    flag = 0

    def __init__(self, name=None, octave=2, index=None):
        "To construct a note"
        if not (name is None) or (index is None):
            self.name = name
            self.octave = octave
            self.index = _first_C_offset + self.octave * 12 + _notename_to_int[name]
        else:
            self.index = index
            self.name = None
            self.octave = (index + (12 - _first_C_offset)) // 12 + 1
        self.check_index()
        self._update_name()
        return

    def inc(self, step=1):
        if not type(step) == int:
            if not step in _interval_to_offset:
                raise Exception("inc step err : {}".format(step))
            else:
                step = _interval_to_offset[step]
        self.flag = 1
        self.index += step
        self.octave = (self.index - _first_C_offset + 12) // 12
        self.check_index()
        self._update_name()
        return

    def dec(self, step=1):
        if not type(step) == int:
            if not step in _interval_to_offset:
                raise Exception("dec step err")
            else:
                step = _interval_to_offset[step]

        self.flag = -1
        self.index -= step
        self.octave = (self.index - _first_C_offset + 12) // 12
        self.check_index()
        self._update_name()
        return

    def _update_name(self):
        if self.name != None:
            if 'b' in self.name:
                self.flag = -1
            if '#' in self.name:
                self.flag = 1
        self.name = _int_to_notename[(self.index - _first_C_offset) % 12]
        if len(self.name) > 1:
            self._select_name(self.name, self.flag)
        return

    def _select_name(self, name, flag):
        if flag >= 0:
            self.name = name[0]
        else:
            self.name = name[1]
        return

    def check_index(self):
        try:
            if not self.index in range(_highlimit):
                raise Exception('Note index out of range : {}'.format(self.index))
            return
        except Exception as e:
            self.index = self.index - 24

    def show_info(self):
        print("Note: name : {}, index: {},  octave: {}, flag : {}"
              .format(self.name, self.index, self.octave, self.flag))
        return

    def up(self):
        self.inc(12)
        self.check_index()
        return

    def down(self):
        self.dec(12)
        self.check_index()
        return

    def __lt__(self, other):
        return self.index < other.index

    def __eq__(self, other):
        return self.index == other.index

    # def __cmp__(self, other):
    #     return cmp(self.index, other.index)


def cmp_note_name(n1, n2):
    return _notename_to_int[n1.name] == _notename_to_int[n2.name]


class Chord:
    """ A class based on Note.

    constructor:
        __init__(self, name='CMaj7')

    A chord object can be played by 'playsound.playsound(obj)'
    """

    def __init__(self, name='C'):

        # get the root from the name

        if _is_note_name(name):
            self.root = Note(name)
            self.type = 'maj'
            self.name = self.root.name
            self.base = _chord_to_interval[self.type]  # base is an array of intervals.
            self.construct()
        else:
            if len(name) < 1:
                raise Exception('incorrect chord name : {}'.format(name))
            nstr = name[:2]
            if _is_note_name(nstr):
                self.root = Note(nstr)
                self.type = name[2:]
            elif _is_note_name(nstr[0]):
                self.root = Note(nstr[0])
                self.type = name[1:]
            else:
                raise Exception('unrecognized root')
            # get the chord type

            if _is_chord_name(self.type):
                self.base = _chord_to_interval[self.type]
                self.name = name
            else:
                nstr = 'unrecognized chord type : root : {}, type : {}'.format(
                    self.root.name, self.type)
                raise Exception(nstr)

            self.construct()
            #            self.expand()
            return

    def construct(self):
        lower = copy.deepcopy(self.root)
        lower.down()

        self.notes = []
        self.notes.append(lower)
        self.notes.append(self.root)  # These are the two root notes.

        for n in self.base:
            newnote = copy.deepcopy(self.root)
            newnote.inc(_interval_to_offset[n])  # construct chord notes
            self.notes.sort()
            self.notes.append(newnote)

        self.base = self.notes[1:]  # Now base is an array of notes.

        return

    def remove_duplicates(self):
        arr = []
        for note in self.notes:
            exist = False
            for n in arr:
                if note.index == n.index:
                    exist = True
            if not exist:
                arr.append(note)
        arr.sort()
        self.notes = arr

    def show_info(self):
        print('name : {}, root : {}, type: {}'.format(
            self.name, self.root.name, self.type))
        print('\tNote list : {}'.format(map(lambda x: x.name, self.notes)))

    def invert_up(self):
        bot = self.base[0]
        base = self.base[1:]
        bot.up()
        self.base.append(bot)
        self.base.sort()
        self.remove_duplicates()

    def drops_1(self):
        self.notes[-1].down()
        self.remove_duplicates()

    def drops_2(self):
        self.notes[-2].down()
        self.remove_duplicates()

    def drops_3(self):
        if len(self.notes) < 5:
            self.drops_2()
        else:
            self.notes[-3].down()
            self.remove_duplicates()

    def drops_2_3(self):
        if len(self.notes) < 5:
            self.drops_2()
        else:
            self.notes[-2].down()
            self.notes[-3].down()
            self.remove_duplicates()

    def drops_2_4(self):
        if len(self.notes) < 6:
            self.drops_2_3()
        else:
            self.notes[-2].down()
            self.notes[-4].down()
            self.remove_duplicates()

    def expand(self, gap=5):  # gap 5 means M3
        """ 
        Turn itself into a open-arranged form 
        The 'gap' measures the open-level
        """
        '''
        for i in range(len(self.notes)):
            if i > 2:
                newnote=copy.deepcopy(self.notes[i])
                newnote.up()
                self.notes.append(newnote)
        '''
        self.notes.sort()
        global _highlimit
        _highlimit = 65

        i = 2
        while i < (len(self.notes) - 1):  # allow m2 in the endding
            if (self.notes[i].index - self.notes[i - 1].index) < gap:

                try:
                    self.notes[i].up()
                except Exception as value:
                    print('A note has gone missing. ({})'.format(value))
                    del self.notes[i]

                self.notes.sort()
                continue
            else:

                """
                Here we use '2' insdead of '1' to keep the arrangement from 
                being TOO WIDE.
                """

                i = i + 2
                continue
        _highlimit = 87
        return

    def attach_to(self, other):
        if not isinstance(other, Chord):
            raise Exception("not a chord")
        a = map(lambda x: x.index, other.notes)
        a = a[1:]
        # print a
        for note in self.notes[3:4]:
            i, j, k, l = note.index, note.index + 12, note.index + 24, note.index + 36
            b1 = map(lambda x: ((x - i) // 12, ((x - i) *
                                                (x - i) // 80 + abs(i - x) * 10), 0), a)
            b1.sort(key=lambda x: abs(x[1]))
            # print b1
            # print
            b2 = map(lambda x: ((x - j) // 12, ((x - j) *
                                                (x - j) // 80 + abs(j - x) * 10), 1), a)
            b2.sort(key=lambda x: abs(x[1]))
            # print b2
            # print
            b3 = map(lambda x: ((x - k) // 12, ((x - k) *
                                                (x - k) // 80 + abs(k - x) * 10), 2), a)
            b3.sort(key=lambda x: abs(x[1]))
            # print b3
            # print
            b4 = map(lambda x: ((x - l) // 12, ((x - l) *
                                                (x - l) // 80 + abs(l - x) * 10), 3), a)
            b4.sort(key=lambda x: abs(x[1]))
            # print b4
            # print

            b = b1 + b2 + b3 + b4
            b.sort(key=lambda x: x[1])
            # print 'b = {}'.format(b)
            # raise Exception("fin")
            oct = b[0][0] + b[0][2]

            if oct > 0:
                note.inc(oct * 12)
            if oct < 0:
                note.dec((0 - oct) * 12)
        self.notes.sort()
        #        if (self.notes[-1].index - self.notes[1].index) < 40:
        #            self.expand()

        return

    def get_note_list(self):
        return map(lambda x: x, self.notes)

    # def connect_to(self, other):
    #    if not isinstance(other, Chord):
    #        raise Exception("\'{}\'' is not a chord.".format(other))
    #    l = other.get_note_list()
    #    base = map(lambda x:x.index, self.base)
    #    #print base
    #    '''connect the ROOT first. '''

    #    self.notes = []
    #    self.notes.append(
    #        Note(
    #            self.root.name,
    #            octave=min([
    #                (abs(l[0].index - self.root.index), 1), 
    #                (abs(l[1].index - self.root.index), 2)
    #                #(999, 0)
    #            ])[1]
    #        )
    #    )

    #    # note2 = copy.deepcopy(self.notes[0])
    #    # note2.up()
    #    # self.notes.append(note2)

    #    '''connect the rest notes'''

    #    def getoct(x):
    #        return (x + 8) // 12 - 1

    #    for note in l[1:]:

    #        # playsound.play(note, duration=1)

    #        q = []
    #        index, octave = note.index, note.octave
    #        for i in range(index - 10, index + 5):
    #            #print 'i = {}, '.format(i), map(_have_same_name, base, [i]*len(base))
    #            if True in map(_have_same_name, base, [i]*len(base)):
    #                q.append((abs(i - index), i))

    #        #print q

    #        # plst = []
    #        # for tp in q:
    #        #     plst.append(Note(index=tp[1]))
    #        # playsound.play(plst, interval=0.1, duration=1)
    #        

    #        ans = min(q)
    #        q.remove(ans)
    #        #print ans
    #        #print 
    #        if ans[1] == self.notes[-1].index:
    #            #print 'repetion detected'
    #            while len(q) > 1 and q[0][1] <= ans[1]:
    #                q = q[1:]
    #            ans = q[0]

    #        newnote = Note(index=ans[1])

    #        # playsound.play(newnote, duration = 2)
    #        
    #        self.notes.append(newnote)
    #        #print 'Now notes are {}'.format(map(lambda x:x.index, self.notes))
    #        del q
    #        self.notes.sort()
    #    
    #    if self.notes[0].index > self.notes[1].index:
    #        self.notes[0].down()

    def connect_to(self, target):
        """This new algorithm tries to pick up the best from the generated voicings."""

        def chord_dist_loss(chord, target):
            """ The chord_dist_loss(x) to minimize"""
            return chord_dist(chord, target) + chord_dist(chord, _standard_position_chord)

        arr = []
        chord = copy.deepcopy(self)

        for i in range(len(self.base) * 2):
            current_inversion = copy.deepcopy(chord)
            newchord = copy.deepcopy(current_inversion)
            newchord.drops_2()
            arr.append(
                (chord_dist_loss(newchord, target), newchord)
            )

            newchord = copy.deepcopy(current_inversion)
            newchord.drops_3()
            arr.append(
                (chord_dist_loss(newchord, target), newchord)
            )

            newchord = copy.deepcopy(current_inversion)
            newchord.drops_2_3()
            arr.append(
                (chord_dist_loss(newchord, target), newchord)
            )

            newchord = copy.deepcopy(current_inversion)
            newchord.drops_2_4()
            arr.append(
                (chord_dist_loss(newchord, target), newchord)
            )

            del current_inversion
            chord.invert_up()

        # Select the best one.
        arr = list(set(arr))
        arr.sort(key=lambda tp: tp[0])
        # pprint.pprint(arr)

        # for cp in arr:
        #     d, c = cp
        #     print('chord_dist_loss = {}'.format(d))
        #     ps.play(c, interval=0.05, duration=0.5)

        self.notes = copy.deepcopy(arr[0][1].notes)

        del arr
        return


def chord_dist(c1, c2):
    """ c1 and c2 are Chord type"""
    if not (isinstance(c1, Chord) and isinstance(c2, Chord)):
        raise str("not chords")
        return
    d = (c1.notes[1].index - c2.notes[1].index) ** 2 + \
        (c1.notes[-1].index - c2.notes[-1].index) ** 2 + \
        (c1.notes[2].index - c2.notes[2].index) ** 2 + \
        (c1.notes[-2].index - c2.notes[-2].index) ** 2 + \
        (c1.notes[3].index - c2.notes[3].index) ** 2 + \
        (c1.notes[-3].index - c2.notes[-3].index) ** 2
    return d


def gen_mode(tonic, name='Ionion'):
    base = Note(tonic, octave=1)
    if not (name in _modetable):
        print(name + ' mode does not exist.')
        return
    pos = base.index
    arr = []
    while 1:
        for i in _modetable[name]:
            x = pos + i
            if x > 87:
                break
            arr.append(pos + i)
        pos = pos + 12
        if pos + 12 > 87:
            break
    return arr


_standard_position_chord = Chord('Cmaj7')


def main():
    # n = Note(index=36)
    # n.show_info()
    c = Chord('D')
    c.show_info()
    c2 = Chord('G7')
    c2.show_info()

    c2.connect_to(c)
    c2.show_info()


if __name__ == '__main__':
    main()

if __name__ == 'music':
    print("Module 'music' loaded.")
    _standard_position_chord.expand()
    for note in _standard_position_chord.notes[1:]:
        note.up()
    _standard_position_chord.show_info()
