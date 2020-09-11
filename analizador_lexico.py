import os
from classes import Procesador


class Acciones_Semanticas():
    operadores = {'=': ['IGUAL', ''],
                  ',': ['COMA', ''],
                  ';': ['PUNTOCOMA', ''],
                  '(': ['ABIRPAR', ''],
                  ')': ['CERRARPAR', ''],
                  '{': ['ABRIRLLAVE', ''],
                  '}': ['CERRARLLAVE', ''],
                  '+': ['SUMA', ''],
                  '<': ['MENOR', '']}

    palabras_clave = {'boolean': ['BOOLEAN', ''],
                      'function': ['FUNCTION', ''],
                      'if': ['IF', ''],
                      'input': ['INPUT', ''],
                      'int': ['INT', ''],
                      'print': ['PRINT', ''],
                      'return': ['RETURN', ''],
                      'string': ['STRING', ''],
                      'var': ['VAR', ''],
                      'while': ['WHILE', '']}

    def __init__(self, file, Procesador=None):
        if Procesador is None:
            self.Procesador = Procesador()
        else:
            self.Procesador = Procesador

        self.linea = 0
        self.flag_error = False
        self.estado = 0
        self.caracter = ''
        self.letra = ''
        self.dig = ''
        self.op = ''
        self.delimitador = ''
        self.char = ''
        self.lex = ''
        self.file = file
        self.numero_linea = 1

    def transformar(self):

        if self.caracter in self.operadores:
            self.op = self.caracter
            self.caracter = 'op'
        elif self.caracter.isdigit():
            self.dig = self.caracter
            self.caracter = 'd'
        elif self.caracter.isalpha():
            self.letra = self.caracter
            self.caracter = 'l'
        elif self.estado == 3:
            if self.caracter == ' ':
                self.delimitador = self.caracter
                self.caracter = 'del'
            elif self.caracter and self.caracter != '\'' and not self.caracter.isspace():
                self.char = self.caracter
                self.caracter = 'c'
        elif self.caracter.isspace():
            if (self.caracter == '\n'):
                self.numero_linea += 1
            self.delimitador = self.caracter
            self.caracter = 'del'

    def transformar_1(self, letra):
        if letra == 'op':
            return self.op
        elif letra == 'd':
            return self.dig
        elif letra == 'l':
            return self.letra
        elif letra == 'c':
            return self.char
        elif letra == 'del':
            return self.delimitador
        elif letra == '\n':
            return "'\\" + "n'"
        elif letra == '\t':
            return "\\'" + "t'"
        return letra

    def lee(self):
        if self.caracter == '\n' or self.delimitador == '\n':
            self.linea = 0
        self.caracter = self.file.read(1)
        self.linea += 1
        self.transformar()

    def leer_linea(self):
        self.file.readline()
        self.lee()

    def concat(self, caracter):
        self.lex = self.lex + caracter
        self.lee()

    def gen_token_abrirpar(self):
        return ['ABIRPAR', '']

    def gen_token_cerrarpar(self):
        return ['CERRARPAR', '']

    def gen_token_abrirllave(self):
        return ['ABRIRLLAVE', '']

    def gen_token_cerrarllave(self):
        return ['CERRARLLAVE', '']

    def gen_token_op(self, op):
        self.lee()
        return self.operadores[op]

    def gen_token_simbolo(self):
        # Si es palabra reservada...
        if self.lex in self.palabras_clave:
            return self.palabras_clave[self.lex]

        pos = self.Procesador.get_pos_TS_actual(self.lex)
        if self.Procesador.flag_decl:
            if pos != -1:
                self.Procesador.gestor_errores.generar_error(('error, variable \'%s\' ya declarada' % self.lex),
                                                             self.numero_linea, lexico=True, letra=self.linea)
            else:
                return ['ID', self.Procesador.insertar_en_TS_actual(self.lex)]
        else:
            pos = self.Procesador.get_pos_en_TS(self.lex)
            if pos != 0:
                return ['ID', pos]
            else:
                pos = self.Procesador.insertar_en_TS_actual(self.lex, 'entero')
                self.Procesador.insertar_Despl_TS(pos)
                if self.Procesador.tabla_actual == 'TSG':
                    self.Procesador.despl_G += 8 * 2
                else:
                    self.Procesador.despl_L += 8 * 2
                return ['ID', pos]

    def gen_token_asig_o_logico(self):
        if not self.op == '=':
            self.Procesador.gestor_errores.generar_error(
                ('error: no se esperaba el caracter %s' % (self.transformar_1(self.caracter))), self.numero_linea,
                lexico=True, letra=self.linea + 1)
        self.lee()
        return ['ASIGOLOG', '']

    def gen_token_y_logico(self):
        self.lee()
        return ['YLOGICO', '']

    def gen_token_string(self):
        if len(self.lex) > 64:
            self.flag_error = True
            self.Procesador.gestor_errores.generar_error(('error: cadena, %s, no permitida' % self.lex),
                                                         self.numero_linea, lexico=True, letra=self.linea)
        self.lee()
        return ['CADENA', '"' + self.lex + '"']

    def gen_token_int(self):
        if int(self.lex) > 32767:
            self.flag_error = True
            self.Procesador.gestor_errores.generar_error(('error: numero, %s, no permitido' % self.lex),
                                                         self.numero_linea, lexico=True, letra=self.linea)
        return ['CINT', int(self.lex)]


class Analizador_Lexico(Acciones_Semanticas):
    # '(' : [,'gen_token_op(self.caracter)'], ')' : [,'gen_token_op(self.caracter)'], '{' : [,'gen_token_op(self.caracter)'], '}' : [,'gen_token_op(self.caracter)'],
    #  '=' : [,'gen_token_op(self.caracter)'], '+' : [,'gen_token_op(self.caracter)'], '<' : [,'gen_token_op(self.caracter)']

    automata_finito = [{'l': [1, 'concat(self.letra)'], 'd': [2, 'concat(self.dig)'], '\'': [3, 'lee()'],
                        '|': [4, "concat('" + '|' + "')"], '/': [5, 'lee()'],
                        '&': [6, 'lee()'], 'op': [12, 'gen_token_op(self.op)'], 'del': [0, 'lee()']},
                       {'l': [1, 'concat(self.letra)'], 'd': [1, 'concat(self.dig)'], '_': [1, 'concat(self.caracter)'],
                        'del': [9, 'gen_token_simbolo()'],
                        'op': [9, 'gen_token_simbolo()'], '|': [9, 'gen_token_simbolo()'],
                        '&': [9, 'gen_token_simbolo()']},
                       {'d': [2, 'concat(self.dig)'], 'del': [9, 'gen_token_int()'], 'op': [9, 'gen_token_int()']},
                       {'l': [3, 'concat(self.letra)'], 'd': [3, 'concat(self.dig)'],
                        'del': [3, 'concat(self.delimitador)'], 'op': [3, 'concat(self.op)'],
                        'c': [3, 'concat(self.char)'], '\'': [10, 'gen_token_string()']},
                       {'op': [11, 'gen_token_asig_o_logico()']},
                       {'/': [0, 'leer_linea()']},
                       {'&': [13, 'gen_token_y_logico()']}]

    def __init__(self, file_name, Procesador=None):

        self.file_name = file_name
        self.file_dir = os.getcwd() + '/prueba/' + file_name + '/'

        Acciones_Semanticas.__init__(self, open(self.file_dir + file_name + '.txt', 'r'), Procesador)
        self.lee()

        print('\n\nreading from: ', self.file_dir + self.file_name + '.txt')
        print('writing tokens in: ', self.file_dir + 'tokens_' + self.file_name + '.txt\n\n')

    def tokennizar(self):

        self.lex = ''
        self.estado = 0

        while self.caracter:

            try:
                self.estado, accion = self.automata_finito[self.estado][self.caracter]
            except KeyError:
                self.flag_error == True
                self.Procesador.gestor_errores.generar_error(
                    ('error: no se esperaba el caracter %s' % (self.transformar_1(self.caracter))), self.numero_linea,
                    lexico=True, letra=self.linea + 1)
                return 'error: no esperada %s' % (self.caracter)

            if accion.startswith('gen'):
                token = eval('self.' + accion)
                return token

            eval('self.' + accion)

        return ['$']

    def write(self):

        with open(self.file_dir + 'tokens_' + self.file_name + '.txt', 'w') as to_file:

            i = 0
            token = ''

            while i < 1000:
                token = self.tokennizar()
                if self.flag_error:
                    self.flag_error = False
                else:
                    if token[0] == '$':
                        print('numero de tokens: ', str(i))
                        break
                    to_file.write('< ' + token[0] + ', ' + str(token[1]) + ' >\n')

                i = 1 + i

        print(self.numero_linea)

        self.Procesador.TSG.write(self.file_dir + 'tabla_' + self.file_name + '.txt')
