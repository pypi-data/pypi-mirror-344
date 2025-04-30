## pyproject.py
![image](https://github.com/user-attachments/assets/b7af20b5-8504-4b56-85fc-471bf45eca90)
## divide.py
```
#나눗셈
import sys

def divide(a: int, b: int):
    result = a / b
    print(f"{result:.3f}")  # 소수점 3자리까지

def main():
    args = sys.argv[1:]
    a, b = int(args[0]), int(args[1])
    divide(a, b)
```
## divide.py 결과
### pdm run
![image](https://github.com/user-attachments/assets/12405935-bfd8-445d-97e1-70137ad4b404)
### python
![image](https://github.com/user-attachments/assets/92f402ca-542b-45ff-8516-b9e8502af4cd)
