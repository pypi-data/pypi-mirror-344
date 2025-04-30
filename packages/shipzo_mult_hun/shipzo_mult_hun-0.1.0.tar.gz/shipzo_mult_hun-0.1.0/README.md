## pyproject.py
![image](https://github.com/user-attachments/assets/ea66cb92-66bf-49f9-afe5-535c72004e4b)
## mult.py
```
#곱셈
import sys

def mult(a: int, b: int):
    print(a * b)

def main():
    args = sys.argv[1:]
    a, b = int(args[0]), int(args[1])
    mult(a, b)
```
## mult.py 결과
### pdm run
![image](https://github.com/user-attachments/assets/43798cfe-ab1f-411e-a347-9841c1dd9d8d)
### python
![image](https://github.com/user-attachments/assets/e2474ff5-a7d3-4935-8370-2c6cc4be817e)
