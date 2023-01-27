class Settings:
    # def __init__(self):
        
    @property
    def disciplines(self):
        """Available options for disciplines"""
        return ['SL', 'GS', 'SG', 'DH', 'CR', 'ND']
    
    @property
    def version(self):
        """App current version"""
        return "alpha0.2"
    
    @property
    def deprecated_versions(self):
        """"Deprecated versions still accepted"""
        return ["alpha0.1"]

settings = Settings()
