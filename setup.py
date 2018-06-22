from setuptools import setup

setup(
    name='luma',
    version='',
    packages=['luma', 'luma.lcd', 'luma.core', 'luma.core.legacy', 'luma.core.interface', 'luma.oled', 'luma.emulator',
              'luma.led_matrix', 'examples', 'examples.hotspot'],
    install_requires=["Pillow >= 5.1.0", 'monotonic', 'psutil', 'spidev'],
    url='',
    license='',
    author='Kenneth A. Jones',
    author_email='',
    description=''
)
