#!/usr/bin/python -u

import time
import os

class Beep :
  FrequencyData = """
C  0    8.1757989156    12    16.3515978313    24    32.7031956626
Db 1    8.6619572180    13    17.3239144361    25    34.6478288721
D  2    9.1770239974    14    18.3540479948    26    36.7080959897
Eb 3    9.7227182413    15    19.4454364826    27    38.8908729653
E  4   10.3008611535    16    20.6017223071    28    41.2034446141
F  5   10.9133822323    17    21.8267644646    29    43.6535289291
Gb 6   11.5623257097    18    23.1246514195    30    46.2493028390
G  7   12.2498573744    19    24.4997147489    31    48.9994294977
Ab 8   12.9782717994    20    25.9565435987    32    51.9130871975
A  9   13.7500000000    21    27.5000000000    33    55.0000000000
Bb 10  14.5676175474    22    29.1352350949    34    58.2704701898
B  11  15.4338531643    23    30.8677063285    35    61.7354126570

C  36  65.4063913251    48   130.8127826503    60   261.6255653006
Db 37  69.2956577442    49   138.5913154884    61   277.1826309769
D  38  73.4161919794    50   146.8323839587    62   293.6647679174
Eb 39  77.7817459305    51   155.5634918610    63   311.1269837221
E  40  82.4068892282    52   164.8137784564    64   329.6275569129
F  41  87.3070578583    53   174.6141157165    65   349.2282314330
Gb 42  92.4986056779    54   184.9972113558    66   369.9944227116
G  43  97.9988589954    55   195.9977179909    67   391.9954359817
Ab 44  103.8261743950   56   207.6523487900    68   415.3046975799
A  45  110.0000000000   57   220.0000000000    69   440.0000000000
Bb 46  116.5409403795   58   233.0818807590    70   466.1637615181
B  47  123.4708253140   59   246.9416506281    71   493.8833012561

C  72  523.2511306012   84  1046.5022612024    96  2093.0045224048
Db 73  554.3652619537   85  1108.7305239075    97  2217.4610478150
D  74  587.3295358348   86  1174.6590716696    98  2349.3181433393
Eb 75  622.2539674442   87  1244.5079348883    99  2489.0158697766
E  76  659.2551138257   88  1318.5102276515   100  2637.0204553030
F  77  698.4564628660   89  1396.9129257320   101  2793.8258514640
Gb 78  739.9888454233   90  1479.9776908465   102  2959.9553816931
G  79  783.9908719635   91  1567.9817439270   103  3135.9634878540
Ab 80  830.6093951599   92  1661.2187903198   104  3322.4375806396
A  81  880.0000000000   93  1760.0000000000   105  3520.0000000000
Bb 82  932.3275230362   94  1864.6550460724   106  3729.3100921447
B  83  987.7666025122   95  1975.5332050245   107  3951.0664100490

C  108 4186.0090448096  120  8372.0180896192
Db 109 4434.9220956300  121  8869.8441912599
D  110 4698.6362866785  122  9397.2725733570
Eb 111 4978.0317395533  123  9956.0634791066
E  112 5274.0409106059  124 10548.0818212118
F  113 5587.6517029281  125 11175.3034058561
Gb 114 5919.9107633862  126 11839.8215267723
G  115 6271.9269757080  127 12543.8539514160
Ab 116 6644.8751612791
A  117 7040.0000000000
Bb 118 7458.6201842894
B  119 7902.1328200980
"""

  def __init__ (self) :
    self._NoteTable = {
      'C'  :  0,
      'Cs' :  1, 'Df' :  1, 'Csharp' :  1, 'Dflat' :  1,
      'D'  :  2,
      'Ds' :  3, 'Ef' :  3, 'Dsharp' :  3, 'Eflat' :  3,
      'E'  :  4,
      'F'  :  5,
      'Fs' :  6, 'Gf' :  6, 'Fsharp' :  6, 'Gflat' :  6,
      'G'  :  7,
      'Gs' :  8, 'Af' :  8, 'Gsharp' :  8, 'Aflat' :  8,
      'A'  :  9,
      'As' : 10, 'Bf' : 10, 'Asharp' : 10, 'Bflat' : 10,
      'B'  : 11,
      }

    self._FrequencyTable = self._parseFrequencyData(self.FrequencyData)

    # TBD. figure out if we're on X11 or console.
    # self.beep = self.X11Beep
    # self.reset = self.X11Reset
    # self.beep = self.ConsoleBeep
    # self.reset = self.ConsoleReset
    self.beep = self.BeepBeep
    self.reset = self.BeepReset

  def __del__(self) :
    self.reset()

  def _parseFrequencyData(self,data) :
    table = {}
    lines = data.split('\n')
    for line in lines:
      line = line.strip()
      if not line : continue
      parts = line.split()

      i = 1 # skip first index; label
      while (i < len(parts)) :
        note = parts[i]
        frequency = parts[i+1]
        table[int(note)] = int(float(frequency)+0.5)
        i = i + 2
    return table


  def delay(self,duration=0.2) : time.sleep(duration)

  def ConsoleBeep(self,frequency,length=150) :
    print "\33[10;%d]\33[11;%d]\a\33[10]\33[11]" % (frequency,length)
    self.delay()

  def ConsoleReset(self) :
    pass

  def X11Beep(self,frequency,length=150):
    frequency = int(frequency) # Some X11 require int freq.
    os.system("xset b 100 %d %d" % (frequency,length))
    print "\a\b",
    self.delay()

  def X11Reset(self):
    os.system("xset b")

  def BeepBeep(self, frequency, length=150) :
    os.system("beep -f %d -l %d" % (frequency, length))
    self.delay(0.05)

  def BeepReset(self) :
    pass

  def play(self, note, octave=5) :
    note_off = self._NoteTable[note]
    note = (octave*12)+note_off
    frequency = self._FrequencyTable[note]
    self.beep(frequency)

  def generic(self) :
    self.play("C")
    self.play("C")
    self.play("C")
    self.play("C")
  
  def salt_n_pepa(self,rpt=1) :
    for i in (range(rpt)) :
      self.play("D",5)
      self.delay()
      self.play("A",6)
      self.play("G",5)
      self.delay()
      self.play("F")
      self.delay()
      self.play("E")
      self.delay()
      self.play("C")
      self.delay()
      self.play("C",5)
      self.play("E",5)
      self.play("F",5)
      self.play("E",5)
      self.play("C",5)

    self.play("D",5)

  def shave_and_a_haircut(self) :
    # shave and a haircut...
    self.play("C",6)
    self.delay(0.2)
    self.play("G")
    self.play("G")
    self.play("A")
    self.delay(0.2)
    self.play("G")
    self.delay(0.6)
    self.play("B")
    self.delay(0.2)
    self.play("C",6)

  def charge(self) :
    self.play("G")
    self.play("B")
    self.play("D",6)
    self.play("G",6)
    self.delay(0.2)
    self.play("D",6)
    self.play("G",6)
    self.play("G",6)

  def impossible(self) :
    self.play("C")
    self.delay(0.1)
    self.play("C")
    self.delay(0.1)
    self.play("D")
    self.play("E")
    self.play("C")
    self.delay(0.1)
    self.play("C")
    self.delay(0.1)
    self.play("A",4)
    self.play("B",4)

  def take_on_me(self) :
    # tbd. parse this syntax. octave on left, caps are sharps.
    
    # 4|--F-F-d--------e--e--e-G-G-a-b--a-a-a-e--C--F--F--F-e-e-F-e----|
    # 3|--------b---b--------------------------------------------------|
    #
    # 4|--F-F-d--------e--e--e-G-G-a-b--a-a-a-e--C--F--F--F-e-e-F-e----|
    # 3|--------b---b--------------------------------------------------|
    #
    # 4|--F-F-d--------e--e--e-G-G-a-b--a-a-a-e--C--F--F--F-e-e-e------|
    # 3|--------b---b--------------------------------------------------|
    #
    # 5|-F-F-F-d-d-b-b-b-e-e-G-a-a-a-a-e-d-F-F-F-e-e-f-e--

    # no octave information:
    # F#-F#-D-B-B-E-E-E-Ab-Ab-A-B-A-A-A-E-D-F#-F#-F#-E-E-F#-E

    base_octave = 5
    sequence = [ "Fs",
                 "Fs",
                 "D",
                 ("B",-1),
                 "delay",
                 ("B",-1),
                 "delay",
                 "E",
                 "delay",
                 "E",
                 "delay",
                 "E",
                 "Gs",
                 "Gs",
                 "A",
                 "B",
                 "A",
                 "A",
                 "A",
                 "E",
                 "delay",
                 "D",
                 "delay",
                 "Fs",
                 "delay",
                 "Fs",
                 "delay",
                 "Fs",
                 "E",
                 "E",
                 "Fs",
                 "E" ]
    for n in sequence :
      if n == 'delay' :
        self.delay(0.2)
      elif isinstance(n,tuple) :
        (n,octave_shift) = n
        self.play(n,base_octave+octave_shift)
      else :
        self.play(n,base_octave)
    
def beep_test():
  b = Beep()
  try :
    b.salt_n_pepa(2)
    #b.shave_and_a_haircut()
    #b.charge()
    #b.generic()
    # b.take_on_me()
  finally :
    b.reset()
  del b
  
if __name__ == '__main__' :
  beep_test()

# play("CDEFGAB",5)
# play("C",6)
# play("CDEFGAB")
# play("C",6)

