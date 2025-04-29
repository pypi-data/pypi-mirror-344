import pytest
from example_package_thomas_barbe.xml import Partiels

def test_export():
    partiels = Partiels()
    partiels.setExecPath("/home/toto/Bureau/IRCAM/Partiels/build/Partiels/Partiels")
    partiels.setVampPath("/opt/Partiels/PlugIns")
    partiels.export("spectrogram", "/home/toto/Musique/patatine_mono.wav", "/home/toto/Bureau/IRCAM/Exports/json/", "json")
