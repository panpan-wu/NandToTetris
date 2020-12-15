# NandToTetris

- 官网：[https://www.nand2tetris.org](https://www.nand2tetris.org)
- 课程地址：[https://www.coursera.org/learn/build-a-computer/home/welcome](https://www.coursera.org/learn/build-a-computer/home/welcome)

## Boolean functions and gate logic

Any boolean function can be represented using an expression containing NAND operations.

- not(x) = x nand x
- x and y = not(x nand y) = (x nand y) nand (x nand y)
- x or y = not(not(x)) or not(not(y)) = not(not(x) and not(y)) = not(x) nand not(y) = (x nand x) nand (y nand y)

**Commutative laws**

- x and y = y and x
- x or y = y or x

**Associative laws**

- x and (y and z) = (x and y) and z
- x or (y or z) = x or (y or z)

**Distributive laws**

- x and (y or z) = (x and y) or (x and z)
- x or (y and z) = (x or y) and (x or z)

**De Morgan laws**

- not(x and y) = not(x) or not(y)
- not(x or y) = not(x) and not(y)
