from web_backend import get_base64_datatype, base_64_to_PIL_Image, PIL_Image_to_base_64
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

def test_pil_base64():
    image_base_64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAIAAAACUFjqAAABhWlDQ1BJQ0MgUHJvZmlsZQAAeJx9kT1Iw0AcxV9TtVIqInYQcQhSBcGCqIijVLEIFkpboVUHk0u/oElLkuLiKLgWHPxYrDq4OOvq4CoIgh8gbm5Oii5S4v+SQosYD4778e7e4+4dINRLTDU6JgBVM/VENCKmM6ui7xVd8KMPYxiWmFGJJRdTcB1f9/Dw9S7Ms9zP/Tl6lKzBAI9IPMcqukm8QTyzaVY47xMHWUFSiM+Jx3W6IPEj12WH3zjnbRZ4ZlBPJeaJg8Rivo3lNmYFXSWeJg4pqkb5QtphhfMWZ7VUZc178hcGstpKkus0hxDFEmKIQ4SMKooowUSYVo0UAwnaj7j4B21/nFwyuYpg5FhAGSok2w/+B7+7NXJTk05SIAJ0vljWxwjg2wUaNcv6PrasxgngfQautJa/XAdmP0mvtbTQEdC7DVxctzR5D7jcAQaeKpIu2ZKXppDLAe9n9E0ZoP8W8K85vTX3cfoApKir5Rvg4BAYzVP2usu7u9t7+/dMs78fmnVyt4b1boIAAACjSURBVHicPY5JkgQhDAMRGC80iwsI/v/UOVBTuiojJTzPs/c+56y15pzu7u5jjN57ay3uvWutzExEAGKMAEIIIQQAdM5h5lKKiJjZ5W5SSrTWIiIRqbWqKjOLyEfQnBOAmanq7/e7GhF5Ne4eY2TmO6H/eQl3B3D9IqKqpRQze+sxRgjhDt3azD4N9d6/+v66EDPnnKm1BiCl9BHMrKo5ZxH5A20KCWlvyX1qAAAAAElFTkSuQmCC"
    image_pil = base_64_to_PIL_Image(image_base_64)
    image_base_64_converted = PIL_Image_to_base_64(image_pil)

    assert image_base_64 == image_base_64_converted
