import macromol_dataframe as mmdf
import numpy as np
import parametrize_from_file as pff
import pytest

from visible_residues import (
        sample_visible_residues, find_visible_residues, Sphere, Grid,
)
from polars.testing import assert_frame_equal
from functools import partial
from pathlib import Path

CIF_DIR = Path(__file__).parent / 'resources'
FIND_OR_SAMPLE_VISIBLE_RESIDUE = pytest.mark.parametrize(
        'find_visible_residue', [
            find_visible_residues,
            partial(
                sample_visible_residues,
                rng=np.random.default_rng(0),
                n=1,
            ),
        ],
)

def grid(params):
    return Grid(
            length_A=float(params['length_A']),
            center_A=np.array(eval(params['center_A'])),
    )

def sidechain_sphere(params):
    return Sphere(
            center_A=np.array(eval(params['center_A'])),
            radius_A=float(params['radius_A']),
    )


@pff.parametrize(
        schema=[
            pff.cast(
                grid=grid,
                sphere=sidechain_sphere,
                expected=eval,
            ),
            pff.defaults(
                visible_rule='all',
            ),
        ],
)
def test_find_visible_residues(grid, sphere, visible_rule, expected):
    # I deliberately constructed this amino acid structure so that the global 
    # and residue-local coordinate frames are the same, to make it easy to 
    # reason about the expected results.

    atoms = mmdf.read_asymmetric_unit(CIF_DIR / 'axis_aligned_residue.cif')
    atoms = mmdf.assign_residue_ids(atoms)

    visible = find_visible_residues(
            atoms=atoms,
            grid=grid,
            sidechain_sphere=sphere,
            visible_rule=visible_rule,
    )
    assert len(visible) == expected
    assert (visible['radius_A'] == sphere.radius_A).all()

@pytest.mark.parametrize('n', [0, 1, 2])
@pff.parametrize(
        key='test_find_visible_residues',
        schema=[
            pff.cast(
                grid=grid,
                sphere=sidechain_sphere,
                expected=eval,
            ),
            pff.defaults(
                visible_rule='all',
            ),
        ],
)
def test_sample_visible_residues(n, grid, sphere, visible_rule, expected):
    # I deliberately constructed this amino acid structure so that the global 
    # and residue-local coordinate frames are the same, to make it easy to 
    # reason about the expected results.

    atoms = mmdf.read_asymmetric_unit(CIF_DIR / 'axis_aligned_residue.cif')
    atoms = mmdf.assign_residue_ids(atoms)

    visible = sample_visible_residues(
            rng=np.random.default_rng(0),
            atoms=atoms,
            grid=grid,
            n=n,
            sidechain_sphere=sphere,
            visible_rule=visible_rule,
    )
    assert len(visible) == min(expected, n)
    assert (visible['radius_A'] == sphere.radius_A).all()

@FIND_OR_SAMPLE_VISIBLE_RESIDUE
def test_find_visible_residues_4rek_G49(find_visible_residue):
    # This is a residue with two completely separate backbone conformations.  
    # The A conformation has 69% occupancy, so it should always be used, 
    # regardless of the actual order of the atoms in the input file.  We test 
    # by comparing to a file with only the A conformation.

    def find_visible(alt_ids):
        atoms = mmdf.read_asymmetric_unit(CIF_DIR / f'4rek_G49_{alt_ids}.cif')
        atoms = mmdf.assign_residue_ids(atoms, maintain_order=True)

        return find_visible_residue(
                atoms=atoms,
                grid=None,
        )

    visible_A = find_visible('A')
    visible_AB = find_visible('AB')
    visible_BA = find_visible('BA')

    assert len(visible_A) == 1
    assert len(visible_AB) == 1
    assert len(visible_BA) == 1

    assert_frame_equal(visible_A, visible_AB)
    assert_frame_equal(visible_A, visible_BA)

@FIND_OR_SAMPLE_VISIBLE_RESIDUE
def test_find_visible_residues_4rek_M154(find_visible_residue):
    # This is a residue with three Cα conformations, but only one N/C 
    # conformation.  The A conformation has 62% occupancy, so it should always 
    # be used, regardless of the actual order of the atoms in the input file.  
    # We test by comparing to a file with only the A conformation.

    def find_visible(alt_ids):
        atoms = mmdf.read_asymmetric_unit(CIF_DIR / f'4rek_M154_{alt_ids}.cif')
        atoms = mmdf.assign_residue_ids(atoms, maintain_order=True)

        return find_visible_residue(
                atoms=atoms,
                grid=None,
        )

    visible_A = find_visible('A')
    visible_ABC = find_visible('ABC')
    visible_CBA = find_visible('CBA')

    assert len(visible_A) == 1
    assert len(visible_ABC) == 1
    assert len(visible_CBA) == 1

    assert_frame_equal(visible_A.drop('alt_ids'), visible_ABC.drop('alt_ids'))
    assert_frame_equal(visible_A.drop('alt_ids'), visible_CBA.drop('alt_ids'))
    assert_frame_equal(visible_ABC, visible_CBA)

@FIND_OR_SAMPLE_VISIBLE_RESIDUE
def test_find_visible_residues_1bna(find_visible_residue):
    # This structure doesn't contain any amino acid residues, but that 
    # shouldn't cause any problems.

    atoms = mmdf.read_asymmetric_unit(CIF_DIR / '1bna.cif')
    atoms = mmdf.assign_residue_ids(atoms, maintain_order=True)

    visible = find_visible_residue(
            atoms=atoms,
            grid=None,
    )
    assert len(visible) == 0

def test_find_visible_residues_1lz1():
    # The purpose of this test is to make sure that `find_visible_residues` 
    # produces qualitatively reasonable results on a real protein structure.  

    atoms = mmdf.read_asymmetric_unit(CIF_DIR / '1lz1.cif')
    atoms = mmdf.assign_residue_ids(atoms, maintain_order=True)

    grid = Grid(length_A=15)

    visible = find_visible_residues(
            atoms=atoms,
            grid=grid,
    )
    visible = visible.join(
            atoms.group_by('residue_id', 'seq_id').agg(),
            on='residue_id',
    )

    # These expected sequence ids are based on a manual inspection, see 
    # `resources/1lz1_notes.xlsx` for details.
    assert len(visible) == 3
    assert set(visible['seq_id']) == {35, 57, 96}

@pytest.mark.parametrize('n', [0, 1, 2, 3, 4, 5])
def test_sample_visible_residues_1lz1(n):
    # The purpose of this test is to make sure that `sample_visible_residues` 
    # produces qualitatively reasonable results on a real protein structure.  

    atoms = mmdf.read_asymmetric_unit(CIF_DIR / '1lz1.cif')
    atoms = mmdf.assign_residue_ids(atoms, maintain_order=True)

    grid = Grid(length_A=15)

    visible = sample_visible_residues(
            rng=np.random.default_rng(0),
            atoms=atoms,
            grid=grid,
            n=n,
    )
    visible = visible.join(
            atoms.group_by('residue_id', 'seq_id').agg(),
            on='residue_id',
    )

    # These expected sequence ids are based on a manual inspection, see 
    # `resources/1lz1_notes.xlsx` for details.
    assert len(visible) == min(n, 3)
    assert set(visible['seq_id']) <= {35, 57, 96}

