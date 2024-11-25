
from src.emailOperations import send_email


if __name__ == "__main__":
    email = {
        "Receiver_id": "252447",
        "Receiver": "davide.sirico@gmail.com",
        "Uid": ["conferma_registrazione"],
        "Subject": "prova email",
        "Raw": "Ci sono nuovi eventi che ti coinvolgono sul calendario giornaliero (ao daje roma annamo al fermi).",
        "Body": "vamoraga forza iuve",
    }
    send_email(email)