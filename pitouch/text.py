import pygame
from pygame.locals import *

from . import colors
from . import settings

class Text:
  def __init__(self, 
               content="", 
               y=settings.TOP_MARGIN, 
               fontpath=None, 
               fontsize=12, 
               lineheight=18, 
               bold=False, 
               color=colors.WHITE,
               alignment="l",
               surface=None,
               bg_color=settings.BACKGROUND_COLOR):

    if surface:
      self._surface = surface
    else:
      self._surface = pygame.display.get_surface()

    self._font = pygame.font.Font(fontpath, fontsize)
    self._fontsize = fontsize
    self._lineheight = lineheight
    self._bold = bold
    self._content = content 
    self._color = color
    self._alignment = alignment
    self._y = y
    self._rects = []
    self._bg_color = bg_color

    if self._bold:
      self._font.set_bold(True)

  def set_content(self, content):
    self._content = content

  def draw(self):
    for r in self._rects:
      pygame.draw.rect(self._surface, self._bg_color, r, 0)

    self._rects = []
    offset = 0
    for line in self._content.split("\n"):
      t = self._font.render(line, 1, self._color)
      trect = t.get_rect()
      
      trect.top = self._y + offset
      if self._alignment == "r":
        trect.right = self._surface.get_rect().width - settings.RIGHT_MARGIN
      if self._alignment == "c":
        trect.centerx = self._surface.get_rect().centerx
      else:
        trect.left = settings.LEFT_MARGIN

      self._surface.blit(t, trect)
      self._rects.append(trect)
      offset += self._lineheight




