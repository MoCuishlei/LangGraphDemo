class DependencyGraph:
    def __init__(self):
        # Initialize data structures to track dependencies
        self.function_calls = {}
        self.class_dependencies = {}
        self.import_relationships = {}
        self.call_chains = {}

    def track_function_call(self, caller, callee):
        # Track function call relationship
        if caller not in self.function_calls:
            self.function_calls[caller] = []
        self.function_calls[caller].append(callee)

    def track_class_dependency(self, class_name, dependency):
        # Track class dependency
        if class_name not in self.class_dependencies:
            self.class_dependencies[class_name] = []
        self.class_dependencies[class_name].append(dependency)

    def track_import(self, module_name, imported_module):
        # Track import relationships
        if module_name not in self.import_relationships:
            self.import_relationships[module_name] = []
        self.import_relationships[module_name].append(imported_module)

    def build_call_chain(self, function_name, called_functions):
        # Build call chain for a function
        self.call_chains[function_name] = called_functions

    def __str__(self):
        return f"Function Calls: {self.function_calls}\nClass Dependencies: {self.class_dependencies}\nImport Relationships: {self.import_relationships}\nCall Chains: {self.call_chains}"