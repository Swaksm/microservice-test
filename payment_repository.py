# /payment_repository.py
import uuid

class PaymentRepository:
    """
    Couche d'accès aux données pour les transactions.
    Elle abstrait la source de données (ici, un simple dictionnaire en mémoire).
    """
    def __init__(self):
        self._transactions = {}

    def find_by_id(self, transaction_id):
        """Récupère une transaction par son ID."""
        return self._transactions.get(transaction_id)

    def save(self, transaction_data):
        """
        Sauvegarde une nouvelle transaction.
        Génère un ID unique et l'ajoute au dictionnaire.
        """
        transaction_id = str(uuid.uuid4())
        self._transactions[transaction_id] = transaction_data
        return transaction_id, transaction_data

    def update_status(self, transaction_id, new_status):
        """Met à jour le statut d'une transaction existante."""
        if transaction_id in self._transactions:
            self._transactions[transaction_id]['status'] = new_status
            return self._transactions[transaction_id]
        return None
