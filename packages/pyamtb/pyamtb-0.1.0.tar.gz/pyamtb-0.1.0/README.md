# PyAMTB

A Python package for tight-binding model calculations in materials science.

## Features

- Tight-binding model calculations for materials
- Support for various lattice structures
- Band structure calculations
- Easy configuration through TOML files
- Command-line interface for quick calculations

## Installation

### From PyPI

```bash
pip install pyamtb
```

### From source

```bash
git clone https://github.com/wangdinghui/pyamtb.git
cd pyamtb
pip install -e .
```

## Usage

### Python API

```python
from pyamtb import Parameters, TightBindingModel

# Load parameters from TOML file
params = Parameters.from_toml('config.toml')

# Create tight-binding model
model = TightBindingModel(params)

# Calculate energy bands
k_path = np.array([[0.0, 0.0, 0.0], [0.5, 0.5, 0.5]])
bands = model.calculate_bands(k_path)
```

### Command Line Interface

```bash
# Show help
pyamtb --help

# Calculate bands using configuration file
pyamtb calculate --config config.toml
```

## Configuration

The package uses TOML files for configuration. Here's an example configuration:

```toml
lattice_constant = 1.0
hopping_parameters = { t1 = 1.0, t2 = 0.5 }
```

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{pyamtb,
  author = {Wang Dinghui},
  title = {PyAMTB: A Python package for tight-binding model calculations},
  year = {2024},
  url = {https://github.com/wangdinghui/pyamtb}
}
``` 