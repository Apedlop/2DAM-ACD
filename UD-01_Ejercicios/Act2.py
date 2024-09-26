class FileHandler:
    def read_file(self, file_path, mode='r'):
        try:
            with open(file_path, mode) as f:
                content = f.read()
                return content
        except Exception as e:
            print(f"Error leyendo el archivo: {e}")
    def write_file(self, file_path, content, mode='w'):
        try:
            with open(file_path, mode) as f:
                f.write(content)
        except Exception as e:
            print(f"Error escribiendo en el archivo: {e}")

file_handler = FileHandler()
file_handler.write_file("20094042.txt", "10/01/2005")
print(file_handler.read_file("20094042.txt"))

