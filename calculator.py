import math

#TODO: divide by zero error

class Solution:
  def reduction(self, finalVal):
    p = finalVal.split("/")
    num = int(p[0])
    den = int(p[1])

    if num > den:
      remainder = num % den      
      wholeVal = int((num-remainder)/den)
      if remainder == 0:
        return str(wholeVal)
      return str(wholeVal)+"_"+str(remainder)+"/"+p[1]
    elif den == 1:
      return p[0]
    else:
      return finalVal

  def gcd(self, a, b):
    if (a == 0):
      return b
    return self.gcd(b % a, a)

  def lowest(self, den3: str, num3: str) -> str:
    common_factor = self.gcd(num3, den3)

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
      negBool = True 
      fNumber = fNumber[1:]

    parseFrac = fNumber.strip().split("_")
    if len(parseFrac) == 2:
      whole = int(parseFrac[0])
      frac = parseFrac[1]
    else:
      whole = 0
      frac = parseFrac[0]

    fracParse = frac.split("/")
    if len(fracParse) == 1:
      improperReturn = fracParse[0] + "/1"
    else:
      improperReturn = str(whole * int(fracParse[1]) + int(fracParse[0])) + "/" + fracParse[1]
    
    if negBool:
      return "-"+improperReturn
    else:
      return improperReturn

  # Function to add two fractions
  def addFraction(self, frac1, frac2):
    if frac1 == "0":
      return frac2
    
    if frac2 == "0":
      return frac1

    firstHalf = frac1.split("/")
    secondHalf = frac2.split("/")

    num1 = int(firstHalf[0].strip())
    den1 = int(firstHalf[1].strip())
    num2 = int(secondHalf[0].strip())
    den2 = int(secondHalf[1].strip())

    den3 = self.gcd(den1, den2)
    den3 = (den1 * den2) / den3

    num3 = ((num1) * (den3 / den1) + (num2) * (den3 / den2))

    return self.lowest(den3, num3)
  
  def multiplyFraction(self, frac1, frac2):
    if frac1 == "0" or frac2 == "0":
      return "0"
    
    firstHalf = frac1.split("/")
    secondHalf = frac2.split("/")

    num1 = int(firstHalf[0].strip())
    den1 = int(firstHalf[1].strip())
    num2 = int(secondHalf[0].strip())
    den2 = int(secondHalf[1].strip())

    num3 = num1 * num2
    den3 = den1 * den2

    return self.lowest(den3, num3)

  def parseExpression(self, expression):
    pass
  
  def calculate(self, s: str) -> int:   
    inner, outer, result, opt = "", "0", "0", '+'
    s+='+'
    for c in range(len(s)):
      if s[c] == ' ': continue
      if s[c].isdigit() or s[c] == "_":
        inner+=s[c]
        continue
      if s[c] == '/' and s[c-1].isdigit():
        inner+=s[c]
        continue
      if opt == '+':
        result = self.addFraction(self.convert_to_improper(result), self.convert_to_improper(outer))
        outer = inner
      elif opt == '-':
        result = self.addFraction(self.convert_to_improper(result), self.convert_to_improper(outer))
        # result += outer
        outer = "-"+inner
      elif opt == '*':
        outer = self.multiplyFraction(self.convert_to_improper(outer), self.convert_to_improper(inner))
        # print(outer)
      elif opt == '/':
        outer = int(outer / inner)
      inner, opt = "", s[c]
    return self.reduction(self.addFraction(self.convert_to_improper(result), self.convert_to_improper(outer)))



tests = { 
  "1+2+3":"6", 
  "1/2+1/2":"1",
  "2_3/8 + 9/8":"3_1/2",
}

if __name__ == "__main__":
  calculator = Solution()
  # for k,v in tests.items():
  #   assert calculator.calculate(k) == v, k+" test failed"
  while True:
    val  = input("?")
    print(calculator.calculate(val))


