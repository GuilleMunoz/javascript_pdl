class GestorErrores:

    
    def __init__(self, path):
        self.path = path

    def generar_error(self, error, num_linea, lexico = False, sintactico = False, semantico = False, letra = 0):
        from itertools import islice
        with open(self.path) as f:
            i = 0
            for line in islice(f, num_linea):
                if not line.isspace() and i < num_linea:
                    index = i + 1
                    last_line = line
                i += 1

        if lexico:
            print(num_linea, ':',line[:-1])
            pista = ' ' * (letra + 1 + len(str(num_linea)))
            pista = pista + '^'
            print(pista)
            print(error)
            exit()
        
        if sintactico:
            print(num_linea, ':',line[:-1])
            pista = ' ' * (letra + 1 + len(str(num_linea)))
            pista = pista + '^'
            print(pista)
            print('error: se ha producido un error sintactico')
            exit()

        if semantico:
            print(index, ':',last_line[:-1])
            pista = ' ' * (letra + 1 + len(str(num_linea)))
            pista = pista + '^'
            print(pista)
            print(error)
