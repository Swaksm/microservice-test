# /payment_service.py
from payment_repository import PaymentRepository

class PaymentService:
    """
    Couche de service contenant la logique métier.
    Elle ne dépend d'aucun framework web (comme Flask) et
    s'appuie sur le repository pour la gestion des données.
    """
    def __init__(self, payment_repository: PaymentRepository):
        self._repository = payment_repository

    def initiate_payment(self, user_id, event_id, amount):
        """
        Contient la logique de création d'un paiement.
        """
        if not amount or amount <= 0:
            raise ValueError("Le montant doit être positif.")

        transaction_data = {
            "user_id": user_id,
            "event_id": event_id,
            "amount": amount,
            "status": "PENDING"
        }
        
        transaction_id, created_transaction = self._repository.save(transaction_data)
        return transaction_id, created_transaction

    def get_payment_status(self, transaction_id):
        """Récupère le statut d'une transaction."""
        return self._repository.find_by_id(transaction_id)

    def confirm_payment(self, transaction_id):
        """Marque un paiement comme étant un succès."""
        return self._repository.update_status(transaction_id, 'SUCCESS')
