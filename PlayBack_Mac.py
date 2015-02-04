import random
import os
os.environ['PYGLET_SHADOW_WINDOW']="0"
import pylablib

experiment = pylablib.experiment.Experiment()
experiment.fullscreen()

#Set keyboard as one of the ways a user interacts with the script
experiment.inputs.add(pylablib.input.Keyboard())
#Makes the mouse invisible
experiment.window.set_mouse_visible(False)


#
# USER SETTINGS:
#
ssf_file = 'Playback-short.ssf'
subject = "Pilot3"



#
(x, y) = experiment.screen.center()
#
#Load all the necessary, non-trial-specific stuff:
instruct1 = 'resources/Playback_inst.jpg'
response_cue = 'resources/Playback_prompt.jpg'
break1 = 'resources/Playback_br1.jpg'
break2 = 'resources/Playback_br2.jpg'
break3 = 'resources/Playback_br3.jpg'
end = 'resources/Playback_end.jpg'


#Run settings
font_size = 24
randomize = True

isi_time = 0750
iti_time = 0750
inst_time = 30000
break_time = 120000
#Note: break_time equals 2 minutes (120,000 ms)


#Make it set things up to actually run (SSF, log file)
ssf_path = os.path.join("resources", ssf_file)
ssf = pylablib.stimulus.SSF(ssf_path)

log_file = "%s_playback.log" % (subject)
log_file = os.path.join('output', log_file)
log = file(log_file, 'w+')

#Creates headers for the log file
header = [ "subject#", "pair#", "repetition", "trial#", "user_resp","Ep1_AvB","RT","stimA","Ep1_stim","PRTV_stim", "talker" ,"comp_type","sentence","gender","S-type"]
log.write(','.join(header) + '\n')


#(midx, midy) = experiment.screen.center()
(w, h) = experiment.screen.dimensions()


#
#Set up the big SSF file with two randomized run throughs of the full SSF
#
master_list = []

ssf_rep1 = ssf[:]
ssf_rep2 = ssf[:]

trial = 1

if randomize:
    random.shuffle(ssf_rep1)
    random.shuffle(ssf_rep2)

rep_no = 1
for row in ssf_rep1:
    master_list.append( [ row, trial, rep_no ] )
    trial += 1
    
rep_no = 2
for row in ssf_rep2:
    master_list.append( [ row, trial, rep_no ] )
    trial += 1










#
#This shows instructions and two practice trials, with no recording of speech or responses
#
#It loads an image containing the instructions and centers it on the center of the screen
#
inst_text1 = pylablib.stimulus.Image(instruct1, x=x, y=y)
inst_text1.x = x - (inst_text1.w / 2)
inst_text1.y = y - (inst_text1.h / 2)

x=inst_text1.x
y=inst_text1.y

#This loads the file so that it is ready to be displayed on the screen
experiment.screen.add(inst_text1)

#This displays the loaded screen
experiment.update()    

#If uncommented, this would be the set time for instructions to show, regardless of user response.
#experiment.timer.wait(inst_time)
#This allows the user to cut the instructions time short by pressing "down" on their keyboard
experiment.timer.start()
while (experiment.response != 'DOWN') and (experiment.timer.check() < inst_time):
    experiment.timer.wait(1)
    #clear out any other key presses:
    if experiment.response != 'DOWN':
        experiment.response = ''
    
#This clears the experiment.response variable
experiment.response = ''

#Loads a clear screen, then displays that (blank) screen for the allotted inter-trial interval
experiment.screen.clear()
experiment.update()
experiment.timer.wait(iti_time)









#RUN!

count = 0
prompt = pylablib.stimulus.Image(response_cue, x=x, y=y)
break_1 = pylablib.stimulus.Image(break1, x=x, y=y)
break_2 = pylablib.stimulus.Image(break2, x=x, y=y)
break_3 = pylablib.stimulus.Image(break3, x=x, y=y)

while len(master_list):
    row, trial, rep_no = master_list.pop(0)
    
    if random.randint(0,1) == 0:
        stimA = row[0]
        stimB = row[1]
        baseline_is = "A"
    else:
#    elif random.randint(0,1) == 1:
        stimB = row[0]
        stimA = row[1]
        baseline_is = "B"
    
    sound_a = ''
    sound_a = pylablib.stimulus.QTSound()
    sound_a.load(stimA, preload=True)
#    sound_a = pylablib.stimulus.Sound(stimA)
     
    sound_b = ''
    sound_b = pylablib.stimulus.QTSound()
    sound_b.load(stimB, preload=True)
#    sound_b = pylablib.stimulus.Sound(stimB)
    experiment.update()
    
    sound_a.play()
    sound_a.wait(experiment)
#    sound_a.wait()
#    experiment.update()
    
    experiment.timer.wait(isi_time)
    
    sound_b.play()
    sound_b.wait(experiment)
#    sound_b.wait()
#    experiment.update()
    
    experiment.screen.add(prompt)
    experiment.timer.start()
    experiment.update()
    experiment.inputs.add(pylablib.input.Keyboard())
    
    while not experiment.response in ["S", "K"]:
        experiment.response = ''
        experiment.update()
        experiment.timer.wait(1)

    RT = experiment.timer.check()
    del sound_a
    del sound_b
    stimulus_number = ssf.index(row) + 1
    
    results =  [ str(subject), str(stimulus_number), str(rep_no), str(trial), experiment.response, str(baseline_is), str(RT), str(stimA) ]
    results.extend(row)
    log.write(','.join(results) + '\n')
    
    experiment.response = ''
    
    experiment.screen.clear()
    experiment.update()
    experiment.inputs.add(pylablib.input.Keyboard(False))
    
    experiment.timer.wait(iti_time)


    # Breaks at one-quarter intervals (3 breaks)
    if count == 72:
        experiment.screen.add(break_1)
        experiment.update()
        experiment.timer.start()
        while (experiment.response != 'DOWN') and (experiment.timer.check() < break_time):
            experiment.timer.wait(1)
        
        #Clears the response variable, blanks the screen and waits to start experimental trials
        experiment.response = ''
        experiment.screen.clear()
        experiment.update()
        experiment.timer.wait(iti_time)
        
    if count == 144:
        experiment.screen.add(break_2)
        experiment.update()
        experiment.timer.start()
        while (experiment.response != 'DOWN') and (experiment.timer.check() < break_time):
            experiment.timer.wait(1)
        
        #Clears the response variable, blanks the screen and waits to start experimental trials
        experiment.response = ''
        experiment.screen.clear()
        experiment.update()
        experiment.timer.wait(iti_time)
        
    if count == 216:
        experiment.screen.add(break_3)
        experiment.update()
        experiment.timer.start()
        while (experiment.response != 'DOWN') and (experiment.timer.check() < break_time):
            experiment.timer.wait(1)
        
        #Clears the response variable, blanks the screen and waits to start experimental trials
        experiment.response = ''
        experiment.screen.clear()
        experiment.update()
        experiment.timer.wait(iti_time)
        
         
    count += 1
    
    
    
    

log.close()






#Tells the subject they've finished with this part of the experiment
end_text = pylablib.stimulus.Image(end, x=x, y=y)
experiment.screen.add(end_text)
experiment.update()
experiment.inputs.add(pylablib.input.Keyboard())
experiment.timer.start()
while (experiment.response != 'DOWN') and (experiment.timer.check() < inst_time):
    experiment.timer.wait(1)
    #clear out any other key presses:
    if experiment.response != 'DOWN':
        experiment.response = ''
    
    
#Clears the response variable, blanks the screen and waits to start experimental trials
experiment.response = ''
experiment.screen.clear()
experiment.update()
#experiment.timer.wait(iti_time)

experiment.window.close()


