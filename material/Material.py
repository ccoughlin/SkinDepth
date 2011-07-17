'''Material.py - defines a Material and its electromagnetic properties for SkinDepth

Chris Coughlin
'''
import constants
import math

class Material(object):
    '''Defines the basic electromagnetic properties of a material (no temperature correction)'''
    def __init__(self, name, notes=None, sigma_iacs=0.0, mu_rel=1.00):
        '''Required parameter:  name of material
          Optional parameters:
          notes (None):  general descriptive text to add to the material definition
          sigma_iacs (0.0):  electrical conductivity of material in %IACS scale
          mu_rel (1.00):  relative magnetic permeability of the material
        '''
        self.name = name
        self.notes = notes
        self.iacs = sigma_iacs
        self.mu_r = mu_rel

    @property
    def conductivity(self): 
        '''Returns the electrical conductivity in S/m of the material'''
        return (self.iacs / constants.ConductivityOfCopperIACS)*constants.ConductivityOfCopperSI
    @conductivity.setter
    def conductivity(self, conductivitySI):
        '''Sets the electrical conductivity in S/m of the material'''
        self.iacs = (conductivitySI / constants.ConductivityOfCopperSI) *100

    @property
    def permeability(self):
        '''Returns the magnetic permeability in H/m of the material'''
        return self.mu_r * constants.PermeabilityOfFreeSpace
    @permeability.setter
    def permeability(self, new_perm):
        '''Sets the magnetic permeability in H/m of the material'''
        self.mu_r = new_perm / constants.PermeabilityOfFreeSpace

    def calc_skindepth(self, frequency):
        '''Returns the skin depth in metres for the given excitation frequency.'''
        omega = 2*math.pi*frequency
        delta = 0.0
        if omega == 0 or self.conductivity == 0 or self.permeability == 0:
            delta = float('inf')
        elif omega < 0:
            delta = float('NaN')
        else:
            delta = math.sqrt(2/(omega*self.conductivity*self.permeability))
        return delta

    def calc_frequency(self, attenuation):
        '''Returns the frequency in Hz that has the desired attenuation depth in this material.
        Assumes attenuation is in metres.'''
        frequency = 0.0
        if attenuation == 0 or self.conductivity == 0 or self.permeability == 0:
            frequency = float('inf')
        elif attenuation < 0:
            return float('NaN')
        else:
            frequency = (2 / math.pow(attenuation, 2) / (self.conductivity * self.permeability * 2 * math.pi))
        return frequency