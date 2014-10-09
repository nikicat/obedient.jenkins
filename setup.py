import setuptools

if __name__ == '__main__':
    setuptools.setup(
        name='obedient.jenkins',
        version='1.0.0',
        url='https://github.com/yandex-sysmon/obedient.jenkins',
        license='LGPLv3',
        author='Nikolay Bryskin',
        author_email='devel.niks@gmail.com',
        description='Jenkins CI obedient for Dominator',
        platforms='linux',
        packages=['obedient.jenkins'],
        namespace_packages=['obedient'],
        package_data={'obedient.jenkins': []},
        entry_points={'obedient': [
            'create = obedient.jenkins:create',
        ]},
        install_requires=[
            'dominator[full] >=9.1',
        ],
    )
