# from django.core.files import File


# from utils.mcs_storage import upload_file_pay


class BaseProcessor:
    def __init__(self, profile=None):
        self.profile = profile

    def get(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method.")
