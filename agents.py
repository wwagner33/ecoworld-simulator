from mesa import Agent

class EcoloidAgent(Agent):
    def __init__(self, unique_id, model, area, positions):
        super().__init__(unique_id, model)
        self.area = area  # Área em módulos fiscais
        self.tipo = self.classificar_propriedade()
        self.positions = positions  # Lista de posições que o agente ocupa
        self.estado = 'inicio'  # Estado inicial
        self.ciclo = 0  # Ciclos para controlar evolução

    def classificar_propriedade(self):
        if self.area == 1:
            return 'minifundio'
        elif self.area == 4:
            return 'pequena propriedade'
        elif self.area == 9:
            return 'media propriedade'
        elif self.area == 16:
            return 'latifundio'
        else:
            return 'desconhecido'

    def step(self):
        # Evolução dos estados (pode ser ajustada conforme necessário)
        self.ciclo += 1

    def advance(self):
        print(f"Ecoloid {self.unique_id} ({self.tipo}, {self.area} módulos) no estado {self.estado}")

class AreaPreservacaoAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.estado = 'protegida'
        self.ciclo = 0

    def step(self):
        self.ciclo += 1

    def advance(self):
        print(f"Área de Preservação {self.unique_id} no ciclo {self.ciclo}, estado: {self.estado}")

class ViaComunicacaoAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.estado = 'ativa'
        self.ciclo = 0

    def step(self):
        self.ciclo += 1

    def advance(self):
        print(f"Via de Comunicação {self.unique_id} no ciclo {self.ciclo}, estado: {self.estado}")
