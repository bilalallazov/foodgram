from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.utils import build_shopping_list_text
from api.serializers import (
    AuthTokenSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeMinifiedSerializer,
    RecipeSerializer,
    SetAvatarSerializer,
    SetPasswordSerializer,
    TagSerializer,
    UserCreateSerializer,
    UserSerializer,
    UserWithRecipesSerializer,
)
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    ShortLink,
    Tag,
)
from users.models import Subscription

User = get_user_model()


class AuthTokenLoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'auth_token': token.key})


class AuthTokenLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        return Response(status=status.HTTP_200_OK)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author').prefetch_related(
        'tags',
        'recipe_ingredients__ingredient',
    )
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'get_link'):
            return (AllowAny(),)
        if self.action in (
            'favorite',
            'shopping_cart',
            'download_shopping_cart',
            'create',
        ):
            return (IsAuthenticated(),)
        return (IsAuthenticated(), IsAuthorOrReadOnly())

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeSerializer

    def _create_relation(self, model, request, recipe, exists_error):
        _, created = model.objects.get_or_create(
            user=request.user,
            recipe=recipe,
        )
        if not created:
            return Response(
                {'errors': exists_error},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = RecipeMinifiedSerializer(
            recipe,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete_relation(self, model, request, recipe, missing_error):
        deleted, _ = model.objects.filter(
            user=request.user,
            recipe=recipe,
        ).delete()
        if not deleted:
            return Response(
                {'errors': missing_error},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('post',))
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        return self._create_relation(
            Favorite,
            request,
            recipe,
            'Recipe already in favorites.',
        )

    @favorite.mapping.delete
    def favorite_delete(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        return self._delete_relation(
            Favorite,
            request,
            recipe,
            'Recipe not in favorites.',
        )

    @action(detail=True, methods=('post',))
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        return self._create_relation(
            ShoppingCart,
            request,
            recipe,
            'Recipe already in shopping cart.',
        )

    @shopping_cart.mapping.delete
    def shopping_cart_delete(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        return self._delete_relation(
            ShoppingCart,
            request,
            recipe,
            'Recipe not in shopping cart.',
        )

    @action(detail=True, methods=('get',), url_path='get-link')
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        link, _ = ShortLink.objects.get_or_create(
            recipe=recipe,
            defaults={'code': ShortLink.generate_unique_code()},
        )
        short_link = request.build_absolute_uri(f'/s/{link.code}/')
        return Response({'short-link': short_link})

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_cart__user=request.user,
            )
            .values(
                'ingredient__name',
                'ingredient__measurement_unit',
            )
            .annotate(amount=Sum('amount'))
            .order_by('ingredient__name')
        )
        content = build_shopping_list_text(ingredients)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping-list.txt"'
        )
        return response


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return (AllowAny(),)
        if self.action in ('retrieve', 'list'):
            return (AllowAny(),)
        return (IsAuthenticated(),)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action in ('subscribe', 'subscriptions'):
            return UserWithRecipesSerializer
        return UserSerializer

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
    )
    def set_password(self, request):
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('put', 'delete'),
        url_path='me/avatar',
        permission_classes=(IsAuthenticated,),
    )
    def avatar(self, request):
        if request.method == 'PUT':
            serializer = SetAvatarSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            avatar_url = request.build_absolute_uri(
                request.user.avatar.url,
            )
            return Response({'avatar': avatar_url})
        if request.user.avatar:
            request.user.avatar.delete(save=False)
            request.user.avatar = None
            request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        authors = User.objects.filter(
            subscribers__user=request.user,
        ).prefetch_related('recipes')
        page = self.paginate_queryset(authors)
        context = self.get_serializer_context()
        context['recipes_limit'] = self._get_recipes_limit()
        serializer = UserWithRecipesSerializer(
            page if page is not None else authors,
            many=True,
            context=context,
        )
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            if author == request.user:
                return Response(
                    {'errors': 'Cannot subscribe to yourself.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscription, created = Subscription.objects.get_or_create(
                user=request.user,
                author=author,
            )
            if not created:
                return Response(
                    {'errors': 'Already subscribed.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            context = self.get_serializer_context()
            context['recipes_limit'] = self._get_recipes_limit()
            serializer = UserWithRecipesSerializer(
                author,
                context=context,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        deleted, _ = Subscription.objects.filter(
            user=request.user,
            author=author,
        ).delete()
        if not deleted:
            return Response(
                {'errors': 'Not subscribed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_recipes_limit(self):
        recipes_limit = self.request.query_params.get('recipes_limit', 3)
        try:
            return int(recipes_limit)
        except (TypeError, ValueError):
            return 3
