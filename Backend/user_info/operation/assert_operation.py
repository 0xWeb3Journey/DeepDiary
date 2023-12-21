# assert_operation.py
# force on dealing with Assert model
from django.db import transaction
from user_info.models import Assert
from user_info.operation.base_operation import BaseOperation
from utilities.common import trace_function


class AssertOperation(BaseOperation):

    def __init__(self, profile_instance=None):
        super().__init__(Assert, profile_instance)
        self.asserts, _ = Assert.objects.get_or_create(profile=profile_instance)

    @transaction.atomic
    @trace_function
    def update_asserts(self):
        try:
            self.asserts.face_cnt = self.profile_instance.faces.count()
            self.asserts.img_cnt = self.profile_instance.imgs.count()
            self.asserts.friend_cnt = self.profile_instance.re_from_relations.count() + self.profile_instance.re_to_relations.count()
            self.asserts.save()
            print(f'INFO: {self.profile_instance.name} : updated asserts successfully')
        except Exception as e:
            print(f'ERROR: Failed to update asserts for {self.profile_instance.name} - {e}')

