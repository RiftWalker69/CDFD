from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import FraudModel, Transaction
from .form import TransactionForm
import pandas as pd
from django.contrib import messages
from datetime import datetime
from django.utils.timezone import make_naive, get_current_timezone
from django.core.serializers.json import DjangoJSONEncoder
import json

fraud_model = FraudModel()
def home(request):
    return render(request, 'detector/home.html')
def cyber(request):
    return render(request, "detector/cyber.html")
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
    
    # Prepare data for charts
    transactions_data = []
    for tx in transactions:
        transactions_data.append({
            'distance_from_home': float(tx.distance_from_home),
            'ratio_to_median_purchase_price': float(tx.ratio_to_median_purchase_price),
            'is_fraud': tx.is_fraud
        })
    
    context = {
        'transactions': transactions,
        'total_transactions': total_transactions,
        'fraud_count': fraud_count,
        'fraud_rate': fraud_rate,
        'transactions_json': json.dumps(transactions_data)
    }
    return render(request, 'detector/dashboard.html', context)

def delete_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully.')
    except Transaction.DoesNotExist:
        messages.error(request, 'Transaction not found.')
    return redirect('dashboard')

def clear_all_transactions(request):
    if request.method == 'POST':
        Transaction.objects.all().delete()
        messages.success(request, 'All transactions have been cleared successfully.')
    return redirect('dashboard')

def export_transactions(request):
    # Check if there are any transactions
    if not Transaction.objects.exists():
        messages.warning(request, 'No transactions available to export.')
        return redirect('dashboard')
        
    # Get all transactions
    transactions = Transaction.objects.all()
    
    # Convert to DataFrame with timezone-naive datetimes
    data = []
    for tx in transactions:
        # Convert timezone-aware datetime to naive datetime
        naive_timestamp = make_naive(tx.timestamp, get_current_timezone())
        
        data.append({
            'Timestamp': naive_timestamp,
            'Distance from Home': tx.distance_from_home,
            'Distance from Last Transaction': tx.distance_from_last_transaction,
            'Ratio to Median': tx.ratio_to_median_purchase_price,
            'Used Chip': 'Yes' if tx.used_chip else 'No',
            'Online Order': 'Yes' if tx.online_order else 'No',
            'Is Fraud': 'Yes' if tx.is_fraud else 'No',
            'Fraud Probability': tx.probability
        })
    
    df = pd.DataFrame(data)
    
    # Create response with Excel file
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    # Write DataFrame to Excel
    df.to_excel(response, index=False)
    
    return response