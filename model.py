from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from agents import EcoloidAgent, AreaPreservacaoAgent, ViaComunicacaoAgent
from mesa.datacollection import DataCollector

class EcoWorldModel(Model):
    def __init__(
        self,
        width,
        height,
        num_minifundios,
        num_pequenas,
        num_medias,
        num_latifundios,
        num_preservacoes,
        num_vias
    ):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)  # Grid não-toroidal
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.datacollector = DataCollector(
            {
                "Latifundios": lambda m: self.count_type(m, 'latifundio'),
                "Médias Propriedades": lambda m: self.count_type(m, 'media propriedade'),
                "Pequenas Propriedades": lambda m: self.count_type(m, 'pequena propriedade'),
                "Minifundios": lambda m: self.count_type(m, 'minifundio'),
                "Áreas de Preservação": lambda m: self.count_agents(m, AreaPreservacaoAgent),
                "Vias de Comunicação": lambda m: self.count_agents(m, ViaComunicacaoAgent),
            }
        )

        self.occupied_cells = set()  # Conjunto de células ocupadas
        agent_id = 0  # Para IDs únicos

        # Função auxiliar para colocar propriedades
        def place_property(agent_id, area, size):
            max_attempts = 100
            attempts = 0
            while attempts < max_attempts:
                x_start = self.random.randrange(self.grid.width - size + 1)
                y_start = self.random.randrange(self.grid.height - size + 1)
                positions = []
                overlap = False
                for dx in range(size):
                    for dy in range(size):
                        x = x_start + dx
                        y = y_start + dy
                        pos = (x, y)
                        if pos in self.occupied_cells:
                            overlap = True
                            break
                        positions.append(pos)
                    if overlap:
                        break
                if not overlap:
                    # Colocar o agente
                    ecoloid = EcoloidAgent(agent_id, self, area, positions)
                    for pos in positions:
                        self.grid.place_agent(ecoloid, pos)
                        self.occupied_cells.add(pos)
                    self.schedule.add(ecoloid)
                    return True
                attempts += 1
            return False

        # Criar Latifúndios
        for _ in range(num_latifundios):
            area = 16  # Latifúndio: 16 módulos fiscais
            size = 4  # Tamanho do quadrado: 4x4
            success = place_property(agent_id, area, size)
            if success:
                agent_id += 1
            else:
                print(f"Não foi possível alocar latifúndio {agent_id}")

        # Criar Médias Propriedades
        for _ in range(num_medias):
            area = 9  # Média Propriedade: 9 módulos fiscais
            size = 3  # Tamanho do quadrado: 3x3
            success = place_property(agent_id, area, size)
            if success:
                agent_id += 1
            else:
                print(f"Não foi possível alocar média propriedade {agent_id}")

        # Criar Pequenas Propriedades
        for _ in range(num_pequenas):
            area = 4  # Pequena Propriedade: 4 módulos fiscais
            size = 2  # Tamanho do quadrado: 2x2
            success = place_property(agent_id, area, size)
            if success:
                agent_id += 1
            else:
                print(f"Não foi possível alocar pequena propriedade {agent_id}")

        # Criar Minifúndios
        for _ in range(num_minifundios):
            area = 1  # Minifúndio: 1 módulo fiscal
            size = 1  # Tamanho do quadrado: 1x1
            success = place_property(agent_id, area, size)
            if success:
                agent_id += 1
            else:
                print(f"Não foi possível alocar minifúndio {agent_id}")

        # Criar Áreas de Preservação
        for _ in range(num_preservacoes):
            success = False
            attempts = 0
            while not success and attempts < 100:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                pos = (x, y)
                if pos not in self.occupied_cells:
                    preservacao = AreaPreservacaoAgent(agent_id, self)
                    self.grid.place_agent(preservacao, pos)
                    self.schedule.add(preservacao)
                    self.occupied_cells.add(pos)
                    success = True
                    agent_id += 1
                attempts += 1
            if not success:
                print(f"Não foi possível alocar Área de Preservação {agent_id}")

        # Criar Vias de Comunicação
        for _ in range(num_vias):
            success = False
            attempts = 0
            while not success and attempts < 100:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                pos = (x, y)
                if pos not in self.occupied_cells:
                    via = ViaComunicacaoAgent(agent_id, self)
                    self.grid.place_agent(via, pos)
                    self.schedule.add(via)
                    self.occupied_cells.add(pos)
                    success = True
                    agent_id += 1
                attempts += 1
            if not success:
                print(f"Não foi possível alocar Via de Comunicação {agent_id}")

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    @staticmethod
    def count_type(model, tipo):
        agents = set(model.schedule.agents)
        count = sum(1 for agent in agents if isinstance(agent, EcoloidAgent) and agent.tipo == tipo)
        return count

    @staticmethod
    def count_agents(model, agent_type):
        agents = set(model.schedule.agents)
        count = sum(1 for agent in agents if isinstance(agent, agent_type))
        return count
