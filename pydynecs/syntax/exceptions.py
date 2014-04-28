
class EcsSyntaxError(Exception): pass
class EcsSyntaxKeyError(EcsSyntaxError, KeyError): pass
class EcsSyntaxArgumentError(EcsSyntaxError): pass

