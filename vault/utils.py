import secrets
import string


def generate_password(
    length=16, use_upper=True, use_lower=True, use_digits=True, use_symbols=True
):
    pools = []
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append("!@#$%^&*()-_=+[]{}")

    if not pools:
        raise ValueError("At least one character set must be selected")

    all_chars = "".join(pools)

    # Guarantee at least one character from each selected pool
    password_chars = [secrets.choice(pool) for pool in pools]
    password_chars += [secrets.choice(all_chars) for _ in range(length - len(pools))]
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)
