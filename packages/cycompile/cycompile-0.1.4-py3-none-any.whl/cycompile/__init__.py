"""
@author: Ranuja Pinnaduwage

This file is part of cycompile, a Python package for optimizing function performance via a Cython decorator.

Description:
This file defines the initialization of the package.

Copyright (C) 2025 Ranuja Pinnaduwage  
Licensed under the Apache License, Version 2.0 (the "License");  
you may not use this file except in compliance with the License.  
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software  
distributed under the License is distributed on an "AS IS" BASIS,  
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
See the License for the specific language governing permissions and  
limitations under the License.
"""

from .cythonize_decorator import cycompile, clear_cache

__all__ = ['cycompile', 'clear_cache']
