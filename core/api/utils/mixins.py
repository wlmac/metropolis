class LookupField:
    @property
    def lookup_field(self):
        if hasattr(self.provider, "lookup_field"):
            return self.provider.lookup_field
        return "id"

    lookup_url_kwarg = "id"
