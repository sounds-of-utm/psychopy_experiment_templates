#################################
## 
## This script presents words from a user-specified file.
## Number of repetitions is specified (and blocked). 
## Words within a block are randomized.
## Output file includes word and timestamp.
## Recommended to use non-fullscreen version for testing.
## Change to FullScreen = T for full screen. 
## Escape will exit the experiment. 
## 
## Jessamyn Schertz
## March 15, 2017
##
#################################

from psychopy import visual, core, event, gui
import random, time

expInfo = {'Participant':'000',  
  'Repetitions':'1',
  'Filename':'wordlist.txt',
  'FullScreen': 'F'
}
dateStr = time.strftime("%b_%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(dictionary=expInfo, title='The Experiment', fixed=[dateStr])
if dlg.OK:
    print dateStr
    clock = core.Clock()
else:
    core.quit()

#create text file to save data
fileName = expInfo['Participant'] + "_" + dateStr
num_blocks = int(expInfo['Repetitions'])
wordlist = expInfo['Filename']
fullScreen = expInfo['FullScreen']

dataFile = open('results/'+fileName+'.txt', 'w')
dataFile.write('word\ttime\n')  

#compile list of stimuli (randomized)
fi = open(wordlist, 'r')
stim = fi.readlines()
        
#Create window, give instructions
if fullScreen != 'T':
  win = visual.Window([1400, 800], pos=(0,10), color=1)
else: 
  win = visual.Window(fullscr=True, color = 1)
mouse = event.Mouse()
message = visual.TextStim(win, wrapWidth=1.3, height=0.1, color=-1)
message1 = visual.TextStim(win, wrapWidth=1.3, height=0.1, color=(1,0,0))
message.setAutoDraw(True)

message.setText('Instructions:\n\n Please read the words on the screen.')
win.flip()
event.waitKeys()

block = 1
while block <= num_blocks:
    message.setText("Block " + str(block) + ": Press any key to begin.")
    message.draw()
    win.flip()
    event.waitKeys()
    random.shuffle(stim, random.random)
    for word in stim:
        print word
        word = word.strip()
        time = str(clock.getTime())
        message.setText(word) 
        message.draw()
        win.flip()
        pressed = event.waitKeys()
        if "escape" in pressed:
            core.quit()
        dataFile.write(word+'\t'+time+'\n')
        pressed = event.getKeys(keyList="escape")
        if pressed=="escape":
            core.quit()
    block += 1
        

message.setText("That's it - Thanks!")
win.flip()
event.waitKeys()