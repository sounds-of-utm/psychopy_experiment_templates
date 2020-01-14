#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################################
## 
## This script presents words from a user-specified file.
## Number of repetitions is specified (and blocked). 
## Words within a block are randomized.
## Output file includes word info and timestamp.
## Recommended to use non-fullscreen version for testing.
## Change to FullScreen = T for full screen. 
## Escape will exit the experiment. 
## 
## Jessamyn Schertz
## March 15, 2017
##
##-------------------------------
##
## Edited to add:
##    - arabic_reshaper (31, 115-118) - reshapes indiv Urdu letters properly
##    - bidi/algorithm (32, 115-118) - reverses order of reshaped Urdu letters
##    - practice text block (37, 54, 68-70, 102-105)
## 
## Anna Lyashenko
## June 2018
##
## Edited to add 10 extra lines to the output because of cut-off output text
## 
## J Schertz
## July 2018
##
#################################

from psychopy import visual, core, event, gui
import random, time, codecs
import arabic_reshaper
from bidi import algorithm

expInfo = {'Participant':'000',
  'Repetitions':'2',
  'Filename':'hindi_urdu_wordlist.txt',
  'Practice':'practice_list.txt',
  'Language':'Urdu',
  'FullScreen': 'F'
}

dateStr = time.strftime("%b_%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(dictionary=expInfo, title='The Experiment', fixed=[dateStr])
if dlg.OK:
    print dateStr
    clock = core.Clock()
else:
    core.quit()

sub = expInfo['Participant']
fileName = sub + "_" + dateStr
num_blocks = int(expInfo['Repetitions'])
wordlist = expInfo['Filename']
practice = expInfo['Practice']
fullScreen = expInfo['FullScreen']
lang = expInfo['Language']

#create text file to save data
dataFile = codecs.open('results/'+fileName+'.csv', 'w', 'utf-8')

#compile list of stimuli (randomized)
fi = codecs.open(wordlist, 'r', 'utf-8')
lines = fi.readlines()
header = lines[0].strip()
stim = lines[1:]
dataFile.write('sub\tlang\ttrial\tblock\ttime\t'+header+'\n')

#set up practice words (not randomized)
practice_fi = codecs.open(practice, 'r', 'utf-8')
p = practice_fi.readlines()

#Create window, give instructions
if fullScreen != 'T':
  win = visual.Window([1200, 800], color=1)
else: 
  win = visual.Window(fullscr=True, color = 1)
message = visual.TextStim(win, wrapWidth=2, height=0.15, pos=(0,0.4), color=-1, alignHoriz="center")
message2 = visual.TextStim(win, wrapWidth=2, height=0.15, pos=(0,0), color=-1, alignHoriz="center")
message3 = visual.TextStim(win, wrapWidth=2, height=0.15, pos=(0,-0.4), color=-1, alignHoriz="center")
message.setAutoDraw(True)
message2.setAutoDraw(True)
message3.setAutoDraw(True)

message.setText('Instructions:')
message2.setText('Please read the words on the screen.')
message3.setText('Press any key to begin.')
win.flip()
event.waitKeys()

# Loop through blocks
block = 1
trial = 1
while block <= num_blocks:
    message.setText("Block " + str(block) + " of "+str(num_blocks)+": Press any key to begin.")
    message2.setText("")
    message3.setText("")
    win.flip()
    event.waitKeys()
    
    random.shuffle(stim, random.random)
    
    # adding practice words to start of shuffled list:
    if block == 1:
        for word in p:
            stim.insert(0, word)
        
    for word in stim:
        wordInfo1 = word.strip()
        wordInfo = wordInfo1.split('\t')
        time = str(clock.getTime())
        
        transcription = wordInfo[0]
        romanization = wordInfo[1]
        urdu_orth = wordInfo[2]
        # reshape urdu orthography vv
        urdu_orth = arabic_reshaper.reshape(urdu_orth)
        urdu_orth = algorithm.get_display(urdu_orth)
        # reshape urdu orthography ^^
        hindi_orth = wordInfo[3]
        eng_gloss = wordInfo[4]
        phone = wordInfo[5]
        
        if lang[0].lower()=="h": 
            orth = hindi_orth
        elif lang[0].lower()=="u":
            orth = urdu_orth
        else:
            print "Language must be Hindi or Urdu."
            core.quit()
        
        message.setText(romanization) 
        message2.setText(orth) 
        message3.setText(eng_gloss) 
        win.flip()
        pressed = event.waitKeys()
        if "escape" in pressed:
            core.quit()
        dataFile.write(sub+'\t'+lang+'\t'+str(trial)+'\t'+str(block)+'\t'+str(time)+'\t'+wordInfo1+'\n')
        pressed = event.getKeys(keyList="escape")
        if pressed=="escape":
            core.quit()
        trial += 1
    block += 1
        

for i in range(0,10):
    dataFile.write('DELETE ME\n')
    
message.setText("That's it - Thanks!")
message2.setText("")
message3.setText("")
win.flip()
event.waitKeys()
