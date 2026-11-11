# ==============================================================================
# Autor: Wilson Fabián Ramírez Joya
# Programa: Ingeniería Electrónica
# Curso: Programación (213023) - UNAD
# Fase 4: Componente Práctico - Sistema Integral Software FJ
# ==============================================================================

from abc import ABC, abstractmethod      # Se importa el módulo ABC para crear clases abstractas.
import datetime                          # Se importa datetime para manejar fechas en los registros y logs.
import traceback                         # Se importa traceback para registrar el historial completo de los errores.

# ------------------------------------------------------------------------------
# 1. MANEJO DE ARCHIVOS (LOGS) Y EXCEPCIONES PERSONALIZADAS
# ------------------------------------------------------------------------------
def registrar_error_log(mensaje, excepcion=None):  # Función para escribir los errores en un archivo de texto plano.
    fecha_actual = datetime.datetime.now()         # Se obtiene la fecha y hora exacta del error.
    # Se abre el archivo 'errores.log' en modo 'a' (append) para no borrar los registros anteriores.
    with open("errores.log", "a", encoding="utf-8") as archivo_log: 
        archivo_log.write(f"[{fecha_actual}] ERROR: {mensaje}\n") # Se escribe la cadena formateada en el archivo.
        if excepcion:                              # Si se pasó un objeto de excepción, se procede a registrar sus detalles.
            archivo_log.write(f"Detalle técnico: {str(excepcion)}\n") # Se escribe el texto directo de la excepción.
            archivo_log.write(traceback.format_exc() + "\n")          # Se escribe la traza completa (pila de llamadas).

class ErrorValidacionCliente(Exception):           # Excepción personalizada que hereda de la clase base Exception.
    def __init__(self, mensaje):                   # Constructor de la excepción.
        super().__init__(mensaje)                  # Llama al constructor de la clase padre.
        registrar_error_log(f"ErrorValidacionCliente: {mensaje}") # Al instanciarse, registra automáticamente el error en el log.

class ErrorServicioNoDisponible(Exception):        # Excepción personalizada para servicios inexistentes o fallos en servicios.
    def __init__(self, mensaje):                   # Constructor de la excepción.
        super().__init__(mensaje)                  # Llama al constructor padre.
        registrar_error_log(f"ErrorServicioNoDisponible: {mensaje}") # Registra el evento en el archivo de texto.

class ErrorReservaInvalida(Exception):             # Excepción personalizada para fallos lógicos en las reservas.
    def __init__(self, mensaje, causa=None):       # Constructor que acepta un mensaje y una causa (encadenamiento).
        super().__init__(mensaje)                  # Llama al constructor padre.
        registrar_error_log(f"ErrorReservaInvalida: {mensaje}", causa) # Escribe el error y la traza de la causa si existe.
        class ErrorCancelacionInvalida(Exception):
    """Excepción personalizada para errores en la cancelación o gestión de estados de reservas."""
    def __init__(self, mensaje, causa=None):
        super().__init__(mensaje)
        registrar_error_log(f"ErrorCancelacionInvalida: {mensaje}", causa)

# ------------------------------------------------------------------------------
# 2. CLASES ABSTRACTAS (ABSTRACCIÓN Y HERENCIA)
# ------------------------------------------------------------------------------
class EntidadGeneral(ABC):                         # Clase abstracta base que obliga a implementar polimorfismo.
    @abstractmethod                                # Decorador que define un método abstracto obligatorio.
    def mostrar_detalles(self):                    # Método que las clases hijas deberán sobrescribir.
        pass                                       # El método abstracto no lleva lógica en la clase padre.

class Servicio(EntidadGeneral):                    # Clase abstracta para servicios que hereda de EntidadGeneral.
    def __init__(self, id_servicio, nombre, tarifa_base): # Constructor de Servicio.
        self._id_servicio = id_servicio            # Atributo protegido (encapsulamiento parcial).
        self._nombre = nombre                      # Atributo protegido para el nombre del servicio.
        self._tarifa_base = tarifa_base            # Atributo protegido para el valor monetario base.

    @property                                      # Decorador para acceder al ID como propiedad.
    def id_servicio(self):                         # Método getter del ID del servicio.
        return self._id_servicio                   # Retorna el ID protegido.

    @property                                      # Decorador getter para el nombre.
    def nombre(self):                              # Método que devuelve el nombre.
        return self._nombre                        # Retorna el atributo protegido.

    @abstractmethod                                # Método abstracto para forzar el cálculo especializado de costos.
    def calcular_costo(self, cantidad, descuento=0, impuesto=0): # Se simula SOBRECARGA mediante parámetros por defecto.
        pass                                       # Sin implementación, delegada a las subclases.

# ------------------------------------------------------------------------------
# 3. CLASES DERIVADAS Y ENCAPSULAMIENTO
# ------------------------------------------------------------------------------
class Cliente(EntidadGeneral):                     # Clase Cliente que hereda de EntidadGeneral.
    def __init__(self, identificacion, nombre, correo): # Constructor del cliente.
        self.__identificacion = identificacion     # Atributo PRIVADO (encapsulamiento estricto).
        self.__nombre = nombre                     # Atributo PRIVADO para el nombre.
        self.__correo = correo                     # Atributo PRIVADO para el correo.

    @property                                      # Getter para la identificación.
    def identificacion(self):                      # Método que permite lectura segura del atributo privado.
        return self.__identificacion               # Retorna la identificación.

    @property                                      # Getter para el nombre.
    def nombre(self):                              # Método de lectura del nombre.
        return self.__nombre                       # Retorna el nombre privado.

    def mostrar_detalles(self):                    # Implementación del método abstracto de EntidadGeneral (POLIMORFISMO).
        return f"Cliente: {self.__nombre} - ID: {self.__identificacion} - Correo: {self.__correo}" # Retorna cadena formateada.

class ServicioSala(Servicio):                      # Clase derivada de Servicio para alquiler de salas.
    def calcular_costo(self, horas, descuento=0, impuesto=0): # Sobrescribe el cálculo abstracto (POLIMORFISMO).
        if horas <= 0:                             # Valida que el tiempo lógico no sea negativo o cero.
            raise ValueError("Las horas de reserva de sala deben ser mayores a 0.") # Lanza un error nativo si no se cumple.
        costo_base = self._tarifa_base * horas     # Multiplica la tarifa por el tiempo consumido.
        costo_descuento = costo_base - (costo_base * (descuento / 100)) # Resta el porcentaje del descuento.
        costo_total = costo_descuento + (costo_descuento * (impuesto / 100)) # Suma el porcentaje del impuesto.
        return round(costo_total, 2)               # Retorna el valor redondeado a dos decimales.

    def mostrar_detalles(self):                    # Sobrescribe mostrar_detalles para la Sala.
        return f"Servicio de Sala [ID: {self._id_servicio}] - {self._nombre} - Tarifa/hora: ${self._tarifa_base}" # Retorna detalles.

class ServicioEquipo(Servicio):                    # Clase derivada de Servicio para alquiler de equipos de cómputo.
    def calcular_costo(self, dias, descuento=0, impuesto=0): # Sobrescribe método, adaptado a días.
        if dias <= 0:                              # Valida que los días lógicos no sean negativos.
            raise ValueError("Los días de alquiler deben ser mayores a 0.") # Lanza error nativo.
        costo_base = self._tarifa_base * dias      # Calcula en base a días.
        costo_final = (costo_base - (costo_base * (descuento / 100))) * (1 + (impuesto / 100)) # Ecuación factorizada del costo.
        return round(costo_final, 2)               # Retorna valor con 2 decimales.

    def mostrar_detalles(self):                    # Sobrescribe mostrar_detalles.
        return f"Servicio de Equipo [ID: {self._id_servicio}] - {self._nombre} - Tarifa/Día: ${self._tarifa_base}" # Retorna info.

class ServicioAsesoria(Servicio):                  # Clase derivada para asesorías especializadas.
    def calcular_costo(self, sesiones, descuento=0, impuesto=0): # Sobrescribe método basado en número de sesiones.
        if sesiones <= 0:                          # Valida sesiones válidas.
            raise ValueError("La cantidad de sesiones debe ser mayor a 0.") # Error lógico.
        costo = (self._tarifa_base * sesiones)     # Costo inicial.
        costo -= (costo * (descuento / 100))       # Aplica descuento (asignación con resta).
        costo += (costo * (impuesto / 100))        # Aplica impuesto (asignación con suma).
        return round(costo, 2)                     # Retorna valor monetario.

    def mostrar_detalles(self):                    # Polimorfismo en la salida de datos.
        return f"Servicio de Asesoría [ID: {self._id_servicio}] - {self._nombre} - Tarifa/Sesión: ${self._tarifa_base}" # Cadena final.

# ------------------------------------------------------------------------------
# 4. CLASE RESERVA Y LÓGICA DE NEGOCIO
# ------------------------------------------------------------------------------
class Reserva:                                     # Clase para integrar clientes y servicios.
    contador_reservas = 1                          # Atributo de clase (estático) para auto-incrementar IDs.

    def __init__(self, cliente, servicio, cantidad_tiempo): # Constructor de la reserva.
        self.id_reserva = Reserva.contador_reservas # Asigna el ID actual estático.
        Reserva.contador_reservas += 1             # Incrementa el contador para la próxima instancia.
        self.cliente = cliente                     # Asocia el objeto Cliente.
        self.servicio = servicio                   # Asocia el objeto Servicio (Asociación/Agregación).
        self.cantidad_tiempo = cantidad_tiempo     # Asocia la cantidad de uso (horas, días, etc.).
        self.estado = "Pendiente"                  # Estado inicial de la reserva.
        self.costo_total = 0                       # Inicializa el costo en cero.

    def confirmar(self, descuento=0, impuesto=0):  # Método para validar y procesar el cobro.
        try:                                       # Inicia bloque TRY para controlar excepciones durante el cálculo.
            # Llama al método polimórfico calcular_costo del servicio asociado.
            self.costo_total = self.servicio.calcular_costo(self.cantidad_tiempo, descuento, impuesto)
            self.estado = "Confirmada"             # Si pasa sin errores, cambia el estado a Confirmada.
            print(f"Reserva {self.id_reserva} confirmada con éxito. Costo: ${self.costo_total}") # Imprime éxito.
        except ValueError as e:                    # Captura el error nativo lanzado por cantidades negativas.
            self.estado = "Error en Confirmación"  # Marca la reserva con error.
            # ENCADENAMIENTO DE EXCEPCIONES: Lanza un error personalizado basado en el ValueError original ('from e').
            raise ErrorReservaInvalida(f"Fallo al confirmar reserva {self.id_reserva}.", causa=e) from e

# ------------------------------------------------------------------------------
# 5. SISTEMA GESTOR Y SIMULACIÓN (10 OPERACIONES DE PRUEBA)
# ------------------------------------------------------------------------------
class SistemaGestor:                               # Clase principal que administra las listas en memoria.
    def __init__(self):                            # Constructor del sistema.
        self.clientes = []                         # Lista en memoria para almacenar objetos Cliente (sustituye BD).
        self.servicios = []                        # Lista para objetos Servicio.
        self.reservas = []                         # Lista para objetos Reserva.

    def registrar_cliente(self, identificacion, nombre, correo): # Método para agregar clientes nuevos.
        print(f"\n--- Intentando registrar cliente: {nombre} ---") # Traza en consola.
        try:                                       # Inicio de bloque TRY/EXCEPT/ELSE/FINALLY (Requisito estricto).
            if not identificacion or not nombre:   # Valida que los datos obligatorios no estén vacíos.
                raise ErrorValidacionCliente("La identificación y el nombre no pueden estar vacíos.") # Lanza excepción propia.
            nuevo_cliente = Cliente(identificacion, nombre, correo) # Instancia el objeto Cliente.
            self.clientes.append(nuevo_cliente)    # Agrega a la lista.
        except ErrorValidacionCliente as e:        # Atrapa la excepción específica generada arriba.
            print(f"❌ FALLO CAPTURADO: {e}")        # Notifica al usuario del fallo controlado.
        else:                                      # Bloque ELSE: Se ejecuta ÚNICAMENTE si el bloque TRY fue exitoso.
            print(f"✅ ÉXITO: Cliente {nuevo_cliente.nombre} registrado correctamente.") # Confirmación de alta.
        finally:                                   # Bloque FINALLY: Se ejecuta SIEMPRE, haya error o no.
            print("[Info] Operación de registro de cliente finalizada.") # Mensaje de cierre del proceso.

    def buscar_cliente(self, identificacion):      # Método de apoyo para buscar en la lista.
        for c in self.clientes:                    # Itera sobre la lista de clientes.
            if c.identificacion == identificacion: # Compara la ID solicitada con la privada expuesta por el getter.
                return c                           # Retorna el objeto si coincide.
        return None                                # Retorna None si no existe.

    def buscar_servicio(self, id_servicio):        # Método de apoyo para buscar servicios.
        for s in self.servicios:                   # Itera los servicios registrados.
            if s.id_servicio == id_servicio:       # Si coinciden los ID.
                return s                           # Retorna el objeto servicio.
        return None                                # Retorna None si no existe.

    def registrar_reserva(self, id_cliente, id_servicio, cantidad, desc=0, imp=0): # Función compleja para reservar.
        print(f"\n--- Procesando Reserva (Cliente: {id_cliente}, Servicio: {id_servicio}) ---") # Traza.
        try:                                       # Intento de construir la reserva.
            cliente = self.buscar_cliente(id_cliente) # Busca el objeto cliente.
            if not cliente:                        # Si el cliente no está en la lista.
                raise ErrorReservaInvalida("Cliente no encontrado en el sistema.") # Dispara error personalizado.

            servicio = self.buscar_servicio(id_servicio) # Busca el servicio.
            if not servicio:                       # Si el servicio no existe.
                raise ErrorServicioNoDisponible(f"El servicio con ID {id_servicio} no existe.") # Dispara error de servicio.

            nueva_reserva = Reserva(cliente, servicio, cantidad) # Instancia la reserva si todo existe.
            self.reservas.append(nueva_reserva)    # Agrega la reserva a la lista.
            nueva_reserva.confirmar(descuento=desc, impuesto=imp) # Intenta calcular costos y confirmar.
            
        except ErrorReservaInvalida as e:          # Captura error de reservas o cliente inexistente.
            print(f"❌ ERROR RESERVA: {e}")          # Imprime el error.
        except ErrorServicioNoDisponible as e:     # Captura error de servicio no encontrado.
            print(f"❌ ERROR SERVICIO: {e}")         # Imprime el error.
        except Exception as e:                     # Captura cualquier otra anomalía inesperada.
            print(f"❌ ERROR INESPERADO: {e}")       # Imprime advertencia general.
        else:                                      # Si todo sale bien.
            print("✅ ÉXITO: Todo el proceso de reserva se ejecutó sin anomalías.") # Confirma.

def cancelar_reserva(self, id_reserva):
        """Método analítico del estudiante para cancelar una reserva existente aplicando validaciones y manejo de errores."""
        print(f"\n--- Intentando cancelar la Reserva ID: {id_reserva} ---")
        try:
            reserva_encontrada = None
            for r in self.reservas:
                if r.id_reserva == id_reserva:
                    reserva_encontrada = r
                    break
            
            if not reserva_encontrada:
                raise ErrorCancelacionInvalida(f"No se encontró ninguna reserva con el ID {id_reserva}.")
            
            if reserva_encontrada.estado == "Cancelada":
                raise ErrorCancelacionInvalida(f"La reserva {id_reserva} ya se encuentra cancelada previamente.")
                
            reserva_encontrada.estado = "Cancelada"
            reserva_encontrada.costo_total = 0.0
        except ErrorCancelacionInvalida as e:
            print(f"❌ ERROR CANCELACIÓN: {e}")
        else:
            print(f"✅ ÉXITO: Reserva {id_reserva} cancelada y costo recalculado correctamente.")
        finally:
            print("[Info] Proceso de cancelación finalizado.")
            
# --- EJECUCIÓN PRINCIPAL (Simulación de las 10 operaciones exigidas) ---
if __name__ == "__main__":                         # Punto de entrada estándar en Python.
    # Instanciamos el sistema general
    sistema = SistemaGestor()                      # Se crea el objeto gestor.

    # Precargamos los servicios disponibles en el inventario del sistema
    sistema.servicios.append(ServicioSala("S01", "Sala de Juntas VIP", 50000))       # Agrega un servicio de Sala.
    sistema.servicios.append(ServicioEquipo("E01", "Portátil Core i7", 85000))       # Agrega un servicio de Equipo.
    sistema.servicios.append(ServicioAsesoria("A01", "Auditoría de Software", 200000)) # Agrega un servicio de Asesoría.

    print("\n" + "="*50)                           # Decoración de terminal.
    print(" INICIO DE SIMULACIÓN - SOFTWARE FJ ")  # Título en consola.
    print("="*50)                                  # Decoración de terminal.

    # Operación 1: Registro Válido (TRY/ELSE/FINALLY exitoso)
    sistema.registrar_cliente("1001", "Carlos Pérez", "cperez@mail.com") 

    # Operación 2: Registro Inválido (Excepción personalizada capturada en bloque EXCEPT)
    sistema.registrar_cliente("", "", "fantasma@mail.com") 

    # Operación 3: Registro Válido
    sistema.registrar_cliente("1002", "Ana Gómez", "agomez@mail.com")

    # Operación 4: Reserva Válida (Usa parámetros por defecto)
    sistema.registrar_reserva("1001", "S01", 3)

    # Operación 5: Reserva Válida (Emulación de sobrecarga, envía descuento e impuesto)
    sistema.registrar_reserva("1002", "E01", 5, desc=10, imp=19)

    # Operación 6: Reserva Inválida (Cliente no existe - dispara ErrorReservaInvalida)
    sistema.registrar_reserva("9999", "A01", 2)

    # Operación 7: Reserva Inválida (Servicio no existe - dispara ErrorServicioNoDisponible)
    sistema.registrar_reserva("1001", "X99", 4)

    # Operación 8: Reserva Inválida (Cantidad negativa - dispara ValueError y encadena a ErrorReservaInvalida)
    sistema.registrar_reserva("1002", "S01", -2)

    # Operación 9: Lectura de las entidades (Demostración de polimorfismo en listados válidos)
    print("\n--- Reporte de Clientes Registrados ---") # Cabecera reporte clientes.
    for c in sistema.clientes:                     # Itera la memoria.
        print(c.mostrar_detalles())                # Llama método polimórfico del cliente.

    # Operación 10: Lectura de las reservas
    print("\n--- Reporte de Reservas Existentes ---")  # Cabecera reporte reservas.
    for r in sistema.reservas:                     # Itera la lista.
        # Demuestra que el programa no se detuvo por los errores, sino que siguió ejecutando e imprimiendo la data.
        print(f"Reserva {r.id_reserva} | Estado: {r.estado} | {r.cliente.nombre} | {r.servicio.nombre} | Costo: ${r.costo_total}")
        
    # Operación 11: Aporte Individual - Prueba de cancelación válida
    sistema.cancelar_reserva(1)

    # Operación 12: Aporte Individual - Prueba de cancelación con error controlado
    sistema.cancelar_reserva(999)    
