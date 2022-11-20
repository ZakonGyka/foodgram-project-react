from django.db import transaction
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Follow

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag, TagRecipe, User)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient
        read_only_fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag
        read_only_fields = ('id', 'name', 'color', 'slug')


class AuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj.pk).exists()


class IngredientRecipeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Создание сериализатора модели продуктов в рецепте для чтения.
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientRecipe.objects.all(),
                fields=('ingredient', 'recipe')
            )
        ]


class RecipeListSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(source='ingredient_to_recipe',
                                             many=True)
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user.id, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=user.id,
            recipe=obj.id
        ).exists()


class IngredientCreateSerializer(serializers.ModelSerializer):
    """
    Создание сериализатора продуктов по id с количеством для записи.
    """
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientCreateSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def to_representation(self, created_recipes):
        """
         Метод представления результатов сериализатора.
         """
        request = self.context.get('request')
        serializer = RecipeListSerializer(
            created_recipes,
            context={'request': request}
        )
        return serializer.data

    @transaction.atomic
    def ingredients_list(self, tags, ingredients, recipe):
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            if not IngredientRecipe.objects.filter(
                    ingredient_id=ingredient['ingredient']['id'],
                    recipe=recipe).exists():
                IngredientRecipe.objects.create(
                    ingredient_id=ingredient['ingredient']['id'],
                    amount=ingredient['amount'],
                    recipe=recipe)
        return recipe

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        recipe = Recipe.objects.create(**validated_data)
        recipe = self.ingredients_list(tags, ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, old_recipe, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        IngredientRecipe.objects.filter(recipe=old_recipe).delete()
        TagRecipe.objects.filter(recipe=old_recipe).delete()
        old_recipe = self.ingredients_list(
            tags, ingredients, old_recipe)
        super().update(old_recipe, validated_data)
        return old_recipe

    def validate(self, data):
        ingredients = data['ingredients']
        if not ingredients:
            raise serializers.ValidationError(
                'Добавьте хотя бы один ингредиент')
        tags = data['tags']
        if not tags:
            raise serializers.ValidationError(
                'Добавьте хотя бы один тэг')
        ingredients_list = []
        for ingredient in ingredients:
            id_to_check = ingredient['ingredient']['id']
            ingredient_to_check = Ingredient.objects.filter(id=id_to_check)
            if not ingredient_to_check:
                raise serializers.ValidationError(
                    'Продукт отсутствует в каталоге')
            else:
                if id_to_check in ingredients_list:
                    name_of_ingredient = ingredient_to_check[0].name
                    raise serializers.ValidationError(
                        f'Продукт "{name_of_ingredient}" '
                        f'- повторяется в рецепте')
                ingredients_list.append(id_to_check)
        return data


class FollowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
