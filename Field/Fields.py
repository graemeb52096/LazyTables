class Integer:
    """
    Represents INTEGER type for mysql columns
    """
    def __init__(self, kind="INT"):
        self.kind = kind

    def __str__(self):
        return self.kind

    def __repr__(self):
        return "%s" % self.kind


class VarChar:
    """
    Represents VARCHAR type for mysql columns
    """
    def __init__(self, length=64):
        self.length = length

    def __str__(self):
        return """VARCHAR(%s)""" % self.length

    def __repr__(self):
        return """VARCHAR(%s)""" % self.length