from setuptools import setup, find_packages

setup(
    name='cortexable',                   # 라이브러리 이름
    version='0.1.0',                     # 최초 버전
    author='nemo1866',
    author_email='newkikakika@gmail.com',
    description='this is cortexable library.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cortexable/py',  # 라이브러리 저장소 URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
