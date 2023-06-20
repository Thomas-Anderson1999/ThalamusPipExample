# Thalamus DLL Test code - Window / Linux
 - Tested in window 10 64bit / Ubuntu 20.
 - Downlaod  Simul3DDLL.dll, freeglut.dll, opencv_world450d.dll / thalamus.so
 - from https://drive.google.com/drive/folders/1JN-bPuIM96y6vYkXszekqJNGTuY8BF_5?usp=sharing
 - Script.txt : three objects
 ![Script.txt](Readme_data/01.png) 
 - ScriptFreeModel.txt : one free model 
 - Depth Pnt : depth map from depth cam

# Intallation
## Linux
  - pip install -r requirements.txt
## window 

# Excute on Linux
 - python3 -m venv venv 
 - source venv/bin/activate
 - python3 main.py

# Excute on Window
 - virtualenv venv 
 - venv/script/activate.bat
 - python3 main.py