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

def read_words_exp(filepath: str, fontsize: int, style: str, font='Arial'):
    """Presents words from a specific file to the user to read.
    :param filepath - the path to the .txt file to be used. i.e: ../samples/mandarin_wordlist, ../samples/urdu_wordlist
    :param fontsize - the size of the words in the wordlist .txt file
    :param style - the language style i.e. LTF (left to right), RTL (right to left), Arabic (works with Urdu too).
    :param font - the font to be used for the specific .txt file. Default value is Arial.
        Mandarin requires Songti SC font. Arabic can't use Songti SC font.
    """
    exp_info = {'Participant':'000',
               'Repetitions':'1',
               'Filename':'{}.txt'.format(filepath, font, style),
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

    #Create window, give instructions
    if fullScreen != 'T':
      win = visual.Window([1400, 800], pos=(0,10), color=1)
    else:
      win = visual.Window(fullscr=True, color = 1)
    message = visual.TextStim(win, wrapWidth=1.3, height=0.1, color=-1,
                              pos=(0.7, 0), font='{}'.format(font), languageStyle='{}'.format(style))
    # Songti SC font doesn't crop out Mandarin characters
    # Songti font doesn't work for Urdu; use another font i.e. Arial, Times New Roman, ...
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
            # Change text size
            message.height = fontsize
            message.draw()
            win.flip()
            pressed = event.waitKeys()
            if "escape" in pressed:
                core.quit()
            dataFile.write(word+'\t'+time_var+'\n')
            pressed = event.getKeys(keyList="escape")
            if pressed == "escape":
                core.quit()
        block += 1

    message.setText("That's it - Thanks!")
    message.height = 0.1
    win.flip()
    event.waitKeys()


if __name__ == "__main__":
    # parameters: filepath, fontsize, language style, font name (default: Arial)
    read_words_exp('../samples/urdu_wordlist', 0.4, 'Arabic' )
    # read_words_exp('../samples/mandarin_wordlist', 0.3,  'RTL', 'Songti SC')
    # read_words_exp('../speech_production/wordlist', 0.2, 'RTL')