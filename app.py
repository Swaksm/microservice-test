# app.py (Couche Controller)
from flask import Flask, request, jsonify
from payment_repository import PaymentRepository
from payment_service import PaymentService

app = Flask(__name__)


payment_repository = PaymentRepository()
payment_service = PaymentService(payment_repository)

# --- Endpoints du contrôleur ---

@app.route('/payment/initiate', methods=['POST'])
def initiate_payment_endpoint():
    """
    Endpoint pour initier un paiement.
    Le contrôleur extrait les données et appelle le service. Il ne contient pas de logique métier.
    """
    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({"error": "Données invalides : 'amount' est requis."}), 400

    try:
        transaction_id, transaction = payment_service.initiate_payment(
            user_id=data.get('user_id'),
            event_id=data.get('event_id'),
            amount=data.get('amount')
        )
        return jsonify({
            "transaction_id": transaction_id,
            "status": transaction['status'],
            "checkout_url": f"https://fake-payment-gateway.com/pay/{transaction_id}"
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/payment/status/<transaction_id>', methods=['GET'])
def get_status_endpoint(transaction_id):
    """Endpoint pour vérifier le statut d'un paiement."""
    transaction = payment_service.get_payment_status(transaction_id)
    
    if not transaction:
        return jsonify({"error": "Transaction non trouvée"}), 404
    
    return jsonify(transaction), 200

@app.route('/payment/webhook', methods=['POST'])
def payment_webhook_endpoint():
    """Endpoint simulant la réception d'un webhook de paiement."""
    data = request.get_json()
    tid = data.get('transaction_id')

    if not tid:
        return jsonify({"error": "transaction_id manquant"}), 400
        
    updated_transaction = payment_service.confirm_payment(tid)
    
    if updated_transaction:
        print(f"Paiement confirmé pour la transaction {tid} via webhook.")
        return jsonify({"message": "Statut mis à jour"}), 200
    
    return jsonify({"error": "Transaction inconnue"}), 404

if __name__ == '__main__':
    app.run(port=5003, debug=True)