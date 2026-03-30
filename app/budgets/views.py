from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.exceptions import PermissionDenied


class AccountListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(responses={200: AccountSerializer(many=True)})
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    @extend_schema(request=AccountSerializer, responses={201: AccountSerializer})
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, request, pk):
        account = Account.objects.filter(user=request.user, pk=pk).first()
        if not account:
            return None
        return account

    @extend_schema(responses={200: AccountSerializer})
    def get(self, request, pk):
        account = self.get_object(request, pk)
        if not account:
            return Response({"error":"계좌를 찾을수 없습니다"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(account)
        return Response(serializer.data)

    @extend_schema(request=AccountSerializer, responses={200: AccountSerializer})
    def patch(self, request, pk):
        account = self.get_object(request, pk)
        if not account:
            return Response({"error": "계좌를 찾을수 없습니다"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountSerializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(responses={204: None})
    def delete(self, request, pk):
        account = self.get_object(request, pk)
        if not account:
            return Response({"detail": "계좌를 찾을수 없습니다"}, status=status.HTTP_404_NOT_FOUND)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionListView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'date', 'account']
    ordering_fields = ['date', 'amount']

    def get_queryset(self):
        return Transaction.objects.select_related('account').filter(account__user=self.request.user)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Transaction.objects.select_related('account').filter(account__user=self.request.user)