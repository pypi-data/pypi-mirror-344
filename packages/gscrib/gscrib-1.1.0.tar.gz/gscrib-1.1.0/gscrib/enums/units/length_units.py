# -*- coding: utf-8 -*-

# Gscrib. Supercharge G-code with Python.
# Copyright (C) 2025 Joan Sala <contact@joansala.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gscrib.enums.base_enum import BaseEnum


# Pixels to units

CONVERSIONS_FACTORS = {
    "inches": 1.0 / 96.0,
    "millimeters": 25.4 / 96.0,
}

SYNONYMS = {
    "in": "inches",
    "mm": "millimeters",
}

class LengthUnits(BaseEnum):
    """Units of length measurement."""

    INCHES = "inches"
    MILLIMETERS = "millimeters"

    @classmethod
    def _missing_(cls, value):
        if value in SYNONYMS:
            return cls(SYNONYMS[value])
        return None

    def __init__(self, value):
        self.scale_factor = CONVERSIONS_FACTORS[value]

    def scale(self, value_in_px: float) -> float:
        """Scale a value in pixels to this unit"""

        return value_in_px * self.scale_factor

    def to_pixels(self, value_in_units: float) -> float:
        """Scale a value in this unit to pixels"""

        return value_in_units / self.scale_factor
