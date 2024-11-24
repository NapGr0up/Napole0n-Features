def Randomize(s):
    return ''.join(random.sample(s, len(s)))

def Encode64(s):
    return ''.join([base64.b64encode(c.encode()).decode() if (i + 1) % 3 == 0 else c for i, c in enumerate(s)]).split("==")[0]

def RandomizeSymb(s):
    symbols = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"
    s = list(s)
    for _ in range(random.randint(2, 4)):
        s.insert(random.randint(0, len(s)), random.choice(symbols))
    return ''.join(s)

def ApplyTransformations(s):
    transformations = [Randomize, Encode64, RandomizeSymb]
    random.shuffle(transformations)
    for transformation in transformations:
        s = transformation(s)
    return s

def KeyDerivation(password, length=16):
    result = password
    result = ApplyTransformations(result)

    original_part = ''.join([random.choice([c.upper(), c.lower(), c]) for c in password])
    result = result + original_part[:int(length / 3)]

    if len(result) < length:
        result += ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()", k=length - len(result)))

    return result[:length]

print(f"\n   {Green}>{Yellow}> {Reset}Password as been generated: {Blue}{KeyDerivation(prompt, length)}{Reset}\n")
