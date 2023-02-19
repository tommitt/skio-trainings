class Settings:
    # def __init__(self):
        
    @property
    def disciplines(self):
        """Available options for disciplines"""
        return ['SL', 'GS', 'SG', 'DH', 'CR', 'ND']
    
    @property
    def version(self):
        """App current version"""
        return "alpha0.3"

settings = Settings()
