dash-template frontend
======================


# Run locally

```bash
export API_URL=localhost:8080
conda activate dash-template
python index.py
```

# Run as Docker Image

```bash
export API_URL=http://localhost:8080
make run
```

# Run tests

```bash
python -m pip install dash\[testing]
pytest
```
