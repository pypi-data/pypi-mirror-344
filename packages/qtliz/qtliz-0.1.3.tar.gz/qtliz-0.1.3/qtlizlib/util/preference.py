from typing import Any

from PySide6.QtWidgets import QLabel, QCheckBox, QComboBox, QGroupBox, QFormLayout, QSizePolicy, QSpinBox
from pylizlib.domain.config import ConfigItem
from pylizlib.handler.config import ConfigHandler

from qtlizlib.domain.preference import PreferenceItemPath, PreferenceItemCheck, PreferenceItemCombo, \
    PreferenceItemSpinBox
from qtlizlib.widget.data import PathLineSelector


def create_prf_path(item: ConfigItem) -> PreferenceItemPath:
    return PreferenceItemPath(
        label=QLabel(item.name),
        widget=PathLineSelector(),
        config_id=item.id,
        getter=lambda: ConfigHandler.read(item),
        setter=lambda value: ConfigHandler.write(item, value),
    )


def create_prf_checkbox(item: ConfigItem) -> PreferenceItemCheck:
    widget = QCheckBox()
    return PreferenceItemCheck(
        label=QLabel(item.name),
        widget=widget,
        config_id=item.id,
        getter=lambda: ConfigHandler.read(item),
        setter=lambda value: ConfigHandler.write(item, value),
    )


def create_prf_combo_box(item: ConfigItem) -> PreferenceItemCombo:
    widget = QComboBox()
    for value in item.values:
        widget.addItem(value)
    return PreferenceItemCombo(
        label=QLabel(item.name),
        widget=widget,
        config_id=item.id,
        getter=lambda: ConfigHandler.read(item),
        setter=lambda value: ConfigHandler.write(item, value),
    )


def create_prf_spin_box(item: ConfigItem) -> PreferenceItemSpinBox:
    widget = QSpinBox()
    widget.setMinimum(int(item.min_value))
    widget.setMaximum(int(item.max_value))
    widget.setSingleStep(1)
    return PreferenceItemSpinBox(
        label=QLabel(item.name),
        widget=widget,
        config_id=item.id,
        getter=lambda: int(ConfigHandler.read(item)),
        setter=lambda value: ConfigHandler.write(item, str(value)),
    )


def create_prf_group_box_form_layout(name: str, parent: Any) -> tuple:
    group_box = QGroupBox(name, parent)
    group_box.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
    form_layout = QFormLayout(group_box)
    form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
    group_box.setLayout(form_layout)
    return group_box, form_layout