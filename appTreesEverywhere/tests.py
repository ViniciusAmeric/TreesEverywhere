from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Account, Profile, Tree, PlantedTree

User = get_user_model()

class PlantedTreeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Criar usuários
        cls.user1 = User.objects.create_user(username="user1", password="password1")
        cls.user2 = User.objects.create_user(username="user2", password="password2")
    
        # Criar conta
        cls.account1 = Account.objects.create(name="Account 1")
    
        # Atribuir usuários diretamente (passando IDs)
        cls.account1.users.set([cls.user1.id, cls.user2.id])


    # --- Testes de templates ---

    def test_list_trees_by_user(self):
        """
        Testa se a listagem de árvores plantadas por um usuário específico é renderizada corretamente.
        """
        self.client.login(username="user1", password="password")
        response = self.client.get(reverse("trees:user_trees", kwargs={"username": self.user1.username}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Oak")
        self.assertNotContains(response, "Pine")
        self.assertNotContains(response, "Maple")

    def test_access_other_user_trees_forbidden(self):
        """
        Testa se ao tentar acessar as árvores plantadas por outro usuário é retornado um erro 403.
        """
        self.client.login(username="user1", password="password")
        response = self.client.get(reverse("trees:user_trees", kwargs={"username": self.user2.username}))  # Corrigido para user2
        self.assertEqual(response.status_code, 403)

    def test_list_trees_by_account_users(self):
        """
        Testa se a listagem de árvores plantadas pelos usuários das contas das quais o usuário é membro
        é renderizada corretamente.
        """
        self.client.login(username="user1", password="password")
        response = self.client.get(reverse("trees:account_trees", kwargs={"account_id": self.account1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Oak")
        self.assertContains(response, "Pine")
        self.assertNotContains(response, "Maple")


    # --- Testes unitários para métodos de plantação ---

    def test_user_plant_tree(self):
        """
        Testa se o método User.plant_tree() cria uma árvore plantada e a associa ao usuário.
        """
        tree = Tree.objects.create(name="Birch", scientific_name="Betula")
        planted_tree = self.user1.plant_tree(tree, location=(50.123456, -60.654321))

        self.assertEqual(planted_tree.user_id, self.user1.id)  # Usando user_id
        self.assertEqual(planted_tree.tree, tree)
        self.assertEqual(planted_tree.location, (50.123456, -60.654321))

    def test_user_plant_trees(self):
        """
        Testa se o método User.plant_trees() cria múltiplas árvores plantadas e as associa ao usuário.
        """
        tree_data = [
            (Tree.objects.create(name="Cedar", scientific_name="Cedrus"), (30.123456, -40.654321)),
            (Tree.objects.create(name="Willow", scientific_name="Salix"), (35.123456, -45.654321)),
        ]
        planted_trees = self.user2.plant_trees(tree_data)

        self.assertEqual(len(planted_trees), 2)
        self.assertEqual(planted_trees[0].user_id, self.user2.id) 
        self.assertEqual(planted_trees[0].tree.name, "Cedar")
        self.assertEqual(planted_trees[1].tree.name, "Willow")
