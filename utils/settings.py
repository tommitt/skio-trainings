class Settings:
    # def __init__(self):
        
    @property    
    def version(self):
        return "alpha0.1"

    @property
    def disciplines(self):
        return ['SL', 'GS', 'SG', 'DH', 'CR', 'ND']

settings = Settings()
