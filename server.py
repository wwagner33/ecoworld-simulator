from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from model import EcoWorldModel
from agents import EcoloidAgent, AreaPreservacaoAgent, ViaComunicacaoAgent

def agent_portrayal(agent):
    portrayal = {
        "Shape": "rect",
        "Filled": "true",
        "Layer": 1,
        "w": 1.0,
        "h": 1.0
    }

    if isinstance(agent, EcoloidAgent):
        if agent.tipo == "latifundio":
            portrayal["Color"] = "blue"
        elif agent.tipo == "media propriedade":
            portrayal["Color"] = "purple"
        elif agent.tipo == "pequena propriedade":
            portrayal["Color"] = "green"
        elif agent.tipo == "minifundio":
            portrayal["Color"] = "lightgreen"
        else:
            portrayal["Color"] = "gray"
    elif isinstance(agent, AreaPreservacaoAgent):
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 0
    elif isinstance(agent, ViaComunicacaoAgent):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 2

    return portrayal

grid_width = 20
grid_height = 20

grid = CanvasGrid(agent_portrayal, grid_width, grid_height, 500, 500)

chart = ChartModule(
    [
        {"Label": "Latifundios", "Color": "Blue"},
        {"Label": "Médias Propriedades", "Color": "Purple"},
        {"Label": "Pequenas Propriedades", "Color": "Green"},
        {"Label": "Minifundios", "Color": "LightGreen"},
        {"Label": "Áreas de Preservação", "Color": "Yellow"},
        {"Label": "Vias de Comunicação", "Color": "Red"},
    ],
    data_collector_name='datacollector'
)

server = ModularServer(
    EcoWorldModel,
    [grid, chart],
    "EcoWorld Model",
    {
        "width": grid_width,
        "height": grid_height,
        "num_minifundios": 10,
        "num_pequenas": 5,
        "num_medias": 3,
        "num_latifundios": 2,
        "num_preservacoes": 5,
        "num_vias": 5,
    }
)

server.port = 8521  # Porta padrão
if __name__ == '__main__':
    server.launch()
