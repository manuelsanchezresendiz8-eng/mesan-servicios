# core/inventario.py

class InventoryManager:
    """
    Gestiona el cálculo automático de insumos basado en metros cuadrados y servicios.
    """
    def __init__(self):
        # Ratios de consumo (ajustables según necesidad)
        self.ratios = {
            "quimico": 0.015, # Litros por m2
            "bolsas": 1.1, # Unidades por servicio
            "guantes": 0.8, # Pares por servicio
            "toallas": 0.3 # Unidades por servicio
        }

    def calcular_consumo(self, metros_cuadrados, servicios):
        consumo = {}

        for item, ratio in self.ratios.items():
            if item == "quimico":
                # Cálculo por área
                consumo[item] = round(ratio * metros_cuadrados, 2)
            else:
                # Cálculo por cantidad de servicios/turnos
                consumo[item] = round(ratio * servicios, 2)

        return consumo
