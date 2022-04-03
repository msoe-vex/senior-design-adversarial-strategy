# MSOE Senior Design - Adversarial Strategy VEX Robot Program
![Unit Tests](https://github.com/msoe-vex/senior-design-adversarial-strategy/actions/workflows/test-runner.yml/badge.svg)

Adversarial strategy and game playing project for the MSOE Senior Design Team focused on bringing AI to the MSOE VEX U Team's robots.

## Get started
Install multi-agent fork:
```
git clone https://github.com/ChipHennig/marl-baselines3.git
pip install /pathto/marl-baselines3
```
After installing packages and activating the virtual env, run
```
python src/training.py
```
To view all training benchmarks in tensorboard:
```
python -m tensorboard.main --logdir logs/tensorboard/
```
![Interpret results here](https://stable-baselines3.readthedocs.io/en/master/common/logger.html?highlight=eval#eval)
## Running Locally
Running this project locally requires installing some Pip packages to get all dependencies sorted. We **highly** recommend utilizing a Python virtual environment, which can be set up with one of the following command sets running in the project root:

**Executing in Bash**
```
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

**Executing in Powershell**
```
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Unit Testing
This code utilizes the python `unittest` library for running unit tests. This can be done by running the following at the root of the project:

```
python -m unittest discover
```

Optionally, you can utilize the built-in VSCode tasks to run unit tests, located in the top menu (`Terminal` > `Run Task` > `Run Unit Tests`). This requires adding a `settings.json` file to your local `.vscode` folder, with the `python.pythonPath` variable being set (either to your virtual environment python interpreter, or your system python interpreter).

An example configuration, with a virtual environment called `venv` is shown below:

```
{
    "python.pythonPath": "venv/Scripts/python.exe"
}
```

## Contributing

Some libraries are currently used by this repository to help boost code quality and functionality. To download them, run the following line from the project root directory:

```
pip install -r requirements.txt
```

**NOTE:** We recommend a Python virtual environment is used for this.

The libraries included are discussed below as needed.

### Black: Python Formatting Utility
Black is a [python formatting utility](https://pypi.org/project/black/) which is included in this project to help with formatting. It can be run using the following command, which will format all files within a specified directory:

```
black *.py
```

This will automatically format all files within a specific directory. Currently, no recursive option exists for this formatting.

