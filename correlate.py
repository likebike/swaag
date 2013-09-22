#!/usr/bin/env python
# Works in Python2 or Python3

def correlate(vectorA, vectorB, weights):
    #  Example: correlate([1,2,3], [4,5,6], [0.5, 0.5, 1])
    #
    #  Correllation is determined as a dot product normalized to the length of the vectors:
    #
    #  correlation between vectors v1 and v2 are:
    #
    #   v1 * v2
    #  ----------  where (v1 * v2) indicates a dot product between v1 and v2
    #   |v1||v2|
    #
    #  v1 represents the image_COM, which is a 3-vector of the "ideal" values we're matching against.
    #  v2 represents the char_COM, which is a 3-vector for the character component we're checking
    #
    #  "COM" stands for "Center of Mass". All vectors v1 and v2 are in this form:
    #
    #  v = <COM_x, COM_y, Intensity>
    #
    #  For the sake of our formula, we will let:
    #   v1 = <x, y, z> 
    #   v2 = <a, b, c>
    #
    #  And furthermore we have three constant weighting factors: A, B, C
    #
    #
    #  The weighted, normalized dot-product formula becomes:
    #
    #                                       A*x*a + B*y*b + C*z*c
    #  correlation =  -----------------------------------------------------------------
    #                   (A*x^2 + B*y^2 + C*z^2)^(1/2) * (A*a^2 + B*b^2 + C*c^2)^(1/2)
    #
    #  (Thank you, Don Jones!)
    #
    vLen = len(vectorA)
    assert vLen == len(vectorB) == len(weights)
    dotProduct, vA_norm, vB_norm = 0, 0, 0
    for i in range(vLen):
        w, a, b = weights[i], vectorA[i], vectorB[i]
        dotProduct += w*a*b
        vA_norm += w*a*a
        vB_norm += w*b*b
    if dotProduct == 0: return 0
    return float(dotProduct) / float( (vA_norm**0.5) * (vB_norm**0.5) )  # Ensure floating-point division.  # If this produces a division by zero, it means that your inputs are invalid.  DO NOT TRY TO FIX THE DIVISION-BY-ZERO HERE.  Fix/Check your inputs intead.  For example, you could try adding a dummy element to your vectors with a low weight.
    

