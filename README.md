# cave-generator

## User Guide

### Installation
```poetry install```

### Running
```poetry run cave-generator```

### CLI arguments
```
Map width: -W (default = 100)
Map height: -H (default = 100)
Room count: -R (default = 10)
Seed: -s (leave unset for a random map)
Minimum room size: -m (default 5)
Maximum room size: -M (default 10)
```
**Note:** minimum room size cannot be larger than maximum room size. Map width & map height must always be at least maximum room size + 2 (max_size + 2); otherwise a ValueError will be raised. Room count must be greater than 0.