"""simple auth method for examples."""


def Auth():
    accountID, token = None, None
    with open("OANDA_account.txt") as I:
        accountID = I.read().strip()
    with open("OANDA_token.txt") as I:
        token = I.read().strip()
    return accountID, token
