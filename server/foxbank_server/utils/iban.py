from .string import str_range_replace


def c_to_iban_i(c: str) -> int:
    a = ord(c)
    if a in range(48, 58):
        return a - 48
    elif a in range(65, 91):
        return a - 65 + 10
    elif a in range(97, 123):
        return a - 97 + 10
    else:
        raise ValueError(f'Invalid IBAN character: {c} (ord: {a})')


def iban_to_int(iban: str) -> int:
    iban = iban[4:] + iban[0:4]
    return int(''.join(map(str, map(c_to_iban_i, iban))))


def check_iban(iban: str) -> bool:
    num = iban_to_int(iban)
    return num % 97 == 1


def gen_check_digits(iban: str) -> str:
    iban = str_range_replace(iban, '00', 2, 4)
    num = iban_to_int(iban)
    check = 98 - (num % 97)
    iban = str_range_replace(iban, str(check).rjust(2, '0'), 2, 4)
    return iban
