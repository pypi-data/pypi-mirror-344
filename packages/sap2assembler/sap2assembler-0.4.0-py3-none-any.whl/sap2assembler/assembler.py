import os
import re

class assemblerError(Exception):
    pass

def insert(idx, string, char):
    return string[:idx] + char + string[idx:]

def normalize_spaces(string):
    # Replace multiple spaces with a single space
    return re.sub(r'\s+', ' ', string).strip()


class SAP2Assembler:
    def __init__(self):
        self.MnemonicToOpcode = {"add b": ["10000000", 1],
                                "add c": ["10000001", 1],
                                "adi": ["11000110", 2],
                                "ana b": ["10100000", 1],
                                "ana c": ["10100001", 1],
                                "ani": ["11100110", 2],
                                "call": ["11001101", 3],
                                "cmp b": ["10111000", 1],
                                "cmp c": ["10111001", 1],
                                "cpi": ["11111110", 2],
                                "dcr a": ["00111101", 1],
                                "dcr b": ["00000101", 1],
                                "dcr c": ["00001101", 1],
                                "hlt": ["01110110", 1],
                                "in": ["11011011", 2],
                                "inr a": ["00111100", 1],
                                "inr b": ["00000100", 1],
                                "inr c": ["00001100", 1],
                                "jmp": ["11000011", 3],
                                "jm": ["11111010", 3],
                                "jnz": ["11000010", 3],
                                "jz": ["11001010", 3],
                                "lda": ["00111010", 3],
                                "mov a, b": ["01111000", 1],
                                "mov a, c": ["01111001", 1],
                                "mov b, a": ["01000111", 1],
                                "mov b, c": ["01000001", 1],
                                "mov c, a": ["01001111", 1],
                                "mov c, b": ["01001000", 1],
                                "mvi a": ["00111110", 2],
                                "mvi b": ["00000110", 2],
                                "mvi c": ["00001110", 2],
                                "nop": ["00000000", 1],
                                "ora b": ["10110000", 1],
                                "ora c": ["10110001", 1],
                                "ori": ["11110110", 2],
                                "out": ["11010011", 2],
                                "ret": ["11001001", 1],
                                "sta": ["00110010", 3],
                                "sub b": ["10010000", 1],
                                "sub c": ["10010001", 1],
                                "sui": ["11010110", 2],
                                "xra b": ["10101000", 1],
                                "xra c": ["10101001", 1],
                                "xri": ["11101110", 2]}

        self.fileToAssemble = None
        self.fileToWrite = None
        self.address = "00"
        self.unformattedCodeToAssemble = ""
        self.codeToAssemble = ""
        self.labels = {}
        self.mnemonics_requiring_labels = ["call", "jmp", "jm", "jz", "jnz"]
        self.pseudo_instructions = [".org", ".word"]
        self.assemblyCodeLines = None
        self.mnemonics = [m.lower() for m in self.MnemonicToOpcode.keys()]
        self.assembledCode = [self.convertMnemonicToOpcode("nop") for i in range(65536)]
        self.variables = {}

    def defineVariable(self, assignment):
        equals_index = assignment.find("==")
        expr = insert(equals_index, assignment, " ")
        equals_index = assignment.find("==")
        expr = insert(equals_index+3, expr, " ")
        expr = normalize_spaces(expr)

        expression = expr.split(" ")
        if len(expression) != 3:
            raise assemblerError(f"invalid variable assignment on line {self.find_line_index(assignment)}")

        if expression[2].startswith("$"):
            expression[2] = expression[2][1:]
        elif expression[2].startswith("#"):
            location = expression[2][1:]
            int_location = int(location, 2)
            hex_location = hex(int_location)[2:]
            expression[2] = hex_location

        variable_name = expression[0]
        variable_location = expression[2].zfill(4)
        variable_symbol = [variable_location, None]

        if len(variable_location) > 4:
            raise assemblerError(f"invalid variable assignment on line {self.find_line_index(assignment)}")
        self.variables[variable_name] = variable_symbol

        # print(f"assigned variable {variable_name} to location {variable_location}")

    def setVariable(self, variable_set_expression):
        equals_index = variable_set_expression.find("=")
        expr = insert(equals_index, variable_set_expression, " ")
        equals_index = variable_set_expression.find("=")
        expr = insert(equals_index + 2, expr, " ")
        expr = normalize_spaces(expr)
        variable_specs = expr.split(" ")

        if len(variable_specs) != 3:
            raise assemblerError(f"invalid variable assignment on line {self.find_line_index(variable_set_expression)}")

        if variable_specs[2].startswith("$"):
            value = variable_specs[2][1:]
            int_value = int(value, 16)
            bin_value = bin(int_value)[2:]
            variable_specs[2] = bin_value

        elif variable_specs[2].startswith("#"):
            value = variable_specs[2][1:]
            int_value = int(value, 2)
            bin_value = bin(int_value)[2:]
            variable_specs[2] = bin_value

        variable_name = variable_specs[0]
        variable_value = variable_specs[2].zfill(8)

        if len(variable_value) > 8:
            raise assemblerError(f"invalid variable assignment on line {self.find_line_index(variable_set_expression)}")

        self.variables[variable_name][1] = variable_value
        self.assembledCode[int(self.variables[variable_name][0], 16)] = variable_value

        # print(f"set variable {variable_name} to value {variable_value}")

    def handleVariable(self, expression):
        if "==" in expression:
            self.defineVariable(expression)
        elif "=" in expression:
            self.setVariable(expression)

    def addressCheck(self):
        if int(self.address, 16) > 65535:
            raise assemblerError(
                f"the SAP2 architecture only supports 16 bits of address (65536 addresses), which is exceeded by {int(self.address, 16) - 65535}")

    def printAssembledCode(self, row_width=16, hex_data=False, n_bytes=256):
        # Loop through the assembled code
        for idx, data in enumerate(self.assembledCode):
            if idx >= n_bytes:
                break  # Exit early if we reach the n_bytes limit

            # If hex_data is True, convert data to hexadecimal
            if hex_data:
                data = hex(int(data, 2))[2:].zfill(2)

            # Print the address at the start of the row
            if idx % row_width == 0:
                print(f"{hex(idx)[2:].zfill(4)}: {data}", end=" ")
            elif (idx % row_width) != (row_width - 1):  # Printing middle bytes
                print(f"{data} ", end="")
            else:  # End of the row
                print(f"{data}")

    def identifyLabels(self):
        assemblyCode = ""
        assemblyCodeLines = []
        self.identifyVariables()
        self.address = "00"
        for line in self.assemblyCodeLines:
            keyword_detected = False
            for mnemonic in self.MnemonicToOpcode.keys():
                if line.startswith(mnemonic):
                    num_bytes = self.getNumBytesForMnemonic(mnemonic)
                    self.address = str(int(self.address, 16) + num_bytes)
                    assemblyCode += "\n" + line
                    assemblyCodeLines.append(line)
                    keyword_detected = True
                    break

            if "==" in line:
                pass

            if ".word" in line:
                self.address = str(int(self.address, 16) + 2)
                assemblyCode += "\n" + line
                assemblyCodeLines.append(line)
                keyword_detected = True

            if ".org" in line:
                origin = line[6:]
                operand_identifier = line[5]

                if operand_identifier == "$":
                    self.address = origin

                elif operand_identifier == "#":
                    int_origin = int(origin, 2)
                    hex_origin = hex(int_origin)[2:]
                    self.address = hex_origin

                assemblyCode += "\n" + line
                assemblyCodeLines.append(line)
                keyword_detected = True

            if ":" in line:
                label = line.split(":")[0]
                self.labels[label] = self.address
                keyword_detected = True

            if line.strip() != "" and keyword_detected == False:
                assemblyCode += "\n" + line
                assemblyCodeLines.append(line)
        self.address = "00"
        self.assemblyCodeLines = assemblyCodeLines
        self.codeToAssemble = assemblyCode

    def convertMnemonicToOpcode(self, mnemonic):
        return self.MnemonicToOpcode[mnemonic][0]

    def getNumBytesForMnemonic(self, mnemonic):
        return self.MnemonicToOpcode[mnemonic][1]

    def areKeywordsInLine(self, line):
        for mnemonic in self.MnemonicToOpcode.keys():
            if mnemonic in line:
                return True

        if (".org" in line) or (".word" in line) or "=" in line:
            return True

        return False

    def getCodeFromFile(self):
        with open(self.fileToAssemble, "r") as file:
            self.codeToAssemble = file.read()
        self.assemblyCodeLines = self.codeToAssemble.split("\n")
        self.unformattedCodeToAssemble = self.codeToAssemble

    def incrementAddress(self):
        self.address = int(self.address, 16)
        self.address += 1
        self.address = hex(self.address)[2:].zfill(2)

    def find_line_index(self, lineToFind):
        lines = self.unformattedCodeToAssemble.split("\n")
        for idx, line in enumerate(lines):
            if lineToFind == line:
                return idx+1
        return False

    def parse_number(self, number, identifier):
        if identifier == "$":
            int_number = int(number, 16)

            if int_number < 256:
                return bin(int_number)[2:].zfill(8), "0" * 8
            first_byte = int_number & 0x00FF
            second_byte = int_number >> 8
            return bin(first_byte)[2:].zfill(8), bin(second_byte)[2:].zfill(8)

        elif identifier == "#":
            int_number = int(number, 2)
            if int_number < 256:
                return bin(int_number)[2:].zfill(8), "0" * 8
            first_byte = int_number & 0x00FF
            second_byte = int_number >> 8
            return bin(first_byte)[2:].zfill(8), bin(second_byte)[2:].zfill(8)
        else:
            raise assemblerError(f"Unknown operand identifier {identifier}")

    def formatAssemblyLines(self):
        lines = []
        for line in self.assemblyCodeLines:
            if line.strip():
                if ";" in line:
                    comment_idx = line.find(";")
                    line = line[:comment_idx]
                    line = line.strip()
                lines.append(line)
        self.assemblyCodeLines = lines

    def saveAssembledCode(self, filename, row_width=16, hex_data=False, n_bytes=256):
        with open(filename, 'w') as file:
            if hex_data:
                for idx, data in enumerate(self.assembledCode):
                    if idx < n_bytes:
                        data = hex(int(data, 2))[2:].zfill(2)
                        if idx % row_width == 0:
                            file.write(f"{hex(idx)[2:].zfill(4)}: {data} ")
                        elif (row_width - 1) > (idx % row_width) > 0:
                            file.write(f"{data} ")
                        elif (idx % row_width) == (row_width - 1):
                            file.write(f"{data}\n")
            else:
                for idx, data in enumerate(self.assembledCode):
                    if idx < n_bytes:
                        if idx % row_width == 0:
                            file.write(f"{hex(idx)[2:].zfill(4)}: {data} ")
                        elif (row_width - 1) > (idx % row_width) > 0:
                            file.write(f"{data} ")
                        elif (idx % row_width) == (row_width - 1):
                            file.write(f"{data}\n")

    def identifyVariables(self):
        for line in self.assemblyCodeLines:
            if "=" in line:
                self.handleVariable(line)

    def assemble(self, fileToAssemble, fileToWrite="", row_width=16, hex_data=False, n_bytes=256, print_data=False):
        self.fileToAssemble = fileToAssemble
        self.fileToWrite = fileToWrite

        if not os.path.exists(fileToAssemble):
            raise assemblerError(f"File {fileToAssemble} not found")

        self.getCodeFromFile()
        self.formatAssemblyLines()
        self.identifyLabels()

        for line_idx, line in enumerate(self.assemblyCodeLines):
            if (".org" not in line) and (".word" not in line) and ("=" not in line):
                if not self.areKeywordsInLine(line):
                    raise assemblerError(f"Error in line {self.find_line_index(line)}, '{line}' doesn't contain a mnemonic or pseudo instruction")
                for mnemonic in self.MnemonicToOpcode.keys():
                    if line.startswith(mnemonic):
                        opcode = self.convertMnemonicToOpcode(mnemonic)
                        num_bytes = self.getNumBytesForMnemonic(mnemonic)
                        self.assembledCode[int(self.address, 16)] = opcode
                        if num_bytes == 1:
                            if line != mnemonic:
                                raise assemblerError(f"Error in line {self.find_line_index(line)}, '{line}' isn't a mnemonic")


                        if mnemonic not in self.mnemonics_requiring_labels:
                            if num_bytes > 1:
                                if "$" in line or "#" in line:
                                    number = line[len(mnemonic)+2:]
                                    operand_identifier = line[len(mnemonic)+1]
                                    first_byte, second_byte = self.parse_number(number, operand_identifier)
                                    if second_byte != "00000000" and num_bytes == 2:
                                        raise assemblerError(f"Error in line {self.find_line_index(line)}, invalid operand")
                                    self.incrementAddress()
                                    self.assembledCode[int(self.address, 16)] = first_byte
                                    if num_bytes == 3:
                                        self.incrementAddress()
                                        self.assembledCode[int(self.address, 16)] = second_byte
                                else:
                                    variable_name = line[len(mnemonic)+1:]
                                    if variable_name not in self.variables.keys():
                                        raise assemblerError(f"variable {variable_name} is not defined")

                                    variable_value = self.variables[variable_name][1]
                                    variable_location = self.variables[variable_name][0]

                                    self.incrementAddress()
                                    if num_bytes == 2:
                                        self.assembledCode[int(self.address, 16)] = variable_value
                                    else:
                                        first_byte, second_byte = self.parse_number(variable_location, "$")
                                        self.assembledCode[int(self.address, 16)] = first_byte
                                        self.incrementAddress()
                                        self.assembledCode[int(self.address, 16)] = second_byte

                        else:
                            label = line[len(mnemonic)+1:]
                            if label not in self.labels.keys():
                                raise assemblerError(f"Error in line {self.find_line_index(line)}, label '{label}' doesn't exist")
                            label_address = self.labels[label]
                            first_byte, second_byte = self.parse_number(label_address, "$")
                            self.incrementAddress()
                            self.assembledCode[int(self.address, 16)] = first_byte
                            self.incrementAddress()
                            self.assembledCode[int(self.address, 16)] = second_byte

                        break
                self.incrementAddress()

            if ".word" in line:
                word = line[7:]
                operand_identifier = line[6]
                first_byte, second_byte = self.parse_number(word, operand_identifier)
                self.incrementAddress()
                self.assembledCode[int(self.address, 16)] = first_byte
                self.incrementAddress()
                self.assembledCode[int(self.address, 16)] = second_byte

            if ".org" in line:
                origin = line[6:]
                operand_identifier = line[5]

                if operand_identifier == "$":
                    self.address = origin

                elif operand_identifier == "#":
                    int_origin = int(origin, 2)
                    hex_origin = hex(int_origin)[2:]
                    self.address = hex_origin

                else:
                    raise assemblerError(f"Unknown operand identifier {operand_identifier}")

            if ("=" in line) and ("==" not in line):
                self.handleVariable(line)

            self.addressCheck()

        if self.fileToWrite != "":
            self.saveAssembledCode(filename=self.fileToWrite, hex_data=hex_data, n_bytes=n_bytes, row_width=row_width)

        if print_data:
            self.printAssembledCode(row_width=row_width, hex_data=hex_data, n_bytes=n_bytes)
