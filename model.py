# model.py

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from agents import EcoloidAgent
from mesa.datacollection import DataCollector

class EcoWorldModel(Model):
    def __init__(self, width, height, num_minifundios, num_pequenas, num_medias, num_latifundios, num_mata_atlantica, co2_inicial):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.co2_total = co2_inicial  # Quantidade inicial de CO2 na atmosfera

        # Inicializar as variáveis de absorção de CO2 por tipo
        self.absorcao_co2_latifundio = 0
        self.absorcao_co2_media = 0
        self.absorcao_co2_pequena = 0
        self.absorcao_co2_minifundio = 0
        self.absorcao_co2_mata = 0

        self.datacollector = DataCollector(
            model_reporters={
                "CO2_Total": "co2_total",
                "Absorção_Latifundio": lambda m: m.absorcao_co2_latifundio,
                "Absorção_Media": lambda m: m.absorcao_co2_media,
                "Absorção_Pequena": lambda m: m.absorcao_co2_pequena,
                "Absorção_Minifundio": lambda m: m.absorcao_co2_minifundio,
                "Absorção_Mata": lambda m: m.absorcao_co2_mata
            },
            agent_reporters={"Biomassa": "biomassa"}
        )

        self.ocupados = set()
        self.posicoes_livres = self.gerar_posicoes_livres()
        agente_id = 0

        # Definições dos tipos de propriedade e seus tamanhos
        definicoes_propriedades = [
            ('latifundio', num_latifundios, 4, 4),
            ('media', num_medias, 3, 3),
            ('pequena', num_pequenas, 2, 2),
            ('minifundio', num_minifundios, 1, 1)
        ]

        for tipo_propriedade, quantidade, largura, altura in definicoes_propriedades:
            for _ in range(quantidade):
                sucesso = self.colocar_propriedade(agente_id, tipo_propriedade, largura, altura)
                if sucesso:
                    agente_id += largura * altura

        # Criar Ecoloids da Mata Atlântica
        for _ in range(num_mata_atlantica):
            if len(self.posicoes_livres) == 0:
                break  # Sem posições livres restantes
            pos = self.random.choice(self.posicoes_livres)
            agente = EcoloidAgent(agente_id, self, 'Mata Atlantica', None, 'floresta')
            self.grid.place_agent(agente, pos)
            self.schedule.add(agente)
            self.ocupados.add(pos)
            self.posicoes_livres.remove(pos)
            agente_id += 1

        # O restante das células permanecerá vazio (sem agentes)

    def gerar_posicoes_livres(self):
        return [(x, y) for x in range(self.grid.width) for y in range(self.grid.height)]

    def colocar_propriedade(self, agente_id_inicial, tipo_propriedade, largura, altura):
        posicoes_necessarias = largura * altura
        if len(self.posicoes_livres) < posicoes_necessarias:
            return False

        tentativas_max = 1000
        tentativas = 0
        while tentativas < tentativas_max:
            indice = self.random.randrange(len(self.posicoes_livres))
            x_inicio, y_inicio = self.posicoes_livres[indice]
            posicoes = []
            sobreposicao = False

            for dx in range(largura):
                for dy in range(altura):
                    x = x_inicio + dx
                    y = y_inicio + dy
                    if x >= self.grid.width or y >= self.grid.height:
                        sobreposicao = True
                        break
                    pos = (x, y)
                    if pos in self.ocupados:
                        sobreposicao = True
                        break
                    posicoes.append(pos)
                if sobreposicao:
                    break

            if not sobreposicao:
                # Atribuir tipo de vegetação baseado no tipo de propriedade
                vegetacao_tipo = self.definir_vegetacao(tipo_propriedade)
                # Criar agentes para cada posição
                for i, pos in enumerate(posicoes):
                    agente_id = agente_id_inicial + i
                    agente = EcoloidAgent(agente_id, self, 'ModuloFiscal', tipo_propriedade, vegetacao_tipo)
                    self.grid.place_agent(agente, pos)
                    self.schedule.add(agente)
                self.ocupados.update(posicoes)
                for pos in posicoes:
                    if pos in self.posicoes_livres:
                        self.posicoes_livres.remove(pos)
                return True
            else:
                tentativas += 1
        return False

    def definir_vegetacao(self, tipo_propriedade):
        if tipo_propriedade == 'latifundio':
            # Latifúndios têm monoculturas ou pastagem
            opcoes_vegetacao = ['soja', 'cana_de_acucar', 'pastagem', 'gramineas', 'terra_limpa']
            return self.random.choice(opcoes_vegetacao)
        else:
            # Outras propriedades têm culturas diversificadas
            return 'diversificada'

    def step(self):
        # Inicializar as variáveis de absorção de CO2 por tipo
        self.absorcao_co2_latifundio = 0
        self.absorcao_co2_media = 0
        self.absorcao_co2_pequena = 0
        self.absorcao_co2_minifundio = 0
        self.absorcao_co2_mata = 0

        # Agentes atuam
        self.schedule.step()

        # Calcular a absorção de CO2 por tipo
        for agente in self.schedule.agents:
            absorcao = agente.biomassa * 0.1  # Fator arbitrário de absorção
            if agente.tipo == 'ModuloFiscal':
                if agente.propriedade_tipo == 'latifundio':
                    self.absorcao_co2_latifundio += absorcao
                elif agente.propriedade_tipo == 'media':
                    self.absorcao_co2_media += absorcao
                elif agente.propriedade_tipo == 'pequena':
                    self.absorcao_co2_pequena += absorcao
                elif agente.propriedade_tipo == 'minifundio':
                    self.absorcao_co2_minifundio += absorcao
            elif agente.tipo == 'Mata Atlantica':
                self.absorcao_co2_mata += absorcao

        # Atualizar quantidade de CO2 total
        absorcao_total = (
            self.absorcao_co2_latifundio +
            self.absorcao_co2_media +
            self.absorcao_co2_pequena +
            self.absorcao_co2_minifundio +
            self.absorcao_co2_mata
        )
        self.co2_total -= absorcao_total
        if self.co2_total < 0:
            self.co2_total = 0

        # Coletar dados
        self.datacollector.collect(self)