import ast
import inspect
import sys
from types import ModuleType


class PatternMatcher:
    def __init__(self, value):
        self.value = value
        # Store all available classes by name for later lookup
        self.class_cache = {}
        self._build_class_cache()

    def _build_class_cache(self):
        """Build a cache of class names to class objects from all accessible scopes."""
        # First check current frame
        frame = inspect.currentframe()
        while frame:
            for name, obj in frame.f_globals.items():
                if isinstance(obj, type) and name not in self.class_cache:
                    self.class_cache[name] = obj
            for name, obj in frame.f_locals.items():
                if isinstance(obj, type) and name not in self.class_cache:
                    self.class_cache[name] = obj
            frame = frame.f_back

        # Also check all stack frames
        for frame_info in inspect.stack():
            for name, obj in frame_info.frame.f_globals.items():
                if isinstance(obj, type) and name not in self.class_cache:
                    self.class_cache[name] = obj
            for name, obj in frame_info.frame.f_locals.items():
                if isinstance(obj, type) and name not in self.class_cache:
                    self.class_cache[name] = obj

    def _get_class(self, cls_name):
        """Get a class by name, looking in various scopes."""
        # First check our cache
        if cls_name in self.class_cache:
            return self.class_cache[cls_name]

        # Check builtin types
        builtin_types = {
            'int': int, 'str': str, 'float': float, 'bool': bool,
            'list': list, 'dict': dict, 'tuple': tuple, 'set': set
        }
        if cls_name in builtin_types:
            return builtin_types[cls_name]

        # Look through all frames
        frame = inspect.currentframe()
        while frame:
            if cls_name in frame.f_globals:
                cls = frame.f_globals[cls_name]
                self.class_cache[cls_name] = cls
                return cls
            if cls_name in frame.f_locals:
                cls = frame.f_locals[cls_name]
                self.class_cache[cls_name] = cls
                return cls
            frame = frame.f_back

        # Check all stack frames
        for frame_info in inspect.stack():
            if cls_name in frame_info.frame.f_globals:
                cls = frame_info.frame.f_globals[cls_name]
                self.class_cache[cls_name] = cls
                return cls
            if cls_name in frame_info.frame.f_locals:
                cls = frame_info.frame.f_locals[cls_name]
                self.class_cache[cls_name] = cls
                return cls

        raise NameError(f"Class '{cls_name}' not found")

    def match(self, pattern):
        if isinstance(pattern, ast.MatchValue):
            # Handle literals and named constants
            if isinstance(pattern.value, ast.Name):
                # This is a named constant like True, False, None or a user-defined constant
                const_name = pattern.value.id
                if const_name in ("True", "False", "None"):
                    # Handle built-in constants
                    const_val = {"True": True, "False": False, "None": None}[const_name]
                    return {} if self.value == const_val else None
                else:
                    # Handle user-defined constants
                    frame = inspect.currentframe().f_back
                    while frame:
                        if const_name in frame.f_globals:
                            const_val = frame.f_globals[const_name]
                            return {} if self.value == const_val else None
                        if const_name in frame.f_locals:
                            const_val = frame.f_locals[const_name]
                            return {} if self.value == const_val else None
                        frame = frame.f_back
                    # If we get here, the name wasn't found, look in stack frames
                    for frame_info in inspect.stack():
                        if const_name in frame_info.frame.f_globals:
                            const_val = frame_info.frame.f_globals[const_name]
                            return {} if self.value == const_val else None
                        if const_name in frame_info.frame.f_locals:
                            const_val = frame_info.frame.f_locals[const_name]
                            return {} if self.value == const_val else None
                    raise NameError(f"name '{const_name}' is not defined")
            elif isinstance(pattern.value, ast.Attribute):
                # Handle dotted names like math.pi
                module_name = pattern.value.value.id
                attr_name = pattern.value.attr

                # Get the module
                if module_name in sys.modules:
                    module = sys.modules[module_name]
                else:
                    try:
                        module = __import__(module_name)
                    except ImportError:
                        raise NameError(f"module '{module_name}' not found")

                # Get the attribute
                if hasattr(module, attr_name):
                    const_val = getattr(module, attr_name)
                    return {} if self.value == const_val else None
                else:
                    raise AttributeError(f"module '{module_name}' has no attribute '{attr_name}'")
            else:
                # This is a literal value
                const_val = ast.literal_eval(pattern.value)
                return {} if self.value == const_val else None

        elif isinstance(pattern, ast.MatchSingleton):
            # Handle None, True, False
            const_val = {None: None, True: True, False: False}[pattern.value]
            return {} if self.value == const_val else None

        elif isinstance(pattern, ast.MatchAs):
            if pattern.pattern is not None:
                # This is an AS pattern (e.g., case x as y)
                submatch = self.match(pattern.pattern)
                if submatch is None:
                    return None
                if pattern.name is not None:
                    submatch[pattern.name] = self.value
                return submatch
            elif pattern.name is None:
                return {}  # Wildcard '_'
            else:
                return {pattern.name: self.value}  # Capture pattern

        elif isinstance(pattern, ast.MatchOr):
            for subpattern in pattern.patterns:
                submatch = PatternMatcher(self.value).match(subpattern)
                if submatch is not None:
                    return submatch
            return None

        elif isinstance(pattern, ast.MatchSequence):
            if not isinstance(self.value, (list, tuple)):
                return None

            # Handle star patterns
            star_pattern_idx = None
            for i, p in enumerate(pattern.patterns):
                if isinstance(p, ast.MatchStar):
                    star_pattern_idx = i
                    break

            if star_pattern_idx is None:
                # Simple sequence pattern without star
                if len(pattern.patterns) != len(self.value):
                    return None
                bindings = {}
                for p, v in zip(pattern.patterns, self.value):
                    submatch = PatternMatcher(v).match(p)
                    if submatch is None:
                        return None
                    bindings.update(submatch)
                return bindings
            else:
                # Sequence pattern with star
                min_length = len(pattern.patterns) - 1
                if len(self.value) < min_length:
                    return None

                bindings = {}
                patterns_before_star = pattern.patterns[:star_pattern_idx]
                patterns_after_star = pattern.patterns[star_pattern_idx + 1:]

                # Match patterns before star
                values_before_star = self.value[:len(patterns_before_star)]
                for p, v in zip(patterns_before_star, values_before_star):
                    submatch = PatternMatcher(v).match(p)
                    if submatch is None:
                        return None
                    bindings.update(submatch)

                # Match patterns after star
                values_after_star = self.value[-len(patterns_after_star):] if patterns_after_star else []
                for p, v in zip(patterns_after_star, values_after_star):
                    submatch = PatternMatcher(v).match(p)
                    if submatch is None:
                        return None
                    bindings.update(submatch)

                # Capture star pattern
                star_pattern = pattern.patterns[star_pattern_idx]
                if star_pattern.name is not None:
                    star_values = self.value[len(patterns_before_star):-len(patterns_after_star) or None]
                    bindings[star_pattern.name] = star_values

                return bindings

        elif isinstance(pattern, ast.MatchStar):
            # Standalone star pattern (should not happen in practice)
            return {pattern.name: self.value} if pattern.name is not None else {}

        elif isinstance(pattern, ast.MatchMapping):
            if not isinstance(self.value, dict):
                return None

            # Check if we have a ** rest pattern
            rest_pattern = None
            keys_idx = -1
            for i, p in enumerate(pattern.patterns):
                if isinstance(p, ast.MatchStar):
                    rest_pattern = p
                    keys_idx = i
                    break

            # Handle required keys
            keys = [ast.literal_eval(k) for k in pattern.keys]
            # Check if all required keys are present
            if not all(k in self.value for k in keys):
                return None

            # If rest_pattern is None and no ** is used, this is an exact match and no other keys are allowed
            if rest_pattern is None and len(keys) > 0:
                # If exact matching is required, check that there are no extra keys
                value_keys = set(self.value.keys())
                pattern_keys = set(keys)
                if not pattern_keys.issuperset(value_keys):
                    return None

            bindings = {}
            # Match the required key-value pairs
            for i, (k_node, p) in enumerate(zip(pattern.keys, pattern.patterns)):
                if i == keys_idx:
                    continue  # Skip the ** rest pattern for now

                k = ast.literal_eval(k_node)
                if k not in self.value:
                    return None

                subval = self.value[k]
                submatch = PatternMatcher(subval).match(p)
                if submatch is None:
                    return None
                bindings.update(submatch)

            # Handle ** rest pattern if present
            if rest_pattern is not None and rest_pattern.name is not None:
                rest_keys = set(self.value.keys()) - set(keys)
                rest_dict = {k: self.value[k] for k in rest_keys}
                bindings[rest_pattern.name] = rest_dict

            return bindings

        elif isinstance(pattern, ast.MatchClass):
            # Get class name
            if isinstance(pattern.cls, ast.Name):
                cls_name = pattern.cls.id
            elif isinstance(pattern.cls, ast.Attribute):
                module_path = []
                node = pattern.cls
                while isinstance(node, ast.Attribute):
                    module_path.insert(0, node.attr)
                    node = node.value
                if isinstance(node, ast.Name):
                    module_path.insert(0, node.id)
                cls_name = module_path[-1]
            else:
                cls_name = None

            # Look up the class using our enhanced lookup
            try:
                cls = self._get_class(cls_name)
            except NameError:
                # Special case for built-in types
                builtin_types = {
                    'int': int, 'str': str, 'float': float, 'bool': bool,
                    'list': list, 'dict': dict, 'tuple': tuple, 'set': set
                }
                if cls_name in builtin_types:
                    return {} if isinstance(self.value, builtin_types[cls_name]) else None
                return None

            # Check if the value is an instance of the class
            if not isinstance(self.value, cls):
                return None

            bindings = {}

            # Handle positional attributes using __match_args__
            match_args = getattr(self.value.__class__, '__match_args__', ())
            for idx, subpattern in enumerate(pattern.patterns):
                if idx >= len(match_args):
                    return None
                attr_name = match_args[idx]
                attr_val = getattr(self.value, attr_name, None)
                submatch = PatternMatcher(attr_val).match(subpattern)
                if submatch is None:
                    return None
                bindings.update(submatch)

            # Handle keyword attributes
            for attr, subpattern in zip(pattern.kwd_attrs, pattern.kwd_patterns):
                attr_val = getattr(self.value, attr, None)
                submatch = PatternMatcher(attr_val).match(subpattern)
                if submatch is None:
                    return None
                bindings.update(submatch)

            return bindings

        return None