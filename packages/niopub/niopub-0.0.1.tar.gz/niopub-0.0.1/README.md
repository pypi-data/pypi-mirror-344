# Niopub CLI

A command-line tool for creating and managing context-based agents on Niopub from your browser.

## Installation

You can install Niopub CLI using pip:

```bash
pip install git+https://github.com/Niopub/niopub.git
```

Or install from a local clone:

```bash
git clone https://github.com/Niopub/niopub.git
cd niopub
pip install .
```

## Usage

After installation, you can start the Niopub server with a simple command:

```bash
niopub 8000
```

This will start the server on port 8000. You can then access the Niopub interface by opening your browser to:

```
http://localhost:8000
```

### Features

- Create and manage context-based agents
- Monitor agent processes
- Pause, resume, and stop agents
- Web-based interface for easy management

### Requirements

- Python 3.8 or higher
- Dependencies will be automatically installed with pip

## Development

To install in development mode:

```bash
git clone https://github.com/Niopub/niopub.git
cd niopub
pip install -e .
```

## License

BSD License - See LICENSE file for details
