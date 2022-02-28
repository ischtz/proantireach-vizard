# vexptoolbox: Vizard Toolbox for Behavioral Experiments
# Example Task: Pro-/Anti-Reach Experiment
# 
# Immo Schuetz, 2021-22
# immo.schuetz@psychol.uni-giessen.de

# This version of the experiment illustrates how the experimental 
# design and parameters can be specified within the script file. 
# See *pro_anti_reach.py* for an example of how these settings can
# be dynamically loaded from external files instead.

import viz
import vizfx
import viztask
import vizshape
import vizproximity

import steamvr

import vexptoolbox as vx

# Set experiment configuration parameters using a dictionary
myconfig = {'fix_delay': 1,
            'tar_size':  0.05,
            'use_eyetracker': False,
            'pro_color': [0, 0, 0.9],
            'anti_color': [0.9, 0, 0],
            'text_color': [0.9, 0.9, 0.9],
            'repetitions': 10,
            'environment': 'ground_wood.osgb',
            'controller': 0,
            'tar_dist': 0.5,
            'go_delay': 1}

# Instructions for participants
instructions = """
Welcome to our example pro/anti reach experiment!

On each trial, please fixate the white sphere until it turns red or blue. A target cube will appear either left or right of the sphere, and the color indicates whether you should reach towards the cube (blue) or opposite of the cube (red) using your controller. Please wait until the cube and sphere disappear before starting the movement!

This example experiment presents 80 trials and should not take longer than five minutes to complete. 

Note: If you have enabled eye tracking, an eye tracker calibration will be performed before the start of the main experiment. 

Press the controller trigger to start!
"""

# Initialize the experiment with the provided config 
# To save data automatically after each trial, set auto_save=True below.
ex = vx.Experiment(name='Example', config=myconfig, debug=True, auto_save=False)

# Note: To access or change config parameters later, be sure to always access the
# Experiment's 'config' attribute, not the 'myconfig' dictionary used to create it!
print(ex.config)

# To enable eye tracking, uncomment the following or modify the 'myconfig' dict:
# ex.config.use_eyetracker = True

# Create our trial design by specifying a dict of factors (conditions) and their levels
design = {'target': ['left', 'right'],
          'pro': [0, 1],
          'feedback': [0, 1]}

# Now build the trial list by repeating this design. Factor levels are
# added to each trial's 'params' automatically
ex.addTrialsFullFactorial(levels=design, repeat=ex.config.repetitions)

# Randomize trials
ex.randomizeTrials()

# Enable the SteamVR debugger feature - toggle with F12 key
ex.addSteamVRDebugOverlay()


# Initialize Vizard and the VR hardware
viz.setMultiSample(4)
viz.go(viz.FULLSCREEN)

# Note: SteamVR setup can also be done using the following two lines:
# hmd, controllers = vx.steamVREasySetup()
# controller = controllers[0]
hmd = steamvr.HMD()
navigationNode = viz.addGroup()
viewLink = viz.link(navigationNode, viz.MainView)
viewLink.preMultLinkable(hmd.getSensor())
hmd.setMonoMirror(True)

controller = steamvr.getControllerList()[ex.config.controller]
controller.model = controller.addModel(parent=navigationNode)
if not controller.model:
    controller.model = viz.addGroup(parent=navigationNode)
controller.model.disable(viz.INTERSECTION)
viz.link(controller, controller.model)

# Initialize the Vive Pro Eye eye tracker
eyeTracker = None
if ex.config.use_eyetracker:
    # To use a different eye tracker, initialize the corresponding driver here
    # and assign it to 'eye_tracker' or pass it to 'ex.addSampleRecorder' below. 
    VivePro = viz.add('VivePro.dle')
    eyeTracker = VivePro.addEyeTracker()
    if not eyeTracker:
        sys.exit('Eye tracker not detected')

# Set the scene
room = vizfx.addChild(ex.config.environment)

# Stimulus objects
stimuli = vx.ObjectCollection()
stimuli.add(vizshape.addCube(size=ex.config.tar_size, color=viz.WHITE), key='left')
stimuli.add(vizshape.addCube(size=ex.config.tar_size, color=viz.WHITE), key='right')
stimuli.add(vizshape.addSphere(radius=ex.config.tar_size/2, color=viz.WHITE, pos=[0, 1.8, 0]), key='fix')

# Virtual plane to use for gaze intersection (invisible)
gaze_plane = vizshape.addPlane(size=(100.0, 100.0), pos=[0.0, 0.0, ex.config.tar_dist], axis=vizshape.AXIS_Z, 
                               color=viz.RED, alpha=0.0, flipFaces=True)

# Disable intersection cues for all other stimulus objects
# (SampleRecorder automatically tests for gaze intersection with all
# objects that have viz.INTERSECTION turned on and logs the resulting 3d position)
# This ensures that gaze3d positions are recorded on the target plane only
for s in stimuli:
    s.disable(viz.INTERSECTION)


# Enable sample recording, set to also record controller position
ex.addSampleRecorder(eye_tracker=eyeTracker, tracked_nodes={'controller': controller.model})

# Proximity module for reach detection
reach_sensor = vizproximity.Sensor(vizproximity.Box(size=[1.0, 1.0, 0.1], center=[0,0,0]), stimuli.fix)
reach_proximity = vizproximity.Target(controller)
reach_manager = vizproximity.Manager()
reach_manager.addSensor(reach_sensor)
reach_manager.addTarget(reach_proximity)


# Define two Vizard tasks that will run once per trial
# One to set up stimuli before the trial starts...
def TrialSetup(experiment, trial):
    
    # Set up stimuli for this trial
    stimuli.hideAll()
    yield vx.waitVRText('Blue - towards, red - opposite\nPress trigger to start trial!', distance=1.0, 
                         color=experiment.config.text_color, controller=controller)
    trial.results['start_time'] = viz.tick() * 1000.0

    # Show or hide the controller depending on trial parameters
    if trial.params.feedback == 1:
        controller.model.visible(True)
    else:
        controller.model.visible(False)


# ...and one to run the main trial
def TrialTask(experiment, trial):
    
    # Wait for participant fixation        
    stimuli.showOnly('fix', position=[0.0, experiment.config.eyeheight, experiment.config.tar_dist], color=viz.WHITE)        
    if experiment.config.use_eyetracker:
        yield experiment.recorder.waitGazeNearTarget(stimuli.fix.getPosition())

    trial.results['fix_onset_time'] = viz.tick() * 1000.0
    yield viztask.waitTime(experiment.config.fix_delay)

    # Show target and direction cue
    if trial.params.target == 'left':
        stimuli.show('left', position=[-0.3, experiment.config.eyeheight, experiment.config.tar_dist])
    else:
        stimuli.show('right', position=[0.3, experiment.config.eyeheight, experiment.config.tar_dist])

    if trial.params.pro == 1:
        stimuli.fix.color(experiment.config.pro_color)
    else:
        stimuli['fix'].color(experiment.config.anti_color) # Note the alternative syntaxes

    # Wait for reach
    yield viztask.waitTime(experiment.config.go_delay)
    stimuli.hideAll()
    trial.results['go_time'] = viz.tick() * 1000.0
    
    yield vizproximity.waitEnter(reach_sensor)
    trial.results['reach_time'] = viz.tick() * 1000.0
    pos = controller.getPosition(viz.ABS_GLOBAL)
    
    # Trial results
    trial.results['RT'] = trial.results.reach_time - trial.results.go_time
    trial.results['hit_x'] = pos[0]
    trial.results['hit_y'] = pos[1]
    trial.results['hit_z'] = pos[2]
    trial.results['correct'] = False
    if pos[0] >= 0: 
        trial.results['hemifield'] = 'right'
        if trial.params.pro == 1 and trial.params.target == 'right':
            trial.results['correct'] = True
        elif trial.params.pro == 0 and trial.params.target == 'left':
            trial.results['correct'] = True
    else:
        trial.results['hemifield'] = 'left'
        if trial.params.pro == 1 and trial.params.target == 'left':
            trial.results['correct'] = True
        elif trial.params.pro == 0 and trial.params.target == 'right':
            trial.results['correct'] = True


def Main():
    
    # Collect participant number etc
    yield ex.requestParticipantData()
    
    # Show experiment instructions
    yield vx.waitVRInstruction(instructions, controller=controller)

    # Calibrate and validate the eye tracker
    if ex.config.use_eyetracker:
        yield vx.waitVRText('Press trigger to start eye tracker calibration!', distance=1.0, 
                             color=ex.config.text_color, controller=controller)
        yield ex.recorder.calibrateEyeTracker()
        yield ex.recorder.validateEyeTracker(vx.VAL_TAR_CR5)
    
    ex.config.eyeheight = hmd.getSensor().getPosition(viz.ABS_GLOBAL)[1]
    room.visible(True)

    # Experiment trial loop
    yield ex.run(trial_task=TrialTask, 
                 pre_trial_task=TrialSetup)
    yield vx.showVRText('All done! Thank you!', distance=1.0, duration=3.0, color=ex.config.text_color)

    ex.saveExperimentData()
    ex.saveTrialDataToCSV()
    viz.quit()


viztask.schedule(Main)