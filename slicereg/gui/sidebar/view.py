from __future__ import annotations

from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QComboBox, QLineEdit, QHBoxLayout, QLabel

from slicereg.gui.base import BaseQtWidget
from slicereg.gui.sidebar.viewmodel import SidebarViewModel
from slicereg.gui.sidebar.slider_widget import LabelledSliderWidget
from vendor.napari_qrange_slider.qt_range_slider import QHRangeSlider


class SidebarView(BaseQtWidget):

    def __init__(self, _model: SidebarViewModel):

        self._model = _model
        self._model.register(self.update)

        self.widget = QWidget()

        layout = QVBoxLayout()
        self.widget.setLayout(layout)

        # Load atlas controls
        load_atlas_layout = QHBoxLayout()
        load_atlas_layout.addWidget(QLabel(text='Res (μm):'))

        self.atlas_resolution_textbox = QLineEdit(self._model.atlas_resolution_text)
        load_atlas_layout.addWidget(self.atlas_resolution_textbox)
        self.atlas_resolution_textbox.textEdited.connect(lambda text: setattr(self._model, 'atlas_resolution_text', text))

        self.load_atlas_from_file_button = QPushButton("Load Atlas File")
        load_atlas_layout.addWidget(self.load_atlas_from_file_button)
        self.load_atlas_from_file_button.clicked.connect(lambda: self.show_load_atlas_dialog())

        layout.addLayout(load_atlas_layout)

        self.update_bgatlas_button = QPushButton("Update Brainglobe Atlases")
        layout.addWidget(self.update_bgatlas_button)
        self.update_bgatlas_button.clicked.connect(lambda: self._model.click_update_bgatlas_list_button())

        self.list_atlas_dropdown = QComboBox()
        layout.addWidget(self.list_atlas_dropdown)
        self.list_atlas_dropdown.currentTextChanged.connect(
            lambda text: self._model.change_bgatlas_selection_dropdown(text))

        self.load_atlas_button = QPushButton("Load Atlas")
        layout.addWidget(self.load_atlas_button)
        self.load_atlas_button.clicked.connect(lambda: self._model.click_load_bgatlas_button())

        # Load atlas controls
        load_section_layout = QHBoxLayout()
        load_section_layout.addWidget(QLabel(text='Res (μm):'))

        self.section_resolution_textbox = QLineEdit()
        load_section_layout.addWidget(self.section_resolution_textbox)
        self.section_resolution_textbox.textEdited.connect(lambda text: setattr(self._model, 'section_resolution_text', text))

        # Load Section Buttons
        self.load_image_button = QPushButton("Load Section")
        load_section_layout.addWidget(self.load_image_button)
        self.load_image_button.clicked.connect(lambda: self.show_load_image_dialog())

        layout.addLayout(load_section_layout)

        self.quick_load_section_button = QPushButton("Quick Load Section")
        layout.addWidget(self.quick_load_section_button)
        self.quick_load_section_button.clicked.connect(lambda: self._model.click_quick_load_section_button())

        # Scale Sliders (Set Section Resolution)
        self.resample_widget = LabelledSliderWidget(min=15, max=200, label="Resample")
        layout.addLayout(self.resample_widget.layout)
        self.resample_widget.connect(lambda val: self._model.slide_resample_slider(val))

        self.resolution_widget = LabelledSliderWidget(min=1, max=100, label="Resolution")
        layout.addLayout(self.resolution_widget.layout)
        self.resolution_widget.connect(lambda val: self._model.slide_resolution_slider(val))

        # Movement Sliders
        self.x_slider = LabelledSliderWidget(min=-10000, max=10000, label='x')
        layout.addLayout(self.x_slider.layout)
        self.x_slider.connect(lambda val: self._model.change_x_slider(val))

        self.y_slider = LabelledSliderWidget(min=-10000, max=10000, label='y')
        layout.addLayout(self.y_slider.layout)
        self.y_slider.connect(lambda val: self._model.change_y_slider(val))

        self.z_slider = LabelledSliderWidget(min=-10000, max=10000, label='z')
        layout.addLayout(self.z_slider.layout)
        self.z_slider.connect(lambda val: self._model.change_z_slider(val))

        self.rotx_slider = LabelledSliderWidget(min=-180, max=180, label='rotx')
        layout.addLayout(self.rotx_slider.layout)
        self.rotx_slider.connect(lambda val: self._model.change_rotx_slider(val))

        self.roty_slider = LabelledSliderWidget(min=-180, max=180, label='roty')
        layout.addLayout(self.roty_slider.layout)
        self.roty_slider.connect(lambda val: self._model.change_roty_slider(val))

        self.rotz_slider = LabelledSliderWidget(min=-180, max=180, label='rotz')
        layout.addLayout(self.rotz_slider.layout)
        self.rotz_slider.connect(lambda val: self._model.change_rotz_slider(val))

        # Quick-rotation buttons
        buttons_layout = QHBoxLayout()

        self.coronal_button = QPushButton("Coronal")
        buttons_layout.addWidget(self.coronal_button)
        self.coronal_button.clicked.connect(lambda: self._model.click_coronal_button())

        self.annotation_atlas_button = QPushButton("Sagittal")
        buttons_layout.addWidget(self.annotation_atlas_button)
        self.annotation_atlas_button.clicked.connect(lambda: self._model.click_sagittal_button())

        self.axial_button = QPushButton("Axial")
        buttons_layout.addWidget(self.axial_button)
        self.axial_button.clicked.connect(lambda: self._model.click_axial_button())

        layout.addLayout(buttons_layout)

        # clim sliders
        self.slice_clim_slider = QHRangeSlider(initial_values=(0., 1.), data_range=(0., 1.), step_size=0.01)
        layout.addWidget(self.slice_clim_slider)
        self.slice_clim_slider.valuesChanged.connect(lambda vals: self._model.move_clim_section_2d_slider(vals))

        self.volume_slice_clim_slider = QHRangeSlider(initial_values=(0., 1.), data_range=(0., 1.), step_size=0.01)
        layout.addWidget(self.volume_slice_clim_slider)
        self.volume_slice_clim_slider.valuesChanged.connect(lambda vals: self._model.move_clim_section_3d_slider(vals))

        # Atlas Type Buttons
        buttons_layout = QHBoxLayout()

        self.registration_atlas_button = QPushButton("Registration")
        buttons_layout.addWidget(self.registration_atlas_button)
        self.registration_atlas_button.clicked.connect(lambda: self._model.click_registration_atlas_selector_button())

        self.annotation_atlas_button = QPushButton("Annotation")
        buttons_layout.addWidget(self.annotation_atlas_button)
        self.annotation_atlas_button.clicked.connect(lambda: self._model.click_annotation_atlas_selector_button())

        layout.addLayout(buttons_layout)

    def show_load_image_dialog(self):
        filename, filetype = QFileDialog.getOpenFileName(
            parent=self.qt_widget,
            caption="Load Image",
            dir="../../../data/RA_10X_scans/MeA",
            filter="OME-TIFF (*.ome.tiff) ;;TIFF (*.tif *.tiff)"
        )
        if not filename:
            return
        self._model.submit_load_section_from_file(filename=filename)

    def show_load_atlas_dialog(self):
        filename, filetype = QFileDialog.getOpenFileName(
            parent=self.qt_widget,
            caption="Load Atlas from File",
            dir="..",
            filter="Image Files (*.tif *.tiff *.nii *.nii.gz)"
        )
        if not filename:
            return
        self._model.submit_load_atlas_from_file(filename=filename)

    @property
    def qt_widget(self) -> QWidget:
        return self.widget

    def update(self, changed: str) -> None:
        render_funs = {
            'bgatlas_dropdown_entries': self._render_bgatlas_list_dropdown,
            'selected_bgatlas': (lambda: None),
            'atlas_resolution_text': self._render_atlas_resolution_textbox,
            'section_resolution_text': self._render_section_resolution_textbox,
            'x_slider_value': self._update_x_slider,
            'y_slider_value': self._update_y_slider,
            'z_slider_value': self._update_z_slider,
            'rx_slider_value': self._update_rotx_slider,
            'ry_slider_value': self._update_roty_slider,
            'rz_slider_value': self._update_rotz_slider,
        }
        render_funs[changed]()

    def _render_bgatlas_list_dropdown(self):
        self.list_atlas_dropdown.clear()
        self.list_atlas_dropdown.addItems(self._model.bgatlas_dropdown_entries)

    def _render_atlas_resolution_textbox(self):
        self.atlas_resolution_textbox.setText(self._model.atlas_resolution_text)

    def _render_section_resolution_textbox(self):
        self.section_resolution_textbox.setText(self._model.section_resolution_text)

    def _update_x_slider(self):
        self.x_slider.set_value(value=int(self._model.x_slider_value))

    def _update_y_slider(self):
        self.y_slider.set_value(value=int(self._model.y_slider_value))

    def _update_z_slider(self):
        self.z_slider.set_value(value=int(self._model.z_slider_value))

    def _update_rotx_slider(self):
        self.rotx_slider.set_value(value=int(self._model.rx_slider_value))

    def _update_roty_slider(self):
        self.roty_slider.set_value(value=int(self._model.ry_slider_value))

    def _update_rotz_slider(self):
        self.rotz_slider.set_value(value=int(self._model.rz_slider_value))
