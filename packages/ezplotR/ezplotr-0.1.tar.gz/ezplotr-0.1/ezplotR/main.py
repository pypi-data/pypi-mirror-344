import os

class ExperimentBase:
    def __init__(self, index):
        self.index = index
        self.file_name = f"exp_{self.index}.py"
        self.content = self._read_file()

    def _get_file_path(self):
        # Get the directory where *this* file is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Point to the data folder
        data_dir = os.path.join(base_dir, 'data')
        return os.path.join(data_dir, self.file_name)

    def _read_file(self):
        file_path = self._get_file_path()
        if not os.path.exists(file_path):
            return f"File {file_path} does not exist."
        with open(file_path, 'r') as f:
            return f.read()

    def print_content(self):
        print(self.content)

    def save_content(self, output_file):
        with open(output_file, 'w') as f:
            f.write(self.content)
        print(f"Content saved to {output_file}")



class Plot1(ExperimentBase):
    def __init__(self):
        super().__init__(1)

class Plot2(ExperimentBase):
    def __init__(self):
        super().__init__(2)

class Plot3(ExperimentBase):
    def __init__(self):
        super().__init__(3)

class Plot4(ExperimentBase):
    def __init__(self):
        super().__init__(4)

class Plot5(ExperimentBase):
    def __init__(self):
        super().__init__(5)

class Plot6(ExperimentBase):
    def __init__(self):
        super().__init__(6)

class Plot7(ExperimentBase):
    def __init__(self):
        super().__init__(7)

class Plot8(ExperimentBase):
    def __init__(self):
        super().__init__(8)

class Plot9(ExperimentBase):
    def __init__(self):
        super().__init__(9)

class Plot10(ExperimentBase):
    def __init__(self):
        super().__init__(10)

