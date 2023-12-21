from rest_framework import serializers




class DisplayChoiceField(serializers.ChoiceField):  # 获取choice 属性值方式一, 重写Field 类

    def to_representation(self, obj):
        """返回选项的值"""
        return self._choices[obj]


class RecursiveField(serializers.Serializer):
    # 这个类代码保持不变
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

