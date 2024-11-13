class AutomataFD:
    def __init__(self):
        """Inicialización del DFSM desde un archivo CSV proporcionado por el usuario."""
        self.load_csv(input("Ingrese el nombre del archivo CSV (con extensión): "))
        
    def load_csv(self, csv_path):
        """Cargar y configurar el autómata desde un archivo CSV"""
        self.csv_path = csv_path
        self.Q, self.SIGMA, self.DELTA, self.START_STATE, self.ACCEPT_STATES = self.extract_data_from_df(csv_path)
        self.ACTUAL_STATE = self.START_STATE
        self.print_info()

    def extract_data_from_df(self, csv_path):
        """Extraer datos del archivo CSV y definir Q, SIGMA, DELTA, START_STATE y ACCEPT_STATES"""
        import pandas as pd

        df = pd.read_csv(csv_path)
        
        # Definir estados y alfabeto
        Q = []
        SIGMA = list(df.columns[1:])  # Obtener el alfabeto desde la segunda columna
        
        DELTA = {}
        START_STATE = None
        ACCEPT_STATES = []

        # Definir transiciones y determinar estado inicial y de aceptación
        for index, row in df.iterrows():
            state = row[df.columns[0]].strip()  # Obtener el estado

            if state.startswith('-'):
                state = state[1:]  # Quitar el "-" del estado inicial
                START_STATE = state

            if state.startswith('*'):
                state = state[1:]  # Quitar el "*" del estado de aceptación
                ACCEPT_STATES.append(state)
            
            Q.append(state)
            DELTA[state] = {}

            for i, symbol in enumerate(SIGMA):
                DELTA[state][symbol] = row.iloc[i + 1].strip()  # Almacenar la transición
                
        return Q, SIGMA, DELTA, START_STATE, ACCEPT_STATES
    
    def iterateWord(self):
        """Pedir la cadena al usuario y verificarla en el autómata"""
        cadena = input('Ingrese una cadena elaborada con el alfabeto {}: '.format(self.SIGMA))
        
        # recorrer la cadena
        for currentChar in cadena:
            print('Estoy en el caracter: ', currentChar)
            # Validar que los caracteres de la cadena pertenezcan al alfabeto
            if currentChar not in self.SIGMA:
                print('La cadena es inválida ya que', currentChar, 'no pertenece al alfabeto {}'.format(self.SIGMA))
                return False
            
            # Verificar si la transición es correcta
            nextChar = self.DELTA[self.ACTUAL_STATE].get(currentChar, "JACHI")
            print('Me voy a: ', nextChar)

            # Verificar si no apuntó a un estado indefinido (JACHI)
            if nextChar == "JACHI":
                print('La cadena es inválida ya que entramos a un estado indefinido')
                return False
            
            print('Estoy en {} con '.format(self.ACTUAL_STATE), currentChar, 'voy a -> ', nextChar)
            # Actualizar el estado
            self.ACTUAL_STATE = nextChar

        # Verificar si la cadena es correcta o no
        if self.ACTUAL_STATE in self.ACCEPT_STATES:
            print('La cadena ', cadena, ' es válida')
            return True
        else:
            print('La cadena ', cadena, ' no es válida')
            return False 
        
    def print_info(self):
        """Imprimir estados, alfabeto y transiciones"""
        print("Estados (Q):", self.Q)
        print("Alfabeto (SIGMA):", self.SIGMA)
        print("Estado inicial:", self.START_STATE)
        print("Estados de aceptación:", self.ACCEPT_STATES)
        
        print("\nFunción de transición (DELTA):")
        print("Estado actual \t Símbolo \t Estado siguiente")
        for state in self.DELTA:
            for symbol in self.SIGMA:
                print(f"{state} \t\t {symbol} \t\t {self.DELTA[state][symbol]}")

    def menu(self):
        """Mostrar menú"""
        print('\nMenu')
        print('1. Probar otra cadena')
        print('2. Cargar nuevo archivo .csv')
        print('3. Salir')

if __name__ == "__main__":
    print("Automata de estado finito Determinista desde CSV")
    m = AutomataFD()
    m.iterateWord()

    while True:
        m.menu()
        opc = input('Seleccione una opción: ')
        if opc == '1':
            m.iterateWord()
        elif opc == '2':
            m.load_csv(input("Ingrese el nombre del nuevo archivo CSV (con extensión): "))
        elif opc == '3':
            print('Gracias por usar :)')
            break
        else:
            print(f'{opc} no es una opción válida :/')
