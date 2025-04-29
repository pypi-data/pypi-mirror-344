# Copyright (C) 2025, Simona Dimitrova

import os
import pytest
import tempfile

from faceblur.image import image_open
from data import IMAGE_FILES


@pytest.mark.parametrize("filename", IMAGE_FILES)
def test_image_load(filename):
    with image_open(filename) as image:
        assert image


@pytest.mark.parametrize("filename", IMAGE_FILES)
def test_image_save(filename):
    with tempfile.TemporaryDirectory() as tempdir:
        with image_open(filename) as image:
            assert image

            output = os.path.join(tempdir, os.path.basename(filename))
            image.save(output)
