# Copyright (C) 2024- Davide Mollica <davide.mollica@inaf.it>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of iactsim.
#
# iactsim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iactsim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with iactsim.  If not, see <https://www.gnu.org/licenses/>.

from dataclasses import dataclass
from tabulate import tabulate

@dataclass(frozen=True)
class Material:
    """Represents a material with a name and a key."""
    name: str
    value: int

    def __repr__(self):
        return f"<Material: {self.name} (value={self.value})>"

class MaterialsMeta(type):
    def __str__(cls):
        return ", ".join(str(material) for material in cls._members())

    def __repr__(cls):
        return f"<Materials: {', '.join(repr(material) for material in cls._members())}>"

    def _repr_html_(cls):
        return cls._to_table(tablefmt="html")

    def _repr_markdown_(cls):
        return cls._to_table(tablefmt="pipe")

    def _members(cls):
        """Returns an iterator over the Material instances."""
        return (
            value for name, value in vars(cls).items() if isinstance(value, Material)
        )

    def _to_table(cls, tablefmt="html"):
        """Generates a table of all materials using tabulate."""
        table_data = [[material.name, material.value] for material in cls._members()]
        return tabulate(table_data, headers=["Material", "Key"], tablefmt=tablefmt)

class Materials(metaclass=MaterialsMeta):
    """
    A collection of Material instances.
    """
    AIR = Material(name='Air', value=0)
    FUSED_SILICA = Material(name='Fused Silica', value=1)