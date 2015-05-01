import pygame
from pygame.locals import *

import pitouch
import timedisplay
import os
import argparse
import time
import network_info

class App:
    def __init__(self, pitft=False):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 320, 240
        self._clickables = []
        self._pitft = pitft

    def on_init(self):
        if self._pitft:
            os.putenv('SDL_FBDEV', '/dev/fb1')
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            os.putenv('SDL_MOUSEDRV', 'TSLIB')
            os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

        pygame.init()
        # pygame.display.init()

        if self._pitft:
            pygame.mouse.set_visible(False)

        self._display_surf = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        
        self._running = True
        self._default_fontpath = "/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono.ttf"

        self.background = pygame.Surface(self._display_surf.get_size())
        self.background = self.background.convert()
        self.background.fill( pitouch.colors.BLACK )

        self.config_btn = pitouch.button.Button(rect=(10, 200, 93, 30), text="Config", fontpath=self._default_fontpath, fontsize=12, surface=self.background)
        self.config_btn.subscribe(self.display_config)
        self._clickables.append(self.config_btn)
        self.config_btn.draw()

        self.quit_btn = pitouch.button.Button(rect=(113, 200, 93, 30), text="Quit", fontpath=self._default_fontpath, fontsize=12, surface=self.background)
        self.quit_btn.subscribe(self.quit)
        self._clickables.append(self.quit_btn)
        self.quit_btn.draw()

        self.title = pitouch.text.Text(content="Dave's RPi", fontpath=self._default_fontpath, alignment="c", bold=True, surface=self.background, color=pygame.Color("antiquewhite"))
        self.title.draw()

        bodytxt = """Oh freddled gruntbuggly,
Thy micturations are to me
As plurdled gabbleblotchits on a lurgid bee.
Groop, I implore thee, my foonting turlingdromes,
And hooptiously drangle me with crinkly bindlewurdles,
Or I will rend thee in the gobberwarts
With my blurglecruncheon, see if I don't!
"""
        self.body = pitouch.text.Text(content=bodytxt, y=23, fontpath=self._default_fontpath, fontsize=12, alignment="l", surface=self.background)
        self.body.draw()

        self.timer = timedisplay.TimeDisplay(y=175, alignment="c", fontpath=self._default_fontpath, fontsize=12, surface=self.background)

 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for obj in self._clickables:
                    obj.mouseDown(event.pos)
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                for obj in self._clickables:
                    obj.mouseUp(event.pos)


    def on_loop(self):
        pass
        # time.sleep(0.2)
        # self.timer.update()

    def on_render(self):
        self._display_surf.blit(self.background, (0, 0))
        pygame.display.flip()
        

    def on_cleanup(self):
        pygame.quit()

    def quit(self, obj):
        self._running = False

    def display_config(self, obj):
        content = network_info.network_info()
        self.body.set_content(content)
        self.body.draw()
 
    def on_execute(self):
        print "Execute"
        if self.on_init() == False:
            self._running = False
        print "Start loop"
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--pitft", help="uses PiTFT display", action="store_true")
    args = vars(ap.parse_args())

    if args['pitft']:
        print "Using PiTFT"
    else:
        print "Using window on main display"
    theApp = App(pitft=args['pitft'])
    theApp.on_execute()
