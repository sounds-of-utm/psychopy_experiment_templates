Notes on PsychoPy experiment templates
December 28, 2019

All files available here: https://www.dropbox.com/sh/24b1c126n0fam7x/AAA6UTxnvsaB6vdYs9Ma5emca?dl=0

## OVERALL ##############

There are two general categories of experiments we do: 
1. Speech Production, where people are asked to produce speech (and are recorded)
2. Speech Perception, where people listen to sounds and respond. 

For each of these types of experiments, I've included a "basic version" of a full experiment and all ancillary files. Below, I give a basic description of each type, as well as some other components that would be good to incorporate. Perhaps the best way to go would be to first port the basic version of each to make sure everything works fine in the new version, then work on adding the other components. 

We can see how this goes, and move on to more complex experiments later if things go smoothly. 

Contents of this folder:
- speech_production/: Basic speech production experiment
- speech_perception/: Basic speech perception experiment
- other_exps/: Some other full experiments I have built that include various optional components that I talk about, in case they are useful for reference in how to deal with the optional components. 
- samples/: bits and pieces of things that will be useful or necessary for the optional components. For example, I've included a list of Mandarin Chinese words that should also (eventually) be able to be used in read_wordlist.py instead of the default English wordlist. I reference these below when relevant. 


## SPEECH PRODUCTION EXPERIMENTS ##############

read_wordlist.py

Basic version:
- Words/sentences are presented one at a time.
- Each presentation is one line from a text file. 
- User-advanced via keypress
- Time-stamped output

Optionality I'd like to add:
1. Images: instead of presenting words, display images (no text)
   - sample images in images/
2. Make sure this can support non-Roman text encoding in the wordlist (instead of English)
   - e.g. Chinese characters, and then scripts that are written right-to-left like Urdu or Arabic cause additional problems
   - sample wordlists: mandarin_wordlist.txt, urdu_wordlist.txt
   - Urdu will be the trickiest. We might want to talk about this in person. What it should actually look like is in the file urdu_wordlist.pdf
   - sample experiments I've used this in before (that are a bit more complicated, but in case there are components that are useful): other_exps/hindi_urdu/, other_exps/chinese/ 
   
## SPEECH PERCEPTION EXPERIMENTS ##############
   
forced_choice.py

Basic version:   
- Each experiment trial consists of an audio file being played
- Listener presses a key to indicate what they have heard. 
- Output: timestamp (from the onset of the sound stimulus) and listener choice recorded

Optionality I'd like to add: 
1. Mouse-click instead of keypress: Listeners click a button corresponding to their choice
   - Example in other_exps/click_keypress_option/4cat_perception.py. 
   - This has 4 choices, but you can just make it have 2 choices if that's simpler. 
   - (eventually may want to add touch option as well; I did this before to present experiments on a tablet, but this was in 2015 and I think things have evolved quite a bit since then. We don't do this a lot so this is not a priority - but if it is super easy to add, that could be done as well.)
2. Not-optional, but something that can be done later: make it so that people can't respond until after the sound is finished. 
   
   
   

