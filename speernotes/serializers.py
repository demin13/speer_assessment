from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Note

User = get_user_model()

class CreateNotesSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=2000)

class UpdateNotesSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, max_length=100)
    content = serializers.CharField(required=False, max_length=2000)

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

class ShareNoteSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())

    def validate_user_ids(self, value):
        shared_by_user = self.context.get('shared_by_user')
        users_to_share_with = User.objects.filter(id__in=value)
        valid_user_ids = set(users_to_share_with.values_list('id', flat=True))
        invalid_user_ids = set(value) - valid_user_ids
        if invalid_user_ids:
            raise serializers.ValidationError(f"Invalid user IDs: {list(invalid_user_ids)}")
        
        if shared_by_user.id in valid_user_ids:
            raise serializers.ValidationError("Cannot share with self.")

        return value