from rest_framework import serializers
from accounts.serializers import UserSerializer
from student.models import QualifyingTest, QualifyingTestStatus



class QualifyingTestStatusSSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = QualifyingTestStatus
        fields = "__all__"


class QualifyingTestSerializer(serializers.ModelSerializer):
    qualifying_test = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = QualifyingTest
        fields = "__all__"

    def get_qualifying_test(self, instance):
        data = QualifyingTestStatusSSerializer(
            instance.status_qualifying_test.all().select_related("user"),
            many=True
        ).data
        return data