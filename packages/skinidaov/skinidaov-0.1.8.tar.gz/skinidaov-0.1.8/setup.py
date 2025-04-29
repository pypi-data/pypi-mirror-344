from setuptools import setup, find_packages

setup(
    name='skinidaov',
    version='0.1.8',
    packages=find_packages(),
    description='Một bộ chuyển đổi ID đơn giản của Ron AOV',
    long_description=open('README.md', encoding='utf-8').read(),  # <-- thêm dòng này
    long_description_content_type='text/markdown',                # <-- và dòng này
    author='Ron AOV',
    author_email='ronlatoiday@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)