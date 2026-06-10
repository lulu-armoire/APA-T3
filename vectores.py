class Vector:
    
    # Estandares universales
    
    """
    Classe para representar vectores y operaciones vectoriales
    """
    def __init__(self, iterable):
        """
        Constructor de Vector.
        Args: iterable (lista, tupla, etc.): coordenadas del vector
        """
        self.coordenadas = list(iterable)  # Convertimos a lista por si es tupla
    
    def __repr__(self):
        """
        Representación oficial del vector para depuración
        """
        return f"Vector({self.coordenadas})"
    
    def __str__(self):
        """
        Representación amigable para el usuario
        """
        return str(self.coordenadas)
    
    def __len__(self):
        """
        Devuelve la dimensión del vector
        """
        return len(self.coordenadas)
    
    def __getitem__(self, i):
        """
        Permite acceder a v[i] para obtener la coordenada i
        """
        return self.coordenadas[i]
    
    def __eq__(self, other):
        """
        Compara dos vectores para igualdad
        """
        if not isinstance(other, Vector):
            return False
        return self.coordenadas == other.coordenadas

# Inicio Tarea 
    
    def __mul__(self, other):
        """
        Multiplica un vector por un escalar o realiza el producto de Hadamard.

        Args:
            other (int, float o Vector): Si es número, multiplica cada coordenada.
                                    Si es Vector, multiplica elemento a elemento.

        Salida:
            Vector: Nuevo vector con el resultado.

        """
        # Caso 1: multiplicación escalar
        if isinstance(other, (int, float)):
            nuevas = []
            for x in self.coordenadas: # recorremos cada coordenada
                nuevas.append(x * other) # multiplicamos y añadimos
            return Vector(nuevas)
    
        # Caso 2: multiplicación por otro vector (Hadamard)
        if isinstance(other, Vector): # si other es un vector
            nuevas = []
            for i in range(len(self.coordenadas)):
                nuevas.append(self.coordenadas[i] * other.coordenadas[i])
            return Vector(nuevas)
    
        raise TypeError("No se puede multiplicar")
    
# Ahora creamos __rmul__ por si encontramos un caso que sea 2 * v1. Python como empieza a leer por la izquierda, primero intenta con (2).__mul__(v1) y falla. Entonces, automáticamente, prueba con v1.__rmul__(2). Por eso necesitamos __rmul__, para que el vector sepa multiplicarse cuando el número está a la izquierda

    def __rmul__(self, other):
        """
        Multiplica un escalar por un vector (operación conmutativa).

        Args:
            other (int, float): Escalar que multiplica al vector.

        Salida:
            Vector: Nuevo vector con cada coordenada multiplicada por el escalar.
        """
        return self.__mul__(other)   # Reutiliza __mul__ 

    def __matmul__(self, other):
        """
        Calcula el producto escalar de dos vectores usando el operador @.

        Args:
            other (Vector): Segundo vector.

        Salida:
            float or int: Suma de los productos elemento a elemento.
        """
        # Solo se puede multiplicar vector por vector
        if not isinstance(other, Vector):
            raise TypeError(f"No se puede hacer producto escalar de Vector con algo que no sea otro vector")
    
        # Comprobar dimensión
        if len(self.coordenadas) != len(other.coordenadas):
            raise ValueError("Los vectores deben tener la misma dimensión")
    
        # Hacemos la suma de productos
        resultado = 0  
        for i in range(len(self.coordenadas)):
            resultado = resultado + (self.coordenadas[i] * other.coordenadas[i])
        
        return resultado

    def __rmatmul__(self, other):
        """
        Producto escalar con escalar a la izquierda (no permitido)

        Args:
            other: Cualquier tipo (número, etc.)

        Salida:
            None: No retorna nada
        """
        raise TypeError(f"No se puede hacer producto escalar de {type(other)} con Vector")

    def __floordiv__(self, other):
        """
        Calcula la componente paralela de un vector respecto a otro

        Args:
            other (Vector): Vector de referencia para la proyección

        Salida:
            Vector: Componente tangencial (paralela) de self respecto a other
        """
        if not isinstance(other, Vector): # Si other NO es un Vector
            raise TypeError("// solo puede ser entre vectores")

        # calcular producto escalar v1 · v2
        producto_escalar = 0
        for i in range(len(self.coordenadas)):
            producto_escalar = producto_escalar + (self.coordenadas[i] * other.coordenadas[i])
        # v2 al cuadrado 
        v2_cuadrado = 0
        for i in range(len(other.coordenadas)):
            v2_cuadrado = v2_cuadrado + (other.coordenadas[i] * other.coordenadas[i])

        # comprovar que v2 no sea 0 
        if v2_cuadrado == 0:
            raise TypeError("No se puede proyectar sobre el vector cero")

        # Calcular factor
        factor = producto_escalar / v2_cuadrado

        # Multiplicar cada coordenada de other por el factor
        nuevas_coordenadas = []
        for i in range(len(other.coordenadas)):
            nuevas_coordenadas.append(other.coordenadas[i] * factor)
    
        return Vector(nuevas_coordenadas)

    def __rfloordiv__(self, other):
        """ 
        Evita que se haga la operacion entre algo que no son dos vectores
        """
        raise TypeError(f"No se puede hacer //")

    def __mod__(self, other):
        """
        Calcula la componente perpendicular de un vector respecto a otro.

        Args:
             other (Vector): Vector de referencia.

        Salida:
            Vector: Componente normal (perpendicular) de self respecto a other
        """
        if not isinstance(other, Vector):
            raise TypeError("% solo entre Vectores")
    
        # Calculamos la componente paralela usando //
        paralela = self // other
    
        # Restamos v1 - v1∥
        nuevas_coordenadas = []
        for i in range(len(self.coordenadas)):
            nuevas_coordenadas.append(self.coordenadas[i] - paralela.coordenadas[i])
    
        return Vector(nuevas_coordenadas)

    def __rmod__(self, other):
        """
        Evita que se haga la operacion entre algo que no son dos vectores
        """
        raise TypeError(f"No se puede hacer % con {type(other)} y Vector")


# test unitarios
if __name__ == '__main__':
    import unittest

    class TestVector(unittest.TestCase):
        
        def test_multiplicacion_escalar(self):
            v1 = Vector([1, 2, 3])
            resultado = v1 * 2
            self.assertEqual(resultado, Vector([2, 4, 6]))
        
        def test_producto_hadamard(self):
            v1 = Vector([1, 2, 3])
            v2 = Vector([4, 5, 6])
            resultado = v1 * v2
            self.assertEqual(resultado, Vector([4, 10, 18]))
        
        def test_rmul_escalar(self):
            v1 = Vector([1, 2, 3])
            resultado = 2 * v1
            self.assertEqual(resultado, Vector([2, 4, 6]))
        
        def test_producto_escalar(self):
            v1 = Vector([1, 2, 3])
            v2 = Vector([4, 5, 6])
            resultado = v1 @ v2
            self.assertEqual(resultado, 32)
        
        def test_componente_paralela(self):
            v1 = Vector([2, 1, 2])
            v2 = Vector([0.5, 1, 0.5])
            resultado = v1 // v2
            esperado = Vector([1.0, 2.0, 1.0])
            for a, b in zip(resultado.coordenadas, esperado.coordenadas):
                self.assertAlmostEqual(a, b)
        
        def test_componente_perpendicular(self):
            v1 = Vector([2, 1, 2])
            v2 = Vector([0.5, 1, 0.5])
            resultado = v1 % v2
            esperado = Vector([1.0, -1.0, 1.0])
            for a, b in zip(resultado.coordenadas, esperado.coordenadas):
                self.assertAlmostEqual(a, b)
        
        def test_composicion(self):
            v1 = Vector([2, 1, 2])
            v2 = Vector([0.5, 1, 0.5])
            paralela = v1 // v2
            perpendicular = v1 % v2
            suma = Vector([a + b for a, b in zip(paralela.coordenadas, perpendicular.coordenadas)])
            self.assertEqual(v1, suma)
    
    unittest.main(verbosity=2)