from setuptools import find_packages, setup
import sys
import os

# Force the use of the virtual environment Python if available
if 'VIRTUAL_ENV' in os.environ:
    venv_python = os.path.join(os.environ['VIRTUAL_ENV'], 'bin', 'python')
    if os.path.exists(venv_python):
        sys.executable = venv_python

package_name = 'r2d2_audio'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'pyttsx3', 'pyaudio', 'soundfile', 'google-generativeai', 'whisper'],
    zip_safe=True,
    maintainer='amine',
    maintainer_email='amine@todo.todo',
    description='R2D2 Audio ROS2 package with STT, Gemini LLM, and TTS',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'stt_node = r2d2_audio.nodes.stt_node:main',
            'llm_node = r2d2_audio.nodes.llm_node:main',
            'tts_node = r2d2_audio.nodes.tts_node:main',
        ],
    },
)
