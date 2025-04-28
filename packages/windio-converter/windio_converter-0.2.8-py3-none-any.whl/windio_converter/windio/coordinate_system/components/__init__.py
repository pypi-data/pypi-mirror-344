from copy import deepcopy

import aesoptparam as apm

from ..common import cs_base
from .blade import blade
from .floating_platform import floating_platform
from .tower_monopile import monopile, tower


class components(cs_base):
    """Settings for transformations applied for components"""

    blade = apm.SubParameterized(blade)
    tower = apm.SubParameterized(tower)
    monopile = apm.SubParameterized(monopile)
    floating_platform = apm.SubParameterized(floating_platform)

    def convert(self):
        components = deepcopy(self.windio_dict)
        if "blade" in components:
            components["blade"] = self.blade.convert()
        if "tower" in components:
            components["tower"] = self.tower.convert()
        if "monopile" in components:
            components["monopile"] = self.monopile.convert()
        if "floating_platform" in components:
            components["floating_platform"] = self.floating_platform.convert()
        return components
