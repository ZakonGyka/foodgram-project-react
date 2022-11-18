from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Follow

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag, User)


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

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj.pk).exists()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """
    Создание сериализатора модели продуктов в рецепте для чтения.
    """
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id', queryset=Ingredient.objects.all()
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )
    name = serializers.CharField(
        source='ingredient.name', read_only=True
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
    author = AuthorSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        queryset = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(queryset, many=True).data

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


class IngredientCreateSerializer(serializers.ModelSerializer):
    """
    Создание сериализатора продуктов с количеством для записи.
    """
    # id = serializers.PrimaryKeyRelatedField(
    #     # queryset=Ingredient.objects.filter(id='id')
    #     queryset=Ingredient.objects.all()
    # )
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientRecipe
        # fields = ('id', 'amount', 'ingredient_id')
        fields = ('id', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientCreateSerializer(many=True)
    image = Base64ImageField()

    def to_representation(self, instance):
        request = self.context.get('request')
        serializer = RecipeListSerializer(
            instance,
            context={'request': request}
        )
        return serializer.data

    # def add_tags_and_ingredients(self, tags_data, ingredients, recipe):
    #     """
    #     Метод выполнения общих функции
    #     для создания и изменения рецептов.
    #     """
    #     for tag_data in tags_data:
    #         recipe.tags.add(tag_data)
    #         recipe.save()
    #     for ingredient in ingredients:
    #         if not IngredientRecipe.objects.filter(
    #                 ingredient_id=ingredient['ingredient']['id'],
    #                 recipe=recipe).exists():
    #             ingredientrecipe = IngredientRecipe.objects.create(
    #                 ingredient_id=ingredient['ingredient']['id'],
    #                 recipe=recipe)
    #             ingredientrecipe.amount = ingredient['amount']
    #             ingredientrecipe.save()
    #         else:
    #             IngredientRecipe.objects.filter(
    #                 recipe=recipe).delete()
    #             recipe.delete()
    #             raise serializers.ValidationError(
    #                 'Данные продукты повторяются в рецепте!')
    #     return recipe
    #
    # def create(self, validated_data):
    #     """
    #     Метод создания рецептов.
    #     """
    #     author = validated_data.get('author')
    #     tags_data = validated_data.pop('tags')
    #     name = validated_data.get('name')
    #     image = validated_data.get('image')
    #     text = validated_data.get('text')
    #     cooking_time = validated_data.get('cooking_time')
    #     ingredients = validated_data.pop('ingredients')
    #     recipe = Recipe.objects.create(
    #         author=author,
    #         name=name,
    #         image=image,
    #         text=text,
    #         cooking_time=cooking_time,
    #     )
    #     recipe = self.add_tags_and_ingredients(tags_data, ingredients, recipe)
    #     return recipe
    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        ingredients_list = [
            IngredientRecipe(
                recipe=recipe,
                # ingredient=ingredient['ingredient']['id'],
                ingredient_id=ingredient['ingredient']['id'],
                amount=ingredient['amount'],
                # ingredient=ingredient.get('id'),
                # amount=ingredient.get('amount')
            )
            for ingredient in ingredients
        ]
        IngredientRecipe.objects.bulk_create(ingredients_list)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.set(tags)
        if ingredients:
            instance.ingredients.clear()
            ingredients_list = [
                IngredientRecipe(
                    recipe=instance,
                    ingredient=ingredient.get('id'),
                    amount=ingredient.get('amount')
                )
                for ingredient in ingredients
            ]
            IngredientRecipe.objects.bulk_create(ingredients_list)
        return instance

    # def validate(self, data):
    #     """Посмотри как было изначально"""
    #     # ingredient_data = self.initial_data.get('ingredients')
    #     # ingredient_data = data.pop('ingredients', None)
    #     ingredient_data = data.pop('ingredients')
    #     if ingredient_data:
    #         checked_ingredients = set()
    #         for ingredient in ingredient_data:
    #             ingredient_obj = get_object_or_404(
    #                 Ingredient, id=ingredient['id']
    #             )
    #             if ingredient_obj in checked_ingredients:
    #                 raise serializers.ValidationError(
    #                     'Такой ингредиент уже есть'
    #                 )
    #             checked_ingredients.add(ingredient_obj)
    #         return data
    def validate(self, data):
        ingredients_list = []
        ingredients = data['ingredients']
        if not ingredients:
            raise serializers.ValidationError(
                'Добавьте хотя бы один ингредиент')
        tags = data['tags']
        if not tags:
            raise serializers.ValidationError(
                'Добавьте хотя бы один тэг')
        for ingredient in ingredients:
            id_to_check = ingredient['ingredient']['id']
            ingredient_to_check = Ingredient.objects.filter(id=id_to_check)
            if not ingredient_to_check.exists():
                raise serializers.ValidationError(
                    'Данный продукт отсутствует в каталоге')
            if ingredient_to_check in ingredients_list:
                raise serializers.ValidationError(
                    'Данный продукт уже есть в рецепте')
            ingredients_list.append(ingredient_to_check)
        return data

    # PRE WORK version
    # def validate(self, data):
    #     ingredients_list = []
    #     # ingredients = data.pop('ingredients')
    #     ingredients = data['ingredients']
    #     tags = data['tags']
    #     for ingredient in ingredients:
    #         if ingredient['ingredient']['id'] < 1:
    #             raise serializers.ValidationError(
    #                 'Добавьте хотя бы один ингредиент')
    #         id_to_check = ingredient['ingredient']['id']
    #         ingredient_to_check = Ingredient.objects.filter(id=id_to_check)
    #         if not ingredient_to_check.exists():
    #             raise serializers.ValidationError(
    #                 'Данный продукт отсутствует в каталоге')
    #         if ingredient_to_check in ingredients_list:
    #             raise serializers.ValidationError(
    #                 'Данный продукт уже есть в рецепте')
    #         ingredients_list.append(ingredient_to_check)
    #     return data
    # _________________________

    # def validate(self, data):
    #     ingredients = data.pop('ingredients')
    #     ingredient_list = []
    #     for item in ingredients:
    #         ingredient = get_object_or_404(Ingredient, id=item['id'])
    #         if ingredient in ingredient_list:
    #             raise serializers.ValidationError(
    #             'Ингредиент уже существует.'
    #             )
    #         ingredient_list.append(ingredient)
    #     data['ingredients'] = ingredients
    #     return data

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


class FollowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
