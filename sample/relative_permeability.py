import math

class Saturations:

    def __init__(self):
        self._swi = None
        self._swc = None
        self._sorw = None

        self._sgi = None
        self._sgc = None
        self._sorg = None

    def set_swi(self, s):
        self._swi = s
    def set_swc(self, s):
        self._swc = s
    def set_sorw(self, s):
        self._sorw = s
    def set_sgi(self, s):
        self._sgi = s
    def set_sgc(self, s):
        self._sgc = s
    def set_sorg(self, s):
        self._sorg = s

    def get_swi(self):
        return self._swi
    def get_swc(self):
        return self._swc
    def get_sorw(self):
        return self._sorw
    def get_sgi(self):
        return self._sgi
    def get_sgc(self):
        return self._sgc
    def get_sorg(self):
        return self._sorg

    def get_swd(self, sw):
        if sw <= self.get_swc():
            return 0.
        if sw > (1 - self.get_sorw()):
            return 1.
        return (sw - self.get_swc()) / (1 - self.get_sorw() - self.get_swc())
    def get_sodw(self, sw):
        if sw <= self.get_swi():
            return 1.
        if sw >= (1 - self.get_sorw()):
            return 0.
        return 1 - (sw - self.get_swi()) / (1 - self.get_sorw() - self.get_swi())
    def get_sgd(self, sg):
        return 1 - (sg - self.get_sgc()) / (1 - self.get_sorg() - self.get_sgi())
    def get_sodg(self, sg):
        return 1 - (sg - self.get_swi() - self.get_sgi()) / (1 - self.get_sorg() - self.get_swi() - self.get_sgi())

class Corey:

    def __init__(self):
        self.sat = Saturations()

        self._nw = None
        self._ng = None
        self._now = None
        self._nog = None

        self._krw = None
        self._krg = None
        self._kro = None

    def set_nw(self, n):
        self._nw = n
    def set_ng(self, n):
        self._ng = n
    def set_now(self, n):
        self._now = n
    def set_nog(self, n):
        self._nog = n
    def set_krw_max(self, kr):
        self._krw = kr
    def set_krg_max(self, kr):
        self._krg = kr
    def set_kro_max(self, kr):
        self._kro = kr

    def get_nw(self):
        return self._nw
    def get_ng(self):
        return self._ng
    def get_now(self):
        return self._now
    def get_nog(self):
        return self._nog
    def get_krw_max(self,):
        return self._krw
    def get_krg_max(self,):
        return self._krg
    def get_kro_max(self,):
        return self._kro

    def get_krw_2f(self, sw):
        if sw <= self.sat.get_swc():
            return 0.
        if sw > (1 - self.sat.get_sorw()):
            return self.get_krw_max() + (1. - self.get_krw_max()) * (sw - (1. - self.sat.get_sorw())) / self.sat.get_sorw()
        return self.get_krw_max() * math.pow(self.sat.get_swd(sw), self.get_nw())
    def get_krow_2f(self, sw):
        if sw <= self.sat.get_swi():
            return self.get_kro_max()
        if sw >= (1 - self.sat.get_sorw()):
            return 0.
        return self.get_kro_max() * math.pow(self.sat.get_sodw(sw), self.get_now())

    def get_krg_2f(self, sg):
        return self._krg * math.pow(self.sat.get_sgd(sg), self.get_ng())
    def get_krog_2f(self, sg):
        return self._kro * math.pow(self.sat.get_sodg(sg), self.get_nog())

    def get_dkrw_2f(self, sw):
        if sw <= self.sat.get_swc():
            return 0.
        if sw > (1 - self.sat.get_sorw()):
            return (1. - self.get_krw_max()) / self.sat.get_sorw()
        return self.get_krw_max() * self.get_nw() * math.pow(self.sat.get_swd(sw), self.get_nw() - 1.) / (1 - self.sat.get_sorw() - self.sat.get_swc())

    def get_dkrow_2f(self, sw):
        if sw <= self.sat.get_swi():
            return 0.
        if sw >= (1 - self.sat.get_sorw()):
            return 0.
        return self.get_kro_max() * self.get_now() * math.pow(self.sat.get_sodw(sw), self.get_now() - 1.) / (1 - self.sat.get_sorw() - self.sat.get_swi())