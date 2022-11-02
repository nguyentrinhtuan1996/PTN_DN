#!/usr/bin/env python3

"""
this engine is to convert data types
"""
class Convent_Engine_Class:
    def __init__(self) -> None:
        pass

    def binaryOfFraction_str(self,fraction_number):
        """
        Function to convert a fraction to binary string
        - fraction_number : fraction to be converted.
        - return binary string for fraction number
        """

        # Declaring an empty string
        # to store binary bits.
        binary = str()

        # Iterating through
        # fraction until it
        # becomes Zero.
        while (fraction_number):
            
            # Multiplying fraction by 2.
            fraction_number *= 2

            # Storing Integer Part of
            # Fraction in int_part.
            if (fraction_number >= 1):
                int_part = 1
                fraction_number -= 1
            else:
                int_part = 0
        
            # Adding int_part to binary
            # after every iteration.
            binary += str(int_part)

        # Returning the binary string.
        return binary

    def float_to_FP32(self,float_number):
        """
        convert the float to 2 byte of 32bit within IEE 754 standard
        - float_number : number to 
        - return a dictionary within 2 bytes ["First Byte":<first byte>, "Second Byte"=<second byte>]
        """
        # this dictionary contains 2 bytes to return
        result_dictionary = {
            "First Byte":0,
            "Second Byte":0,
        }
        # Setting Sign bit
        # default to zero.
        sign_bit = 0

        # Sign bit will set to
        # 1 for negative no.
        if(float_number < 0):
            sign_bit = 1

        # converting given no. to
        # absolute value as we have
        # already set the sign bit.
        float_number = abs(float_number)

        # Converting Integer Part
        # of Real no to Binary
        int_str = bin(int(float_number))[2 : ]

        # Function call to convert
        # Fraction part of real no
        # to Binary.
        fraction_str = self.binaryOfFraction_str(float_number - int(float_number))

        # Getting the index where
        # Bit was high for the first
        # Time in binary repress
        # of Integer part of real no.
        ind = int_str.index('1')

        # The Exponent is the no.
        # By which we have right
        # Shifted the decimal and
        # it is given below.
        # Also converting it to bias
        # exp by adding 127.
        exp_str = bin((len(int_str) - ind - 1) + 127)[2 : ]

        # getting mantissa string
        # By adding int_str and fraction_str.
        # the zeroes in MSB of int_str
        # have no significance so they
        # are ignored by slicing.
        mant_str = int_str[ind + 1 : ] + fraction_str

        # Adding Zeroes in LSB of
        # mantissa string so as to make
        # it's length of 23 bits.
        mant_str = mant_str + ('0' * (23 - len(mant_str)))

        # graft binary paths to binary string
        result_str = str(sign_bit) + exp_str + mant_str[:23]

        # separate 2 bytes from result string
        first_byte_str  = result_str[:16]
        second_byte_str = result_str[17:32]

        #  convert string to int 
        result_dictionary["First Byte"] = int(first_byte_str,2)
        result_dictionary["Second Byte"] = int(second_byte_str,2)

        return  result_dictionary
a = Convent_Engine_Class()
print(a.float_to_FP32(-2.250003))