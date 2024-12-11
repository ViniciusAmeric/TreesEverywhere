from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import User, Account, Tree, PlantedTree, Profile


### FORMULÁRIO PERSONALIZADO PARA ACCOUNT ###
class AccountForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=FilteredSelectMultiple(
            verbose_name="Users", is_stacked=False
        ),  # Widget com busca e seleção múltipla
        required=False,
    )

    class Meta:
        model = Account
        fields = "__all__"


### ADMIN PARA O MODELO USER ###
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email")
    ordering = ("username",)


### ADMIN PARA O MODELO ACCOUNT ###
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    form = AccountForm
    list_display = ("name", "active", "created_at")
    search_fields = ("name",)
    list_filter = ("active",)
    autocomplete_fields = ["users"]  # Para busca eficiente de usuários no admin
    actions = ["activate_accounts", "deactivate_accounts"]  # Ações disponíveis na listagem

    # Função para ativar contas
    def activate_accounts(self, request, queryset):
        queryset.update(active=True)
        self.message_user(request, "Selected accounts have been activated.")

    # Função para desativar contas
    def deactivate_accounts(self, request, queryset):
        queryset.update(active=False)
        self.message_user(request, "Selected accounts have been deactivated.")

    activate_accounts.short_description = "Activate selected accounts"  # Descrição no botão
    deactivate_accounts.short_description = "Deactivate selected accounts"  # Descrição no botão


### ADMIN PARA O MODELO TREE ###
@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ("name", "scientific_name", "get_planted_trees")
    search_fields = ("name", "scientific_name")

    # Função personalizada para mostrar as árvores plantadas associadas a essa árvore
    def get_planted_trees(self, obj):
        planted_trees = PlantedTree.objects.filter(tree=obj)
        return ", ".join([f"{pt.user.username} ({pt.location})" for pt in planted_trees])

    get_planted_trees.short_description = "Planted By"  # Título da coluna

    # Remover get_planted_trees dos fieldsets, pois não é um campo do modelo
    fieldsets = (
        (None, {
            'fields': ('name', 'scientific_name'),
        }),
    )



### FORMULÁRIO PERSONALIZADO PARA PLANTEDTREE ###
class PlantedTreeForm(forms.ModelForm):
    class Meta:
        model = PlantedTree
        fields = ['user', 'tree', 'location', 'account']

    # Personalizando o widget de localização para exibição de um campo de coordenadas
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Latitude, Longitude'}))


### ADMIN PARA O MODELO PLANTEDTREE ###
@admin.register(PlantedTree)
class PlantedTreeAdmin(admin.ModelAdmin):
    form = PlantedTreeForm
    list_display = ("get_tree_name", "user", "location", "planted_at")
    search_fields = ("tree__name", "user__username")
    list_filter = ("user", "planted_at")

    # Função personalizada para mostrar o nome da árvore
    def get_tree_name(self, obj):
        return obj.tree.name

    get_tree_name.short_description = "Tree Name"

    # Exibindo a página de detalhes de cada árvore plantada
    def tree_details(self, obj):
        return f"{obj.tree.name} planted by {obj.user.username} at {obj.location}"

    tree_details.short_description = "Details"

    # Definindo os campos para o formulário de edição do PlantedTree
    fieldsets = (
        (None, {
            'fields': ('user', 'tree', 'account', 'location'),
        }),
        ('Details', {
            'fields': ('tree_details',),
        }),
    )

    # Personalizando a página de adição do modelo PlantedTree
    def add_view(self, request, *args, **kwargs):
        """
        Customiza a página de adicionar PlantedTree no admin.
        """
        # Garantir que as opções de árvores e usuários estejam disponíveis para seleção
        extra_context = {'tree_options': Tree.objects.all(), 'user_options': User.objects.all()}
        return super().add_view(request, *args, **kwargs, extra_context=extra_context)


### ADMIN PARA O MODELO PROFILE ###
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "joined")
    search_fields = ("user__username",)
    # Campos básicos para o Profile sem muitos detalhes, pois a visualização do usuário já está disponível
    fieldsets = (
        (None, {
            'fields': ('user', 'about', 'joined'),
        }),
    )
