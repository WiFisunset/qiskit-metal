# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.base import QComponent
import numpy as np


class ShortToGround(QComponent):
    """A basic short to ground termination. Functions as a pin for auto CPW
    drawing.

    Inherits `QComponent` class.

    Default Options:
        * width: '10um' -- The width of the 'cpw' terminating to ground (this is merely for the purpose of
          generating a value to pass to the pin)
        * pos_x: '0um' -- The x position of the ground termination.
        * pos_y: '0um' -- The y position of the ground termination.
        * rotation: '0' -- The direction of the termination. 0 degrees is +x, following a
          counter-clockwise rotation (eg. 90 is +y)
        * chip: 'main' -- The chip the pin should be on.
        * layer: '1' -- Layer the pin is on. Does not have any practical impact to the short.

    Values (unless noted) are strings with units included, (e.g., '30um')
    """
    component_metadata = Dict(short_name='term')
    """Component metadata"""

    default_options = Dict(width='10um',
                           pos_x='0um',
                           pos_y='0um',
                           orientation='0',
                           chip='main',
                           layer='1')
    """Default connector options"""

    def make(self):
        """Build the component."""
        p = self.p  # p for parsed parameters. Access to the parsed options.

        port_line = draw.LineString([(0, -p.width / 2), (0, p.width / 2)])

        # Rotates and translates the connector polygons (and temporary port_line)
        port_line = draw.rotate(port_line, p.orientation, origin=(0, 0))
        port_line = draw.translate(port_line, p.pos_x, p.pos_y)

        port_points = list(draw.shapely.geometry.shape(port_line).coords)

        #Generates the pin
        self.add_pin('short', port_points, p.width)
