from os import environ as env
import xmltodict

HOME=env.get('HOME')
MONITORS_XML_PATH='/.config/monitors.xml'

class Monitor:

    def __init__(self, width, height, offset_x, offset_y, index, name, primary=False):
        self.width = int(width)
        self.height = int(height)
        self.primary = primary
        self.offset_x = int(offset_x)
        self.offset_y = int(offset_y)
        self.index = index
        self.name = name
        self.wallpaper = None

    def __repr__(self):
        return self.name

def build_monitors_from_dict(path_to_monitors_xml='{0}{1}'.format(HOME, MONITORS_XML_PATH)):
    """Builds a list of Monitor objects from a logicalmonitor dictionary list
    parsed from ~/.config/monitors.xml"""
    with open(path_to_monitors_xml) as fd:
        doc = xmltodict.parse(fd.read())
    lm_list = doc['monitors']['configuration'][1]['logicalmonitor']
    monitors = []
    index = 1
    for lm in lm_list:
        monitors.append(Monitor(
            lm['monitor']['mode']['width'],
            lm['monitor']['mode']['height'],
            lm['x'],
            lm['y'],
            index,
            '{0} - {1}'.format(
                lm['monitor']['monitorspec']['vendor'],
                lm['monitor']['monitorspec']['connector']
            ),
            ('primary' in lm)
        ))
        index += 1
    if not monitors[0].primary:
        monitors[0], monitors[1] = monitors[1], monitors[0]
    return monitors
