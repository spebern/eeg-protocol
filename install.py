import pip

_all_ = [
    "pygame",
    "screeninfo",
    "pylsl",
    "scipy"
]

windows = [
    "pypiwin32"
]


def install(packages):
    for package in packages:
        pip.main(['install', package])


if __name__ == '__main__':

    from sys import platform

    install(_all_)
    if platform == 'windows':
        install(windows)
