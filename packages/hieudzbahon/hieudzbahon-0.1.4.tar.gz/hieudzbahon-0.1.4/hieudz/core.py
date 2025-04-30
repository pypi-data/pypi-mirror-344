import re
import math
from typing import List, Union

def songuyento(n: int, m: int) -> List[int]:
    """Tìm tất cả số nguyên tố từ n đến m."""
    def is_prime(num: int) -> bool:
        if num < 2:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    return [x for x in range(max(2, n), m + 1) if is_prime(x)]

def tachds(n: int, m: List[int]) -> List[int]:
    """Tách các chữ số của n và đưa vào danh sách m."""
    digits = [int(d) for d in str(abs(n))]
    m.extend(digits)
    return m

def uocchung(n: int, m: int) -> List[int]:
    """Tìm các ước chung của n và m."""
    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a
    def get_divisors(num: int) -> List[int]:
        divisors = []
        for i in range(1, int(math.sqrt(abs(num))) + 1):
            if num % i == 0:
                divisors.append(i)
                if i != num // i:
                    divisors.append(num // i)
        return sorted(divisors)
    g = gcd(abs(n), abs(m))
    return get_divisors(g)

def boichung(n: int, m: int) -> List[int]:
    """Tìm các bội chung của n và m."""
    def lcm(a: int, b: int) -> int:
        return abs(a * b) // math.gcd(a, b)
    l = lcm(n, m)
    # Trả về một số bội chung (có thể giới hạn để tránh danh sách quá dài)
    return [l * i for i in range(1, 11)]  # Ví dụ: 10 bội chung đầu tiên

def uoclonnhat(n: int) -> int:
    """Tìm ước lớn nhất của n (không tính chính n)."""
    for i in range(abs(n) - 1, 0, -1):
        if n % i == 0:
            return i
    return 1

def nguyento(n: int) -> bool:
    """Kiểm tra n có phải số nguyên tố không."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def sohoanhao(n: int) -> bool:
    """Kiểm tra n có phải số hoàn hảo không."""
    if n <= 0:
        return False
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n

def phantich(n: int) -> List[int]:
    """Phân tích n ra thừa số nguyên tố."""
    factors = []
    num = abs(n)
    i = 2
    while i * i <= num:
        while num % i == 0:
            factors.append(i)
            num //= i
        i += 1
    if num > 1:
        factors.append(num)
    return factors

def daonguoc(n: int) -> int:
    """Đảo ngược số n."""
    return int(str(abs(n))[::-1]) * (-1 if n < 0 else 1)

def tamgiac(a: float, b: float, c: float) -> bool:
    """Kiểm tra tam giác hợp lệ."""
    if a <= 0 or b <= 0 or c <= 0:
        return False
    return (a + b > c) and (b + c > a) and (a + c > b)

def dinhgiang(vb: str) -> str:
    """Chuẩn hóa chuỗi văn bản."""
    vb = vb.strip()
    vb = re.sub(r'\s+', ' ', vb)
    for d in [',', '.', ';', ':', '?', '!']:
        vb = vb.replace(f' {d}', d)
        vb = re.sub(rf'\{d}(?![\s\)])', f'{d} ', vb)
    vb = re.sub(r'\s*\(\s*', ' (', vb)
    vb = re.sub(r'\s*\)\s*', ') ', vb)
    vb = re.sub(r'\)\s+([.,;:!?])', r')\1', vb)
    vb = re.sub(r'\)\s*$', ')', vb)
    vb = re.sub(r'\s+', ' ', vb).strip()
    return vb