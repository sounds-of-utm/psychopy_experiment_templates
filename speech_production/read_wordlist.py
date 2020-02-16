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
from PIL import Image
import random, time
import os


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
    # wordlist = exp_info['Filename']
    fullScreen = exp_info['FullScreen']
    dataFile = open('results/'+fileName+'.txt', 'w')
    dataFile.write('image file\ttime\n')

    directory = r"../samples/images"

    #Create window, give instructions
    if fullScreen != 'T':
      win = visual.Window(size=(1400, 800), pos=(0,10), screen=0, color=1)
    else:
      win = visual.Window(fullscr=True, color = 1)
    message = visual.TextStim(win, wrapWidth=1.3, height=0.1, color=-1, pos=(0.7,0))
    message.setAutoDraw(True)

    message.setText('Instructions:\n\n Please take a look at the images on the screen.')
    win.flip()
    event.waitKeys()

    block = 1
    while block <= num_blocks:
        message.setText("Block " + str(block) + ": Press any key to begin.")
        message.draw()
        win.flip()
        message.setText('')  # 'Clear' the previous text
        event.waitKeys()

        # IMAGE
        for i in range(len(os.listdir(directory))):
            win.flip() # clears the sometimes-no-image-appears-after-a-key-is-pressed issue
            img = random.choice(os.listdir(directory)) # randomly select an image in the images directory
            image = Image.open(directory + "/" + img)
            stim = visual.ImageStim(win, image=image)
            # Reduce the size of this image; on a laptop it is too big
            if img == 'monster1.png':
                size_x = stim.size[0]
                size_y = stim.size[1]
                stim.size = [size_x / 2, size_y / 2]
            time_var = str(clock.getTime())
            stim.draw()
            win.flip()
            pressed = event.waitKeys()
            if "escape" in pressed:
                core.quit()
            else:
                dataFile.write(img + '\t' + time_var + '\n')  # writing in the name of the image file i.e. monster3.png
        block += 1

    message.setText("That's it - Thanks!")
    win.flip()
    event.waitKeys()


if __name__ == "__main__":
    read_words_exp()