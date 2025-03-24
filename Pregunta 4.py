import os
import datetime
from tabulate import tabulate  # type: ignore # Si no tienes este módulo, puedes instalarlo con: pip install tabulate

# Definición de clases
class Cliente:
    """Clase para representar a un cliente de la autoescuela."""
    
    def __init__(self, cedula, nombre, edad, sexo, referido_colegio):
        """
        Inicializa un nuevo cliente.
        
        Args:
            cedula (str): Cédula de identidad del cliente
            nombre (str): Nombre completo del cliente
            edad (int): Edad del cliente
            sexo (str): Sexo del cliente ('M' o 'F')
            referido_colegio (bool): Indica si el cliente viene referido por un colegio
        """
        self.cedula = cedula
        self.nombre = nombre
        self.edad = edad
        self.sexo = sexo
        self.referido_colegio = referido_colegio
        self.clases = []
    
    def es_menor_edad(self):
        """Verifica si el cliente es menor de edad."""
        return self.edad < 18
    
    def __str__(self):
        return f"{self.nombre} (CI: {self.cedula})"


class ClaseManejo:
    """Clase para representar una clase de manejo."""
    
    # Tarifas por tipo de vehículo
    TARIFAS = {
        "Automático": 25,
        "Sincrónico": 35
    }
    
    def __init__(self, cliente, tipo_vehiculo, horas, fecha=None):
        """
        Inicializa una nueva clase de manejo.
        
        Args:
            cliente (Cliente): El cliente que toma la clase
            tipo_vehiculo (str): Tipo de vehículo ('Automático' o 'Sincrónico')
            horas (float): Número de horas que durará la clase
            fecha (datetime.date, optional): Fecha de la clase
        """
        self.cliente = cliente
        if tipo_vehiculo not in self.TARIFAS:
            raise ValueError("Tipo de vehículo no válido. Debe ser 'Automático' o 'Sincrónico'.")
        self.tipo_vehiculo = tipo_vehiculo
        self.horas = horas
        self.fecha = fecha if fecha else datetime.date.today()
        
        # Añadir esta clase a la lista de clases del cliente
        cliente.clases.append(self)
    
    def calcular_descuento(self):
        """
        Calcula el porcentaje de descuento aplicable.
        
        Returns:
            float: Porcentaje de descuento (entre 0 y 1)
        """
        descuento = 0
        
        # Descuento por referido de colegio (25%)
        if self.cliente.referido_colegio:
            descuento += 0.25
        
        # Descuento por menor de edad (20%)
        if self.cliente.es_menor_edad():
            descuento += 0.20
        
        # Descuento por más de 3 horas (15%)
        if self.horas > 3:
            descuento += 0.15
        
        return descuento
    
    def calcular_costo_total(self):
        """
        Calcula el costo total de la clase aplicando descuentos.
        
        Returns:
            float: Costo total en USD
        """
        tarifa_base = self.TARIFAS[self.tipo_vehiculo]
        costo_base = tarifa_base * self.horas
        descuento = self.calcular_descuento()
        
        return costo_base * (1 - descuento)
    
    def generar_factura(self):
        """
        Genera un resumen de la factura para la clase.
        
        Returns:
            str: Resumen de la factura
        """
        tarifa_base = self.TARIFAS[self.tipo_vehiculo]
        costo_base = tarifa_base * self.horas
        descuento_porcentaje = self.calcular_descuento() * 100
        descuento_monto = costo_base * self.calcular_descuento()
        costo_final = self.calcular_costo_total()
        
        factura = f"""
        AUTOESCUELA "LA RÁPIDA" - FACTURA
        ---------------------------------
        Cliente: {self.cliente.nombre}
        Cédula: {self.cliente.cedula}
        Edad: {self.cliente.edad} años
        Fecha: {self.fecha.strftime('%d/%m/%Y')}
        Tipo de vehículo: {self.tipo_vehiculo}
        Tarifa: ${tarifa_base}/hora
        Horas: {self.horas}
        
        Costo base: ${costo_base:.2f}
        """
        
        # Añadir detalles de descuentos si aplican
        if self.cliente.referido_colegio:
            factura += f"Descuento por referido de colegio: 25%\n"
        
        if self.cliente.es_menor_edad():
            factura += f"Descuento por menor de edad: 20%\n"
        
        if self.horas > 3:
            factura += f"Descuento por más de 3 horas: 15%\n"
        
        factura += f"""
        Total de descuentos: {descuento_porcentaje:.2f}%
        Monto de descuento: ${descuento_monto:.2f}
        
        TOTAL A PAGAR: ${costo_final:.2f}
        """
        
        return factura


class Autoescuela:
    """Clase para gestionar la autoescuela."""
    
    def __init__(self, nombre):
        """
        Inicializa una nueva autoescuela.
        
        Args:
            nombre (str): Nombre de la autoescuela
        """
        self.nombre = nombre
        self.clientes = {}  # Diccionario: cedula -> Cliente
        self.clases = []    # Lista de ClaseManejo
    
    def registrar_cliente(self, cedula, nombre, edad, sexo, referido_colegio):
        """
        Registra un nuevo cliente en la autoescuela.
        
        Args:
            cedula (str): Cédula de identidad del cliente
            nombre (str): Nombre completo del cliente
            edad (int): Edad del cliente
            sexo (str): Sexo del cliente ('M' o 'F')
            referido_colegio (bool): Indica si el cliente viene referido por un colegio
            
        Returns:
            Cliente: El cliente registrado
        """
        if cedula in self.clientes:
            raise ValueError(f"Ya existe un cliente con la cédula {cedula}")
        
        cliente = Cliente(cedula, nombre, edad, sexo, referido_colegio)
        self.clientes[cedula] = cliente
        return cliente
    
    def obtener_cliente(self, cedula):
        """
        Obtiene un cliente por su cédula.
        
        Args:
            cedula (str): Cédula de identidad del cliente
            
        Returns:
            Cliente: El cliente con la cédula especificada, o None si no existe
        """
        return self.clientes.get(cedula)
    
    def registrar_clase(self, cedula, tipo_vehiculo, horas, fecha=None):
        """
        Registra una nueva clase de manejo.
        
        Args:
            cedula (str): Cédula de identidad del cliente
            tipo_vehiculo (str): Tipo de vehículo ('Automático' o 'Sincrónico')
            horas (float): Número de horas que durará la clase
            fecha (datetime.date, optional): Fecha de la clase
            
        Returns:
            ClaseManejo: La clase registrada
        """
        cliente = self.obtener_cliente(cedula)
        if not cliente:
            raise ValueError(f"No existe un cliente con la cédula {cedula}")
        
        clase = ClaseManejo(cliente, tipo_vehiculo, horas, fecha)
        self.clases.append(clase)
        return clase
    
    def generar_reporte_clases(self):
        """
        Genera un reporte de todas las clases.
        
        Returns:
            str: Reporte formateado de las clases
        """
        if not self.clases:
            return "No hay clases registradas"
        
        # Crear una tabla con los datos de las clases
        data = []
        for c in self.clases:
            data.append([
                c.cliente.cedula,
                c.cliente.nombre,
                c.fecha.strftime('%d/%m/%Y'),
                c.tipo_vehiculo,
                c.horas,
                f"${c.calcular_costo_total():.2f}"
            ])
        
        return tabulate(data, headers=["Cédula", "Nombre", "Fecha", "Vehículo", "Horas", "Total"])
    
    def generar_reporte_ingresos(self):
        """
        Genera un reporte de ingresos.
        
        Returns:
            str: Reporte formateado de ingresos
        """
        if not self.clases:
            return "No hay clases registradas"
        
        # Calcular ingresos totales
        total_automatico = sum(c.calcular_costo_total() for c in self.clases if c.tipo_vehiculo == "Automático")
        total_sincronico = sum(c.calcular_costo_total() for c in self.clases if c.tipo_vehiculo == "Sincrónico")
        total_general = total_automatico + total_sincronico
        
        reporte = f"""
        REPORTE DE INGRESOS - {self.nombre}
        ---------------------------------
        Total de clases: {len(self.clases)}
        
        Ingresos por vehículo Automático: ${total_automatico:.2f}
        Ingresos por vehículo Sincrónico: ${total_sincronico:.2f}
        
        TOTAL DE INGRESOS: ${total_general:.2f}
        """
        
        return reporte


# Funciones de utilidad para la interfaz de usuario
def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu_principal():
    """Muestra el menú principal."""
    limpiar_pantalla()
    print("=" * 50)
    print(f"AUTOESCUELA 'LA RÁPIDA' - SISTEMA DE CONTROL")
    print("=" * 50)
    print("1. Registrar nuevo cliente")
    print("2. Registrar clase de manejo")
    print("3. Generar factura")
    print("4. Ver clientes registrados")
    print("5. Ver reporte de clases")
    print("6. Ver reporte de ingresos")
    print("0. Salir")
    print("-" * 50)


def input_fecha():
    """
    Solicita una fecha al usuario.
    
    Returns:
        datetime.date: La fecha ingresada
    """
    while True:
        try:
            fecha_str = input("Fecha (DD/MM/AAAA): ")
            day, month, year = map(int, fecha_str.split('/'))
            return datetime.date(year, month, day)
        except ValueError:
            print("Error: Formato de fecha inválido. Utilice DD/MM/AAAA.")


def pausa():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    print("\nPresione Enter para continuar...")
    input()


# Programa principal
def main():
    # Inicializar la autoescuela
    autoescuela = Autoescuela("La Rápida")
    
    # Cargar algunos datos de prueba
    try:
        cliente1 = autoescuela.registrar_cliente("12345678", "Juan Pérez", 22, "M", False)
        cliente2 = autoescuela.registrar_cliente("87654321", "María López", 17, "F", True)
        
        # Registrar algunas clases
        clase1 = autoescuela.registrar_clase("12345678", "Automático", 2, datetime.date(2023, 5, 15))
        clase2 = autoescuela.registrar_clase("87654321", "Sincrónico", 4, datetime.date(2023, 5, 16))
    except Exception as e:
        print(f"Error al cargar datos de prueba: {e}")
    
    while True:
        mostrar_menu_principal()
        opcion = input("Ingrese una opción: ")
        
        if opcion == "1":
            # Registrar nuevo cliente
            limpiar_pantalla()
            print("REGISTRAR NUEVO CLIENTE")
            print("-" * 30)
            
            try:
                cedula = input("Cédula de identidad: ")
                nombre = input("Nombre completo: ")
                edad = int(input("Edad: "))
                sexo = input("Sexo (M/F): ").upper()
                referido = input("¿Viene referido por algún colegio? (S/N): ").upper() == "S"
                
                cliente = autoescuela.registrar_cliente(cedula, nombre, edad, sexo, referido)
                print(f"\nCliente {cliente} registrado con éxito!")
            except ValueError as e:
                print(f"\nError: {e}")
            
            pausa()
            
        elif opcion == "2":
            # Registrar clase de manejo
            limpiar_pantalla()
            print("REGISTRAR CLASE DE MANEJO")
            print("-" * 30)
            
            try:
                cedula = input("Cédula de identidad del cliente: ")
                
                if not autoescuela.obtener_cliente(cedula):
                    print(f"Error: No existe un cliente con la cédula {cedula}")
                    pausa()
                    continue
                
                print("\nTIPOS DE VEHÍCULO:")
                print("1. Automático - $25/hora")
                print("2. Sincrónico - $35/hora")
                opcion_vehiculo = input("Seleccione el tipo de vehículo (1/2): ")
                
                if opcion_vehiculo == "1":
                    tipo_vehiculo = "Automático"
                elif opcion_vehiculo == "2":
                    tipo_vehiculo = "Sincrónico"
                else:
                    print("Error: Opción no válida")
                    pausa()
                    continue
                
                horas = float(input("Número de horas para la clase: "))
                if horas <= 0:
                    print("Error: El número de horas debe ser mayor que cero")
                    pausa()
                    continue
                
                fecha = input_fecha()
                
                clase = autoescuela.registrar_clase(cedula, tipo_vehiculo, horas, fecha)
                print(f"\nClase registrada con éxito para el cliente {clase.cliente}!")
                print(f"Costo total: ${clase.calcular_costo_total():.2f}")
            except ValueError as e:
                print(f"\nError: {e}")
            
            pausa()
            
        elif opcion == "3":
            # Generar factura
            limpiar_pantalla()
            print("GENERAR FACTURA")
            print("-" * 30)
            
            if not autoescuela.clases:
                print("No hay clases registradas")
                pausa()
                continue
            
            # Mostrar lista de clases para seleccionar
            print("Clases registradas:")
            for i, clase in enumerate(autoescuela.clases, 1):
                print(f"{i}. {clase.cliente.nombre} - {clase.fecha.strftime('%d/%m/%Y')} - {clase.tipo_vehiculo}")
            
            try:
                idx = int(input("\nSeleccione el número de clase: ")) - 1
                if idx < 0 or idx >= len(autoescuela.clases):
                    print("Error: Selección no válida")
                    pausa()
                    continue
                
                clase = autoescuela.clases[idx]
                print(clase.generar_factura())
            except ValueError:
                print("Error: Entrada no válida")
            
            pausa()
            
        elif opcion == "4":
            # Ver clientes registrados
            limpiar_pantalla()
            print("CLIENTES REGISTRADOS")
            print("-" * 30)
            
            if not autoescuela.clientes:
                print("No hay clientes registrados")
            else:
                # Crear tabla de clientes
                data = []
                for cliente in autoescuela.clientes.values():
                    data.append([
                        cliente.cedula,
                        cliente.nombre,
                        cliente.edad,
                        cliente.sexo,
                        "Sí" if cliente.referido_colegio else "No",
                        len(cliente.clases)
                    ])
                
                print(tabulate(data, headers=["Cédula", "Nombre", "Edad", "Sexo", "Referido", "Clases"]))
            
            pausa()
            
        elif opcion == "5":
            # Ver reporte de clases
            limpiar_pantalla()
            print("REPORTE DE CLASES")
            print("-" * 30)
            
            print(autoescuela.generar_reporte_clases())
            
            pausa()
            
        elif opcion == "6":
            # Ver reporte de ingresos
            limpiar_pantalla()
            print("REPORTE DE INGRESOS")
            print("-" * 30)
            
            print(autoescuela.generar_reporte_ingresos())
            
            pausa()
            
        elif opcion == "0":
            # Salir
            limpiar_pantalla()
            print("¡Gracias por utilizar el Sistema de Control de Autoescuela 'La Rápida'!")
            break
        
        else:
            print("Opción no válida. Intente nuevamente.")
            pausa()


if __name__ == "__main__":
    main()