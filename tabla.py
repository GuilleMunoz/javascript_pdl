#Tabla de simbolos analizador lexico



class Tabla_Simbolos:

    def __init__(self, num, file, id = ''):
        self.num = num
        self.id = id
        self.tabla = {}
        self.file = file

    def get_lex(self, pos):
        return list(self.tabla)[pos]
    
    def insertar_lex(self, lex, tipo = ''):
        
        if self.num == 1:
            self.tabla[lex] = {'tipo' : tipo, 'argumentos': '', 'tipo_return' : '', 'despl' : 0}
            return list(self.tabla).index(lex)
        
        self.tabla[lex] = {'tipo' : tipo, 'despl' : None}
        return list(self.tabla).index(lex)


    def esta_en_tabla(self, lex):
        """ Devuelve True si esta, False si no esta """
        return lex in self.tabla

    def set_despl(self, pos, despl):
        try:
            if self.id == 'TSG':
                self.tabla[list(self.tabla)[pos]]['despl'] = despl
            else:
                self.tabla[list(self.tabla)[pos]]['despl'] = -despl
        except KeyError:
            print('no existe la posicion: %s ' % (pos))

    def set_tipo(self, pos, tipo): 
        try:
            self.tabla[list(self.tabla)[pos]]['tipo'] = tipo
        except KeyError:
            print('no existe la posicion: %s ' % (pos))
    
    def set_tipo_ret(self, pos, tipo_ret):
        try:
            self.tabla[list(self.tabla)[pos]]['tipo_return'] = tipo_ret
        except KeyError:
            print('no existe la posicion: %s ' % (pos))

    def set_args(self, pos, args):
        try:
            self.tabla[list(self.tabla)[pos]]['argumentos'] = args
        except KeyError:
            print('no existe la posicion: %s ' % (pos))

    def get_tipo(self, pos):
        try:
            return self.tabla[list(self.tabla)[pos]]['tipo']
        except KeyError:
            print('no existe la posicion: %s ' % (pos))

    def get_tipo_arg(self, pos):
        try:
            return self.tabla[list(self.tabla)[pos]]['argumentos']
        except KeyError:
            print('no existe la posicion: %s ' % (pos))

    def get_tipo_ret(self, pos):
        try:
            return self.tabla[list(self.tabla)[pos]]['tipo_return']
        except KeyError:
            print('no existe la posicion: %s ' % (pos))


    def get_pos(self, lex):
        """ Devuelve -1 si no esta en la tabla de simbolos o la posicion si esta """

        if lex in self.tabla:
            return list(self.tabla).index(lex)
        return -1
    
    def show(self):
        for key in self.tabla:
            print('CONTENIDO DE LA TABLA ', str(self.id) , '# ' , str(self.num) , ' :\n')
            print("* LEXEMA : '" + key )
            print("  ATRIBUTOS : ")
            if self.tabla[key]['tipo'] == 'funcion':
                for key2 in self.tabla[key]:
                    if key2 == 'argumentos' and type(self.tabla[key][key2]).__name__ == 'list':
                        print('         +numParam :', len(self.tabla[key][key2]))
                        j = 1
                        for i in self.tabla[key][key2]:
                            print('         +tipoParam%s : ' % str(j) + str(i) + '\n')
                            j += 1
                    else:
                        print('         +' + key2 + ': ' + str(self.tabla[key][key2]) + '\n')
            else:
                print('         +tipo :', self.tabla[key]['tipo'])
                print('         +despl :', self.tabla[key]['despl'])
            
            print('\n---------- ---------')
            print('\n')

    def write(self):
        self.file.write('CONTENIDO DE LA TABLA ' + str(self.id) + '# ' + str(self.num) + ' :\n')
        for key in self.tabla:
            self.file.write("* LEXEMA : '" + key + '\n')
            self.file.write("  ATRIBUTOS : "+ '\n')
            if self.tabla[key]['tipo'] == 'funcion':
                for key2 in self.tabla[key]:
                    if key2 == 'argumentos' and type(self.tabla[key][key2]).__name__ == 'list':
                        self.file.write('         +numParam :' + str(len(self.tabla[key][key2]))+ '\n')
                        j = 1
                        for i in self.tabla[key][key2]:
                            self.file.write('         +TipoParam%s : ' % str(j) + str(i) + '\n')
                            j += 1
                    elif key2 == 'tipo_return':
                        self.file.write('         +TipoRetorno: ' + str(self.tabla[key][key2]) + '\n')
                    elif key2 == 'despl':
                        pass
                    else:
                        self.file.write('         +' + key2 + ': ' + str(self.tabla[key][key2]) + '\n')
            else:
                self.file.write('         +tipo :' + self.tabla[key]['tipo']+ '\n')
                self.file.write('         +despl :' + str(self.tabla[key]['despl'])+ '\n')
            
            self.file.write('\n--- ---\n')
        
        self.file.write('\n---------------------------------------------------------------------------------\n\n')

    def clear_tabla(self):
        self.write()
        self.tabla.clear()
        self.num += 1

        
