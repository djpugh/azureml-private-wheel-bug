
from azureml.core import Run

print('Hello World')

RUN = Run.get_context(allow_offline=True)
RUN.log('hello', 'world')
