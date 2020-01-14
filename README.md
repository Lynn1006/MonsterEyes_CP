# MonsterEyes_CP
Animated eyes for monster m4sk from adafruit, using circuitpython. 

### Requirements

Libs required : 
* adafruit_st7789
* adafruit_imageload
* adafruit_seesaw
* adafruit_display_shapes

Others requirements:
* CircuitPyithon version **5.0.0 beta 3** (to activate the second display)

### Description

Using roughly the same method as [the original M4_Eyes coded in C](https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/master/M4_Eyes) to apply textures to iris and sclera.
no 3d render, no blinking (yet ?) and iris movement is a little jerky.
BMP images must be 8bits or 256 colors (better).

### Known issues

* Making the sclera move make animation terribly slow and eyes are not sync.
* Memory error randomly raised


