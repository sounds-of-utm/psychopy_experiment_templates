#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################
## Presents words for reading
##
## - Stimulus list should be a tab-separated text file with one word on each line. 
##   - The first line of this should be a header with column names
##   - The word to be presented should be in the first column
##   - The other columns can be populated with any additional information
##   - Results file will include the subject, language, word, 
##     and all other additional information in the stimulus file.
##
## - User can specify the following within the script:
##   - Random presentation (or not)
##   - Number of reps of entire stimulus set
##   - Number of breaks
##   - Wait time between stimuli (or 0 for user-controlled)
## 
## - Note that timing is delayed when using mouse input mode.
##
## July 15, 2015
## jessamyn.schertz@gmail.com
############################################

from psychopy import visual, core, event, gui, sys, os
import random, time, codecs

lang = 'chi'
stimlist = 'stim_chi_chi.txt'
practice_stimlist = 'stim_chi_practice.txt'
input_mode = 'key'

# Information to be elicited from user {Field: [acceptable_args, default]}.
user_input = {
'participant':[[], '000']
}

expInfo = {}
for arg in user_input.keys():
    expInfo[arg] = user_input[arg][1]

dateStr = time.strftime("%b_%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(dictionary=expInfo, title='User Input', order=['participant'])
     
for arg in user_input.keys():
    if len(user_input[arg][0]):
        if expInfo[arg] not in user_input[arg][0]:
            myDlg = gui.Dlg(title='Error')
            myDlg.addText("Variable '"+arg+"' must come from the following set: " + ', '.join(user_input[arg][0]))
            myDlg.show()
            core.quit()

participant = expInfo['participant']
if participant != "test":
    par_parts = participant.split("_")
    if len(par_parts) != 4:
        myDlg = gui.Dlg(title='Error')
        myDlg.addText("SubjectID must be of the form 'P_1989_F_YHJ'.")
        myDlg.show()
        core.quit()

auto_advance = 'no'
korean_dialect = "none"
fileName = participant + "_expCH1_" + dateStr

## Define language-specific directions

text = {
    'instructions':{
        'eng':'Please read the words on the screen.',
        'kor':u'모니터에 나타나는 문장들을 읽으세요.',
        'chi':u'请大声念出，待会实验中，出现的单词。'
        },
    'continue':{
        'mouse':{
            'eng':'When you are ready, click "continue."',
            'kor':u'준비 되셨으면, “다음”을 눌러 주세요.',
            'chi':u'当您准备好了，请点击“继续”'
             },
        'key':{
            'eng':'Press any key to continue.',
            'kor':u'시작하시려면 키보드를 누르세요.',
            'chi':u'请按任意键到下一部分。'
            },
        'touch':{
            'eng':'When you are ready, tap "continue."',
            'kor':u'준비 되셨으면, “다음”을 눌러 주세요.',
            'chi':u'当您准备好了，请点击“继续”'
            }
        },
    'practice':{
        'eng':'You will start with a short practice session.',
        'kor':u'먼저 짧은 연습 세션입니다.',
        'chi':u'正式实验之前，请先进行几次练习。'
        },
    'block':{
        'eng':'Block',
        'kor':u'세션',
        'chi':'TRANS:BLOCK'
        },
    'practice_block':{
        'eng':'Practice Block',
        'kor':u'연습',
        'chi':''
        },
    'next':{
        'eng':'Next',
        'kor':u'다음',
        'chi':u'继续'
        },
    'break':{
        'eng':'You can take a break now.',
        'kor':'이제 조금 쉬고나서 계속 하겠습니다.',
        'chi':u'您可以稍事休息一下。'
        },
    'end':{
        'eng':'You have reached the end of the experiment.',
        'kor':u'실험이 끝났습니다.',
        'chi':u'实验结束'
        },
    'thanks':{
        'eng':'Thank you for your participation!',
        'kor':u'참여해주셔서 감사합니다!',
        'chi':u'谢谢您的参与！'
        }
}

##### ADMIN FUNCTIONS ####

slash = "/"
if sys.platform[:3] == "win":
    slash = "\\"

homedir = os.getcwd()
resultsdir = homedir + slash + "results" + slash

# Creates text files to save data
dataFile = codecs.open(resultsdir+fileName+'.txt', 'w', 'utf-8')

# Open stimulus file
if lang == "kor":
    fi = codecs.open(stimlist, 'r', 'utf-8')
    fi = fi.readlines()
    for line in fi:
        line = line.strip()
        parts = line.split()
        yb_sen = parts[0]
        yb_word = parts[1]
        pa_sen = parts[0]
        pa_word = parts[1]
    header_line = fi[0].strip()
    stimuli = fi[1:]

else:
    fi = codecs.open(stimlist, 'r', 'utf-8')
    fi = fi.readlines()
    header_line = "sub" + '\t' + fi[0].strip()
    stimuli = fi[1:]

dataFile = codecs.open(resultsdir+fileName+'.txt', 'w', 'utf-8')
header = header_line + '\ttime\n'
dataFile.write(header)

# number of repetitions of stimulus list
num_reps = 3

# number of TOTAL breaks in the experiment
num_breaks = 3

# time to wait between each stimulus (if 0, will not automatically advance)
if auto_advance == 'yes':
    wait_time = 2
else:
    wait_time = 0

# Escape key
escape_key = 'escape'

# Full screen? 
fullscreen = 'T'

def get_response(allowed_keys=[],in_shape=0):
    event.clearEvents()
    mouse.getPos()
    response = ''
    while response == '':
        if input_mode == 'key':
            response = event.waitKeys()
            for key in response:
                if key==escape_key:
                    core.quit()
        elif input_mode == 'touch':
            if mouse.mouseMoved():
                if nextshape.contains(mouse):
                    response = 'done'
        elif input_mode == 'mouse':
            if mouse.getPressed()[0]==1:
                if nextshape.contains(mouse):
                    response = 'done'
            while mouse.getPressed()[0]==1:
                pass
        for key in event.getKeys():
            if key == escape_key:
                core.quit()
                
def read_words(stimlist, reps=1, rand=0, breaks=0):
    global trial
    global count
    global block
    full_stimlist = []
    for i in range(reps):
        if rand == 1:
            random.shuffle(stimlist)
        full_stimlist = full_stimlist + stimlist
    break_points = []
    if breaks > 0:
        num_in_block = int(len(full_stimlist))/int(num_breaks+1)
        counter = 0
        for i in range(num_breaks):
            counter = int(counter + num_in_block)
            break_points.append(counter)
    for line in full_stimlist:
        line = line.strip()
        parts = line.split('\t')
        word = parts[0]
        time = str(clock.getTime())
        message.setText(word)
        message2.setText(str(count) + "/" + str(len(full_stimlist)))
        win.flip()
        iti = 0.3
        if wait_time > 0:
            core.wait(wait_time, hogCPUperiod=wait_time-iti)
        else:
            get_response()
        message.setText("")
        win.flip()
        core.wait(iti)
        if "escape" in event.getKeys():
            core.quit()
        if trial in break_points:
            message.setText(text['break'][lang])
            message2.setText(text['continue'][input_mode][lang])
            win.flip()
            get_response()
            block += 1
        count += 1
        trial += 1
        if block != 0:
            dataFile.write(participant + '\t' + line + '\t' + time + '\n')
        message.setText("")
    block += 1

## SETUP ##################

#Create window, give instructions
if fullscreen == 'T':
    win = visual.Window(fullscr=True, color = 1)
else:
    win = visual.Window([800, 600], color=1)
    
message = visual.TextStim(win, wrapWidth=1.3, pos=(0, .1), font="SimSun", height=0.13, color=-1)
message2 = visual.TextStim(win, wrapWidth=1.3, pos=(0, -0.5), font="SimSun", height=0.13, color=-1)
message.setAutoDraw(True)
message2.setAutoDraw(True)
mouse = event.Mouse()
clock = core.Clock()

if input_mode != 'key':
    nextshape = visual.Rect(win=win, name='mshape',
        width=[0.35, 0.35][0], height=[0.25, 0.25][1],
        pos=[.7, -.7], lineWidth=1, lineColor=-1, opacity=.3)
    nextword = visual.TextStim(win, pos=(.7, -.7), height=0.1, color=-1)
    nextword.setText(text['next'][lang])
    nextshape.setAutoDraw(True)
    nextword.setAutoDraw(True)

message.setText(text['instructions'][lang])
message2.setText(text['continue'][input_mode][lang])
win.flip()
get_response()
message.setText("")
message2.setText("")
win.flip()

## Practice block

if os.path.exists(practice_stimlist):
    fi = codecs.open(practice_stimlist, 'r', 'utf-8')
    practice_stimlist = fi.readlines()[1:]
    message.setText(text['practice'][lang])
    message2.setText(text['continue'][input_mode][lang])
    win.flip()
    get_response()
    block = 0
    count = 1
    trial = 0
    read_words(practice_stimlist, reps=1, rand=0, breaks=0)
    message.setText(text['continue'][input_mode][lang])
    message2.setText("")
    win.flip()
    get_response()
    
## Main experiment block

block = 1
trial = 1
count = 1
read_words(stimuli, reps=2, rand=1, breaks=num_breaks)
if input_mode != "key":
    nextshape.setAutoDraw(False)
    nextword.setAutoDraw(False)
message.setText(text['end'][lang])
message2.setText(text['thanks'][lang])
win.flip()
get_response()
