import math
import sys

class Solution:
  # function to reduce fraction into proper formatted form for end output 
  def reduction(self, finalVal: str) -> str:
    #0 is already final reduced form
    if finalVal == "0":
      return "= 0"
    
    elif finalVal == "0/0":
      return "= undefined"

    negBoolReduc = False
    p = finalVal.split("/")
    
    #check if fraction is negative and parse numerator and denominator 
    num = int(p[0])
    if num < 0:
      negBoolReduc = True
      num = abs(num)
    den = int(p[1])

    #fraction is in improper form
    if num > den:
      #calculate whole value and remainder 
      remainder = num % den      
      wholeVal = int((num-remainder)/den)

      #account for a negative fraction
      if negBoolReduc:
        wholeVal*=-1

      #if reduction contains no fractional part 
      if remainder == 0:
        return "= "+str(wholeVal)

      return "= "+str(wholeVal)+"_"+str(remainder)+"/"+p[1]

    #return just numerator since denominator is 1
    elif den == 1:
      return "= "+p[0]
    
    else:
      #fraction is already in most reduced form
      return "= "+finalVal


  # function to find the gcd of two integers 
  def gcd(self, a: int, b: int) -> int:
    if (a == 0):
      return b
    return self.gcd(b % a, a)


  # function to reduce fractions to lowest form but keeps fraction as improper
  def lowest(self, den3: str, num3: str) -> str:
    common_factor = abs(self.gcd(num3, den3))
    
    #divide numerator and denominator by their gcd
    den3 = int(den3 / common_factor)
    num3 = int(num3 / common_factor)

    if num3 == den3:
      return "1/1"
    else:
      return str(num3)+"/"+str(den3)
  

  # function to convert fraction to improper form
  def convert_to_improper(self, fNumber: str) -> str:
    if fNumber == "0":
      return "0"

    negBool = False
    if fNumber[0] == "-":
      #double negative so convert to positive 
      if fNumber[1] == "-":
        negBool = False 
        fNumber = fNumber[2:]
      else:
        #number is negative so slice from index 1 -> end to get rid of '-' sign 
        negBool = True 
        fNumber = fNumber[1:]

    parseFrac = fNumber.strip().split("_")

    #fraction has a whole and fractional component 
    if len(parseFrac) == 2:
      whole = int(parseFrac[0])
      frac = parseFrac[1]
    else:
      #only fractional component exists
      whole = 0
      frac = parseFrac[0]

    # parse num and denom
    fracParse = frac.split("/")
    if len(fracParse) == 1:
      #no denominator so denominator becomes 1 to keep format for future operations
      improperReturn = fracParse[0] + "/1"
    else:
      #recombine fraction into its improper form 
      improperReturn = str(whole * int(fracParse[1]) + int(fracParse[0])) + "/" + fracParse[1]
    
    #number is negative 
    if negBool:
      return "-"+improperReturn
    else:
      return improperReturn


  # function to add two fractions
  def addFraction(self, frac1: str, frac2: str) -> str:

    #short circuit since adding 0 to anything results in the original number 
    if frac1 == "0":
      return frac2
    
    if frac2 == "0":
      return frac1

    #parse the two fractions numerators and denominators 
    firstHalf = frac1.split("/")
    secondHalf = frac2.split("/")

    num1 = int(firstHalf[0].strip())
    den1 = int(firstHalf[1].strip())
    num2 = int(secondHalf[0].strip())
    den2 = int(secondHalf[1].strip())

    #find the gcd and use it to find the new numerator and denominator 
    den3 = self.gcd(den1, den2)
    den3 = (den1 * den2) / den3
    num3 = ((num1) * (den3 / den1) + (num2) * (den3 / den2))

    #return the lowest reduced but still improper form 
    return self.lowest(den3, num3)

  # function to multiply two fractions
  def multiplyFraction(self, frac1: str, frac2: str) -> str:
    if frac1 == "0" or frac2 == "0":
      return "0"
    
    firstHalf = frac1.split("/")
    secondHalf = frac2.split("/")

    num1 = int(firstHalf[0].strip())
    den1 = int(firstHalf[1].strip())
    num2 = int(secondHalf[0].strip())
    den2 = int(secondHalf[1].strip())

    #multiply num and den
    num3 = num1 * num2
    den3 = den1 * den2

    return self.lowest(den3, num3)

  # function to divide two fractions
  def divideFraction(self, frac1: str, frac2: str) -> str:
    if frac1 == "0":
      if frac2 == "0":
        print("undefined")
      return "0"
    
    if frac2 == "0":
      print("Error: divide by zero")
      return "0"
    
    firstHalf = frac1.split("/")
    secondHalf = frac2.split("/")

    num1 = int(firstHalf[0].strip())
    den1 = int(firstHalf[1].strip())
    num2 = int(secondHalf[0].strip())
    den2 = int(secondHalf[1].strip())

    #flip num2 and den2 and multiply 
    num3 = num1 * den2
    den3 = den1 * num2 

    return self.lowest(den3, num3)

  # function that parses expression given and returns the result  
  def calculate(self, s: str) -> int:   
    inner, outer, result, opt = "", "0", "0", '+'
    s+='+'
    for c in range(len(s)):
      if s[c] == ' ': continue
      #part of operand
      if s[c].isdigit() or s[c] == "_":
        inner+=s[c]
        continue
      #/ sign is part of fractional value and not classified as an operator
      if s[c] == '/' and s[c-1].isdigit():
        inner+=s[c]
        continue
      #- sign is part of operand value and not classified as an operator
      if s[c] == '-' and s[c+1].isdigit():
        inner+=s[c]
        continue
      #cases for operators below
      if opt == '+':
        result = self.addFraction(self.convert_to_improper(result), self.convert_to_improper(outer))
        outer = inner
      elif opt == '-':
        result = self.addFraction(self.convert_to_improper(result), self.convert_to_improper(outer))
        outer = "-"+inner
      elif opt == '*':
        outer = self.multiplyFraction(self.convert_to_improper(outer), self.convert_to_improper(inner))
      elif opt == '/':
        outer = self.divideFraction(self.convert_to_improper(outer), self.convert_to_improper(inner))
      inner, opt = "", s[c]
    #return reduced answer in proper form
    return self.reduction(self.addFraction(self.convert_to_improper(result), self.convert_to_improper(outer)))


#note: first two test cases should also output an error
testCases = { 
  "3/4 / 0":"= 0",
  "0 / 0":"= 0",
  "1+2+3+4+5+7":"= 22",
  "2+ -3 + 5 - 2 / 8 * 3/4":"= 3_13/16",
  "1+2+3":"= 6", 
  "6/5 + 2":"= 3_1/5",
  "1/2+1/2":"= 1",
  "2_3/8 + 9/8":"= 3_1/2",
  "-1 - 1":"= -2",
  "1 - 1":"= 0",
  "1 - -1":"= 2",
  "1 + -1":"= 0",
  "-1 + 1":"= 0",
  "-1 + -1":"= -2",
  "-1 - -1":"= 0",
  "-1 - -1 + -1":"= -1",
  "1/2 + -1":"= -1/2",
  "-1 + 1/2":"= -1/2",
  "-1/2 - 1/2":"= -1",
  "-1/2 - -1/2":"= 0",
  "-1_1/2 + -1":"= -2_1/2",
  "1_1/2 + -1":"= 1/2",
  "1_1/2 - -1":"= 2_1/2",
  "1/2 + -1_1/2":"= -1",
  "0 + 0":"= 0",
  "3/4 / 1/2 * 1_1/2":"= 2_1/4",
  "1_3/4 / 1/3 + 4_1/2 - 3/8":"= 9_3/8",
  "3/4 * 4/5 / 3/8 + -4/5 / 1_3/4":"= 1_1/7",
  "0 / 2":"= 0",
  "0 / -2":"= 0",
  "0 * 0":"= 0",
  "0 + 0":"= 0",
  "1/2 * 1/2 / 2 + -1/4":"= -1/8",
  "2/3 / 2/3 / 2/3 * 1/2 * 1/8":"= 3/32",
  "3_1/2 * 2_3/4 / 5/4":"= 7_7/10"
}

if __name__ == "__main__":
  pSize = len(sys.argv)
  calculator = Solution()

  if pSize > 2:
    print("Invalid program parameters")
  #program acts like a calculator which waits for input from operator
  elif pSize == 1:
    while True:
      val = input("?")
      print(calculator.calculate(val))
  #run test cases 
  else:
    for k,v in testCases.items():
      assert calculator.calculate(k) == v, k+" test failed"
    print("All tests passed")




