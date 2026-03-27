from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics


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

    @extend_schema(responses={200: AccountSerializer})
    def get(self, request, pk):
        account = Account.objects.filter(user=request.user, pk=pk).first()
        if not account:
            return Response({"error": "계좌를 찾을수 없습니다"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    @extend_schema(request=AccountSerializer, responses={200: AccountSerializer})
    def put(self, request, pk):
        account = Account.objects.filter(user=request.user, pk=pk).first()
        if not account:
            return Response({"error": "계좌를 찾을수 없습니다"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AccountSerializer(account, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(responses={204: None})
    def delete(self, request, pk):
        account = Account.objects.filter(user=request.user, pk=pk).first()
        if not account:
            return Response({"error": "계좌를 찾을수 없습니다"}, status=status.HTTP_404_NOT_FOUND)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionListView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'date', 'account']
    ordering_fields = ['date', 'amount']

    def get_queryset(self):
        return Transaction.objects.select_related('account').filter(account__user=self.request.user)

    def perform_create(self, serializer):
        account = serializer.validated_data.get('account')
        if account.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("본인 계좌에만 거래내역을 추가할수 있습니다")
        serializer.save()


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Transaction.objects.select_related('account').filter(account__user=self.request.user)