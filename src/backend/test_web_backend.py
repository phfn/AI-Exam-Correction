from web_backend import get_base64_datatype
from pytest import raises


def test_get_base64_datatype():
    image_base_64 = "data:image/png;base64,iVBORw0KGgoAAAANS"
    assert get_base64_datatype(image_base_64) == "img"

    pdf_base_64 = "data:application/pdf;base64,JVBERi0xLjcKJaqrrK0"
    assert get_base64_datatype(pdf_base_64) == "pdf"

    with raises(ValueError):
        get_base64_datatype("something else")
    with raises(ValueError):
        get_base64_datatype("")
    with raises(TypeError):
        get_base64_datatype(None)
