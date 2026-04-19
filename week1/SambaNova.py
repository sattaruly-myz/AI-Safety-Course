import os
os.environ['SAMBANOVA_API_KEY'] = '96982bb7-97b0-4055-89d5-ded6239603ca'

from inspect_ai import eval
eval(
    "hello_model",
    model="sambanova/DeepSeek-V3",
)