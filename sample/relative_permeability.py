import math

class Saturations:

    def __init__(self):
        self._swi = None
        self._swc = None
        self._sorw = None
        self._sorg = None
        self._sgi = None
        self._sgc = None

    def set_swi(self, s):
        self._swi = s
    def set_swc(self, s):
        self._swc = s
    def set_sorw(self, s):
        self._sorw = s
    def set_sorg(self, s):
        self._sorg = s
    def set_sgi(self, s):
        self._sgi = s
    def set_sgc(self, s):
        self._sgc = s

    def get_swi(self, s):
        return self._swi
    def get_swc(self, s):
        return self._swc
    def get_sorw(self, s):
        return self._sorw
    def get_sorg(self, s):
        return self._sorg
    def get_sgi(self, s):
        return self._sgi
    def get_sgc(self, s):
        return self._sgc

    def get_swd(self, sw):
        return (sw - self.get_swc()) / (1 - self.get_sorw() - self.get_swc())
    def get_sgd(self, sg):
        return 1 - (sg - self.get_sgc()) / (1 - self.get_sorg() - self.get_sgi())
    def get_sodw(self, sw):
        return 1 - (sw - self.get_swi()) / (1 - self.get_sorw() - self.get_swi())
    def get_sodg(self, sw):
        return 1 - (sw - self.get_swi() - self.get_sgi()) / (1 - self.get_sorg() - self.get_swi() - self.get_sgi())

class Corey:

    def __init__(self):
        self._nw = None
        self._ng = None
        self._now = None
        self._nog = None

    def set_nw(self, n):
        self._nw = n
    def set_ng(self, n):
        self._ng = n
    def set_now(self, n):
        self._now = n
    def set_nog(self, n):
        self._nog = n
