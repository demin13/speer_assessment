from django.urls import path
from .views import NotesView, ShareNote, SearchNote

urlpatterns = [
    path('', NotesView.as_view(), name='create_notes'),
    path('', NotesView.as_view(), name='list_notes'),
    path('<int:id>', NotesView.as_view(), name='get_single_note'),
    path('<int:id>', NotesView.as_view(), name='update_note'),
    path('<int:id>', NotesView.as_view(), name='delete_note'),
    path('<int:id>/share', ShareNote.as_view(), name='share_note'),
    path('search', SearchNote.as_view(), name='search_notes')
]