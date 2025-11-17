import uuid, os
from django.utils.deconstruct import deconstructible

@deconstructible
class UploadToUUID:
    def __init__(self, subdir):
        self.subdir = subdir

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        return os.path.join(self.subdir, filename)

upload_product_image = UploadToUUID('products/')
upload_product_type_image = UploadToUUID('product_types/')
upload_slide_image = UploadToUUID('slide/')