class User:
    def __init__(self,
                 telegram_id: int,
                 username: str,
                 first_name: str,
                 last_name: str,
                 language_code: str,
                 is_premium: bool,
                 phone: str):
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.language_code = language_code
        self.is_premium = is_premium
        self.phone = phone

    def to_dict(self):
        user_dict = {
            'Telegram ID': self.telegram_id,
            'Username': self.username,
            'First Name': self.first_name,
            'Last Name': self.last_name,
            'Language Code': self.language_code,
            'Is Premium': self.is_premium,
            'Phone': self.phone
        }
        return user_dict
