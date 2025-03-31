from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import FraudModel, Transaction
from .form import TransactionForm
import pandas as pd

fraud_model = FraudModel()

def index(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                # Convert form data to model format
                transaction_data = {
                    'distance_from_home': data['distance_from_home'],
                    'distance_from_last_transaction': data['distance_from_last_transaction'],
                    'ratio_to_median_purchase_price': data['ratio_to_median'],
                    'used_chip': int(data['used_chip']),
                    'online_order': int(data['online_order'])
                }
                
                # Get prediction
                result = fraud_model.predict(transaction_data)
                
                # Save to database
                Transaction.objects.create(
                    **transaction_data,
                    is_fraud=result['is_fraud'],
                    probability=result['probability']
                )
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse(result)
                return render(request, 'detector/result.html', {'result': result})
            
            except Exception as e:
                error = str(e)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'error': error}, status=400)
                form.add_error(None, error)
    else:
        form = TransactionForm()
    
    return render(request, 'detector/index.html', {'form': form})

def dashboard(request):
    transactions = Transaction.objects.all()[:100]
    total_transactions = Transaction.objects.count()
    fraud_count = Transaction.objects.filter(is_fraud=True).count()
    fraud_rate = (fraud_count / total_transactions * 100) if total_transactions > 0 else 0
    
    context = {
        'transactions': transactions,
        'total_transactions': total_transactions,
        'fraud_count': fraud_count,
        'fraud_rate': fraud_rate
    }
    return render(request, 'detector/dashboard.html', context)