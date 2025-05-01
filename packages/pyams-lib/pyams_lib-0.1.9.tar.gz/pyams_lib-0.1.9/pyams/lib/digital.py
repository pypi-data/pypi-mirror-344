#-------------------------------------------------------------------------------
# Name:        digital
# Author:      d.fathi
# Created:     03/04/2025
# Copyright:   (c) pyams 2025
# Licence:     free GPLv3
#-------------------------------------------------------------------------------

class dsignal:
    """
    dsignal is a binary signal model that supports logical and arithmetic operations.
    It can handle binary values ('0', '1') as well as undefined values ('X', 'Z').
    Supports logical operations such as AND, OR, XOR, NOT, and arithmetic operations such as addition, subtraction, division, and modulus.
    Designed for use in digital circuits with input/output port support.
    """
    def __init__(self, direction: str = "out", port: str = '0', value: str = '0', name: str = '', bitwidth: int = None):
        if direction not in {'in', 'out'}:
            raise ValueError("Direction must be 'in' or 'out'")

        self.direction = direction
        self.port = port
        self.pindex = 0
        self._name = name or "dsignal"
        self.bitwidth = bitwidth or len(value)
        self._validate(value)
        self._value = self._adjust_to_bitwidth(value)

    def _validate(self, value):
        if not all(bit in {'0', '1', 'X', 'Z'} for bit in value):
            raise ValueError("Value must contain only '0', '1', 'X', or 'Z'")

    def _adjust_to_bitwidth(self, value: str) -> str:
        if len(value) > self.bitwidth:
            return value[-self.bitwidth:]  # اقتطع من اليسار
        else:
            return value.zfill(self.bitwidth)  # أكمل بالأصفار من اليسار

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_value: str):
        self._validate(new_value)
        self._value = self._adjust_to_bitwidth(new_value)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        if not isinstance(new_name, str):
            raise TypeError("Name must be a string")
        self._name = new_name

    def __str__(self):
        return f"{self.name} ({self.direction}): {self.value} on port {self.port}"

    def _bitwise_operation(self, other, op):
        """Perform logical operations with support for X and Z values."""
        if not isinstance(other, dsignal):
            raise TypeError("Operand must be an instance of dsignal")

        min_length = min(len(self.value), len(other.value))
        result = ''
        for i in range(min_length):
            a, b = self.value[i], other.value[i]

            if op == 'AND':
                result += '1' if a == '1' and b == '1' else ('0' if a == '0' or b == '0' else 'X')
            elif op == 'OR':
                result += '1' if a == '1' or b == '1' else ('0' if a == '0' and b == '0' else 'X')
            elif op == 'XOR':
                result += 'X' if 'X' in (a, b) else str(int(a != b))

        return dsignal(self.direction, self.port, result)

    def __and__(self, other): return self._bitwise_operation(other, 'AND')
    def __or__(self, other): return self._bitwise_operation(other, 'OR')
    def __xor__(self, other): return self._bitwise_operation(other, 'XOR')

    def __invert__(self):
        """Perform NOT operation with support for 'X' and 'Z'"""
        result = ''.join('0' if bit == '1' else '1' if bit == '0' else 'X' for bit in self.value)
        return dsignal(self.direction, self.port, result)

    def _to_decimal(self):
        """Convert the binary value to a decimal number."""
        return int(self.value.replace('X', '0').replace('Z', '0'), 2)

    def _from_decimal(self, num, length):
        """Convert a decimal number to a `dsignal` value with the same original length."""
        return bin(num)[2:].zfill(length)

    def __add__(self, other):
        return dsignal(self.direction, self.port, self._from_decimal(self._to_decimal() + other._to_decimal(), len(self.value)))
    def __sub__(self, other):
        return dsignal(self.direction, self.port, self._from_decimal(self._to_decimal() - other._to_decimal(), len(self.value)))
    def __truediv__(self, other):
        return dsignal(self.direction, self.port, self._from_decimal(self._to_decimal() // other._to_decimal(), len(self.value)))
    def __mod__(self, other):
        return dsignal(self.direction, self.port, self._from_decimal(self._to_decimal() % other._to_decimal(), len(self.value)))

    def __iadd__(self, other):
        self.value =  other.value
        return self
    def __isub__(self, other):
        self.value = (self - other).value
        return self
    def __itruediv__(self, other):
        self.value = (self / other).value
        return self
    def __imod__(self, other):
        self.value = (self % other).value
        return self

    def __lshift__(self, bits):
      """Left shift the binary string (logical shift left)"""
      if not isinstance(bits, int):
          raise TypeError("Shift amount must be an integer")

      # Shift left by appending zeros and truncating left bits
      shifted_value = self.value[bits:] + '0' * bits
      return dsignal(self.direction, self.port, shifted_value)

    def __rshift__(self, bits):
      """Right shift the binary string (logical shift right)"""
      if not isinstance(bits, int):
         raise TypeError("Shift amount must be an integer")

      # Shift right by prepending zeros and truncating right bits
      shifted_value = '0' * bits + self.value
      shifted_value = shifted_value[:len(self.value)]
      return dsignal(self.direction, self.port, shifted_value)



class dcircuit:
    """
    Represents an digital circuit with elements and nodes.
    """
    def __init__(self):
        """
        Initialize an empty circuit with a ground node ('0').
        """

        self.elem = {}  # Dictionary to store digital elements by name
        self.cir= []    # list of digital elments in circuit
        self.nodes = ['0']  # List of digital nodes, starting with ground
        self.outputs=[]
        self.tempOutputs=[]
        self.x=[]

    def addDigitalElement(self,elm):
        if hasattr(elm, 'digital') and callable(getattr(elm, 'digital')):
            self.cir+=[elm]
            self.elem[elm.name]=elm

    def classifyInOutSignals(self):
        """
        classify input and output dsignals from the digital circuit.
            - inDSignals: List of input digital signals with details. (pos node , dsignal)
            - outDSignals: List of output digital signals with details. (pos node , dsignal)
            - dsignals:  Collect all signals from circuit elements.
        """
        self.inDSignals=[]
        self.outDSignals=[]
        self.dsignals=[]

        for name, element in self.elem.items():
            self.dsignals+=element.getDSignals()

        for i in range(len(self.dsignals)):
            signal_=self.dsignals[i]

            if signal_.port in self.nodes:
                signal_.pindex = self.nodes.index(signal_.port)
            else:
                self.nodes.append(signal_.port)
                signal_.pindex= self.nodes.index(signal_.port)

            if signal_.direction=='in':
               self.inDSignals+=[[signal_,signal_.pindex]]
            else:
               self.outDSignals+=[[signal_,signal_.pindex]]

        self.x = ['0'] * len(self.nodes)



    def feval(self):
      """
      Evaluate the circuit digital
      """

      for  signal,pos in self.outDSignals:
           self.x[pos] =signal.value

      for  signal,pos in self.inDSignals:
           signal.value = self.x[pos]

      for element in self.cir:
          element.digital()
















if __name__ == '__main__':

  # Example usage
  A0 = dsignal("out", "A", "1")
  A1 = dsignal("out", "A", "01")
  A2 = dsignal("out", "A", "1")
  A3 = dsignal("out", "A", "1")

  D = A0 + (A1 << 1) + (A2 << 2) + (A3 << 3)

  print("D      =", A1 << 1)
  print(type(D))

