# MSOE Senior Design - Adversarial Strategy VEX Robot Program
Adversarial strategy and game playing project for the MSOE Senior Design Team focused on bringing AI to the MSOE VEX U Team's robots.

## Get started
After installing packages and activating the virtual env, run
```
python src/training.py
```
To view all training benchmarks in tensorboard:
```
python -m tensorboard.main --logdir logs/tensorboard/
```
Interpret results here[https://stable-baselines3.readthedocs.io/en/master/common/logger.html?highlight=eval#eval]

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
