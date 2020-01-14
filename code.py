import time
import board

import digitalio
import busio

import gc
#print(gc.mem_alloc(), gc.mem_free())
# accelerometer
#import adafruit_lis3dh

from random import randint

import displayio
from adafruit_st7789 import ST7789

import math
import adafruit_imageload

# usefull for left TFT backlight and access to the buttons
from adafruit_seesaw.seesaw import Seesaw

from adafruit_display_shapes.circle import Circle

i2c = busio.I2C(board.SCL, board.SDA)

# init accelerometer
#int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
#lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x18, int1=int1)

ss = Seesaw(i2c)

# left screen backlight
ss.pin_mode(5, ss.OUTPUT);

# display setup for m4sk

displayio.release_displays()

spi1 = busio.SPI(board.RIGHT_TFT_SCK, MOSI=board.RIGHT_TFT_MOSI)
display1_bus = displayio.FourWire(spi1, command=board.RIGHT_TFT_DC, chip_select=board.RIGHT_TFT_CS, reset=board.RIGHT_TFT_RST)
display1 = ST7789(display1_bus, width=240, height=240, rowstart=80,
                 backlight_pin=board.RIGHT_TFT_LITE)

spi2 = busio.SPI(board.LEFT_TFT_SCK, MOSI=board.LEFT_TFT_MOSI)
display2_bus = displayio.FourWire(spi2, command=board.LEFT_TFT_DC, chip_select=board.LEFT_TFT_CS)
display2 = ST7789(display2_bus, width=240, height=240, rowstart=80)

# left TFT lite on
ss.analog_write(5, 255)

print("Monster Eyes with CircuitPython")
print("by Marius_450")
#filename "/iris9.bmp"

def draw_outlines():
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xffffff
    palette.make_transparent(1)
    bitmap = displayio.Bitmap(240, 240, 2)
    for x in range(0,240):
        for y in range(0,240):
            if (120 - x)**2 + (120 - y)**2 < 118**2:
                bitmap[x,y] = 1
            else:
                bitmap[x,y] = 0
    left_tilegrid = displayio.TileGrid(bitmap, pixel_shader=palette)
    right_tilegrid = displayio.TileGrid(bitmap, pixel_shader=palette)
    return left_tilegrid, right_tilegrid



def sclera_processing(filename):
    start = time.monotonic()
    sclera_texture, sclera_palette = adafruit_imageload.load(filename,
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)
    sclera_bitmap = displayio.Bitmap(120, 120, len(sclera_palette))

    sclera_tilegrid = displayio.TileGrid(sclera_bitmap, pixel_shader=sclera_palette)
    right_sclera_tilegrid = displayio.TileGrid(sclera_bitmap, pixel_shader=sclera_palette)

    a= 0
    imgX = 120
    imgY = 120
    #maxradius = math.sqrt(imgX**2 + imgY**2)/2
    maxradius = 59
    rscale = imgX / maxradius
    tscale = imgY / (2*math.pi)

    max_t = 0
    max_r = 0

    for y in range(0, 120):
        dy = y - imgY/2
        for x in range(0,120):
            a += 1
            dx = x - imgX/2
            t = math.ceil(math.atan2(dy,dx)%(2*math.pi)*tscale)
            #t = math.ceil(math.atan2(dy,dx)%(2*math.pi))
            ## r = math.ceil(math.sqrt(dx**2+dy**2)*rscale)
            r = math.ceil(math.sqrt(dx**2+dy**2))
            if t > max_t:
                max_t = t
            if r > max_r:
                max_r = r
            if 0 <= t < 125 and 0 <= r < 85:
                #print(t, r)
                col = sclera_texture[t,r]
                sclera_bitmap[x,y] = col


    end = time.monotonic()
    print(end - start, "s for", a, "iterations drawing sclera" )
    print("max_r =", max_r, "max_t = ", max_t )

    #gc.collect()
    #print(gc.mem_alloc(), gc.mem_free())

    #gc.collect()
    #print(gc.mem_alloc(), gc.mem_free())
    return sclera_tilegrid, right_sclera_tilegrid

def iris_processing(filename):
    start = time.monotonic()
    iris_texture, iris_palette = adafruit_imageload.load(filename,
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)
    iris_bitmap = displayio.Bitmap(110, 110, len(iris_palette))

    iris_palette.make_transparent(0)

    iris_tilegrid = displayio.TileGrid(iris_bitmap, pixel_shader=iris_palette)

    right_iris_tilegrid = displayio.TileGrid(iris_bitmap, pixel_shader=iris_palette)


    a= 0
    imgX = 110
    imgY = 110
    #maxradius = math.sqrt(imgX**2 + imgY**2)/2
    maxradius = 55
    rscale = imgX / maxradius
    tscale = imgY / (2*math.pi)

    max_t = 0
    max_r = 0
    # draw the iris bitmap
    for y in range(0, 110):
        dy = y - imgY/2
        for x in range(0,110):
            a += 1
            dx = x - imgX/2
            # Where all the magic happen.
            t = math.ceil(math.atan2(dy,dx)%(2*math.pi)*tscale)
            #t = math.ceil(math.atan2(dy,dx)%(2*math.pi))
            #r = math.ceil(math.sqrt(dx**2+dy**2)*rscale)
            r = math.ceil(math.sqrt(dx**2+dy**2))
            if t > max_t:
                max_t = t
            if r > max_r:
                max_r = r
            if 0 <= t < 111 and 0 <= r < 55:
                #print(t, r)
                col = iris_texture[t,r]
                iris_bitmap[x,y] = col



    end = time.monotonic()
    print(end - start, "s for", a, "iterations drawing iris" )
    print("max_r =", max_r, "max_t = ", max_t )

    return iris_tilegrid, right_iris_tilegrid


# load iris texture, interpolate it on a circle, returns 2 tilegrids
# BMP file, 8bits or 256 colors work fine (16 or 24bits bmp are unsupported)
# 79x111 minimum
left_iris_tilegrid, right_iris_tilegrid = iris_processing("/iris9.bmp")

# fix memory error
gc.collect()


# same for the sclera
# BMP file, 8bits or 256 colors work fine (16 or 24bits bmp are unsupported)
# 86x121 minimum
left_eye, right_eye = sclera_processing("/sclera7.bmp")

gc.collect()


left_eye_outline,  right_eye_outline = draw_outlines()


left_pupil = Circle(0, 0, 7, fill=0x000000)
left_sclera_group =displayio.Group(scale=2)
left_sclera_group.append(left_eye)
left_eye_group = displayio.Group()
left_eye_group.append(left_sclera_group)
left_mobile_group = displayio.Group()
left_mobile_group.append(left_iris_tilegrid)
left_pupil_group = displayio.Group()
left_pupil_group.append(left_pupil)
left_mobile_group.append(left_pupil_group)
left_eye_group.append(left_mobile_group)
left_eye_group.append(left_eye_outline)
left_mobile_group.x = left_mobile_group.y = 120


# right eye graph initialisation
right_pupil = Circle(0, 0, 7, fill=0x000000)
right_sclera_group = displayio.Group(scale=2)
right_eye.flip_x = True
right_sclera_group.append(right_eye)
right_eye_group = displayio.Group()
right_eye_group.append(right_sclera_group)
right_mobile_group = displayio.Group()
right_mobile_group.append(right_iris_tilegrid)
right_iris_tilegrid.flip_x = True
right_pupil_group = displayio.Group()
right_pupil_group.append(right_pupil)
right_mobile_group.append(right_pupil_group)
right_eye_group.append(right_mobile_group)
right_eye_group.append(right_eye_outline)
right_mobile_group.x = right_mobile_group.y = 120


display1.show(right_eye_group)
display2.show(left_eye_group)

# Loop forever


left_iris_tilegrid.x = -55
left_iris_tilegrid.y = -55

right_iris_tilegrid.x = -55
right_iris_tilegrid.y = -55
target_x = 0
target_y = 0

# Bad idea
#display1.autorefresh = False
#display2.autorefresh = False

while True:
    if (((120+ target_x) - left_mobile_group.x )**2 + ((120+target_y) - left_mobile_group.y )**2) < 9 :
        # Iris is close enough to the target coordinates
        # choose new target
        target_x = randint(-40,40)
        target_y = randint(-20,20)
        # no movement
        delta_x = 0
        delta_y = 0
        # pupil scale change randomly
        left_pupil_group.scale = right_pupil_group.scale = randint(1,2)
        # sleep time at the end of the loop
        # random between 1s and 2.5s, 0.1s steps
        dodo = randint(10,25)/10.0

    else:
        # angle mesure between iris position and target position.
        op_angle = math.degrees(math.atan2(left_mobile_group.y - (120+target_y), left_mobile_group.x - (120+ target_x))) + 90.0
        if op_angle < 0:
            op_angle = op_angle + 360.0
        # change to apply to x and y to make a movement of 3px toward the target.
        delta_x = -3 * math.sin(math.radians(op_angle))
        delta_y = 3 * math.cos(math.radians(op_angle))
        #minimal sleep time at the end of the loop (too low, the movement is not rendered)
        dodo = 0.012

    # apply movement to the iris + pupil group
    left_mobile_group.x = right_mobile_group.x = left_mobile_group.x + math.ceil(delta_x)
    left_mobile_group.y = right_mobile_group.y = left_mobile_group.y + math.ceil(delta_y)

    # sclera movement
    # make it terribly slow
    # refresh = 1/2 FPS ... one sec per eye...
    #left_sclera_group.x = right_sclera_group.x = left_sclera_group.x + math.ceil(delta_x)
    #left_sclera_group.y = right_sclera_group.y = left_sclera_group.y + math.ceil(delta_y)
    # manual refresh make it worst
    #display2.refresh()
    #display1.refresh()

    time.sleep(dodo)
