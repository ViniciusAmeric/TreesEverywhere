from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from decimal import Decimal

class User(AbstractUser):
    """
    Custom User model extending AbstractUser to add the plant_tree and plant_trees methods.
    """
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def plant_tree(self, tree, location, account):
        """
        Plants a single tree and associates it with the user.
        """
        return PlantedTree.objects.create(
            user=self,
            tree=tree,
            location=location,
            account=account,
            age=0,
        )

    def plant_trees(self, tree_data, account):
        """
        Plants multiple trees based on the given tree_data.
        tree_data is a list of tuples (tree, location), where:
            - tree is an instance of Tree
            - location is a tuple (latitude, longitude)
        """
        planted_trees = [
            PlantedTree.objects.create(
                user=self,
                tree=tree,
                location=Decimal(str(location)),
                account=account,
                age=0,
            )
            for tree, location in tree_data
        ]
        return planted_trees


class Profile(models.Model):
    """
    A profile model associated with the User to store additional information.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    about = models.TextField(blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Account(models.Model):
    """
    Represents an account to group multiple users and share planted trees.
    """
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name="accounts")

    def __str__(self):
        return self.name


class Tree(models.Model):
    """
    Represents a type of tree with a common name and a scientific name.
    """
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class PlantedTree(models.Model):
    """
    Represents a tree planted by a user, associated with a specific account and location.
    """
    age = models.IntegerField()
    planted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="planted_trees",
    )
    tree = models.ForeignKey(
        Tree,
        on_delete=models.CASCADE,
        related_name="planted_trees",
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="planted_trees",
    )
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.tree.name} planted by {self.user.username} at {self.location}"
