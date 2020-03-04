import os
import glob
import subprocess
import sys


from azureml.core import Experiment, Workspace
from azureml.core.environment import Environment
from azureml.core.conda_dependencies import CondaDependencies
from azureml.train.estimator import Estimator
import click

# Env vars are:

SUBSCRIPTION_ID_ENV_KEY = 'AML_SUBSCRIPTION_ID'
RESOURCE_GROUP_ENV_KEY = 'AML_RESOURCE_GROUP'
WORKSPACE_NAME_ENV_KEY = 'AML_WORKSPACE_NAME'
COMPUTE_NAME_ENV_KEY = 'AML_COMPUTE_NAME'

@click.command()
@click.option('--private-wheel/--no-private-wheel', default=False)
def submit(private_wheel=False):
    # Load environment parameters
    subscription_id = os.environ.get(SUBSCRIPTION_ID_ENV_KEY)
    resource_group = os.environ.get(RESOURCE_GROUP_ENV_KEY)
    workspace_name = os.environ.get(WORKSPACE_NAME_ENV_KEY)
    compute_name = os.environ.get(COMPUTE_NAME_ENV_KEY)
    # Assumes authentication is correctly setup and doesn't need to be provided
    ws = Workspace(subscription_id, resource_group, workspace_name)

    experiment = Experiment(workspace=ws, name="bug-repro-script-run")
    env = Environment('base-env')
    cd = CondaDependencies.create(pip_packages=['azureml-sdk'])
    # Build a test wheel
    if private_wheel:
        cwd = os.getcwd()
        os.chdir('basic_wheel')
        subprocess.check_call([sys.executable, 'setup.py', 'bdist_wheel'])
        os.chdir(cwd)
        wheel = glob.glob('basic_wheel/dist/testpackage*.whl')[0]
        cd.add_pip_package(Environment.add_private_pip_wheel(workspace=ws, file_path=wheel, exist_ok=True))

    env.python.conda_dependencies = cd

    compute_target = ws.compute_targets[compute_name]

    est = Estimator(source_directory=os.path.join(os.path.dirname(__file__), 'remote'),
                    script_params={},
                    compute_target=compute_target,
                    environment_definition=env,
                    entry_script='train.py')

    run = experiment.submit(config=est)
    print(run.get_portal_url())


if __name__ == "__main__":
    submit()
