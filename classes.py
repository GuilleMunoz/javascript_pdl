import os
from tabla import Tabla_Simbolos
from error import GestorErrores

class Procesador:


    despl_G = 0
    despl_L = 0

    def __init__(self, path, file_name):
        self.tabla_actual = 'TSG'
        self.file = open(path + 'tabla_' + file_name + '.txt', 'w')
        self.TSG = Tabla_Simbolos(1, self.file, id = 'TSG')
        self.TSL = Tabla_Simbolos(2, self.file)
        self.gestor_errores = GestorErrores(path + file_name + '.txt')
    
    flag_decl = False # flag_decl = True <=> se esta declarando

    #devuelve -1 sin no esta en la tabla de simbolos actual y 
    #el indice si esta
    def get_pos_TS_actual(self, lex):
        """Devuelve la posicion de lex si esta en la tabla actual -1 si no esta """

        if self.tabla_actual == 'TSG':
            return self.TSG.get_pos(lex)
        else:
            return self.TSL.get_pos(lex)

    def get_pos_en_TS(self, lex):
        """Devuelve la posicion + 1 si esta en TSG , -(pos + 1) si esta en TSL o 0 si no esta en ninguna"""
        pos = self.TSG.get_pos(lex)
        
        if pos == -1:
            pos = self.TSL.get_pos(lex)
            if pos == -1:
                return 0
            else:
                return -(pos + 1)

        else:
            return pos + 1

    def insertar_en_TS_actual(self, lex, tipo = ''):
        if self.tabla_actual == 'TSG':
            return self.TSG.insertar_lex(lex, tipo) + 1
        return -( self.TSL.insertar_lex(lex, tipo) + 1)

    def busca_tipo_TS(self, pos):
        if pos < 0:
            return self.TSL.get_tipo(-pos - 1)
        
        return self.TSG.get_tipo(pos - 1)
        

    def insertar_Tipo_TS(self, pos, tipo):
        if pos < 0:
            return self.TSL.set_tipo(- pos - 1, tipo)
        
        return self.TSG.set_tipo(pos - 1, tipo)

    def insertar_Despl_TS(self, pos):
        if pos < 0:
            return self.TSL.set_despl(- pos - 1, self.despl_L)
        
        return self.TSG.set_despl(pos - 1,self.despl_G)

    def insertar_tipo_ret(self, pos, tipo_ret):
        self.TSG.set_tipo_ret(pos - 1, tipo_ret)
    
    def insertar_args(self, pos, args):
        self.TSG.set_args(pos - 1, args)

    def busca_tipo_arg(self, pos):
        return self.TSG.get_tipo_arg(pos - 1)

    def busca_tipo_ret(self, pos):
        return self.TSG.get_tipo_ret(pos - 1)


class No_Terminal:

    def __init__(self, name):

        self.name = name
        self.type = None
        self.type_ret = None
        self.type_func = False
        self.type_err = False
        self.err_name = ''
    
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name 


    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type


    @property
    def type_ret(self):
        return self.__type_ret

    @type_ret.setter
    def type_ret(self, type_ret):
        self.__type_ret = type_ret


    @property
    def type_func(self):
        return self.__type_func

    @type_func.setter
    def type_func(self, type_func):
        self.__type_func = type_func

    @property
    def type_err(self):
        return self.__type_err
    
    @type_err.setter
    def type_err(self, type_err):
        self.__type_err = type_err


    @property
    def err_name(self):
        return self.__err_name

    @err_name.setter
    def err_name(self, err_name):
        self.__err_name = err_name
       

class Identificador:

    def __init__(self, pos = -1):
        self.pos = pos

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos):
        self.__pos = pos