# Kieker for Jupyter

![PyPI Version](https://img.shields.io/pypi/v/kieker-for-jupyter)
![License](https://img.shields.io/pypi/l/kieker-for-jupyter)
![Python Versions](https://img.shields.io/pypi/pyversions/kieker-for-jupyter)

**Kieker for Jupyter** is a Python package designed to seamlessly integrate [Kieker](https://kieker-monitoring.net/) performance monitoring and analysis capabilities into Jupyter Notebooks. This integration simplifies the process of conducting performance analyses within an interactive environment, making it more accessible for data scientists and developers.

## Features

- **Simplified Analysis Execution**: Provides straightforward methods to run various Kieker analyses directly from Jupyter cells.
- **Modular Design**: Easily extendable to include additional analyses as needed.
- **Interactive Visualization**: Leverages Jupyter's interactive features to visualize performance data effectively.

## Installation

**Prerequisites**  
- `graphviz` >= 3.0
- `pypdf` >= 5.4.0 
- `python` >= 3.8

Install the package using pip:

```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps kieker-for-jupyter
```

## Usage

Here's a basic example of how to use the package:

```python
from kieker.tools.trace_analysis import TA, AnalysisType, GraphicType

# 1. Set path to trace-analysis CLI
TA.set_trace_analysis_path("~/kieker/trace-analysis-2.0.2/bin/trace-analysis")

# 2. Perform an Assembly Sequence Diagrams analysis with auto-displayed PDF
TA.draw(
    analysis_type=AnalysisType.ASDIAGRAMS, 
    graphic_type=GraphicType.PDF, 
    input_dir="~/kieker-logs/kieker*", 
    output_dir="output-asdiagrams", 
    limit=10, 
    file_range=range(20,40)
)
```

where numbered pdf files will be created and merged as an output file with
* `limit` as an optional parameter to set the maximum number of pdf files to use,
* `file_range` as an optional parameter to set the range of pdf files to use.

## Available Analyses

- **Call Tree (`aactree`, `adctree`, `ctrees`)**: Visualizes the call tree of deployed components.
- **Dependency Graph (`acdgraph`, `aodgraph`, `cdgraph`, `dcdgraph`, `dodgraph`)**: Displays the relationships between deployed components.
- **Sequence Diagrams (`asdiagrams`, `dsdiagrams`)**: Illustrates the dynamic interactions within the software architecture.

## Extending the Package

The package's modular structure allows for easy integration of new analysis types. To add a new analysis:

**Update the Analysis Dictionary**: Add the new analysis type to the enum of the `AnalysisType` class.

Example:

```python
@staticmethod
class AnalysisType(Enum):
    AACTREE = ("--plot-Aggregated-Assembly-Call-Tree", None)
    ADCTREE = ("--plot-Aggregated-Deployment-Call-Tree", None)
    ACDGRAPH = ("--plot-Assembly-Component-Dependency-Graph", "none")
    ...
    NEWTYPE = ("traceanalysis call", "time parameter")
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to the [Kieker](https://kieker-monitoring.net/) community for their continuous support and development of the Kieker monitoring framework.

