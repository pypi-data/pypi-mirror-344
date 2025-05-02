import numpy as np
import polars as pl

from . import _inner_loop
from macromol_dataframe import Atoms, explode_residue_conformations
from dataclasses import dataclass, field
from functools import cache

from typing import Optional, Literal
from numpy.typing import NDArray

@dataclass(frozen=True)
class Sphere:
    center_A: NDArray[float]
    radius_A: float

@dataclass
class Grid:
    length_A: float
    center_A: NDArray[float] = field(default_factory=lambda: np.zeros(3))

def find_visible_residues(
        atoms: Atoms,
        grid: Optional[Grid],
        *,
        sidechain_sphere: Optional[Sphere] = None,
        visible_rule: Literal['all', 'any'] = 'all',
) -> pl.DataFrame:
    backbone = (
            _select_backbone(atoms)
            .with_columns(
                pl.col('residue_id').cast(pl.Int64).alias('shuffle_id')
            )
    )

    return _find_visible_residues(
            backbone, grid,
            n=len(backbone),
            sidechain_sphere=sidechain_sphere,
            visible_rule=visible_rule,
    )

def sample_visible_residues(
        rng: np.random.Generator,
        atoms: Atoms,
        grid: Optional[Grid],
        n: int,
        *,
        sidechain_sphere: Optional[Sphere] = None,
        visible_rule: Literal['all', 'any'] = 'all',
) -> pl.DataFrame:
    """
    Find residues for which the sidechain sphere is contained entirely within 
    the image.

    Arguments:
        rng:
            A pseudo-random number generator used to ensure that every visible 
            residue has an equal chance of being picked.

        atoms:
            A dataframe of atom coordinates.  The dataframe must contain the 
            following columns:

            - `residue_id`; see `assign_residue_ids()`
            - `atom_id`
            - `x`, `y`, `z`

        img_params:
            The dimensions of the image in question.

        n:
            The maximum number of visible residues to sample.

        sidechain_sphere:
            A simplified representation of the region where most sidechain 
            atoms are expected to be found.  See experiment #127 for details.

        visible_rule:
            How much of the sidechain sphere must be contained within the image 
            for the residue to be considered visible.  This must be either 
            "all" or "any".  The default is "all".

    Returns:
        A dataframe listing all of residues for which the bounding sphere fits 
        entirely within the image.  Each row also specifies the location of the 
        bounding sphere and the alternate location identifiers of the backbone 
        atoms used to compute the coordinate frame for each residue.

    Note that this function is most efficient for relatively small $n$.
    """
    backbone = _select_backbone(atoms)
    backbone = _shuffle_residues(rng, backbone)

    return _find_visible_residues(
            backbone, grid, n,
            sidechain_sphere=sidechain_sphere,
            visible_rule=visible_rule,
    )

@cache
def get_sidechain_sphere() -> Sphere:
    # The center coordinate is in a frame aligned with the N, Cα, and C atoms, 
    # and is optimized to include ≈95% of all observed sidechain atoms.  See 
    # experiment #127 for details.
    return Sphere(
            center_A=np.array([
                -1.2729026455200199,
                -1.9322552322708937,
                 2.3466656042276950,
            ]),
            radius_A=4,
    )


def _select_backbone(atoms):
    return (
            atoms
            .filter(
                pl.struct('atom_id', 'element').is_in([
                    dict(atom_id='N', element='N'),
                    dict(atom_id='CA', element='C'),
                    dict(atom_id='C', element='C'),
                ]),
            )
            .with_columns(
                backbone_id=(
                    pl.col('atom_id')
                    .replace_strict({
                        'N': 0,
                        'CA': 1,
                        'C': 2,
                    })
                )
            )
    )

def _shuffle_residues(rng, atoms):
    residue_ids = (
            atoms
            .select('residue_id')
            .unique(maintain_order=True)
    )
    shuffle_ids = (
            residue_ids
            .with_columns(
                shuffle_id=rng.permutation(len(residue_ids)),
            )
    )
    return atoms.join(shuffle_ids, on='residue_id')

def _find_visible_residues(
        backbone: Atoms,
        grid: Grid,
        n: int,
        *,
        sidechain_sphere: Optional[Sphere] = None,
        visible_rule: Literal['all', 'any'] = 'all',
):
    if sidechain_sphere is None:
        sidechain_sphere = get_sidechain_sphere()

    if grid is None:
        min_corner = np.full(3, -np.inf)
        max_corner = np.full(3, np.inf)
    else:
        if visible_rule == 'all':
            delta_length_A = -sidechain_sphere.radius_A
        elif visible_rule == 'any':
            delta_length_A = sidechain_sphere.radius_A
        else:
            raise ValueError(f"unknown visible rule: {visible_rule}")

        half_boundary_length_A = grid.length_A / 2 + delta_length_A
        min_corner = grid.center_A - half_boundary_length_A
        max_corner = grid.center_A + half_boundary_length_A

    backbone = explode_residue_conformations(backbone, 'alt_id_ex')
    backbone = (
            backbone
            .sort('shuffle_id', 'alt_id_ex', 'backbone_id')
            .rechunk()
    )

    probe_indices = np.zeros(n, dtype=int)
    probe_coords_A = np.zeros((n, 3))

    n_actual = _inner_loop._find_visible_residues(
            backbone['shuffle_id'].to_numpy(allow_copy=False),
            backbone['backbone_id'].to_numpy(allow_copy=False),
            backbone['x'].to_numpy(allow_copy=False),
            backbone['y'].to_numpy(allow_copy=False),
            backbone['z'].to_numpy(allow_copy=False),
            backbone['occupancy'].to_numpy(allow_copy=False),

            sidechain_sphere.center_A,
            min_corner,
            max_corner,

            probe_indices,
            probe_coords_A,
    )

    probe_indices = probe_indices[:n_actual]
    probe_coords_A = probe_coords_A[:n_actual]

    probes = pl.DataFrame({
        'residue_id': backbone[probe_indices, 'residue_id'],
        'alt_id_n': backbone[probe_indices, 'alt_id'],
        'alt_id_ca': backbone[probe_indices + 1, 'alt_id'],
        'alt_id_c': backbone[probe_indices + 2, 'alt_id'],
        'x': probe_coords_A[:,0],
        'y': probe_coords_A[:,1],
        'z': probe_coords_A[:,2],
    })

    return probes.select(
            residue_id='residue_id',
            alt_ids=pl.struct(N='alt_id_n', CA='alt_id_ca', C='alt_id_c'),
            x='x',
            y='y',
            z='z',
            radius_A=sidechain_sphere.radius_A,
    )


