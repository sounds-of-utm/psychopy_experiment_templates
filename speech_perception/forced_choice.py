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

##### USER INPUT #####

if sys.platform[:3] == "win":
    slash = "\\"
else:
    slash = "/"

cwd = os.getcwd()

# these are the choices that will be displayed
choice1_text = 'pa'
choice2_text = 'ba'

# these are the key options that participants should press (left/right)
key1 = 'f'
key2 = 'j'

# iti = inter-trial interval, the duration of time between trials
iti = 0.5

homedir = ""
stimdir = homedir+"stim" + slash
play = 1

######################

expInfo = {'Participant':'000', 'FullScr':'F', 'Repetitions':'2'}
# include num_blocks
dateStr = time.strftime("%b_%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(dictionary=expInfo, title='The Experiment', fixed=[dateStr])
if dlg.OK:
    print dateStr
    clock = core.Clock()
    rt_clock = core.Clock()
else:
    core.quit()

#create text files to save data
fileName = expInfo['Participant']+"_" + dateStr
dataFile_cat = open('results'+slash + fileName+'.txt', 'w')
dataFile_cat.write('sub\ttrial\tfile\tchoice\trt\n')

reps = int(expInfo['Repetitions'])

##### CATEGORIZATION #####
def categorization(stimdir, block):
    global trial
    #compile lists of stimuli (randomized)
    flag = 0
    choice= "NA"
    stim = []
    files = os.listdir(stimdir)
    for file in files:
        if file[-4:] == ".wav" and file[0] != ".":
            stim.append(file)
    num_stim = len(stim)
    count = 1
    message.setText("Block " + str(block))
    message2 = visual.TextStim(win, pos=(0,-.2), wrapWidth=1.3, height=0.1, color=-1)
    message2.setText("Press any key to begin")
    message2.setAutoDraw(True)
    win.flip()
    event.waitKeys()    
    random.shuffle(stim)
    for word in stim:
        if flag == 1:
            flag = 0
            break
        message.setText(choice1_text + "         -----         " + choice2_text)
        message2.setText("Block "+ str(block) + "-- Trial " + str(count) + " of " + str(len(stim)))
        win.flip()

        wav = sound.Sound(value=stimdir+word, sampleRate=44100)
        rt_clock.reset()
        wav.play()
        keys = event.waitKeys(keyList = [key1,key2,'escape'], timeStamped=rt_clock)
        
        # rt = "response time" 
        rt = keys[0][1]
        choice = keys[0][0]
        if choice =="escape":
            core.quit()
        dataFile_cat.write(expInfo['Participant'] + '\t' + str(trial) + '\t' + word+'\t' +choice+'\t'+str(rt)+'\n')
        core.wait(iti)
        count += 1
        trial += 1
    message2.setText("")
    message.setText("")
    win.flip()

if expInfo['FullScr']=="T":
    win = visual.Window(fullscr=True, color = 1)
else:
    win = visual.Window(size=(1000, 600), color = 1)
message = visual.TextStim(win, wrapWidth=1.3, height=0.1, color=-1)
message.setAutoDraw(True)
message.setText("Please press '" +key1+ "' or '" +key2+ "' to indicate what you heard.")
win.flip()
event.waitKeys()

global block
global trial
trial = 1
for i in range(1, reps+1):
    categorization(stimdir, i)

message.setText("Thank you!")
win.flip()
event.waitKeys()
