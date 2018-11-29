def divisibleNumbers(inputNum):
 def getDigits(num):
   return (""+num).split('').map(n => return parseInt(n));
 
 def getSum(digits):
   return digits.reduce((sum, value) => return sum + value, 0);

 def getProduct(digits):
   return digits.reduce((prod, value) => {
     return prod * value;
   }, 1);

 function hasZero(digits) {
   return digits.reduce((or, value) => {
     return or || !value;
   }, false);
 }
 
 for (let i=1; ; i++) {
   const outputNum = inputNum * i;
   const outputNumDigits = getDigits(outputNum);
   console.log(outputNum, outputNumDigits, !hasZero(outputNumDigits), getProduct(outputNumDigits), getSum(outputNumDigits));

   if (!hasZero(outputNumDigits) && getProduct(outputNumDigits) <= getSum(outputNumDigits)) {
     return outputNum;
   }
 }
}