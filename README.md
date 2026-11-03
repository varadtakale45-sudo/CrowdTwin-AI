# CrowdTwin AI
### Predictive Crowd Digital Twin for Dynamic Stadium Crowd Routing and Evacuation

CrowdTwin AI is an AI-powered stadium Digital Twin designed to simulate crowd movement, predict future congestion, optimize evacuation routes, and support intelligent crowd-management decisions.

The project explores how Artificial Intelligence, Machine Learning, Data Structures and Algorithms, graph theory, and 3D visualization can work together to address real-world challenges in large stadium environments.

Traditional crowd-management approaches often rely on current crowd conditions or predefined evacuation routes. CrowdTwin AI takes a predictive approach by forecasting crowd density at future time intervals and incorporating those predictions into dynamic route calculations.

The system provides an interactive 3D cricket stadium, simulated crowd movement, machine learning-based density forecasting, graph-based navigation, what-if scenario analysis, and performance evaluation through a unified operations interface.

---

## Key Features

- **3D Stadium Digital Twin:** Interactive cricket stadium featuring an oval playing field, pitch and boundary markings, tiered curved stands, roof canopies, corridors, zones, exits, and eight numbered gates mapped to G1–G8.
- **Crowd Simulation:** Simulates spectator movement, crowd distribution, occupancy, and transfers through available graph connections.
- **AI-Based Crowd Prediction:** Forecasts crowd density at +1, +3, and +5-minute intervals.
- **Machine Learning:** Implements a Random Forest baseline for short-term crowd-density forecasting.
- **Dynamic Graph Routing:** Represents stadium pathways as a graph and calculates routes using Dijkstra's and A* algorithms.
- **Prediction-Aware Routing:** Incorporates predicted future congestion into route costs rather than relying exclusively on current crowd conditions.
- **What-If Simulation:** Tests scenarios involving blocked corridors, closed exits, increased crowd density, and emergency situations using isolated copies of the stadium state.
- **Performance Evaluation:** Compares Static, Reactive, and Prediction-Aware routing strategies using calculated performance metrics.
- **Operations Dashboard:** Displays predictions, routes, KPIs, strategy comparisons, recommendations, and simulation timelines.
- **Report Generation:** Captures simulation runs and exports timestamped JSON reports.
- **Research Analytics:** Provides graph analysis, algorithm benchmarking, and experiment tracking.
- **SQLite Storage:** Automatically stores simulation runs, predictions, routes, crowd states, scenarios, and experiments.

## Enhanced Operations Interface

The digital twin includes a detailed 3D cricket stadium with an oval field, pitch markings, boundary lines, tiered curved stands, roof canopies, graph corridors, and eight numbered gates.

The interface follows a minimal black-and-white design, with red reserved for warnings and critical states. All visible text uses a minimum font size of 18px.

The simulation workflow uses two primary actions:

- **Start:** Begins the crowd simulation and captures the evolving stadium state.
- **Finish & Report:** Completes a simulation run and generates a report containing three forecast horizons, route details, KPIs, strategy comparisons, recommendations, and a timestamped timeline.

Additional functionality includes:

- Current and predicted crowd-density visualization.
- Dynamic route visualization inside the 3D stadium.
- Gate and corridor inspection.
- Crowd heatmaps and occupancy monitoring.
- Isolated what-if scenario execution.
- JSON report export through the backend API.

The Export Report feature stores and downloads the captured JSON report through `/api/reports` and `/api/reports/{id}/export`.

Travel-time and evacuation-time values are simplified research-model estimates, not certified operational measurements.

---

## Research Problem and Motivation

Static routing generally focuses on minimizing distance and does not account for changing crowd conditions.

Reactive routing considers current congestion but may respond only after a bottleneck has already started developing.

Prediction-aware routing attempts to address this limitation by incorporating forecast crowd density into graph edge costs before calculating a route.

CrowdTwin AI provides a reproducible research environment for comparing these three approaches under simulated stadium conditions.

The project does not assume that prediction-aware routing will always outperform the alternatives. Instead, it calculates performance metrics from the current simulation and provides a basis for experimental comparison.

## Project Objectives

1. Develop an interactive 3D digital representation of a cricket stadium.
2. Simulate crowd movement and monitor crowd distribution across stadium zones.
3. Forecast crowd density over short-term time horizons.
4. Represent stadium pathways using graph-based data structures.
5. Implement static, reactive, and prediction-aware routing strategies.
6. Dynamically calculate route costs using distance, congestion, queueing, and risk.
7. Evaluate different crowd-management and evacuation scenarios.
8. Compare routing strategies using measurable performance indicators.
9. Store simulation results and experiments for reproducible analysis.

## System Architecture

The overall workflow connects crowd simulation, machine learning, graph algorithms, and the 3D visualization environment.

```text
Synthetic Seed Dataset
        |
        v
Data Preprocessing
        |
        v
Random Forest Model
        |
        v
Crowd Density Prediction
   (+1, +3, +5 min)
        |
        v
Dynamic Graph Edge Costs
        |
        v
Dijkstra / A* Routing
        |
        v
Prediction-Aware Routes
        |
        v
3D Stadium Visualization
        |
        v
What-If Scenario Analysis
        |
        v
Evaluation and Reporting
        |
        v
SQLite Experiment Storage
```

The browser communicates with the FastAPI backend. The backend manages simulation logic, machine learning predictions, graph construction, routing algorithms, scenario processing, evaluation, and database operations.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Machine Learning | Scikit-learn, Random Forest |
| Additional ML Exploration | XGBoost |
| Graph Processing | NetworkX |
| Pathfinding | Dijkstra's, A* |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| 3D Visualization | Three.js |
| Data Processing | Pandas, NumPy |

## Machine Learning Model and Dataset

CrowdTwin AI uses a synthetic seed dataset stored in `data/crowd_data.csv`.

The dataset represents simulated crowd conditions and is not collected from actual stadium operations.

The preprocessing pipeline:

- Validates the required dataset columns.
- Handles missing numerical values.
- Derives minute-based and net-flow features.
- Generates future density targets.
- Prepares data for multiple prediction horizons.

A deterministic Random Forest baseline is used to forecast crowd density at:

- +1 minute
- +3 minutes
- +5 minutes

Model performance is evaluated using:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R-squared (R²)

Evaluation uses a chronological held-out split to preserve the time-series ordering.

## Dynamic Graph-Based Routing

The stadium is represented as a weighted graph.

- Nodes represent stadium zones, gates, corridors, and exits.
- Edges represent available pathways between connected locations.
- Edge weights represent the estimated cost of travelling through a particular pathway.

Three routing strategies are supported:

| Strategy | Routing Logic |
|---|---|
| Static | Uses pathway distance |
| Reactive | Considers current crowd congestion |
| Prediction-Aware | Considers forecast crowd congestion |

The dynamic edge cost is represented as:

`Cost = αD + βC + γW + δR`

Where:

- `D` = Distance
- `C` = Crowd congestion
- `W` = Queue or waiting cost
- `R` = Risk factor
- `α, β, γ, δ` = Configurable weights

Dijkstra's and A* algorithms calculate routes using the resulting graph costs. Blocked pathways are removed from route availability.

## Data Structures and Algorithms

The project incorporates several fundamental Data Structures and Algorithms concepts.

| Data Structure / Algorithm | Application |
|---|---|
| Arrays and 2D Arrays | Density, capacity, and occupancy representation |
| Linked Lists | Crowd trajectory representation |
| Doubly Linked Lists | Bidirectional monitoring records |
| Circular Linked Lists | Repeated monitoring cycles |
| Queues | Service and checkpoint flow |
| Circular Queues | Continuous service processing |
| Stacks | Previous simulation state storage |
| Priority Queues / Heaps | Shortest-path search and congestion ranking |
| Hash Tables | Fast entity lookup |
| BST | Ordered record management |
| AVL Trees | Balanced ordered records |
| Linear Search | Sequential data lookup |
| Binary Search | Search in sorted records |
| Fibonacci Search | Search in ordered collections |
| Merge Sort | Sorting and analytics |
| Quick Sort | General-purpose sorting |
| Heap Sort | Priority-based ordering |
| Bucket Sort | Distribution-based sorting |
| Radix Sort | Digit-based sorting |
| BFS | Graph traversal |
| DFS | Graph exploration |
| Floyd-Warshall | All-pairs shortest-path analysis |
| Dijkstra's Algorithm | Weighted shortest-path calculation |
| A* Algorithm | Heuristic-based route optimization |

Sorting algorithms are also benchmarked through the analytics functionality.

## What-If Simulation and 3D Digital Twin

The what-if engine allows different crowd-management scenarios to be tested without permanently changing the live stadium state.

Supported scenarios include:

- Blocking a corridor or pathway.
- Closing a stadium gate or exit.
- Increasing crowd density in selected zones.
- Simulating emergency evacuation conditions.
- Redirecting crowd movement through alternative pathways.

Each what-if request creates an isolated copy of the stadium state, applies the requested changes, generates fresh predictions, calculates alternative routes, and evaluates the resulting conditions.

The isolated scenario is discarded after execution, leaving the original live simulation unchanged.

The Three.js environment procedurally generates:

- Cricket field and pitch.
- Boundary markings.
- Tiered stadium stands.
- Roof canopies.
- Gates, zones, corridors, and exits.
- Instanced crowd visualization.
- Current and predicted crowd heatmaps.
- Interactive stadium inspection.
- Backend-calculated route visualization.

## Performance Evaluation

CrowdTwin AI compares three routing approaches:

1. Static Routing
2. Reactive Routing
3. Prediction-Aware Routing

The system evaluates them using:

- Estimated travel time.
- Estimated evacuation time.
- Crowd congestion.
- Queue length.
- Route distance.
- Path availability.
- Overall routing performance.

The dashboard calculates comparisons using the current digital twin state rather than relying on predefined performance claims.

## Database and Experiment Storage

SQLite is used for local experiment storage.

The database is automatically initialized when the backend starts.

It includes parameterized tables for:

- Simulation runs.
- Crowd states.
- Predictions.
- Routes.
- What-if results.
- Experiments.

This allows simulation results and evaluation metrics to be stored and retrieved for further analysis.

## API Endpoints

The FastAPI backend provides endpoints for simulation, crowd management, prediction, routing, analytics, and reporting.

**Monitoring and analytics**

| Method | Endpoint |
|---|---|
| GET | `/api/status` |
| GET | `/api/stadium` |
| GET | `/api/crowd` |
| GET | `/api/analytics` |
| GET | `/api/experiments` |

**Simulation operations**

| Method | Endpoint |
|---|---|
| POST | `/api/simulation/start` |
| POST | `/api/simulation/pause` |
| POST | `/api/simulation/reset` |
| POST | `/api/crowd/adjust` |

**Prediction and routing**

| Method | Endpoint |
|---|---|
| POST | `/api/predict` |
| POST | `/api/route` |
| POST | `/api/block` |
| POST | `/api/unblock` |
| POST | `/api/what-if` |

**Reporting**

| Method | Endpoint |
|---|---|
| GET | `/api/reports` |
| GET | `/api/reports/{id}/export` |

Interactive API documentation is available through FastAPI Swagger UI.

## Project Structure

The repository is organized into four main source directories, with exactly three HTML pages.

```text
CrowdTwin-AI/
│
├── backend/
│   ├── main.py
│   ├── stadium.py
│   ├── crowd_simulator.py
│   ├── ml_prediction.py
│   ├── preprocessing.py
│   ├── graph.py
│   ├── routing.py
│   ├── dynamic_cost.py
│   ├── what_if.py
│   ├── decision_engine.py
│   ├── data_structures.py
│   ├── trees_hashing.py
│   ├── searching_sorting.py
│   ├── evaluation.py
│   └── database.py
│
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── simulation.html
│   └── style.css
│
├── 3d_stadium/
│   ├── stadium_scene.js
│   ├── crowd_visualization.js
│   ├── heatmap.js
│   └── route_visualization.js
│
├── data/
│   └── crowd_data.csv
│
├── requirements.txt
└── README.md
```

The SQLite database file is created at runtime in the project root.

## Installation and Setup

### Prerequisites

- Python 3.10 or later.
- pip package manager.
- Internet connection for loading the Three.js CDN on the simulation page.

### Windows CMD Installation

**1. Clone the repository**

```cmd
git clone <YOUR_REPOSITORY_URL>
```

**2. Navigate to the project directory**

```cmd
cd CrowdTwin-AI
```

**3. Create a virtual environment**

```cmd
python -m venv venv
```

**4. Activate the virtual environment**

```cmd
venv\Scripts\activate
```

**5. Install dependencies**

```cmd
pip install -r requirements.txt
```

**6. Start the FastAPI server**

```cmd
uvicorn backend.main:app --reload
```

**7. Open the application**

Visit:

`http://127.0.0.1:8000`

FastAPI serves all three frontend pages, stylesheets, and 3D modules, so a separate frontend development server is not required.

### Alternative Port

If port 8000 is already occupied, run:

```cmd
uvicorn backend.main:app --reload --port 8080
```

Then open:

`http://127.0.0.1:8080`

### API Documentation

Visit:

`http://127.0.0.1:8000/docs`

This provides interactive documentation for exploring and testing the available API endpoints.

## Running an Experiment

A typical experiment can be performed using the following workflow:

1. Start the simulation and observe crowd movement.
2. Generate crowd-density predictions for the future time horizons.
3. Compare Static, Reactive, and Prediction-Aware routes.
4. Open the 3D simulation and inspect the calculated routes.
5. Block a corridor or close an exit.
6. Recalculate the route using the updated graph.
7. Run the same closure as an isolated what-if scenario.
8. Open Analytics to review the calculated performance metrics.
9. Finish the simulation and generate a report.
10. Export the captured JSON report for further analysis.

## Research Scope and Limitations

CrowdTwin AI is a functional research and educational prototype.

- The crowd dataset is synthetic and does not represent actual stadium measurements.
- Machine learning predictions depend on the quality and assumptions of the simulated data.
- Travel-time, queue, and evacuation values are simplified research-model estimates.
- Results from simulated environments may differ significantly from real-world stadium conditions.
- The system has not been certified or validated for operational emergency planning.

> **Disclaimer:** CrowdTwin AI is intended for research, experimentation, and educational purposes. It is not a certified crowd-safety, emergency-response, or evacuation-planning product.

## Future Scope

Potential extensions include:

- Integration with real-time crowd-monitoring sensors.
- Computer vision-based crowd-density estimation.
- Testing additional machine learning and forecasting models.
- More advanced multi-agent crowd movement simulation.
- Improved risk-aware evacuation optimization.
- Validation against real-world crowd-flow datasets.
- Large-scale simulation and scalability testing.

## Conclusion

CrowdTwin AI demonstrates how a predictive Digital Twin can bring together machine learning, graph algorithms, simulation, and interactive 3D visualization to explore more intelligent approaches to stadium crowd management.

The central concept is to move beyond simply reacting to congestion and instead anticipate changing crowd conditions before making routing decisions.

By providing a simulation environment where different routing strategies and emergency scenarios can be tested and compared, CrowdTwin AI offers a practical foundation for exploring predictive crowd management.

---

**Built with Python, FastAPI, Machine Learning, NetworkX, SQLite, JavaScript, and Three.js.**
