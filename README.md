# StepControl
Python script for controlling two 28BYJ-48 Stepper motors with ULN2003 drivers.

![image](https://cloud.githubusercontent.com/assets/21973290/18392627/77cc0bf4-7680-11e6-8155-6b55b4ac018e.jpeg)

-X axis (yaw) is limited to +-180 degrees from starting point, and is controlled with the A and D keys.

-Y axis (pitch) is limited to +-120 degrees from starting point, and is controlled with the W and S keys.

Features include:

-Stepping motors one step at a time for precise control using W,A,S,D keys.

-Stepping motors in 45 degree increments using I,J,K,L keys.

-Homing the X and Y axis using the H key.

-Recording any of the above movements including any pauses over 2 seconds with the R key, then being able to name and save that recording as a .txt file.

-By typing the recorded file's name as an argument upon launch, you may play back your recording with the 'P' Key.

-The X key is used to exit, and stop a recording.

-If you have access to a 3d printer, this whole project costs about $10 with 28byj-48 stepper motors.

I'm pretty new to this (First github project!) and have only been working with python for a couple months now as a hobby.

Let me know what you think!
