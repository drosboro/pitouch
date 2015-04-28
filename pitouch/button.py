import pygame
from pygame.locals import *

from . import colors

class Button:
  def __init__(self, rect=(0,0,0,30), text="", fontpath=None, fontsize=20, bg_color=colors.BLACK, text_color=colors.WHITE, stroke_color=colors.WHITE):
    self._rect = pygame.Rect(rect)
    self._text = text
    self._surface = pygame.display.get_surface()
    self._pressed = False
    self._font = pygame.font.Font(fontpath, fontsize)
    self._font.set_bold(True)
    self._bg_color = bg_color
    self._text_color = text_color
    self._stroke_color = stroke_color
    self._callbacks = []

  def set_rect(self, rect):
    self._rect = pygame.Rect(rect)

  def set_text(self, text):
    self._text = text

  def subscribe(self, callback):
    self._callbacks.append(callback)

  def is_pressed(self):
    return self._pressed

  def press(self):
    self._pressed = True

  def unpress(self):
    self._pressed = False

  def toggle(self):
    self._pressed = not self._pressed

  def draw(self):
    if self._pressed:
      pygame.draw.rect(self._surface, self._text_color, self._rect, 0)
      pygame.draw.rect(self._surface, self._stroke_color, self._rect, 1)
      txt = self._font.render(self._text, 1, self._bg_color)
    else:
      pygame.draw.rect(self._surface, self._bg_color, self._rect, 0)
      pygame.draw.rect(self._surface, self._stroke_color, self._rect, 1)
      txt = self._font.render(self._text, 1, self._text_color)
    txtpos = txt.get_rect()
    txtpos.centerx = self._rect.centerx
    txtpos.centery = self._rect.centery
    self._surface.blit(txt, txtpos)

  def mouseDown(self, pos):
    if self._rect.collidepoint(pos):
      self.press()
      self.draw()

  def mouseUp(self, pos):
    if self.is_pressed():
      self.unpress()
      self.draw()
      for fn in self._callbacks:
        fn(self)



