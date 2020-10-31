from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import connections
from .models import Transaction

class TransactionDetailsView(APIView):
	def put(self, request, transaction_id, *args, **kwargs):
		try:
			data = request.data
			Transaction.objects.filter(pk=transaction_id).update(**data)
			return Response({'status':'ok'}, status=status.HTTP_201_CREATED)
		except Exception as e:
			return Response({'status':'failed','reason': str(e)}, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, transaction_id, *args, **kwargs):
		if transaction_id:
			transaction_obj = Transaction.objects.get(id=transaction_id)
			
			return Response(TransactionSerializer(transaction_obj).data, status=status.HTTP_201_CREATED)

class TransactionTypeDetailView(APIView):
	def get(self, request, type_id, *args, **kwargs):
		if type_id:
			transaction_obj = Transaction.objects.filter(transaction_type=type_id)
			return Response(TransactionSerializer(transaction_obj,many=True).data, status=status.HTTP_201_CREATED)

class TransactionChildAmountDetails(APIView):
	def get(self, request, *args, **kwargs):
		transaction_id = request.GET.get('transaction_id',None)
		if transaction_id:
			data =  execute_query("""
				WITH RECURSIVE c AS (SELECT %s AS id UNION ALL SELECT sa.amount FROM api_transaction AS sa JOIN c ON c.id = sa.parent_id) SELECT id FROM c;
			""", [int(transaction_id)])
			result = sum([value['id'] for value in data])# as this will have current transaction

			return Response({'sum':result-int(transaction_id)}, status=status.HTTP_201_CREATED)

def dictfetchall(cursor):
	"Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]


def execute_query(query, params):
	cursor = connections['default'].cursor()
	print("query", cursor.mogrify(query, params))
	cursor.execute(query, params)
	return dictfetchall(cursor)