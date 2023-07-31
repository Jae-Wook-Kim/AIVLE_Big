from django.urls import path
from . import views
# import reply.views
from django.conf.urls.static import static
from django.conf import settings

app_name = "blog"

urlpatterns = [
    path('', views.blog_view, name="blog"),

    path('<int:post_id>/', views.blogdt_view, name='blogdt'),

    path('create/', views.create, name="create"),
    path('delete/<int:post_id>', views.delete, name="delete"),
    path('edit/<int:post_id>', views.edit, name="edit"),

    path('comment/create/<int:post_id>', views.create),    
    path('comment/delete/<int:post_id>/<int:com_id>', views.delete_comment, name="delete_comment"),    
    path('comment/edit/<int:post_id>/<int:com_id>', views.edit_comment, name="edit_comment"),
    
    path('download/<int:post_id>/', views.download_file, name='download_file'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)