from distutils.core import setup

setup(name='Hive',
      version='1.0',
      description='Python lab hardware abstraction',
      author='Michiel Jordens',
      author_email='michiel.jordens@imec.be',
      url='https://github.imec.be/MCA-IBA/mca-control-panel',
      install_requires=['uvicorn==0.14.0',
                        'pandas==1.2.4',
                        'matplotlib==3.4.2',
                        'dash==1.20.0',
                        'numpy==1.20.3',
                        'requests==2.25.1',
                        'plotly==4.14.3',
                        'pydantic==1.8.2',
                        'dash_core_components==1.16.0',
                        'tornado==6.1',
                        'dash_html_components==1.1.3',
                        'scipy==1.6.3',
                        'fastapi==0.66.0',
                        'pytest==6.2.4',
                        'aiofiles==0.7.0',
                        'python-multipart==0.0.5',
                        'aiohttp==3.7.4'
                        ]
      )
