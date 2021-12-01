import math
def estParfait(n) :
     
    # Final result of summation of divisors
    result = 0
     
    # find all divisors which divides 'num'
    i = 2
    while i<= (math.sqrt(n)) :
       
        # if 'i' is divisor of 'num'
        if (n % i == 0) :
       
            # if both divisors are same then
            # add it only once else add both
            if (i == (n / i)) :
                result = result + i;
            else :
                result = result +  (i + n/i);
        i = i + 1
        
    res = result +1
    if int(res) == n:
        return True
    else:
        return False

def parfaits_entre(binf, bsup):
    x = binf
    l = []
    while x>=binf and x<=bsup:
        var = estParfait(x)
        if var  == True:
            l.append(x)
        x = x +1
    print("Nombres parfaits de [",binf,",",bsup,"]")
    final = ' '.join(str(e) for e in l)
    print(final)


binf =2
bsup=100
parfaits_entre(binf, bsup)