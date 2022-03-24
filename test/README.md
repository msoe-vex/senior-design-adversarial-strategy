Execute tests with the following command *from the root directory*:

```
python -m unittest discover
```

To run a specific directory or package, one of the following can be used:

```
python -m unittest [PACKAGE]

python -m unittest [PACKAGE].[CLASS]
```

More information [can be found here](https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure).

Tests can be added in a folder structure matching the source directly. Test files need to match the pattern `test*.py`.

Any additional folders below the `test` folder require a blank `__init__.py` [to be created within the folder for the tests to be auto-discovered](https://stackoverflow.com/questions/29713541/recursive-unittest-discover). 