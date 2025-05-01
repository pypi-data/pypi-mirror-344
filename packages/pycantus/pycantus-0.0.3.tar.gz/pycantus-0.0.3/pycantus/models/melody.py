"""

"""


class Melody():
    """
    Representation of one chant melody
    """
    
    def __init__(self, volpiano : str, chant):
        self.raw_volpiano = volpiano
        self.vopiano = volpiano
        self.chant = chant

    def __str__(self):
        return self.volpiano
    
    # Here would be functions working with melody cleaning etc