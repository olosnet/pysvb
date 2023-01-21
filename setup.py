from distutils.core import setup, Extension
from os import system
import platform

system = platform.system()
machine = platform.machine()

library_dirs = []
libraries = ['SVBCameraSDK', ]
extra_objects = []

x86_64_arch = ['x86_64', 'x64', 'AMD64']
x86_arch = ['i386', 'i686', 'x86']
armv6_arch = ['armv6l', 'arm']
armv7_arch = ['armv7l', ]
armv8_arch = ['aarch64_be', 'armv8b', 'armv8l', 'arm64', 'aarch64']
data_files = []

if system == 'Linux':
    library_dirs = ['stdc++', ]
    libraries = []

    # x86_64
    if machine in x86_64_arch:
        extra_objects = ['sdk/lib/linux/x64/libSVBCameraSDK.a', ]
    # x86
    elif machine in x86_arch:
        extra_objects = ['sdk/lib/linux/x86/libSVBCameraSDK.a', ]
    # armv6
    elif machine in armv6_arch:
        extra_objects = ['sdk/lib/linux/armv6/libSVBCameraSDK.a', ]
    # armv7
    elif machine in armv7_arch:
        extra_objects = ['sdk/lib/linux/armv7/libSVBCameraSDK.a', ]
    elif machine in armv8_arch:
        extra_objects = ['sdk/lib/linux/armv8/libSVBCameraSDK.a', ]
    else:
        raise Exception("Error: unsupported platform: {}".format(machine))

elif system == 'Windows':

    # x86_64
    if machine in x86_64_arch:
        library_dirs = ['sdk/lib/win/x64', ]
        data_files=[('lib/site-packages/pysvb', ["sdk/lib/win/x64/SVBCameraSDK.dll"]),]
    # x86
    elif machine in x86_arch:
        library_dirs = ['sdk/lib/win/x86', ]
        data_files=[('lib/site-packages/pysvb', ["sdk/lib/win/x86/SVBCameraSDK.dll"]),]
    else:
        raise Exception("Error: unsupported platform: {}".format(machine))

elif system == 'Darwin':
    library_dirs = ['stdc++', ]
    libraries = []

    # x86_64
    if machine in x86_64_arch:
        extra_objects = ['sdk/lib/mac/x64/libSVBCameraSDK.a', ]
    # x86
    elif machine in x86_arch:
        extra_objects = ['sdk/lib/mac/x86/libSVBCameraSDK.a', ]

    else:
        raise Exception("Error: unsupported platform: {}".format(machine))

else:
    raise Exception("Error: unsupported OS")


SVBCameraSDKModule = Extension('pysvb.svbcamerasdk', sources=['pysvb/svbcamerasdk.c'],
                               libraries=libraries,
                               library_dirs=library_dirs,
                               extra_objects=extra_objects,
                               language="c++",
                               include_dirs=['sdk/include', ])

setup(name='pysvb',
      license="MIT",
      version='0.2',
      description='SVBONY SDK Python Binding',
      ext_modules=[SVBCameraSDKModule, ],
      author_email='valerio.faiuolo@gmail.com',
      packages=["pysvb"],
      package_data={
          "pysvb": ["py.typed"],
      },
      data_files = data_files,
      author='Valerio Faiuolo',
      keywords=["svbony", "sdk", "camera"],
      python_requires=">=3.4,<4",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Operating System :: Microsoft :: Windows :: Windows 7',
          'Operating System :: Microsoft :: Windows :: Windows 8',
          'Operating System :: Microsoft :: Windows :: Windows 8.1',
          'Operating System :: Microsoft :: Windows :: Windows 10',
          'Operating System :: Microsoft :: Windows :: Windows Server 2008',
          'Operating System :: POSIX :: Linux',
          'Environment :: MacOS X',
          'Programming Language :: C',
          'Programming Language :: C++',
      ]
)
