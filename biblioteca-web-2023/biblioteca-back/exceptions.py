class UsuarioException(Exception):
    ...

class UsuarioNotFoundError(UsuarioException):
    def __init__(self):
        self.status_code = 404
        self.detail = "USUARIO_NAO_ENCONTRADO"


class UsuarioAlreadyExistError(UsuarioException):
    def __init__(self):
        self.status_code = 409
        self.detail = "EMAIL_DUPLICADO"

class EmprestimoException(Exception):
    ...

class EmprestimoNotFoundError(EmprestimoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "EMPRESTIMO_NAO_ENCONTRADO"
class LivroException(Exception):
    ...

class LivroNotFoundError(LivroException):
    def __init__(self):
        self.status_code = 404
        self.detail = "LIVRO_NAO_ENCONTRADO"