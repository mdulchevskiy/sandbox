from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(trim_whitespace=False)

    @staticmethod
    def validate_username(value):
        return value.strip()
