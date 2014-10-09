from dominator.utils import resource_string
from dominator.entities import (SourceImage, Image, DataVolume, ConfigVolume, TemplateFile,
                                Container, LogVolume,
                                Shipment, Door, LogFile)


def create_one(version):
    jenkins_image = SourceImage(
        name='jenkins',
        parent=Image(namespace='yandex', repository='trusty'),
        scripts=[
            'apt-get update && apt-get install -y --no-install-recommends wget git curl zip openjdk-7-jdk'
            ' maven ant ruby rbenv make apt-transport-https',
            'apt-key adv --keyserver hkp://keyserver.ubuntu.com:80'
            ' --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9',
            'wget -q -O - http://pkg.jenkins-ci.org/debian/jenkins-ci.org.key | apt-key add -',
            'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list && '
            'echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list && '
            'apt-get update',
            'apt-get install -y jenkins={} lxc-docker'.format(version),
            'mkdir -p /var/jenkins_home && chown -R jenkins /var/jenkins_home',
        ],
        env={
            'JENKINS_HOME': '/var/jenkins_home',
        },
        ports={
            'http': 8080,
            'agent': 50000,
        },
        command='bash /scripts/jenkins.sh',
        files={
            '/scripts/jenkins.sh': resource_string('jenkins.sh'),
        },
        volumes={'data': '/var/jenkins_home'},
    )

    jenkins = Container(
        name='jenkins',
        image=jenkins_image,
        doors={
            'http': Door(schema='http', port=jenkins_image.ports['http']),
            'agent': Door(schema='jnlp', port=jenkins_image.ports['agent']),
        },
        volumes={
            'logs': LogVolume(
                dest='/var/log/jenkins',
                files={
                    'jenkins.log': LogFile()
                },
            ),
            'config': ConfigVolume(
                dest='/etc/jenkins',
                files={
                    'init.groovy': TemplateFile(resource_string('init.groovy')),
                },
            ),
            'data': DataVolume(dest='/var/jenkins_home'),
        },
    )

    return jenkins


def create(ships, httpport=80, version='1.583'):
    jenkinses = []
    for ship in ships:
        jenkins = create_one(version)
        ship.place(jenkins)
        jenkins.doors['http'].expose(httpport)
        ship.expose_all(range(50000, 50100))

        jenkinses.append(jenkins)

    return Shipment(name='default', containers=jenkinses)
