# Di Tidy

This project is a formatting/linting utility for various languages

## Development

```sh
pip install -e .
```

To run the specific module

```sh
export PYTHONPATH=src
python -m ditidy.[module name]
```

## Linting

```sh
hatch run lint
```

## Testing

```sh
hatch test
```

## Releasing

```sh
python -m build
twine upload --repository pypi dist/*
```
