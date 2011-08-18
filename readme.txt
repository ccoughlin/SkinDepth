SkinDepth:  an attenuation depth calculator for electromagnetic waves

SkinDepth is a simple utility to calculate the depth of attenuation, or skin depth, of an electromagnetic wave inside a conductive material. At the skin depth, a wave drops to around 37% its original amplitude, so by 4 times the skin depth the wave is almost completely attenuated (37% of 37% of 37% of 37% or about 98% of the original amplitude). Among other things this is an important number to know for EMI/RFI shielding, some types of nondestructive testing, and radiofrequency losses in transmission lines and transformers. The skin depth of a conductive material depends on its electrical conductivity, its magnetic permeability, and the frequency of the wave.

SkinDepth uses an approximation to the skin effect calculation - it's valid for metals up to at least the microwave (GHz) range for the most part, but for poor conductors (insulators) it may only be applicable to a few tens of kHz. SkinDepth won't warn you if the frequencies you're using would make this approximation less than accurate so if you need the "real" results consult some of the above links for a more thorough background on the subject.  It also doesn't make any corrections for temperature which could be a factor if you're working at extremes.

The SkinDepth program keeps a database of conductive materials and can automatically calculate the skin depth of a given material for a given frequency (and vice versa). SkinDepth comes with a list of some conductive materials that you can add materials to as you need them. 

System Requirements

SkinDepth is written in Python and currently uses the wxPython platform for its user interface, so you'll at least need these two packages installed on your local machine. Disk space and memory requirements are minimal-if you can run (wx)Python you can run SkinDepth. SkinDepth has been tested under Linux (Fedora Core 14 x64), Windows XP, and Windows 7, and should work on any platform with Python 2.7 and wxPython installed. SkinDepth should also run under Python 2.6, but hasn't undergone as much testing on this version.

On OS X Snow Leopard, SkinDepth will run under the default Python 2.6 installation with one extra step. The wxPython package that ships as part of the default Python installation is compiled as a 32-bit library but the Python universal binary under Snow Leopard defaults to 64-bit; trying to load SkinDepth or any wxPython-based application will result in an error. There are several ways to get around this but the easiest is to use the arch command to use 32-bit Python. From the Terminal type arch -i386 python skindepth.py from the SkinDepth folder to have Python run SkinDepth. You can use man arch for more information.

Chris Coughlin July 17 2011
