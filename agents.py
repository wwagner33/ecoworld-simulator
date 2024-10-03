# agents.py

from mesa import Agent

class EcoloidAgent(Agent):
    def __init__(self, unique_id, model, tipo, propriedade_tipo, vegetacao_tipo):
        super().__init__(unique_id, model)
        self.tipo = tipo  # 'ModuloFiscal' ou 'Mata Atlantica'
        self.propriedade_tipo = propriedade_tipo  # 'latifundio', 'media', 'pequena', 'minifundio', None
        self.vegetacao_tipo = vegetacao_tipo  # Tipo de vegetação
        self.biomassa = self.calcular_biomassa()

    def calcular_biomassa(self):
        # Valores de biomassa baseados no tipo de vegetação (valores hipotéticos)
        biomassa_valores = {
            'soja': 2.5,
            'cana_de_acucar': 4.0,
            'diversificada': 3.0,
            'pastagem': 1.5,
            'gramineas': 1.0,
            'terra_limpa': 0.0,
            'floresta': 5.0
        }
        return biomassa_valores.get(self.vegetacao_tipo, 0.0)

    def step(self):
        # Aqui poderíamos implementar comportamentos futuros do agente
        pass