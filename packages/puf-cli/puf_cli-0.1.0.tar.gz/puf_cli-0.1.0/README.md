# PUF - Python Universal Framework

PUF is a model version control system designed for data scientists and machine learning engineers. It provides Git-like functionality specifically tailored for managing machine learning models.

## Features

- Initialize model repositories
- Track model versions
- Store model metadata
- MongoDB integration for model and user management
- CLI interface for easy interaction
- Web interface for visualization and management

## Installation

```bash
pip install puf
```

## Quick Start

1. Initialize a new repository:
```bash
puf init
```

2. Add a model:
```bash
puf add model.h5 --name "MyModel" --version "1.0.0" --description "Initial version"
```

3. List models:
```bash
puf list
```

4. View specific model versions:
```bash
puf list mymodel
```

## Configuration

PUF requires MongoDB for storing model metadata. Set your MongoDB URI in the environment:

```bash
export MONGODB_URI="mongodb://localhost:27017"
```

Or create a `.env` file in your project root:
```
MONGODB_URI=mongodb://localhost:27017
```

## Web Interface

PUF comes with a web interface for visualizing your models and their performance. To start the web interface:

1. Install the required dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Visit `http://localhost:3000` in your browser

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
