# test_simulation.py

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from model import EcoWorldModel
from agents import EcoloidAgent

def agent_portrayal(agent):
    # Portrayal padrão para todas as células
    portrayal = {
        "Shape": "rect",
        "Filled": "true",
        "Layer": 0,
        "Color": "#D2B48C",  # Marrom claro
        "w": 1.0,
        "h": 1.0
    }

    if agent is not None:
        # Atualizar o portrayal para células com agentes
        portrayal["Layer"] = 1  # Agentes acima do fundo
        if agent.tipo == 'ModuloFiscal':
            if agent.propriedade_tipo == 'latifundio':
                portrayal["Color"] = "#FF0000"  # Vermelho
            elif agent.propriedade_tipo == 'media':
                portrayal["Color"] = "#FFA500"  # Laranja
            elif agent.propriedade_tipo == 'pequena':
                portrayal["Color"] = "#FFFF00"  # Amarelo
            elif agent.propriedade_tipo == 'minifundio':
                portrayal["Color"] = "#8A2BE2"  # Azul violeta
        elif agent.tipo == 'Mata Atlantica':
            portrayal["Color"] = "#006400"  # Verde escuro
    # Caso contrário, manter o portrayal padrão (marrom claro)
    return portrayal

# Dimensões do grid
largura_grid = 50
altura_grid = 50

# Parâmetros do modelo (definidos no código)
model_params = {
    "width": largura_grid,
    "height": altura_grid,
    "num_minifundios": 10,
    "num_pequenas": 10,
    "num_medias": 10,
    "num_latifundios": 10,
    "num_mata_atlantica": 100,  # Novo parâmetro
    "co2_inicial": 10000,
}

grid = CanvasGrid(agent_portrayal, largura_grid, altura_grid, 600, 600)

chart = ChartModule(
    [
        {"Label": "Absorção_Latifundio", "Color": "#FF0000"},  # Vermelho
        {"Label": "Absorção_Media", "Color": "#FFA500"},       # Laranja
        {"Label": "Absorção_Pequena", "Color": "#FFFF00"},     # Amarelo
        {"Label": "Absorção_Minifundio", "Color": "#8A2BE2"},  # Azul violeta
        {"Label": "Absorção_Mata", "Color": "#006400"}         # Verde escuro
    ],
    data_collector_name='datacollector'
)

server = ModularServer(
    EcoWorldModel,
    [grid, chart],
    "Modelo EcoWorld",
    model_params
)

server.port = 8521  # Porta padrão

if __name__ == '__main__':
    server.launch()








