from model import EcoWorldModel

# Configurações da simulação
grid_width = 20
grid_height = 20
num_minifundios = 10
num_pequenas = 5
num_medias = 3
num_latifundios = 2
num_preservacoes = 5
num_vias = 5
num_cycles = 10

# Criar o modelo
modelo = EcoWorldModel(
    grid_width,
    grid_height,
    num_minifundios,
    num_pequenas,
    num_medias,
    num_latifundios,
    num_preservacoes,
    num_vias
)

# Rodar a simulação por um número de ciclos
for i in range(num_cycles):
    print(f"\nCiclo {i+1}")
    modelo.step()
