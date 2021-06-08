# Updating

Navigate to your local hedgehog repository on the command line.

1. ``conda activate hedgehog``
2. ``git pull`` \
pulls the latest changes from github
3. ``conda env update -f environment.yml`` \
updates the conda environment 
4. ``pip install .`` \
re-installs hedgehog.

## Troubleshooting update

- If you have previously installed hedgehog using ``pip``, you will need to update hedgehog in the same way (``pip install .``)
- Try ``pip uninstall hedgehog`` and then re-install with `python setup.py install`

## [Next: Usage](./usage.md)