from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.postgres.search import SearchVector, SearchQuery

from .models import Note, SharedNote
from speernotes.utility.utils import Validator, handle_exceptions
from .serializers import (CreateNotesSerializer, NoteSerializer, 
                          UpdateNotesSerializer, ShareNoteSerializer)


class NotesView(APIView):

    @staticmethod
    @handle_exceptions
    def post(request):
        user_id = request.user.id
        serializer = CreateNotesSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            note = Note.objects.create(user_id=user_id,
                                    title=data['title'],
                                    content=data['content'])
            note.save()
            response = {'id': note.id, 'created_at': note.created_at, **data}
            return Response(data=response, 
                            status=status.HTTP_201_CREATED)
        return Response({"message": Validator.TrimSerializerError(serializer.errors)},
                        status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    @handle_exceptions
    def get(request, id=None):
        user_id = request.user.id
        if id is None:
            queryset = Note.objects.filter(user_id=user_id)
            serializer = NoteSerializer(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        try:
            note = Note.objects.get(id=id, user_id=user_id)
            serializer = NoteSerializer(note)
            return Response(data=[serializer.data], status=status.HTTP_200_OK)
        except Note.DoesNotExist:
            return Response(data={"message": "Invalid Id"}, 
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @handle_exceptions
    def put(request, id=None):
        user_id = request.user.id
        try:
            note = Note.objects.get(id=id, user_id=user_id)
        except Note.DoesNotExist:
            return Response(data={"message": "Invalid Id"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateNotesSerializer(instance=note, data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            note.title = data.get('title', note.title)
            note.content = data.get('content', note.content)
            note.save()
            response = {'id': note.id, 'updated_at': note.updated_at, **data}
            return Response(data=[response], status=status.HTTP_200_OK)
        return Response({"message": Validator.TrimSerializerError(serializer.errors)},
                        status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    @handle_exceptions
    def delete(request, id=None):
        user_id = request.user.id
        try:
            note = Note.objects.get(id=id, user_id=user_id)
        except Note.DoesNotExist:
            return Response(data={"message": "Invalid Id"},
                            status=status.HTTP_400_BAD_REQUEST)
        note.delete()
        return Response(data={"message": "Note deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)


class ShareNote(APIView):
  
    @staticmethod
    @handle_exceptions
    def post(request, id=None):
        shared_by_user = request.user
        try:
            original_note = Note.objects.get(id=id, user=shared_by_user)
        except Note.DoesNotExist:
            return Response(data={"message": "Invalid Note ID"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ShareNoteSerializer(data=request.data, context={'shared_by_user': shared_by_user})
        if not serializer.is_valid():
            return Response({"message": Validator.TrimSerializerError(serializer.errors)},
                            status=status.HTTP_400_BAD_REQUEST)
        user_ids_to_share_with = serializer.validated_data['user_ids']
        shared_notes = []
        for user_id in user_ids_to_share_with:
            shared_note = Note.objects.create(
                user_id=user_id,
                title=original_note.title,
                content=original_note.content
            )
            shared_note_entry = SharedNote.objects.create(
                note=original_note,
                shared_with_id=user_id,
                shared_by=shared_by_user
            )
            shared_notes.append(shared_note_entry)
        return Response(data={"message": "Note shared successfully"},
                        status=status.HTTP_201_CREATED)
    

class SearchNote(APIView):

    @staticmethod
    @handle_exceptions
    def get(request):
        user_id = request.user.id
        keyword = request.GET.get('q', '')
        queryset = Note.objects.annotate(
            search=SearchVector('title', 'content'),
        ).filter(
            user_id=user_id,
            search=SearchQuery(keyword),
        )
        serializer = NoteSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        