
# Intro

Python import paths can cause trouble, until you understand a bit how they work.

## How imports resolve

The path to absolute imports is resolved from:

- `sys.path` -> best not to modify
- The script location -> where the script is run from. What we can become familiar with
- `PYTHONPATH` environment variable -> what we can use to alter the resolution path

### Example & Explanation

Starting from the folder `/home/.../imports/sibling_folder/`

Running:
```bash
PYTHONPATH=. python3 code_folder/run.py
```

Then the import should be only `from config_folder import config`, not `from sibling_folder.config_folder import config`, because we're already inside the `sibling_folder` package/module.

This is the easiest way if you always start your application/service from the same folder, and run all the tests from there too (e.g. via a Makefile, and/or inside a Docker container).

An alternative is to **always use relative imports**, which nowadays is easy with modern IDEs that automatically refactor the imports for you.


## Notes

- Since Python 3.3, there is no need for `__init__.py` files in folders


## Good readings

- https://realpython.com/python-modules-packages/#python-modules-overview
- https://realpython.com/absolute-vs-relative-python-imports/