# deeplabcut2yolo is licensed under GNU General Public License v3.0, see LICENSE.
# Copyright 2024 Sira Pornsiriprasert <code@psira.me>

"""
Convert DeepLabCut dataset to YOLO format

Quick Start:
- d2y.convert("./deeplabcut-dataset/")
- d2y.convert("./deeplabcut-dataset/", train_paths, val_paths, skeleton_symmetric_pairs, data_yml_path)

============

Copyright (C) 2024 Sira Pornsiriprasert <code@psira.me>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from .__about__ import *
from .deeplabcut2yolo import (
    convert,
    get_flip_idx,
)
