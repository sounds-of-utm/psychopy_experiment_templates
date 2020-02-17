#!/usr/bin/env python
#-- coding: UTF-8 --

#################################
## 
## This script presents a binary forced-choice experiment.
## User can set number of repetitions. Each rep will form a new block.  
## Stimuli within each block are randomized.
## Output file includes stimulus, choice, and timestamp.
## Recommended to use non-fullscreen version for testing.
## Change to FullScreen = T for full screen. 
## Escape will exit the experiment. 
##
## Using audio library 'pygame' instead of default 'pyo' 
## because there are issues with my current version of pyo and Mac OS. 
## Can delete line starting with prefs.general if you prefer to use pyo. 
## 
## Jessamyn Schertz
## March 22, 2017
##
#################################

from psychopy import visual, core, event, gui, prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import sound
import random, time, sys, os

global trial, block


##### USER INPUT #####

if sys.platform[:3] == "win":
    slash = "\\"
else:
    slash = "/"

cwd = os.getcwd()

# these are the choices that will be displayed
choice1_text = 'pa'
choice2_text = 'ba'

input = 'mouse'

# iti = inter-trial interval, the duration of time between trials
iti = 0.5

homedir = ""
stimdir = homedir+"stim" + slash
play = 1

######################

exp_info = {'Participant':'000', 'FullScr':'F', 'Repetitions':'2'}
# include num_blocks
date_str = time.strftime("%b_%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(dictionary=exp_info, title='The Experiment', fixed=[date_str])
if dlg.OK:
    print(date_str)
    clock = core.Clock()
    rt_clock = core.Clock()
else:
    core.quit()

#create text files to save data
fileName = exp_info['Participant']+"_" + date_str
dataFile_cat = open('results'+slash + fileName+'.txt', 'w')
dataFile_cat.write('sub\ttrial\tfile\tchoice\trt\n')

reps = int(exp_info['Repetitions'])


##### CATEGORIZATION #####
def categorization(stimdir, block):
    global trial
    #compile lists of stimuli (randomized)
    # choice= "NA"
    stim = []
    files = os.listdir(stimdir)
    for file in files:
        if file[-4:] == ".wav" and file[0] != ".":
            stim.append(file)
    # num_stim = len(stim)
    count = 1
    message.setText("Block " + str(block))
    message.pos = (0.7, -0.2)
    message2 = visual.TextStim(win, pos=(0.7, -0.4), wrapWidth=1.3, height=0.1, color=-1)
    message2.setText("Press any key to begin")
    message2.setAutoDraw(True)
    win.flip()
    event.waitKeys()
    random.shuffle(stim)

    message.setText('')
    win.flip()
    for word in stim:
        message2.setText("Block "+ str(block) + "-- Trial " + str(count) + " of " + str(len(stim)))
        win.flip()
        screen_elements['bshape'].draw()
        screen_elements['bword'].draw()
        screen_elements['pshape'].draw()
        screen_elements['pword'].draw()
        win.flip()

        choice = ''
        wav = sound.Sound(value=stimdir+word, sampleRate=44100)
        rt_clock.reset()
        dur = wav.getDuration()
        wav.play()
        core.wait(dur)

        if input == 'mouse':
            while choice == '':
                allKeys = event.getKeys(keyList=['escape'])
                for key in allKeys:
                    if "escape" in key:
                        core.quit()
                mouse.getPos()
                mouseClock.reset()
                if mouse.getPressed()[0] == 1:
                    rt = mouseClock.getTime()
                    if bshape.contains(mouse):
                        choice = 'ba'
                    elif pshape.contains(mouse):
                        choice = 'pa'
        screen_elements['bshape'].draw()
        screen_elements['bword'].draw()
        screen_elements['pshape'].draw()
        screen_elements['pword'].draw()
        win.flip()

        dataFile_cat.write(exp_info['Participant'] + '\t' + str(trial) + '\t' + word+'\t' + choice +'\t'+str(rt)+'\n')
        core.wait(iti)
        count += 1
        trial += 1
    message2.setText("")
    message.setText("")
    win.flip()
    block += 1


if exp_info['FullScr']=="T":
    win = visual.Window(fullscr=True, color = 1)
else:
    win = visual.Window(size=(1000, 600), color = 1)

mouse = event.Mouse()
mouse.getPos()
mouseClock = core.Clock()

bshape = visual.Rect(win=win, name='bshape',
                     width=[0.5, 0.7][0], height=[0.4, 0.4][1],
                     pos=[-0.4, 0.2], lineWidth=1, lineColor=-1, opacity=.2)
bword = visual.TextStim(win, pos=(0.5, 0.2), height=0.2, color=-1)
bword.setText('ba')


pshape = visual.Rect(win=win, name='pshape',
                     width=[0.5, 0.5][0], height=[0.4, 0.4][1],
                     pos=[0.2, 0.2], lineWidth=1, lineColor=-1, opacity=.2)
pword = visual.TextStim(win, pos=(1.1, 0.2), height=0.2, color=-1)
pword.setText('pa')

screen_elements = {'bshape': bshape, 'pshape': pshape, 'bword': bword, 'pword': pword}

message = visual.TextStim(win, wrapWidth=1.3, height=0.1, color=-1, pos=(0.7, 0))
message.setAutoDraw(True)
message.setText("Please click " + choice1_text + " or " + choice2_text + " to indicate what you heard.")
win.flip()
event.waitKeys()

global block
global trial
trial = 1
for i in range(1, reps + 1):
    categorization(stimdir, i)

message.setText("Thank you!")
win.flip()
event.waitKeys()






