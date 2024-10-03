# EcoWorld Simulator

An agent-based simulation modeling Brazilian rural properties and the Atlantic Forest (Mata Atlântica), focusing on CO2 absorption based on land use and biomass.

## Author

Wellington Wagner F. Sarmento

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Usage](#usage)
- [Simulation Parameters](#simulation-parameters)
- [Visualization](#visualization)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Dependencies](#dependencies)
- [Contact](#contact)

## Description

The **EcoWorld Simulator** is an agent-based model developed using the Mesa framework in Python. It simulates different types of rural properties and areas of the Atlantic Forest to analyze CO2 absorption in a rural setting. The model reflects Brazilian land scenarios by representing various property types and their impact on CO2 levels through biomass.

## Features

- **Agents (Ecoloids)**: Representing Módulo Fiscal units (15 hectares of farmland) and Mata Atlântica cells.
- **Rural Properties (Propriedades Rurais)**: Matrices of Ecoloids forming different property types.
- **Property Types**:
  - **Minifúndio**: 1x1 matrix (1 Módulo Fiscal).
  - **Pequena Propriedade**: 2x2 matrix (4 Módulos Fiscais).
  - **Média Propriedade**: 3x3 matrix (9 Módulos Fiscais).
  - **Latifúndio**: 4x4 matrix (16 Módulos Fiscais).
- **Vegetation Types**:
  - **Latifúndios**: Monocultures like soy, sugar cane, pasture, or barren land.
  - **Other Properties**: Diversified crops typical of family farming.
  - **Mata Atlântica**: Representing forested areas.
- **CO2 Absorption Calculation**: Based on the biomass of agents.
- **Visual Representation**: Color-coded grid displaying different property types and vegetation.

## Installation

### Prerequisites

- **Python**: Version 3.6 or higher.
- **Mesa Framework**: Version 2.4.0.

### Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/ecoworld-simulator.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd ecoworld-simulator
   ```

3. **Create a Virtual Environment (Optional but Recommended)**:

   ```bash
   python -m venv venv
   ```

4. **Activate the Virtual Environment**:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On Unix or macOS:

     ```bash
     source venv/bin/activate
     ```

5. **Install Dependencies**:

   ```bash
   pip install mesa==2.4.0
   ```

## Usage

1. **Run the Simulation**:

   ```bash
   python test_simulation.py
   ```

2. **Access the Visualization Interface**:

   Open a web browser and navigate to [http://localhost:8521](http://localhost:8521).

3. **Start the Simulation**:

   In the web interface, click the "Start" button to begin the simulation.

## Simulation Parameters

The simulation parameters are defined in the `test_simulation.py` file:

```python
model_params = {
    "width": 50,
    "height": 50,
    "num_minifundios": 20,
    "num_pequenas": 10,
    "num_medias": 5,
    "num_latifundios": 2,
    "num_mata_atlantica": 100,
    "co2_inicial": 10000,
}
```

- **Grid Dimensions**:
  - `width`: Width of the simulation grid.
  - `height`: Height of the simulation grid.
- **Property Quantities**:
  - `num_minifundios`: Number of minifundios.
  - `num_pequenas`: Number of small properties.
  - `num_medias`: Number of medium properties.
  - `num_latifundios`: Number of latifundios.
- **Mata Atlântica**:
  - `num_mata_atlantica`: Number of Mata Atlântica Ecoloids.
- **CO2 Levels**:
  - `co2_inicial`: Initial amount of CO2 in the atmosphere.

To adjust the simulation parameters, modify the values in the `model_params` dictionary in `test_simulation.py`.

## Visualization

### Grid Representation

- **Latifúndio**: Red (`#FF0000`)
- **Média Propriedade**: Orange (`#FFA500`)
- **Pequena Propriedade**: Yellow (`#FFFF00`)
- **Minifúndio**: Blue Violet (`#8A2BE2`)
- **Mata Atlântica**: Dark Green (`#006400`)
- **Empty Cells**: Light Brown (`#D2B48C`)

### Chart

- Displays CO2 absorption over time, separated by property type and Mata Atlântica.
- Color-coded lines correspond to the property types as listed above.

## Project Structure

- **agents.py**: Defines the `EcoloidAgent` class, representing individual agents in the simulation.
- **model.py**: Contains the `EcoWorldModel` class, which sets up the environment and manages the simulation logic.
- **test_simulation.py**: Main script to run the simulation and launch the visualization server.

## Customization

### Adjust Biomass Values

Modify the `calcular_biomassa` method in `agents.py` to change biomass values for different vegetation types:

```python
def calcular_biomassa(self):
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
```

### Adjust CO2 Absorption Factor

In `model.py`, within the `step` method, adjust the absorption factor:

```python
absorcao = agente.biomassa * 0.1  # Modify the factor as needed
```

### Modify Simulation Behavior

- **Add New Property Types**: Extend the `definicoes_propriedades` list in `model.py`.
- **Change Vegetation Types**: Modify the `definir_vegetacao` method in `model.py`.
- **Update Agent Behavior**: Implement new methods or update existing ones in `EcoloidAgent`.

## Dependencies

- **Mesa Framework**: [https://mesa.readthedocs.io/en/stable/](https://mesa.readthedocs.io/en/stable/)

  Install using:

  ```bash
  pip install mesa==2.4.0
  ```
