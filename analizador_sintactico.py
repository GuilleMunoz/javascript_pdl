import os
from analizador_lexico import Analizador_Lexico
from classes import Procesador, No_Terminal, Identificador

class Acciones_Semanticas:

    pila = ['$', No_Terminal('P')]
    pila_aux = []
    token = str()

    def __init__(self, file_name):
        self.path = os.getcwd() + '/prueba/%s/'%(file_name)
        self.Procesador = Procesador(self.path, file_name)
        self.analizador_lexico = Analizador_Lexico(file_name, self.Procesador)

    def generar_error(self, X : No_Terminal, err_name):
        X.err_name = err_name
        self.Procesador.gestor_errores.generar_error('error: ' + err_name, self.analizador_lexico.numero_linea - 1, semantico=True, letra=self.analizador_lexico.linea + 1)
        return 'tipo_error'

    @staticmethod
    def get_size(type):
        vals = {'entero' : 2 * 8, 'cadena' : 64 * 8, 'logico' : 1}
        return vals[type]



    #---------------------------------------------------------------------------------------------------
    #1: P -> DP
    def a_s_1_2(self):
        self.pila_aux[-3].type = self.pila_aux[-1].type
        del self.pila_aux[-2: ]

    #2: P -> FP
    def a_s_2_1(self):
        self.pila_aux[-3].type = self.pila_aux[-1].type
        del self.pila_aux[-2: ]

    def a_s_2_2(self):
        self.pila_aux[-3].type = self.pila_aux[-1].type if self.pila_aux[-2].type != 'tipo_error' else 'tipo_error'
        del self.pila_aux[-2: ]

    #3: P -> S P
    def a_s_3_3(self):
        self.pila_aux[-3].type = self.pila_aux[-1].type if self.pila_aux[-2].type != 'tipo_error' else 'tipo_error'
        del self.pila_aux[-2: ]

    #5: P -> while ( E ){ C } P
    def a_s_5_1(self):

        if self.pila_aux[-3].type == 'tipo_error' or  self.pila_aux[-1].type == 'tipo_error':
            self.pila_aux[-9].type = 'tipo_error'
        else:
            self.pila_aux[-9].type = self.pila_aux[-1].type if self.pila_aux[-6].type == 'logico' else self.generar_error(self.pila_aux[-9], 'La condicion del bucle while no es logica')

        del self.pila_aux[-8: ]

    #6: D -> var T id;
    def a_s_6_1(self):
        self.Procesador.flag_decl = True


    def a_s_6_2(self):

        self.Procesador.insertar_Tipo_TS(self.pila_aux[-1].pos, self.pila_aux[-2].type)

        if self.Procesador.tabla_actual == 'TSG':
            self.Procesador.insertar_Despl_TS(self.pila_aux[-1].pos)
            self.Procesador.despl_G +=  self.pila_aux[-2].tamano
        else:
            self.Procesador.insertar_Despl_TS(self.pila_aux[-1].pos)
            self.Procesador.despl_L +=  self.pila_aux[-2].tamano

        self.Procesador.flag_decl = False

    def a_s_6_3(self):
        del self.pila_aux[-4: ]

    #7: T -> int
    def a_s_7_1(self):
        self.pila_aux[-2].type = 'entero'
        self.pila_aux[-2].tamano = 2 * 8
        del self.pila_aux[-1: ]

    #8: T -> string
    def a_s_8_1(self):
        self.pila_aux[-2].type = 'cadena'
        self.pila_aux[-2].tamano = 64 * 8
        del self.pila_aux[-1: ]

    #9: T -> boolean
    def a_s_9_1(self):
        self.pila_aux[-2].type = 'logico'
        self.pila_aux[-2].tamano = 1
        del self.pila_aux[-1: ]

    #10: F -> function T2 id ( A ){ C }
    #TODO: si a = tipo_error -> error
    #       si C = tipo_error -> error
    def a_s_10_1(self):
        self.Procesador.flag_decl = True

    def a_s_10_2(self):
        self.Procesador.insertar_Tipo_TS(self.pila_aux[-1].pos, 'funcion')
        self.Procesador.TSL.id = self.Procesador.TSG.get_lex(self.pila_aux[-1].pos - 1)
        self.Procesador.tabla_actual = 'TSL'

    def a_s_10_3(self):
        self.Procesador.tabla_actual = 'TSG'
        self.Procesador.insertar_args(self.pila_aux[-4].pos, self.pila_aux[-2].type)
        self.Procesador.insertar_tipo_ret(self.pila_aux[-4].pos, self.pila_aux[-5].type)
        self.Procesador.insertar_Despl_TS(self.pila_aux[-4].pos)
        self.Procesador.tabla_actual = 'TSL'
        self.Procesador.flag_decl = False
        self.pila[-2].type_func = True
        self.pila[-2].type_ret = self.pila_aux[-5].type

    def a_s_10_4(self):
        self.Procesador.tabla_actual = 'TSG'
        self.Procesador.TSL.clear_tabla()
        self.Procesador.despl_L = 0
        del self.pila_aux[-9: ]

    #11: T2 -> lambda
    def a_s_11_1(self):
        self.pila_aux[-2].type = 'vacio'
        del self.pila_aux[-1: ]

    #12: T2 -> T
    def a_s_12_1(self):
        self.pila_aux[-2].type = self.pila_aux[-1].type
        del self.pila_aux[-1: ]

    #13: A -> T id K
    def a_s_13_1(self):
        self.Procesador.insertar_Tipo_TS(self.pila_aux[-1].pos, self.pila_aux[-2].type)
        self.Procesador.insertar_Despl_TS(self.pila_aux[-1].pos)
        self.Procesador.despl_L += self.pila_aux[-2].tamano

    def a_s_13_2(self):
        if self.pila_aux[-1].type == 'vacio':
            self.pila_aux[-4].type = [self.pila_aux[-3].type]
        else:
            tipo = self.pila_aux[-1].type
            tipo.insert(0, self.pila_aux[-3].type)
            self.pila_aux[-4].type = tipo


        del self.pila_aux[-3: ]

    #14: A -> lambda
    def a_s_14_1(self):
        self.pila_aux[-2].type = 'vacio'
        del self.pila_aux[-1: ]

    #15: K -> lambda
    def a_s_15_1(self):
        self.pila_aux[-2].type = 'vacio'
        del self.pila_aux[-1: ]

    #16: K-> , T id K
    def a_s_16_1(self):
        self.Procesador.insertar_Tipo_TS(self.pila_aux[-1].pos, self.pila_aux[-2].type)
        self.Procesador.insertar_Despl_TS(self.pila_aux[-1].pos)
        self.Procesador.despl_L += self.pila_aux[-2].tamano


    def a_s_16_2(self):
        if self.pila_aux[-1].type == 'vacio':
            self.pila_aux[-5].type = [self.pila_aux[-3].type]
        else:
            tipo = self.pila_aux[-1].type
            tipo.insert(0, self.pila_aux[-3].type)
            self.pila_aux[-5].type = tipo
        #self.pila_aux[-5].type = [self.pila_aux[-3].type] if self.pila_aux[-1].type == 'vacio' else tipo.insert(0, self.pila_aux[-3].type)
        del self.pila_aux[-4: ]

    #17: C -> D C1
    def a_s_17_1(self):
        self.pila[-1].type_func = self.pila_aux[-2].type_func
        self.pila[-1].type_ret = self.pila_aux[-2].type_ret

    def a_s_17_2(self):
        self.pila_aux[-3].type = self.pila_aux[-1].type
        del self.pila_aux[-2: ]

    #18: C -> S C
    def a_s_18_1(self):
        self.pila[-1].type_func = self.pila_aux[-1].type_func
        self.pila[-1].type_ret = self.pila_aux[-1].type_ret

    def a_s_18_2(self):
        self.pila[-1].type_func = self.pila_aux[-2].type_func
        self.pila[-1].type_ret = self.pila_aux[-2].type_ret

    def a_s_18_3(self):

        self.pila_aux[-3].type = self.pila_aux[-1].type if self.pila_aux[-2].type == 'tipo_ok' else 'tipo_error'
        del self.pila_aux[-2: ]

    #19: C -> while ( E )- { C } C _
    def a_s_19_1(self):
        self.pila[-2].type_func = self.pila_aux[-5].type_func
        self.pila[-2].type_ret = self.pila_aux[-5].type_ret
        self.pila_aux[-5].type = self.pila_aux[-2].type if self.pila_aux[-2].type == 'logico' else self.generar_error(self.pila_aux[-5], 'La condicion del bucle while no es logica')

    def a_s_19_2(self):
        self.pila[-1].type_func = self.pila_aux[-8].type_func
        self.pila[-1].type_ret = self.pila_aux[-8].type_ret

    def a_s_19_3(self):
        if self.pila_aux[-3] == 'tipo_error':
            self.pila_aux[-9].type = 'tipo_error'
        else:
            pass
            #self.pila_aux[-9].type = self.pila_aux[-1].type if self.pila_aux[-6].type == 'logico' else self.generar_error(self.pila_aux[-9], 'La condicion del bucle while no es logica')
        del self.pila_aux[-8: ]

    #20: C -> lambda
    def a_s_20_1(self):
        self.pila_aux[-2].type = 'vacio'
        del self.pila_aux[-1: ]

    #21: S -> id S3;
    def a_s_21_1(self):

        if self.pila_aux[-2].type == 'tipo_error':
            self.pila_aux[-4].type = 'tipo_error'
        elif self.Procesador.busca_tipo_TS(self.pila_aux[-3].pos) == 'funcion':
            if self.Procesador.busca_tipo_arg(self.pila_aux[-3].pos) == self.pila_aux[-2].type:
                self.pila_aux[-4].type = 'tipo_ok'
            else:
                self.pila_aux[-4].type = self.generar_error(self.pila_aux[-3], 'Se esta intentando llamar a una funcion con un numero o tipo incorrecto de argumentos')

        elif self.Procesador.busca_tipo_TS(self.pila_aux[-3].pos) == self.pila_aux[-2].type:
            self.pila_aux[-4].type = 'tipo_ok'
        else:
            if type(self.pila_aux[-2].type).__name__ == 'list':
                self.pila_aux[-4].type = self.generar_error(self.pila_aux[-4], 'Se esta intentando llamar a una funcion que no ha sido definida')
            else:
                self.pila_aux[-4].type = self.generar_error(self.pila_aux[-4], 'Los tipos no concuerdan')

        del self.pila_aux[-3: ]


    #22: S -> print ( E );
    def a_s_22_1(self):
        self.pila_aux[-6].type = 'tipo_ok'
        del self.pila_aux[-5: ]

    #23: S -> input ( id );
    def a_s_23_1(self):
        self.pila_aux[-6].type = 'tipo_ok' if self.Procesador.busca_tipo_TS(self.pila_aux[-3].pos) == 'entero' or self.Procesador.busca_tipo_TS(self.pila_aux[-3].pos) == 'cadena' else self.generar_error(self.pila_aux[-6], 'La sentencia de asignacion solo almacena en una variable de tipo string o int')
        del self.pila_aux[-5: ]

    #24: S -> if ( E ) S
    def a_s_24_1(self):
        self.pila[-1].type_func = self.pila_aux[-5].type_func
        self.pila[-1].type_ret = self.pila_aux[-5].type_ret

    def a_s_24_2(self):
        self.pila_aux[-6].type = self.pila_aux[-1].type if self.pila_aux[-3].type == 'logico' else self.generar_error(self.pila_aux[-6], 'La condicion del if no es logica')
        """if self.pila_aux[-1].type == 'tipo_error':
            self.pila_aux[-6].err_name = self.pila_aux[-1].err_name"""
        del self.pila_aux[-5: ]

    #25: S -> return X ;
    def a_s_25_1(self):
        if self.pila_aux[-2].type == 'tipo_error':
            self.pila_aux[-4].type = 'tipo_error'
        elif not self.pila_aux[-4].type_func:
            self.pila_aux[-4].type = self.generar_error(self.pila_aux[-4], 'la sentencia de retorno "return" se encuentra fuera de una funcion')
        elif not self.pila_aux[-4].type_ret == self.pila_aux[-2].type:
            self.pila_aux[-4].type = self.generar_error(self.pila_aux[-4], 'la sentencia de retorno "return" intenta devolver un tipo incorrecto')
        else:
            self.pila_aux[-4].type = 'tipo_ok'
        del self.pila_aux[-3: ]

    #26: S -> = E
    def a_s_26_1(self):
        self.pila_aux[-3].type = self.pila_aux[-1].type
        del self.pila_aux[-2: ]

    #27: S -> |= E
    def a_s_27_1(self):
        if self.pila_aux[-1] == 'tipo_error':
            self.pila_aux[-3].type = 'tipo_error'
        if self.pila_aux[-1].type == 'entero':
            self.pila_aux[-3].type = 'entero'
        else:
            self.pila_aux[-3].type = self.generar_error(self.pila_aux[-3], 'Para la asignacion o logica el operando de la derecha ha de ser entero')
        del self.pila_aux[-2: ]

    #28: S -> ( L )
    def a_s_28_1(self):
        self.pila_aux[-4].type = self.pila_aux[-2].type
        del self.pila_aux[-3: ]

    #29: X ->  E
    def a_s_29_1(self):
        self.pila_aux[-2].type = self.pila_aux[-1].type
        del self.pila_aux[-1: ]

    #30: X ->  lambda
    def a_s_30_1(self):
        self.pila_aux[-2].type = 'vacio'
        del self.pila_aux[-1: ]

    #31: L -> E Q
    def a_s_31_1(self):
        if self.pila_aux[-1].type == 'tipo_error' or self.pila_aux[-2].type == 'tipo_error':
            self.pila_aux[-3].type = 'tipo_error'
        else:
            tipo = self.pila_aux[-1].type
            if self.pila_aux[-1].type == 'vacio':
                self.pila_aux[-3].type = [self.pila_aux[-2].type]
            else:
                tipo = self.pila_aux[-1].type
                tipo.insert(0, self.pila_aux[-2].type)
                self.pila_aux[-3].type = tipo
            #self.pila_aux[-3].type = [self.pila_aux[-2].type] if self.pila_aux[-1].type == 'vacio' else tipo.insert(0, self.pila_aux[-2].type)

        del self.pila_aux[-2: ]

    #32: L ->  lambda
    def a_s_32_1(self):
        self.pila_aux[-2].type = 'vacio'
        del self.pila_aux[-1: ]

    #33: Q ->  , E Q
    def a_s_33_1(self):
        if self.pila_aux[-1].type == 'tipo_error' or self.pila_aux[-2].type == 'tipo_error':
            self.pila_aux[-4].type = 'tipo_error'
        else:
            tipo = self.pila_aux[-1].type
            if self.pila_aux[-1].type == 'vacio':
                self.pila_aux[-4].type = [self.pila_aux[-2].type]
            else:
                tipo = self.pila_aux[-1].type
                tipo.insert(0, self.pila_aux[-2].type)
                self.pila_aux[-4].type = tipo

        #self.pila_aux[-4].type = self.pila_aux[-2].type if self.pila_aux[-1].type == 'vacio' else tipo.insert(0, self.pila_aux[-2].type)

        del self.pila_aux[-3: ]

    #34: Q ->  lambda
    def a_s_34_1(self):
        self.pila_aux[-2].type = 'vacio'
        del self.pila_aux[-1: ]


    #35: E -> U E2
    def a_s_35_1(self):
        if self.pila_aux[-1].type == 'tipo_error' or self.pila_aux[-2].type == 'tipo_error':
            self.pila_aux[-3].type = 'tipo_error'
        else:
            self.pila_aux[-3].type = self.pila_aux[-2].type if self.pila_aux[-1].type == 'vacio' or self.pila_aux[-2].type == 'logico' else self.generar_error(self.pila_aux[-3], 'Se esta usando el operador "&&" de forma incorrecta (al menos un dato no es logico)')

        del self.pila_aux[-2: ]

    #36: E2 -> && U E2
    def a_s_36_1(self):
        self.pila_aux[-4].type = 'logico' if self.pila_aux[-2].type == 'logico' and (self.pila_aux[-1].type == 'logico' or self.pila_aux[-1].type == 'vacio') else 'tipo_error'
        del self.pila_aux[-3: ]

    #37: E2 -> lambda
    def a_s_37_1(self):
        self.pila_aux[-2].type = 'vacio'
        del self.pila_aux[-1: ]

    #38: U -> R U2
    def a_s_38_1(self):
        if self.pila_aux[-1].type == 'tipo_error' or self.pila_aux[-1].type == 'tipo_error':
            self.pila_aux[-3].type = 'tipo_error'
        else:
            if self.pila_aux[-1].type == 'vacio':
                self.pila_aux[-3].type = self.pila_aux[-2].type
            elif self.pila_aux[-2].type == self.pila_aux[-1].type == 'entero':
                self.pila_aux[-3].type = 'logico'
            else:
                self.pila_aux[-3].type = self.generar_error(self.pila_aux[-3], 'Se esta usando el operador "<" de forma incorrecta (al menos un dato no es entero)')
        del self.pila_aux[-2: ]

    #39: U -> < R U2
    def a_s_39_1(self):
        if self.pila_aux[-1].type == 'tipo_error' or self.pila_aux[-1].type == 'tipo_error':
            self.pila_aux[-3].type = 'tipo_error'

        else:
            if self.pila_aux[-1].type == 'vacio' and self.pila_aux[-2].type == 'entero':
                self.pila_aux[-4].type = 'entero'
            elif self.pila_aux[-2].type == self.pila_aux[-1].type == 'entero':
                self.pila_aux[-4].type = 'entero'
            else:
                self.pila_aux[-4].type = self.generar_error(self.pila_aux[-4], 'Se esta usando el operador "<" de forma incorrecta (al menos un dato no es entero)')
        del self.pila_aux[-3: ]

    #40: U2 -> lambda
    def a_s_40_1(self):
        self.pila_aux[-2].type = 'vacio'
        del self.pila_aux[-1: ]

    #41: R -> V R2
    def a_s_41_1(self):
        if self.pila_aux[-1].type == 'tipo_error' or self.pila_aux[-1].type == 'tipo_error':
            self.pila_aux[-3].type = 'tipo_error'
        else:
            if self.pila_aux[-1].type == 'vacio':
                self.pila_aux[-3].type = self.pila_aux[-2].type
            elif self.pila_aux[-2].type == self.pila_aux[-1].type == 'entero':
                self.pila_aux[-3].type = 'entero'
            else:
                self.pila_aux[-3].type = self.generar_error(self.pila_aux[-3], 'Se esta usando el operador "+" de forma incorrecta (al menos un dato no es entero)')
        del self.pila_aux[-2: ]

    #42: R2 -> + V R2
    def a_s_42_1(self):
        if self.pila_aux[-1].type == 'tipo_error' or self.pila_aux[-1].type == 'tipo_error':
            self.pila_aux[-3].type = 'tipo_error'
        else:
            if self.pila_aux[-1].type == 'vacio' and self.pila_aux[-2].type == 'entero':
                self.pila_aux[-4].type = 'entero'
            elif self.pila_aux[-2].type == self.pila_aux[-1].type == 'entero':
                self.pila_aux[-4].type = 'entero'
            else:
                self.pila_aux[-4].type = self.generar_error(self.pila_aux[-4], 'Se esta usando el operador "+" de forma incorrecta (al menos un dato no es entero)')
        del self.pila_aux[-3: ]

    #43: R2 -> lambda
    def a_s_43_1(self):
        self.pila_aux[-2].type = 'vacio'
        del self.pila_aux[-1: ]

    #44: V -> ( E )
    def a_s_44_1(self):
        self.pila_aux[-4].type = self.pila_aux[-2].type
        del self.pila_aux[-3: ]

    #45: V -> id V2
    def a_s_45_1(self):
        if self.pila_aux[-1].type == 'tipo_error':
            self.pila_aux[-3].type = 'tipo_error'
        else:
            if self.pila_aux[-1].type == 'vacio':
                self.pila_aux[-3].type = self.Procesador.busca_tipo_TS(self.pila_aux[-2].pos)
            elif self.pila_aux[-1].type == self.Procesador.busca_tipo_arg(self.pila_aux[-2].pos):
                self.pila_aux[-3].type = self.Procesador.busca_tipo_ret(self.pila_aux[-2].pos)
            else:
                self.pila_aux[-3].type = self.generar_error( self.pila_aux[-3], 'Se esta intentando llamar a una funcion con un numero o tipo incorrecto de argumentos')
        del self.pila_aux[-2: ]

    #46: V -> entero
    def a_s_46_1(self):
        self.pila_aux[-2].type = 'entero'
        del self.pila_aux[-1: ]

    #47: V -> cadena
    def a_s_47_1(self):
        self.pila_aux[-2].type = 'cadena'
        del self.pila_aux[-1: ]

    #48: V2 -> lambda
    def a_s_48_1(self):
        self.pila_aux[-2].type = 'vacio'
        del self.pila_aux[-1: ]

    #49: V2 -> ( L )
    def a_s_49_1(self):
        self.pila_aux[-4].type = self.pila_aux[-2].type
        del self.pila_aux[-3: ]


class Analizador_Simantico(Acciones_Semanticas):
    
    tabla = {'P' : {'FUNCTION' : [['F', 'P', '_2'], [2]], 'IF' : [['S','P', '_3'], [3]], 'INPUT' : [['S','P', '_3'], [3]], 'PRINT': [['S','P', '_3'], [3]], 'RETURN' : [['S','P', '_3'], [3]], 'VAR' : [['D','P', '_2'], [1]], 'WHILE' : [['while', 'ABIRPAR', 'E', 'CERRARPAR', 'ABRIRLLAVE', 'C', 'CERRARLLAVE','P', '_1'], [5]], 'ID' : [['S','P', '_3'], [3]], '$' : [[], [4]]},
            'D': {'VAR' : [['_1', 'var', 'T', 'id', '_2', 'PUNTOCOMA', '_3'], [6]]},
            'T': {'BOOLEAN' : [['boolean', '_1'], [9]], 'INT' : [['int', '_1'], [7]], 'STRING' : [['string', '_1'], [8]]},
            'F' : {'FUNCTION' : [['function', '_1', 'T1', 'id', '_2', 'ABIRPAR', 'A', 'CERRARPAR' , '_3', 'ABRIRLLAVE', 'C', 'CERRARLLAVE', '_4'], [10]]},
            'T1' : {'BOOLEAN' : [['T', '_1'], [12]], 'INT': [['T', '_1'], [12]], 'STRING' : [['T', '_1'], [12]], 'ID' : [['lambda', '_1'], [11]]},
            'A': {'BOOLEAN' : [['T', 'id', '_1', 'K', '_2'], [13]], 'INT' : [['T', 'id', '_1', 'K', '_2'], [13]], 'STRING' : [['T', 'id', '_1', 'K', '_2'], [13]], 'CERRARPAR' : [['lambda', '_1'], [14]]},
            'K' : {'COMA' : [['COMA', 'T', 'id', '_1', 'K', '_2'], [16]], 'CERRARPAR' : [['lambda', '_1'], [15]]},
            'C' : {'IF' : [['_1', 'S','_2', 'C', '_3'], [18]], 'INPUT' : [['_1', 'S','_2', 'C', '_3'], [18]], 'PRINT' : [['_1', 'S','_2', 'C', '_3'], [18]], 'RETURN' : [['_1', 'S','_2', 'C', '_3'], [18]], 'VAR' : [['D', '_1', 'C', '_2'], [17]], 'WHILE' : [['while', 'ABIRPAR', 'E', 'CERRARPAR','_1', 'ABRIRLLAVE', 'C', 'CERRARLLAVE', '_2', 'C', '_3'], [19]], 'ID' : [['_1', 'S','_2', 'C', '_3'], [18]], 'CERRARLLAVE' : [['lambda', '_1'], [20]]},
            'S' : {'IF' : [['if', 'ABIRPAR', 'E', 'CERRARPAR','_1', 'S', '_2'], [24]], 'INPUT' : [['input', 'ABIRPAR', 'id', 'CERRARPAR', 'PUNTOCOMA', '_1'], [23]], 'PRINT' : [['print', 'ABIRPAR', 'E', 'CERRARPAR', 'PUNTOCOMA', '_1'], [22]], 'RETURN' : [['return', 'X', 'PUNTOCOMA', '_1'], [25]], 'ID' : [['id', 'S2', 'PUNTOCOMA', '_1'], [21]]},
            'X' : {'CINT' : [['E', '_1'], [29]], 'CADENA' : [['E', '_1'], [29]], 'ID' : [['E', '_1'], [29]], 'PUNTOCOMA' : [['lambda', '_1'], [30]], 'ABIRPAR' : [['E', '_1'], [29]]},
            'L' : {'CINT' : [['E', 'Q', '_1'], [31]], 'CADENA' : [['E', 'Q', '_1'], [31]], 'ID' : [['E', 'Q', '_1'], [31]], 'ABIRPAR' : [['E', 'Q', '_1'], [31]], 'CERRARPAR' : [['lambda', '_1'], [32]]},
            'Q' : {'COMA' : [['COMA', 'E', 'Q', '_1'], [33]], 'CERRARPAR' : [['lambda', '_1'], [34]]},
            'S2' : {'IGUAL' : [['IGUAL', 'E', '_1'], [26]], 'ASIGOLOG' : [['ASIGOLOG', 'E', '_1'], [27]], 'ABIRPAR' : [['ABIRPAR', 'L', 'CERRARPAR', '_1'], [28]]},
            'E' : {'CINT' : [['U', 'E1', '_1'], [35]], 'CADENA' : [['U', 'E1', '_1'], [35]], 'ID' : [['U', 'E1', '_1'], [35]], 'ABIRPAR' : [['U', 'E1', '_1'], [35]]},
            'E1' : {'COMA' : [['lambda', '_1'], [37]], 'PUNTOCOMA' : [['lambda', '_1'], [37]], 'CERRARPAR' : [['lambda', '_1'], [37]], 'YLOGICO' : [['YLOGICO', 'U', 'E1', '_1'], [36]]},
            'U' : {'CINT' : [['R', 'U1', '_1'], [38]], 'CADENA' : [['R', 'U1', '_1'], [38]], 'ID' : [['R', 'U1', '_1'], [38]], 'ABIRPAR' : [['R', 'U1', '_1'], [38]]},
            'U1' : {'COMA' : [['lambda', '_1'], [40]], 'PUNTOCOMA' : [['lambda', '_1'], [40]], 'CERRARPAR' : [['lambda', '_1'], [40]], 'YLOGICO' : [['lambda', '_1'], [40]], 'MENOR' : [['MENOR', 'R', 'U1', '_1'], [39]]},
            'R' : {'CINT' : [['V', 'R1', '_1'], [41]], 'CADENA' : [['V', 'R1', '_1'], [41]], 'ID' : [['V', 'R1', '_1'], [41]], 'ABIRPAR' : [['V', 'R1', '_1'], [41]]},
            'R1' : {'COMA' : [['lambda', '_1'], [43]], 'PUNTOCOMA' : [['lambda', '_1'], [43]], 'CERRARPAR' : [['lambda', '_1'], [43]],'SUMA' : [['SUMA', 'V', 'R1', '_1'], [42]], 'YLOGICO' : [['lambda', '_1'], [43]], 'MENOR' : [['lambda', '_1'], [43]]},
            'V' : {'CINT' : [['CINT', '_1'], [46]], 'CADENA' : [['cadena', '_1'], [47]], 'ID' : [['id', 'V1', '_1'], [45]], 'ABIRPAR' : [['ABIRPAR', 'E', 'CERRARPAR', '_1'], [44]]},
            'V1' : {'COMA' : [['lambda', '_1'], [48]], 'PUNTOCOMA' : [['lambda', '_1'], [48]], 'ABIRPAR' : [['ABIRPAR', 'L', 'CERRARPAR', '_1'], [49]], 'CERRARPAR' : [['lambda', '_1'], [48]],'SUMA' : [['lambda', '_1'], [48]], 'YLOGICO' : [['lambda', '_1'], [48]], 'MENOR' : [['lambda', '_1'], [48]]}
            }
    
    terminales = {'IGUAL', 'COMA', 'PUNTOCOMA', 'ABIRPAR', 'CERRARPAR', 'ABRIRLLAVE', 'CERRARLLAVE', 'YLOGICO', 'SUMA', 'MENOR', 'boolean', 'function', 'if', 
                'input', 'int', 'print', 'return', 'string', 'var', 'while', 'id', 'lambda', 'CINT', 'cadena', '$', 'ASIGOLOG'}


    arbol = []

    def __init__(self, file_name):
        Acciones_Semanticas.__init__(self, file_name)
        
    def get_transicion(self, estado):
        return self.tabla[estado][self.token[0]]

    def insertar_transicion(self, transicion):
        
        self.arbol.append(transicion[1][0])
        for i in reversed(transicion[0]):
            if i in self.tabla:
                self.pila.append(No_Terminal(i))
            elif i == 'id':
                self.pila.append(Identificador())
            else:
                if i.startswith('_'):
                    i = ''.join( ['self.a_s_', str(transicion[1][0]), i, '()'])
                self.pila.append(i)
            

    def pedir_token(self):
        self.token = self.analizador_lexico.tokennizar()

    def es_estado(self, str):
        return str in self.tabla

    def es_terminal(self, str):
        return str in self.terminales

    def syntax_error(self):
       self.Procesador.gestor_errores.generar_error('', self.analizador_lexico.numero_linea, sintactico = True, letra=self.analizador_lexico.linea + 1)


    def analizar(self):

        self.pedir_token()

        while True:
            
            X = self.pila.pop()

            #si es terminal

            if type(X).__name__ == 'Identificador':
                if type(X).__name__[:2].lower() == self.token[0].lower():
                    X.pos = int(self.token[1])
                    self.pila_aux.append(X)
                    self.pedir_token()
                else:
                    # ------------------------ ERROR ------------------------
                    # syntax_error()
                    # 
                    self.syntax_error()

            elif self.es_terminal(X):

                if X.lower() == 'lambda':
                    self.pila_aux.append(X)
                elif X.lower() == self.token[0].lower():
                    self.pila_aux.append(X)
                    self.pedir_token()
                else:
                    # ------------------------ ERROR ------------------------
                    # syntax_error()
                    # 
                    self.syntax_error()

            #si es no terminal
            elif type(X).__name__ == 'No_Terminal':

                #print(X.name)
                if X.name in self.tabla and self.token[0] in self.tabla[X.name]:
                    self.pila_aux.append(X)
                    
                    self.insertar_transicion(self.get_transicion(X.name))
                else:
                    # ------------------------ ERROR ------------------------
                    # syntax_error()
                    # 
                    self.syntax_error()

            #si no es ni terminal ni es terminal entonces es una accion semantica
            else:
                #EJUCUTA {i}
                eval(X)
              
            if X == '$':
                self.Procesador.TSG.write()
                print('\n\n-----------------------------  the end   -----------------------------\n')
                with open(self.path + 'parse_' + self.analizador_lexico.file_name + '.txt', 'w') as file:
                    for i in self.arbol:
                        file.write(str(i) + ' ')

                length = len(self.pila_aux)
                del self.pila_aux[-3: ]
                print(length - len(self.pila_aux))
                return

    def show_tree(self):
        print(self.arbol)