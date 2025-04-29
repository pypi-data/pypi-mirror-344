# Pythils

A Python utilities package.

## Installation

```bash
pip install pythils
```

## Configuration Management

The `pythils.config` module provides tools for managing hierarchical configuration with advanced features.

### Features

- **ConfigDict**: A dictionary-like object with nested key support
- **ConfigRef**: References to other configuration values
- **Wildcard Configuration**: Support for default values with `*` and `.` wildcards
- **Multiple Sources**: Load configuration from environment variables, files (JSON, YAML, Python)
- **Nested Access**: Navigate through configuration hierarchies

### Usage Examples

```python
from pythils.config import ConfigDict, ConfigRef

# Create a configuration
config = ConfigDict({
    'app': {
        'name': 'My App',
        'version': '1.0.0'
    },
    'database': {
        'host': 'localhost',
        'port': 5432
    },
    # Reference another configuration value
    'app_id': ConfigRef('app.name'),
    'features': {
        # Provide defaults with wildcards
        '*': {
            'enabled': True
        },
        'api': {
            '.': ConfigRef('app'), # Default with . wildcard
            'name': 'My App API', # Override default from . wildcard
            'base_url': 'https://example.com/api/'
        },
        'webui': {
            'enabled': False # Override default from * wildcard
        }
    }
})

# Access configuration values
print(config.get('app.name'))  # My App
print(config.get('database.port'))  # 5432
print(config.get('app_id'))  # My App (resolved reference)
print(config.get('feature.enabled'))  # True (from wildcard)

# Nested configuration access
db_config = config['database']
print(db_config.get('host'))  # localhost
print(db_config.get('..app.name'))  # My App (parent/root navigation)

# Configuration references
config = ConfigDict({
    'base_url': 'https://api.example.com',
    'endpoints': {
        'users': ConfigRef('base_url') + '/users',
        'auth': ConfigRef('.users') + '/auth'  # relative reference
    }
})

print(config.get('endpoints.auth'))  # https://api.example.com/users/auth

# Load from environment variables
env_config = ConfigDict.from_env('MYAPP_')

# Load from file
file_config = ConfigDict.from_file('config.json')
```

## Dynamic Interfaces

The `pythils.interface` module provides tools for creating interfaces with multiple implementations that can be dynamically loaded.

### Features

- **DynamicInterface**: Abstract base class for creating interfaces
- **Implementation Discovery**: Automatically discover and load implementations
- **Configuration-based Instantiation**: Create instances of implementations from configuration dictionaries
- **Flexible Selection**: Choose implementations by name or from configuration

### Usage Examples

```python
from pythils.interface import DynamicInterface

# Define an interface
class Database(DynamicInterface):
    __implementation_package__ = "myapp.db.implementations"
    __default_implementation__ = "postgres"
    
    def connect(self):
        """Connect to the database"""
        pass
        
    def query(self, sql):
        """Execute a query"""
        pass

# Create an instance from configuration
config = {
    "implementation": "sqlite",
    "sqlite": {
        "database": "app.db",
        "timeout": 30
    }
}

# Create instance from configuration
db = Database.create_instance(config)

# Create instance by name
postgres_db = Database.create_instance(implementation="postgres", host="localhost", port=5432)
# or
postgres_db = Database.get_implementation("postgres")(host="localhost", port=5432)

# Get available implementations
implementations = Database.get_implementations()
print(implementations)  # ['sqlite', 'postgres', 'mysql']
```

## Development

### Running Tests

```bash
python -m unittest discover -s tests
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License