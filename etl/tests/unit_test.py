import pytest

import pymupdf

from files.extraction.text_extractor import retrieve_input_strings
from files.transformation.row_transformer import preprocess_input_strings


import pytest
import pymupdf  # Assuming you've imported pymupdf

@pytest.mark.parametrize(
    "pdf_file_loc",
    [
        'others/test.pdf',
        'others/template.pdf'
    ]
)

def test_one(pdf_file_loc):
    pdf = pymupdf.open(pdf_file_loc)
    data = retrieve_input_strings(pdf)
    data = preprocess_input_strings(data)

    is_empty = False
    for _, input_item in data.items():
        if input_item == '' or input_item is None:
            is_empty = True
            break
    assert not is_empty
            