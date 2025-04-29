import pkg_resources
from lxml import etree
import subprocess
import os

class Partiels():

    def __init__(self):
        self.exec_path = None

    def setExecPath(self, path):
        self.exec_path = path

    def setVampPath(self, path):
        os.environ["VAMP_PATH"] = path

    '''
    def createReader(self, audiofile, channel):
        reader = etree.Element("reader")
        value = etree.Element("value")
        value.set("file", audiofile)
        value.set("channel", str(channel))
        reader.append(value)
        return reader
    '''
     
    def createXml(self, template, audiofile):
        #xml_path = 'templates/' + template + '.ptldoc'
        xml_path = pkg_resources.resource_filename(
            __name__, 'templates/' + template + '.ptldoc'
        )
        tree = etree.parse(xml_path)
        root = tree.getroot()
        #path = "templates/temp/" + template + ".ptldoc"
        path = pkg_resources.resource_filename(
            __name__, 'templates/temp/' + template + '.ptldoc'
        )
        with open(path, 'wb') as f:
            tree.write(f, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        return path

    def export(self, template, audiofile, dest, format):
        template = self.createXml(template, audiofile)
        cmd = [self.exec_path, "--export", "-i", audiofile, "-t", template, "-o", dest, "-f", format]
        ret = subprocess.run(cmd, capture_output=True, text=True)
        if ret.stderr:
            print(ret.stderr)
        if ret.stdout:
            print(ret.stdout)

'''
def testExport():
    partiels = Partiels()
    partiels.setExecPath("/home/toto/Bureau/IRCAM/Partiels/build/Partiels/Partiels")
    partiels.setVampPath("/opt/Partiels/PlugIns")
    partiels.export("spectrogram", "/home/toto/Musique/patatine_mono.wav", "/home/toto/Bureau/IRCAM/Exports/json/", "json")
'''