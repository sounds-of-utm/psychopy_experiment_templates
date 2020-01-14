       #!/usr/bin/env python
#-- coding: UTF-8 --

#################################
## 
## This script presents a binary forced-choice experiment 
## for the Hindi/Urdu stop contrasts.
## User can set number of repetitions, which will be in different blocks.  
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
## July 8, 2018: Edited to add 10 extra lines to the output because of cut-off output text
## 
##
#################################

from psychopy import visual, core, event, gui, prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import sound
import random, time, sys, os

global block
global trial
global numBlocks


##### USER INPUT #####

if sys.platform[:3] == "win":
    slash = "\\"
else:
    slash = "/"

cwd = os.getcwd()

homedir = ""
stimdir = homedir+"stim" + slash
play = 1

# input = key or mouse
input = 'mouse'

b_key = '1'
bh_key = '2'
p_key = '3'
ph_key = '4'

######################

expInfo = {'Participant':'000', 'FullScr':'F'}
# include num_blocks
dateStr = time.strftime("%b_%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(dictionary=expInfo, title='The Experiment', fixed=[dateStr])
if dlg.OK:
    print dateStr
    clock = core.Clock()
else:
    core.quit()

#create text files to save data
fileName = expInfo['Participant']+"_" + dateStr
dataFile = open('results'+slash + fileName+'.txt', 'w')
dataFile.write('sub\ttrial\tfile\tbase\tvc\tvot\tf0\tchoice\n')

##### CATEGORIZATION #####
def categorization(subStimdir):
    global trial
    global block
    #compile lists of stimuli (randomized)
    
    flag = 0
    choice= "NA"
    stim = []
    files = os.listdir(stimdir)
    for file in files:
        if file[-4:] == ".wav" and file[0] != ".":
            stim.append(file)
    random.shuffle(stim)
            
    num_stim = len(stim)
    count = 1
    message.setText("Block " + str(block))
    message2.setText("Press any key to begin")
    win.flip()
    event.waitKeys()    
    
    for element in screen_elements:
        element.setAutoDraw(True)

    for word in stim:
        if flag == 1:
            flag = 0
            break
        parts = word.split('_')
        base = parts[0]
        vc = parts[1]
        vot = parts[2]
        f0 = parts[3][:-4]
        
        if input=='key':
            message.setText('Choose between b, bh, p, ph')
        else:
            message.setText('')
            
        message2.setText("Block "+ str(block) + " of " + str(numBlocks)+" -- Trial " + str(count) + " of " + str(len(stim)))
        win.flip()
        
        # Play sound
        choice = ''
        wav = sound.Sound(value=stimdir+word, sampleRate=44100)
        dur = wav.getDuration()
        wav.play()
        core.wait(dur)
        
        if input == 'key':
            allKeys = event.waitKeys(keyList=[b_key, bh_key, p_key, ph_key,'escape','1'])
            for key in allKeys:
                if key ==b_key:
                    choice="b"
                elif key==bh_key:
                    choice="bh"
                elif key==p_key:
                    choice="p"
                elif key==ph_key:
                    choice="ph"
                elif key=="escape":
                    core.quit()
                elif key == "1":
                    flag = 1
        elif input == 'mouse':
            key = "0"
            while choice == '':
                in_shape = 0
                mouse.getPos()
                mouseClock.reset()
                if mouse.getPressed()[0]==1:
                    rt = mouseClock.getTime()
                    if bshape.contains(mouse):
                        choice = 'b'
                    elif bhshape.contains(mouse):
                        choice = 'bh'
                    elif pshape.contains(mouse):
                        choice = 'p'
                    elif phshape.contains(mouse):
                        choice = 'ph'
            allKeys = event.getKeys(keyList=['escape','1'])
            for key in allKeys:
                if key == "escape":
                    core.quit()
    
        
        dataFile.write(expInfo['Participant'] + '\t' + str(trial) + '\t' + word+'\t'+base+'\t'+vc+'\t'+vot+'\t' + f0+'\t'+choice+'\n')
        core.wait(0.5)
        count += 1
        trial += 1
    message2.setText("")
    message.setText("")
    win.flip()
    block += 1
    
    

if expInfo['FullScr']=="T":
    win = visual.Window(fullscr=True, color = 1)
else:
    win = visual.Window(size=(1000, 600), color = 1)
    
mouse = event.Mouse()
mouse.getPos()
mouseClock = core.Clock()
    
bshape = visual.Rect(win=win, name='bshape',
    width=[0.5, 0.5][0], height=[0.4, 0.4][1],
    pos=[-.4, .25], lineWidth=1, lineColor=-1, opacity=.2)
bword = visual.TextStim(win, pos=(-.4, .25), height=0.2, color=-1)
bword.setText('b')
bhshape = visual.Rect(win=win, name='bhshape',
    width=[0.5, 0.5][0], height=[0.4, 0.4][1],
    pos=[.4, .25], lineWidth=1, lineColor=-1, opacity=.2)
bhword = visual.TextStim(win, pos=(.4, .25), height=0.2, color=-1)
bhword.setText('bh')

pshape = visual.Rect(win=win, name='pshape',
    width=[0.5, 0.5][0], height=[0.4, 0.4][1],
    pos=[-.4, -.25], lineWidth=1, lineColor=-1, opacity=.2)
pword = visual.TextStim(win, pos=(-.4, -.25), height=0.2, color=-1)
pword.setText('p')
phshape = visual.Rect(win=win, name='phshape',
    width=[0.5, 0.5][0], height=[0.4, 0.4][1],
    pos=[.4, -.25], lineWidth=1, lineColor=-1, opacity=.2)
phword = visual.TextStim(win, pos=(.4, -.25), height=0.2, color=-1)
phword.setText('ph')



screen_elements = [bshape, bhshape, pshape, phshape, bword, bhword, pword, phword]



message = visual.TextStim(win, wrapWidth=1.3, height=0.1, color=-1)
message.setAutoDraw(True)
message.setText("You will hear the following sentence: \n\n Didi _a boliye.\n\nYou will hear one of the following syllables in the middle of the sentence: \n\n  'ba', 'bha', 'pa', or 'pha'." )

message2 = visual.TextStim(win, pos=(0,-.6), wrapWidth=1.3, height=0.1, color=-1)
message2.setText("Press any key to continue.")
message2.setAutoDraw(True)
win.flip()
event.waitKeys()

message.setText("Please click on the letter(s) corresponding to the syllable that you hear.")
message2.setText("Press any key to begin.")


trial = 1
block = 1

numBlocks = 3

for block in range(1, numBlocks+1):
    categorization(stimdir)

for i in range(0,10):
    dataFile.write('DELETE ME\n')

message.setText("Thank you!")
win.flip()
event.waitKeys()
