Car Cutter - Backend Challenge
==========

Task
-----

### As a backend developer you get the task to implement an API route using Python

... which accepts json data from our customers and store certain parts of it to the filesystem.</br>
Since this is a pretty simple task, we want you to think of best practices, edge cases and good software engineering.

Please fork our repo and implement the challenge in `src/core/challenge_api.py`.

Customers will post some json data to this api route, and we want to store each `Vehicle` in the `Vehicle-List` to a single file.
This file should be stored to a folder named like the `user_id` and the filename should be the `id` with a ".json" extension.

Once you are done, just create a pull request to `base:develop`. Please leave a comment what you think about the task and how long it took you to finish.

Run It
-----

Serve the API route with:
```bash
$ python src/cli.py api-server vehicle-features
```

By default, the API is now reachable at `http://127.0.0.1:8080/backend/` </br>
Our customers will post json files to the route `/challenge`.
We provide a [json schema](https://github.com/carcutter/BackendChallenge/blob/develop/json/vehicle-features.v1.schema.json) and an [example](
    https://github.com/carcutter/BackendChallenge/blob/develop/json/vehicle-features.v1.example.json).

Expect our customers to post their data with different approaches like:
```bash
curl --location --request POST 'http://localhost:8080/backend/challenge' \
  --header "Content-Type: application/json" \
  --data @json/vehicle-features.v1.example.json
```
or
```bash
curl --request POST 'http://localhost:8080/backend/challenge' \
  --header "Content-Type: application/json" \
  --form data=@json/vehicle-features.v1.example.json
```


Setup
-----
We use Python 3.7 with Flask to run the http server.


#### Virtual Environment (API and CLI)

You can use [pyenv](https://github.com/pyenv/pyenv)
to manage different versions of Python on your local PC.

To complete the setup run the following command inside the repository
directory. Whenever you enter the repository folder then, `pyenv` will
automatically use Python 3.7:

```bash
pyenv install 3.7.13
pyenv local 3.7.13
python3 --version  # verify whether we're indeed using Python 3.7
```

We need a virtual environment for local development.
Inside the repository directory run:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Formatting
----------

To format your code before committing run `make format` or
[integrate black into your IDE](https://black.readthedocs.io/en/stable/integrations/editors.html).

Caveat: Black either puts all function arguments into a single line or
one argument per line. To split a long line of arguments into several lines,
you must add a trailing comma *after* the last argument.
For example, `transform(argument1, argument2,)` will be
converted to multiple lines by *Black*. The following example on the other hand
will be collapsed into a single line, because it lacks a trailing comma:

```python
transform(
    argument1,
    argument2
)
```

### PyCharm

If you're using PyCharm and you want your files to be auto-formatted on save
follow these steps:

- Setup the virtualenv environment `venv` as outlined above. *Black* should
  automatically be installed, because it's listed in `requirements.txt`.
  As a short-cut (without local development possibility) you can run:
  `python3 -m venv venv && venv/bin/python install black==22.3.0`
- Install the [*File Watchers* plugin](https://plugins.jetbrains.com/plugin/7177-file-watchers)
- In the *File Watchers* plugin, setup black with the following settings:
  - File Type: Python
  - Program: `$PyInterpreterDirectory$/black`
  - Arguments: `--line-length=140 $FilePath$`
  - Output paths to refresh: `$FilePath$`
  - Working Directory: `$ProjectFileDir$`
  - Uncheck "Auto-save edited files to trigger the watcher"
  - Uncheck "Trigger the watcher on external changes"


### VSCode

The repository already contains the required settings for VSCode in
`.vscode`. If you want to automatically format when you save a file, you
can additionally enable the setting *Format on Save* in your VSCode.


Unit Tests
----------

Unit tests require the following dependencies: pytest, coverage

```bash
pip install coverage pytest
make unit-test
make coverage
```
