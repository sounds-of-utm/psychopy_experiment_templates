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

def read_words_exp():
    """Presents words from a specific file to the user to read."""
    exp_info = {'Participant':'000',
               'Repetitions':'1',
               'Filename':'wordlist.txt',
               'FullScreen': 'F'
              }
    date_str = time.strftime("%b_%d_%H%M", time.localtime())
    dlg = gui.DlgFromDict(dictionary=exp_info, title='The Experiment', fixed=[date_str])
    if dlg.OK:
        print(date_str)
        clock = core.Clock()
    else:
        core.quit()

    #create text file to save data
    fileName = exp_info['Participant'] + "_" + date_str
    num_blocks = int(exp_info['Repetitions'])
    wordlist = exp_info['Filename']
    fullScreen = exp_info['FullScreen']

    dataFile = open('results/'+fileName+'.txt', 'w')
    dataFile.write('word\ttime\n')

    #compile list of stimuli (randomized)
    fi = open(wordlist, 'r')
    stim = fi.readlines()


    # TODO: Make window size 'responsive'
    #Create window, give instructions
    if fullScreen != 'T':
      win = visual.Window([900, 600], pos=(0,10), color=1) #original: 1400, 800
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
            print(word)
            word = word.strip()
            time_var = str(clock.getTime())
            message.setText(word)
            message.draw()
            win.flip()
            pressed = event.waitKeys()
            if "escape" in pressed:
                core.quit()
            dataFile.write(word+'\t'+time_var+'\n')
            pressed = event.getKeys(keyList="escape")
            if pressed=="escape":
                core.quit()
        block += 1


    message.setText("That's it - Thanks!")
    win.flip()
    event.waitKeys()


if __name__ == "__main__":
    read_words_exp()