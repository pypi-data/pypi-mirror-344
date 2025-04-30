#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
__all__ = ["SystemRecord", "RecordStatus", "SystemMatrixProperty"]

from copy import copy
from dataclasses import dataclass
from itertools import chain
from typing import Any, Callable, Iterable, Optional, Tuple

import numpy as np

from conformer.systems import default_join
from conformer_core.properties.core import (
    MASTER_PROP_LIST,
    MatrixProperty,
    Property,
    PropertySet,
)
from conformer_core.records import Record, RecordStatus
from conformer_core.util import ind, summarize

from .systems import BoundAtom, NamedSystem, System


@dataclass(repr=False)
class SystemMatrixProperty(MatrixProperty):
    extensive: Tuple[str, ...] = tuple()
    join_fn: Callable = default_join

    @staticmethod
    def atom_filter(a: BoundAtom):
        return a.is_physical

    def __post_init__(self):
        super().__post_init__()
        if len(self.window) != len(self.extensive):
            raise ValueError(
                "The length of `window`, `extensive`, and `dim_labels` must be the same length"
            )

    def validate(self, d: Any):
        if isinstance(d, list):
            d = np.array(d, dtyp=self.type)
        assert isinstance(d, np.ndarray)
        assert d.dtype == self.type
        assert len(d.shape) == len(self.window)
        n_elements = 0
        for dim, w, e in zip(d.shape, self.window, self.extensive):
            if e: # Extensive dims should be a multiple of window
                assert dim % w == 0
                n_elements = dim // w
            else: # Intenseive dims should be a fixed size
                assert dim == w
        return d
        return self.index_data(d, range(n_elements))

    @staticmethod
    def extensive_index(window: int, elements: Iterable[int]):
        """
        Extensive indeces depend on the system size
        
        e.g. A single gradient entry
        """
        return list(chain(*(range(e * window, e * window + window) for e in elements)))

    @staticmethod
    def intensive_index(window: int):
        """
        Intensive indeces don't rely on the system

        e.g. A single degree of freedom in a gradient (x, y, or z)
        """
        return list(range(window))


    def index_mask(
        self, elements: list[int]
    ) -> tuple[np.ndarray, ...]:
        """Expands a selection of elements into numpy indexer
        with the correct window size and extensivity
        """

        assert len(set(elements)) == len(elements), "Cannot handle quasi-periodic systems yet"

        # TODO: Handle cases with repeating elements!
        return np.ix_(*(
            (
                self.extensive_index(w, elements)
                if ext
                else self.intensive_index(w)
            )
            for w, ext in zip(self.window, self.extensive))
        )


    
    def system_mask(self, sys: System) -> tuple[np.ndarray, ...]:
        """Returns an index mask for the dataset with indecies starting 0"""
        elements = [i for (i, a) in enumerate(sys) if self.atom_filter(a)]

        return np.ix_(*(
            [
                self.extensive_index(w, elements)
                if ext
                else self.intensive_index(w)
            ]
            for w, ext in zip(self.window, self.extensive))
        )

    def system_join_map(self, ref_sys: System, other_sys: System):
        """Creates a sorted index for `other_sys` based on `ref_sys`

        Returns two arrays which map ref_sys onto other_sys 
        """
        # We will join from ref_sys to preserve caching
        el1 = []
        el2 = []

        # Get ordered list relative to other_sys
        for i, j in ref_sys.join_map(other_sys, join_fn=self.join_fn):
            if not self.atom_filter(ref_sys[i]):
                continue
            el1.append(i)
            el2.append(j)
        return el1, el2

    def add_into(
        self, sys1: System, mat1: np.ndarray, sys2: System, mat2: np.ndarray, coef=1
    ) -> np.ndarray:
        """Adds data from `mat2` into `mat1`. This function mutates mat1!"""

        # Get elements in common for these matrices
        el1, el2 = self.system_join_map(sys1, sys2)

        # Expand indeces based on extensivity
        idx1 = self.index_mask(el1)
        idx2 = self.index_mask(el2)

        # Do the addition
        mat1[idx1] += (coef * mat2[idx2])
        return mat1
    
    def __hash__(self) -> int:
        return self.name.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name


def empty_properties(system: System, properties=None) -> PropertySet:
    """Creates and empty PropertySet correctly sized for `system`"""
    if properties is None:
        properties = MASTER_PROP_LIST.values()

    P = PropertySet({})
    for p in properties:
        if p.__class__ is Property:
            if p.type is int:
                P[p] = 0
            elif p.type is float:
                P[p] = 0.0
            else:
                raise ValueError(f"Unknown how to zero property type `{p.type}`")
        elif isinstance(p, SystemMatrixProperty):
            shape = [
                w * system.size if e else w for (w, e) in zip(p.window, p.extensive)
            ]
            P[p] = np.zeros(shape, dtype=p.type)
        elif isinstance(p, MatrixProperty):
            P[p] = np.zeros(p.window, dtype=p.type)
        else:
            raise ValueError(f"Unknow property type`{p.type}`")
    return P


@dataclass
class SystemRecord(Record):
    system: Optional[System] = None  # Default appeased dataclass constructor

    def add_into(self, record: "SystemRecord", coef: int = 1) -> None:
        """
        Adds properties P into self. Deletes properties not in both
        """

        if record.properties is None:
            raise ValueError("Other record does not contain properties")
        outer_P = record.properties
        if self.properties is None:
            inner_P = empty_properties(self.system, outer_P.props)
            self.properties = inner_P
        else:
            inner_P = self.properties

        # Remove non-existant properties
        prop_rm = inner_P.props.difference(outer_P.props)
        for p in prop_rm:
            del inner_P[p]

        # Update property list
        inner_P.props.intersection_update(outer_P.props)

        # Accumulate!
        for p in inner_P.props:
            _coef = coef if p.use_coef else 1
            if p.__class__ in (Property, MatrixProperty):
                inner_P.values[p] += _coef * outer_P[p]
            elif isinstance(p, SystemMatrixProperty):
                inner_P.values[p] = p.add_into(
                    self.system, inner_P[p], record.system, outer_P[p], coef=_coef
                )
            else:
                raise ValueError(f"Cannot accumulate property of type `{p.__name__}")

    def swap_system(self, system: System) -> "SystemRecord":
        if self.system is system:
            return self

        # TODO: Removing check speeds things up sooooo much. But we should make it optional
        assert self.system.eq_TI(system), "Cannot swap non-equivalent systems"

        if system._saved == 0:
            system._saved == self.system._saved  # Save the DB some work
        new_record = copy(self) # Use instead of deepcopy to avoid performance hit
        new_record.system = system

        # Re-order matrix properties for non-cannonical systems
        if (
            new_record.properties
            # Rare case where they will have the same order
            and not (self.system.is_canonized and system.is_canonized)
        ):
            # Scalare properties don't care about indexes
            reindex = False
            for p in new_record.properties.props:
                if isinstance(p, SystemMatrixProperty):
                    reindex = True
                    break
            
            # Move the rows and colums!
            if reindex:
                new_record.properties = PropertySet({})
                for p in self.properties.props:
                    if isinstance(p, (SystemMatrixProperty)):
                        # In this case the systems/matrices are the same size
                        # for self.system and system
                        atom_map, _ = p.system_join_map(system, self.system)
                        new_record.properties[p] = self.properties[p][p.index_mask(atom_map)] 
                    else:
                        new_record.properties[p] = self.properties[p]

        return new_record

    def summarize(self, padding=2, level=0) -> str:
        rec_str = ind(padding, level, f"System Record {self.id}: \n")

        level += 1
        rec_str += ind(padding, level, f"Driver: {self.stage.name}\n")
        if self._saved:
            rec_str += ind(padding, level, f"Database ID: {self._saved}\n")
        rec_str += ind(
            padding,
            level,
            f"Created: {self.start_time.isoformat(timespec='minutes')}\n",
        )

        if isinstance(self.system, NamedSystem):
            rec_str += ind(padding, level, f"System: {self.system.name}\n")
        else:
            rec_str += ind(padding, level, f"System: {self.system}\n")
        rec_str += ind(padding, level, f"Status: {self.status.name}\n")

        if self.meta:
            rec_str += summarize("Meta", self.meta, padding=padding, level=level)

        if self.properties:
            rec_str += ind(padding, level, "Properties:\n")
            rec_str += self.properties.summarize(padding=padding, level=level + 1)
        return rec_str
