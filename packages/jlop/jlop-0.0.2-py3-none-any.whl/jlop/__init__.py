"""Top-level package for Jlop."""

__author__ = """dribeiro"""
__version__ = '0.1.0'

from .load_style import set_style
from .colors import set_colorcycle

#
# Note: Jplot overwrites the default keyword arguments of the
# errorbar function so that points are never connected by
# default
#

import matplotlib.pyplot as plt

plt._default_errorbar = plt.errorbar
plt.Axes._default_errorbar = plt.Axes.errorbar

#Overwrite plt.errorbar()
def _custom_errorbar(*args, **kwargs):
    kwargs.setdefault('linestyle', '-') 
    plt._default_errorbar(*args, **kwargs)  

#Overwrite axex.errorbar()
def _custom_ax_errorbar(self, *args, **kwargs):
    kwargs.setdefault('linestyle', '') 
    kwargs.setdefault('lw', 0.8)
    kwargs.setdefault('ms', 3.0)
    kwargs.setdefault('capsize', 2.0)  
    self._default_errorbar(*args, **kwargs)  

plt.errorbar = _custom_errorbar
plt.Axes.errorbar = _custom_ax_errorbar

