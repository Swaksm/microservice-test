from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

transactions = {}

#simple endpoint pour initialiser un paiement
@app.route('/payment/initiate', methods=['POST'])
def initiate_payment():
    data = request.get_json()
    
    if not data or 'amount' not in data:
        return jsonify({"error": "Données invalides"}), 400

    transaction_id = str(uuid.uuid4())
    
    transactions[transaction_id] = {
        "user_id": data.get('user_id'),
        "event_id": data.get('event_id'),
        "amount": data.get('amount'),
        "status": "PENDING"
    }

    return jsonify({
        "transaction_id": transaction_id,
        "status": "PENDING",
        "checkout_url": f"https://fake-payment-gateway.com/pay/{transaction_id}"
    }), 201

#simple endpoint pour vérifier le statut du paiement
@app.route('/payment/status/<transaction_id>', methods=['GET'])
def get_status(transaction_id):
    """Vérifie l'état d'un paiement"""
    transaction = transactions.get(transaction_id)
    if not transaction:
        return jsonify({"error": "Transaction non trouvée"}), 404
    
    return jsonify(transaction), 200

# Simule la réception d'un webhook de la passerelle de paiement
@app.route('/payment/webhook', methods=['POST'])
def payment_webhook():
    data = request.get_json()
    tid = data.get('transaction_id')
    
    if tid in transactions:
        transactions[tid]['status'] = 'SUCCESS'
        print(f"Paiement confirmé pour la transaction {tid}")
        return jsonify({"message": "Statut mis à jour"}), 200
    
    return jsonify({"error": "Inconnu"}), 400

if __name__ == '__main__':
    app.run(port=5003, debug=True)