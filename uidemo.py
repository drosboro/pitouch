import pygame
from pygame.locals import *

import pitouch
import timedisplay
import os
import argparse

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
        pygame.init()
        if self._pitft:
            pygame.mouse.set_visible(False)

        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._default_fontpath = pygame.font.match_font("dejavusansmono")

        self.background = pygame.Surface(self._display_surf.get_size())
        self.background = self.background.convert()
        self.background.fill( pitouch.colors.BLACK )

        self.btn = pitouch.button.Button(rect=(10, 200, 300, 30), text="Quit", fontpath=self._default_fontpath, fontsize=12, surface=self.background)
        self.btn.subscribe(quit)
        self._clickables.append(self.btn)
        self.btn.draw()

        self.title = pitouch.text.Text(content="Hello world!", fontpath=self._default_fontpath, alignment="c", bold=True, surface=self.background, color=pygame.Color("antiquewhite"))
        self.title.draw()

        bodytxt = """Oh freddled gruntbuggly,
Thy micturations are to me
As plurdled gabbleblotchits on a lurgid bee.
Groop, I implore thee, my foonting turlingdromes,
And hooptiously drangle me with crinkly bindlewurdles,
Or I will rend thee in the gobberwarts
With my blurglecruncheon, see if I don't!
"""
        self.body = pitouch.text.Text(content=bodytxt, y=23, fontpath=self._default_fontpath, fontsize=10, alignment="l", surface=self.background)
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
        self.timer.update()

    def on_render(self):
        self._display_surf.blit(self.background, (0, 0))
        pygame.display.flip()
        

    def on_cleanup(self):
        pygame.quit()

    def quit(self, obj):
        self._running = False
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
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
        theApp = App(pitft=True)
    else:
        print "Using window on main display"
        theApp = App()
    theApp.on_execute()