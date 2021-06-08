## Requirements

This pipeline will run on MacOSX or Linux. An install of Miniconda will make the setup of this pipeline on your local machine much more streamlined. To install Miniconda, visit [here](https://docs.conda.io/en/latest/miniconda.html) in a browser, scroll to see the install link specific for your operating system (MacOSX or Linux) and follow the link to the download instructions. 

## Installation

1. Clone this repository and ``cd hedgehog``
2. ``conda env create -f environment.yml``
3. ``conda activate hedgehog``
4. ``pip install .``
5. That's it

## Check the install worked

Type (in the <strong>hedgehog</strong> environment):

```
hedgehog -v
```
and you should see the versions of <strong>hedgehog</strong>.

### [Next: Updating](./updating.md)
