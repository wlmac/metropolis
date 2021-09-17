from metropolis import settings
import colorsys

def get_tag_color(hue):
    return '#%02x%02x%02x' % tuple(int(i*255) for i in colorsys.hsv_to_rgb(hue, settings.TAG_COLOR_SATURATION, settings.TAG_COLOR_VALUE))
