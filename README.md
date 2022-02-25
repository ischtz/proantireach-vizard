# Example VR Paradigm: Pro-/Anti-Reach Task

This repository contains the Python code, data, and example analysis for a simple VR goal-directed movement task (pro-/anti-reach task), implemented using WorldViz Vizard and [our upcoming *vexptoolbox* software toolbox](https://github.com/ischtz/vizard-experiment-toolbox) to aid in developing behavioral experiments on the Vizard platform. 

It can serve as a starting point or tutorial for anyone wanting to implement their own experiments, and as documentation of the data format used by vexptoolbox. 



## Experimental Paradigm

In the pro-/anti-reach paradigm, participants perform reaching movements using the controller towards a visually presented target (pro-reach) or to a location in the visual hemifield opposite to the visual target (anti-reach). This task was originally developed for eye movements (pro-/anti-saccade task, [1-2]) and allows to independently manipulate the visual target position and the movement goal. 

In each trial, a *target* (cube) is presented either left or right of the participant's body midline, together with a *movement cue* (blue: move towards the target, red: move towards the opposite hemifield of the target, see also the image below). In the example data presented here, we recorded eye position, controller movement trajectories, movement timing and the behavioral response (i.e., whether the movement went to the correct hemifield).

![task](https://user-images.githubusercontent.com/7711674/155688192-4626ee39-be66-4eda-be02-921071efeb18.png)

*Top: Screenshot of the virtual scene, with target (cube) and movement cue (red = anti-reach). Bottom: Trial sequence. After the initial sphere is fixated for 1s, it changes color to indicate the movement cue (here: red = anti-reach). A target cube is presented simultaneously for 1s, after which the participant performs a reach movement with the controller (gray).*

The example task can be found in the *code* subfolder and requires Vizard and any SteamVR compatible VR headset and controller. It should run fine also on the evaluation or free license tier of Vizard.



## Example Analysis

We recorded data from N=5 volunteers from our lab, which can be found in the *data* folder. Participants gave written informed consent and consented to data publication. An example analysis of the data can be found in [this Jupyter Notebook](analysis/example_analysis.ipynb).

Because this paradigm was meant as an example and the sample size is limited, we did not test any statistical hypotheses regarding the task. The above notebook shows how to extract the result data and plot the resulting timing data and averaged eye and hand movement trajectories below. 

![fig_controller](https://user-images.githubusercontent.com/7711674/139657676-010ef8cf-a6ce-451e-9347-1bad5c0d0a18.png) ![fig_gaze](https://user-images.githubusercontent.com/7711674/139657726-3b4092f7-f732-4cb4-b18a-edf6ad827ff7.png)

*Dynamic behavioral results: Movement trajectories of one volunteer, left: hand (controller), Right: Eye movements during fixation*

![fig_behavioral](https://user-images.githubusercontent.com/7711674/139660632-304d1c73-68f9-4d14-8c11-9830d3969939.png)

*Per-trial results: Movement timing and spatial error across the five tested volunteers*

## Try it Out!

Out of the box, this example only requires a SteamVR compatible headset and an installation of WorldViz Vizard version 6+. 

1. *Install Vizard:* If you do not already have Vizard installed, you can request a free evaluation license from the manufacturers website at https://www.worldviz.com/virtual-reality-software-downloads (free license is limited to five minutes of script runtime, but this is more than enough to run this example). 

2. *Download:* Clone a copy of the *proantireach-vizard* repository using ```git clone https://github.com/ischtz/proantireach-vizard.git``` or download using Github's "Download ZIP" functionality behind the "Code" button (upper right).

3. *Start SteamVR*: For best results, SteamVR should be running and correctly tracking your headset, with the participant near the world origin and facing forward. This experiment also requires at least one active controller. 

4. *(Optional: Enable Eye Tracking)*: Eye tracking support is turned off by default to allow the experiment to run on all SteamVR headsets. It is currently implemented for the Vive Pro Eye HMD. To enable eye tracking, ensure that the SRanipal SDK is running, then set ```"use_eyetracker": true``` in the *config.json* file. Alternatively, you can add the following statement on line 21 of the *pro_anti_reach.py* script without editing the JSON file: 
```ex.config.use_eyetracker = True```

5. *Run*: Open *pro_anti_reach.py* in the Vizard editor and press *F5* or click the "Run script" button to start!

## Citation

**The manuscript accompanying this project is currently being prepared and will be linked here after peer review.**



## References

[1] Medendorp WP, Goltz HC, Vilis T (2005) Remapping the remembered target location for anti-saccades in human posterior parietal cortex. Journal of neurophysiology 94(1):734{740

[2] Munoz DP, Everling S (2004) Look away: the antisaccade task and the voluntary control of eye movement. Nature Reviews Neuroscience 5(3):218{228

