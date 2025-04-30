# Description
This project includes a *very* small client to access data form 
the WebDataCollector-API. It is meant to provide a simple means 
of accessing the data in Json or as Panda-DataFrames.

More information about is availaible on its project homepage.

# Usage

```
from dss_wdc_client.client import WDCClient

# Somehow initialize environment variables for 
# "WDC_HOST" and "WDC_TOKEN". 
load_dotenv()

client = WDCClient.fromEnv()
df = client.loadAsDataFrame(
	'api/endpoint...', {'param1', 'value has to be encoded'})
```

For more information about the client and usable endpoints, 
see the project homepage of WDC.

# Changelog
- 0.6.0		WDCClient throws an WDCException if a request to the server fails
- 0.5.0		New signatures and methods taking care of encodings and working on large results
- 0.4.3		Add dependencies pandas["excel, plot"] as they are likely to be used.
- 0.4.2		Enhance README with Changelog and code-example.
- 0.4.1		Include a preferred variant for creating WDCClients from the Environment	

# Internal Notes for the Development Environment

## Initialize

	wdc-rest-api-python> poetry install

## Use cases

* Update dependencies: `poetry update`
	 
* Execute Python file: `poetry run python3 src/main.py`
	
* Running tests 
(https://pytest-with-eric.com/getting-started/poetry-run-pytest/)
	
	```
	poetry run pytest 
	poetry run pytest tests/test_module.py::testFunction
	poetry run pytest -s (with output from stdout and stderr)
	```
	
## Publish to PyPI
(https://python-poetry.org/docs/repositories/#publishable-repositories)
	
1. Config token (once)
	
	`poetry config pypi-token.pypi <my-token>`

2. Publish

	`poetry publish --build`
