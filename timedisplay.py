import pitouch
import datetime

class TimeDisplay:
  def __init__(self, y=pitouch.settings.BOTTOM_MARGIN-18, alignment="r", fontpath=None, fontsize=12, lineheight=18, bold=False, color=pitouch.colors.WHITE, surface=None):
    self._txt = pitouch.text.Text(y=y, alignment=alignment, fontpath=fontpath, fontsize=fontsize, lineheight=18, bold=bold, color=color, surface=surface)

  def update(self):
    self._txt.set_content(datetime.datetime.now().strftime("%I:%M:%S %p"))
    self._txt.draw()