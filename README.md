# OSSU Game Project

## Setup

We're using virtualenvs with Python 3.10, ensure you're using something similar:

```
python3 --version
```

To get started, create a virtual environment:

```
python3 -m venv .
```

Activate the virtual environment based on the operating system you're using. See
the Python documentation on [activating your venv](https://docs.python.org/3/library/venv.html#how-venvs-work)
for more details.

Once you're activated, install any requirements necessary:

```
pip install -r requirements.txt
```

## Coding

### Formatting

We're using black to format the code. Why? Because I don't like to argue about
formatting. Just use the default settings.

#### Function Breaks

Sometimes black will format a multiline function call like this:

```python
func(
    arg1, arg2, arg3
)
```

This is tricky to read. In order to get black to format this nicely, put a comma
at the end:

```python
func(
    arg1, arg2, arg3,
)
```

This will cause black to format it with one argument per line:

```python
func(
    arg1,
    arg2,
    arg3,
)
```

### Style

Use the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
to style your code.

In the case of a conflict between black's defaults and the style guide, prefer
the black version.

Note that reviewers may not know/remember the style guide 100%, so feel free to
mention (with references) when a review comment violates it.
