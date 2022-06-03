from setuptools import setup, find_namespace_packages

setup(name='inference_server_client',
      packages=find_namespace_packages(include=["inference_server_client", "inference_server_client.*"]),
      version='0.1',
      description='Inference server client for inference_client',
      url='',
      author='Mathis Ersted Rasmussen',
      author_email='mathis.rasmussen@rm.dk',
      license='Apache License Version 2.0, January 2004',
      install_requires=[
            "requests", "pydantic", "python-dotenv"
      ],
      entry_points={
          'console_scripts': [
              'infer_cli = inference_server_client.main:main',
          ],
      },
      keywords=['']
      )
