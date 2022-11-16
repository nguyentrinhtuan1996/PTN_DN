#!/usr/bin/env python3

"""
this engine is to convert data types
"""
class Convent_Engine_Class:
    def __init__(self) -> None:
        pass

    # Function for converting decimal to binary
    def float_bin(self,my_number, places = 3):
        my_whole = ""
        my_dec = ""
        my_number_str = "%.20f"% my_number

        old_length = len(my_number_str)
        for count in range(0, old_length):
            if(my_number_str[old_length - count -1] == '0'):
                my_number_str = my_number_str[:old_length - count -1]
            else: 
                break
        my_whole, my_dec= my_number_str.split(".")

        my_whole = int(my_whole)
        res = (str(bin(my_whole))+".").replace('0b','')

        for x in range(places):
            my_dec = str('0.')+str(my_dec)
            temp = '%1.20f' %(float(my_dec)*2)
            my_whole, my_dec = temp.split(".")
            res += my_whole
        return res

    def convert_to_fp32(self,float_number):
        """
        convert the float to 2 byte of 32bit within IEE 754 standard
        - float_number : number to 
        - return a dictionary within 2 bytes ["First Byte":<first byte>, "Second Byte"=<second byte>]
        """
        
       
        # identifying whether the number
        # is positive or negative
        sign = 0
        if float_number < 0 :
            sign = 1
            float_number = float_number * (-1)
        p = 30
        # convert float to binary
        dec = self.float_bin(float_number, places = p)

        dotPlace = dec.find('.')
        onePlace = dec.find('1')
        # finding the mantissa
        if onePlace > dotPlace:
            dec = dec.replace(".","")
            onePlace -= 1
            dotPlace -= 1
        elif onePlace < dotPlace:
            dec = dec.replace(".","")
            dotPlace -= 1
        mantissa = dec[onePlace+1:]

        # calculating the exponent(E)
        exponent = dotPlace - onePlace
        exponent_bits = exponent + 127

        # converting the exponent from
        # decimal to binary
        exponent_bits = bin(exponent_bits).replace("0b",'')

        mantissa = mantissa[0:23]

        # the IEEE754 notation in binary	
        result_str = str(sign) + exponent_bits.zfill(8) + mantissa

        # convert the binary to hexadecimal


        # print(result_str)
        # separate 2 bytes from result string
        first_byte_str  = result_str[:16]
        second_byte_str = result_str[16:33]

        result_dictionary = {}
        #  convert string to int 
        try:
            result_dictionary["First Byte"] = int(first_byte_str,2)
        except:
            result_dictionary["First Byte"] = 0
        try:
            result_dictionary["Second Byte"] = int(second_byte_str,2)
        except:
            result_dictionary["Second Byte"] = 0

        if( float_number == 0 or
            float_number == ""):
            result_dictionary["First Byte"] = 0
            result_dictionary["Second Byte"] = 0

        return  result_dictionary
    
    def convertToInt(self,mantissa_str):
        """
        Function to convert Binary
        of Mantissa to float value.
        """
 
        # variable to make a count
        # of negative power of 2.
        power_count = -1
    
        # variable to store
        # float value of mantissa.
        mantissa_int = 0
    
        # Iterations through binary
        # Number. Standard form of
        # Mantissa is 1.M so we have
        # 0.M therefore we are taking
        # negative powers on 2 for
        # conversion.
        for i in mantissa_str:
    
            # Adding converted value of
            # Binary bits in every
            # iteration to float mantissa.
            mantissa_int += (int(i) * pow(2, power_count))
    
            # count will decrease by 1
            # as we move toward right.
            power_count -= 1
            
        # returning mantissa in 1.M form.
        return (mantissa_int + 1)

    def convert_to_real(self,high_int16, low_int16):
        if( high_int16 == 0 and
            low_int16 == 0):
            return 0
        high_int16_str = str(bin(high_int16)[2:].zfill(16))
        low_int16_str = str(bin(low_int16)[2:].zfill(16))
        # print(high_int16_str)
        # print(low_int16_str)

        ieee_32 =   high_int16_str[0] \
                    + "|" \
                    + high_int16_str[1:9] \
                    + "|" \
                    + high_int16_str[9:16] \
                    + low_int16_str 
        # print(ieee_32)       
         # First bit will be sign bit.
        sign_bit = int(ieee_32[0])

        # Next 8 bits will be
        # Exponent Bits in Biased
        # form.
        exponent_bias = int(ieee_32[2 : 10], 2)

        # In 32 Bit format bias
        # value is 127 so to have
        # unbiased exponent
        # subtract 127.
        exponent_unbias = exponent_bias - 127

        # Next 23 Bits will be
        # Mantissa (1.M format)
        mantissa_str = ieee_32[11 : ]

        # Function call to convert
        # 23 binary bits into
        # 1.M real no. form
        mantissa_int = self.convertToInt(mantissa_str)

        # The final real no. obtained
        # by sign bit, mantissa and
        # Exponent.
        real_no = pow(-1, sign_bit) * mantissa_int * pow(2, exponent_unbias)

        # Printing the obtained
        # Real value of floating
        # Point Representation.
        # print("The float value of the given IEEE-754 representation is :",real_no)

        return real_no

if __name__ == '__main__':
    convert_engine = Convent_Engine_Class()
    print(hex(convert_engine.convert_to_fp32(1)["First Byte"]))
    print(hex(convert_engine.convert_to_fp32(1)["Second Byte"]))
    
    # my_number_str = "%.20f"% -0.00000002
    # print(my_number_str)

    # old_length = len(my_number_str)
    # for count in range(0, old_length):
    #     if(my_number_str[old_length - count -1] == '0'):
    #         my_number_str = my_number_str[:old_length - count -1]
    #     else: 
    #         break
    # my_whole, my_dec= my_number_str.split(".")
    # print(my_whole)
    # print(my_dec)

    
    # print(my_dec)
    # convert_engine.convert_to_real(0,0)
    print(convert_engine.convert_to_real(0,0))

