from unittest.mock import Mock

import numpy as np
import numpy.testing as npt
import pytest
from pytest import approx
from hypothesis import given
from hypothesis.strategies import floats, sampled_from

from slicereg.gui.app_model import AppModel
from slicereg.gui.atlas_section_window.viewmodel import AtlasSectionViewModel
from slicereg.utils import DependencyInjector

cases = [
    (0, 'coronal_section_image'),
    (1, 'axial_section_image'),
    (2, 'sagittal_section_image'),
]


@pytest.mark.parametrize("axis, section_attr", cases)
def test_app_model_coronal_section_is_the_first_axis_of_the_atlas_volume_and_at_the_first_atlas_section_coordinate(axis,
                                                                                                                   section_attr):
    atlas_volume = np.random.randint(0, 100, (10, 10, 10), np.uint16)
    app_model = AppModel(_injector=Mock(DependencyInjector), registration_volume=atlas_volume)
    coronal_coord = app_model.atlas_section_coords[axis]
    npt.assert_equal(getattr(app_model, section_attr), np.rollaxis(atlas_volume, axis)[coronal_coord])


def test_coronal_section_view_model_displays_the_coronal_section_image():
    app_model = AppModel(_injector=DependencyInjector())
    view_model = AtlasSectionViewModel(_axis=0, _model=app_model)
    app_model.registration_volume = np.random.randint(0, 100, (10, 10, 10), np.uint16)
    npt.assert_equal(app_model.coronal_section_image, view_model.atlas_section_image)


@given(value=floats(-50, 50), attributes=sampled_from([('coronal', 'x'), ('axial', 'y'), ('sagittal', 'z')]))
def test_atlas_section_viewmodel_updates_depth_on_app_model_coord_change(value, attributes):
    plane, coord_name = attributes
    app_model = AppModel(_injector=DependencyInjector(), x=0, y=0, z=0)
    atlas_section_view = AtlasSectionViewModel(plane=plane, _model=app_model)
    setattr(app_model, coord_name, value)

    assert atlas_section_view.image_coords == (0, 0)
    assert atlas_section_view.depth == value


@given(value=floats(-50, 50), attributes=sampled_from([
    ('coronal', 'y'), ('coronal', 'z'),
    ('axial', 'x'), ('axial', 'z'),
    ('sagittal', 'x'), ('sagittal', 'y'),
]))
def test_atlas_section_viewmodel_updates_image_coords_on_app_model_coord_change(value, attributes):
    if -1 < value < 1:  # test not valid for 0
        return
    plane, coord_name = attributes
    app_model = AppModel(_injector=DependencyInjector(), x=0, y=0, z=0)
    atlas_section_view = AtlasSectionViewModel(plane=plane, _model=app_model)
    setattr(app_model, coord_name, value)
    assert atlas_section_view.image_coords != (0, 0)
    assert atlas_section_view.depth == 0
