"""
SDK Introspector - Discovers and analyzes Python SDK structure.
"""

import inspect
import importlib
import ast
import sys
from typing import Dict, List, Any, Optional, Type, Callable, Union
from pathlib import Path


class SDKIntrospector:
    """
    Introspects Python SDKs to discover classes, methods, and their signatures.
    
    This class analyzes SDK modules to extract:
    - Available classes and their methods
    - Method signatures and parameters
    - Type hints and documentation
    - Inheritance hierarchies
    - Module structure
    """
    
    def __init__(self):
        self.discovered_modules = set()
        self.cache = {}
    
    def introspect_sdk(self, module_name: str, include_private: bool = False) -> Dict[str, Any]:
        """
        Main method to introspect an SDK module.
        
        Args:
            module_name: Name of the SDK module to introspect
            include_private: Whether to include private methods (starting with _)
            
        Returns:
            Dictionary containing discovered SDK structure
        """
        try:
            # Import the module
            module = importlib.import_module(module_name)
            
            # Discover all classes and methods
            classes = self._discover_classes(module, include_private)
            methods = self._discover_methods(module, include_private)
            functions = self._discover_functions(module, include_private)
            
            # Analyze module structure
            module_info = self._analyze_module(module)
            
            return {
                "module_name": module_name,
                "module_info": module_info,
                "classes": classes,
                "methods": methods,
                "functions": functions,
                "total_items": len(classes) + len(methods) + len(functions)
            }
            
        except ImportError as e:
            raise ImportError(f"Could not import module '{module_name}': {e}")
        except Exception as e:
            raise Exception(f"Error introspecting module '{module_name}': {e}")
    
    def _discover_classes(self, module: Any, include_private: bool) -> List[Dict[str, Any]]:
        """Discover all classes in the module."""
        classes = []
        
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and self._is_defined_in_module(obj, module):
                if not include_private and name.startswith('_'):
                    continue
                    
                class_info = {
                    "name": name,
                    "module": obj.__module__,
                    "docstring": inspect.getdoc(obj) or "",
                    "methods": self._get_class_methods(obj, include_private),
                    "bases": [base.__name__ for base in obj.__bases__],
                    "mro": [cls.__name__ for cls in inspect.getmro(obj)]
                }
                classes.append(class_info)
        
        return classes
    
    def _discover_methods(self, module: Any, include_private: bool) -> List[Dict[str, Any]]:
        """Discover all methods across all classes in the module."""
        methods = []
        
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and self._is_defined_in_module(obj, module):
                class_methods = self._get_class_methods(obj, include_private)
                for method_info in class_methods:
                    method_info["class_name"] = name
                    method_info["class_module"] = obj.__module__
                    methods.append(method_info)
        
        return methods
    
    def _discover_functions(self, module: Any, include_private: bool) -> List[Dict[str, Any]]:
        """Discover standalone functions in the module."""
        functions = []
        
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and self._is_defined_in_module(obj, module):
                if not include_private and name.startswith('_'):
                    continue
                    
                function_info = self._analyze_callable(obj)
                function_info["name"] = name
                function_info["module"] = obj.__module__
                functions.append(function_info)
        
        return functions
    
    def _get_class_methods(self, cls: Type, include_private: bool) -> List[Dict[str, Any]]:
        """Get all methods from a class."""
        methods = []
        
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if not include_private and name.startswith('_'):
                continue
                
            method_info = self._analyze_callable(method)
            method_info["name"] = name
            method_info["is_static"] = isinstance(method, staticmethod)
            method_info["is_class"] = isinstance(method, classmethod)
            methods.append(method_info)
        
        return methods
    
    def _analyze_callable(self, callable_obj: Callable) -> Dict[str, Any]:
        """Analyze a callable (function or method) to extract its signature and metadata."""
        try:
            signature = inspect.signature(callable_obj)
            
            parameters = []
            for param_name, param in signature.parameters.items():
                param_info = {
                    "name": param_name,
                    "default": param.default if param.default != inspect.Parameter.empty else None,
                    "annotation": str(param.annotation) if param.annotation != inspect.Parameter.empty else None,
                    "kind": str(param.kind)
                }
                parameters.append(param_info)
            
            return {
                "parameters": parameters,
                "return_annotation": str(signature.return_annotation) if signature.return_annotation != inspect.Parameter.empty else None,
                "docstring": inspect.getdoc(callable_obj) or "",
                "is_async": inspect.iscoroutinefunction(callable_obj),
                "is_generator": inspect.isgeneratorfunction(callable_obj)
            }
            
        except Exception as e:
            # Fallback for callables that can't be analyzed
            return {
                "parameters": [],
                "return_annotation": None,
                "docstring": inspect.getdoc(callable_obj) or "",
                "is_async": False,
                "is_generator": False,
                "analysis_error": str(e)
            }
    
    def _is_defined_in_module(self, obj: Any, module: Any) -> bool:
        """Check if an object is defined in the given module or its submodules."""
        try:
            obj_module = obj.__module__
            module_name = module.__name__
            
            # Direct match
            if obj_module == module_name:
                return True
            
            # Submodule match (e.g., github.MainClass for github module)
            if obj_module.startswith(module_name + "."):
                return True
            
            return False
        except AttributeError:
            return False
    
    def _analyze_module(self, module: Any) -> Dict[str, Any]:
        """Analyze module-level information."""
        return {
            "name": module.__name__,
            "file": getattr(module, '__file__', None),
            "package": getattr(module, '__package__', None),
            "docstring": inspect.getdoc(module) or "",
            "version": getattr(module, '__version__', None),
            "author": getattr(module, '__author__', None)
        }
    
    def get_method_signature_string(self, method_info: Dict[str, Any]) -> str:
        """Convert method info to a readable signature string."""
        params = []
        for param in method_info.get("parameters", []):
            param_str = param["name"]
            if param["annotation"]:
                param_str += f": {param['annotation']}"
            if param["default"] is not None:
                param_str += f" = {repr(param['default'])}"
            params.append(param_str)
        
        signature = f"{method_info['name']}({', '.join(params)})"
        
        if method_info.get("return_annotation"):
            signature += f" -> {method_info['return_annotation']}"
        
        return signature
    
    def filter_methods_by_pattern(self, methods: List[Dict], pattern: str) -> List[Dict]:
        """Filter methods by name pattern."""
        import re
        regex = re.compile(pattern, re.IGNORECASE)
        return [method for method in methods if regex.search(method["name"])]
    
    def group_methods_by_class(self, methods: List[Dict]) -> Dict[str, List[Dict]]:
        """Group methods by their containing class."""
        groups = {}
        for method in methods:
            class_name = method.get("class_name", "standalone")
            if class_name not in groups:
                groups[class_name] = []
            groups[class_name].append(method)
        return groups
