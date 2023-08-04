# Omicron-Bot
This is a first-of-its-kind PixelPlace bot that can imitate a human. The bot works by differing the width of lines based on random numbers and simplex noise. The bot also allows the user to change parameters such as the speed of pixels, the percent of pixels that will be left as holes, variation in thickness and speed, as well line offset. Below is a demonstration of various combinations of the settings the bot provides.

![image](https://github.com/Omnislayer77/Omicron-Bot/assets/35577982/096f0385-800e-4583-8f37-7ab85cb69c2a)


# How To Install
1. Install Python3 if you do not already have it
2. Clone this repository `git clone https://github.com/Omnislayer77/Omicron-Bot.git`
3. Go into the directory and run `pip install -r requirements.txt`
4. To start the bot, run `python main.py`

# How To Use
The bot currently allows you to set eight parameters 
1. Line Width - This is the base width of the wall, it will be altered by some of the variables below
2. Width Variation Factor - This is a percent of Line Width, and will be multiplied by a noise function to add variation to the width of the wall
3. Width Variation Constant - This is a constant, not a percent, that will be multiplied by the noise function and added to the width
4. Line Offset - This is how much the lines can be offset, left or right, from the center of the wall. Setting this to 0 will make walls perfectly symmetrical  
5. Hole Percentage - This is the percentage of pixels the bot will skip while placing, meant to mimic humans skipping pixels when they move too fast
6. Zoom - This is the scale factor, keep it the same as on PixelPlace. Must be a whole number.
7. Speed - Speed of the bot in px/s
8. Speed Variation - Will be multiplied by a noise function and per pixel added to speed to add variation in the placement speed.

Once you want to start the bot, go to Pixelplace and make sure the zoom is the same as you have it set in the bot (must be a whole number). Put your mouse over the top left of where you want to start walling and press X. Once you want it to stop, press X again and the bot will pause. It's best to experiment with these settings on a private canvas or 7 to get a feel for how the bot works before using it somewhere you care about.


NOTE: You and only you are responsible if you misuse this bot. You have been warned.


