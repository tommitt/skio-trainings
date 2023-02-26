class Settings:
    @property
    def disciplines(self):
        """Available options for disciplines"""
        return ["SL", "GS", "SG", "DH", "CR", "ND"]

    @property
    def version(self):
        """App current version"""
        return "beta0.1"

    @property
    def contact_email(self):
        """Email address displayed as contact"""
        return "skio.beta@gmail.com"


settings = Settings()
