document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('transactionForm');
    const resultDiv = document.getElementById('result');
    const resultText = document.getElementById('resultText');
    const probabilityText = document.getElementById('probabilityText');

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultDiv.style.display = 'block';
                    resultDiv.querySelector('.alert').className = 'alert alert-danger';
                    resultText.textContent = data.error;
                    probabilityText.textContent = '';
                } else {
                    resultDiv.style.display = 'block';
                    const alertClass = data.is_fraud ? 'alert alert-danger' : 'alert alert-success';
                    resultDiv.querySelector('.alert').className = alertClass;
                    resultText.textContent = data.is_fraud ? '⚠️ FRAUD DETECTED' : '✅ Transaction Safe';
                    probabilityText.textContent = `Fraud Probability: ${(data.probability * 100).toFixed(2)}%`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resultDiv.style.display = 'block';
                resultDiv.querySelector('.alert').className = 'alert alert-danger';
                resultText.textContent = 'An error occurred while processing your request.';
                probabilityText.textContent = '';
            });
        });
    }
});
