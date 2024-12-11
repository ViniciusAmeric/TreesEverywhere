from django.urls import path
from .views import (
    UserPlantedTreesView,
    PlantedTreeDetailView,
    AddPlantedTreeView,
    AccountPlantedTreesView,
    UserPlantedTreesViewAPI,
)

urlpatterns = [
    path('planted-trees/', UserPlantedTreesView.as_view(), name='user_planted_trees'),
    path('planted-trees/<int:pk>/', PlantedTreeDetailView.as_view(), name='planted_tree_detail'),
    path('add-planted-tree/', AddPlantedTreeView.as_view(), name='add_planted_tree'),
    path('api/planted-trees/', UserPlantedTreesViewAPI.as_view(), name='user_planted_trees_api'),
    path('account/', AccountPlantedTreesView.as_view(), name='account_planted_trees'),
]
