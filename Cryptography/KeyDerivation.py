
def executionKeyDer(password):

    # ------------------------------ Get a new password (more safe) ------------------------------

    def Randomize(s):
        return ''.join(random.sample(s, len(s)))

    def Encode64(s):
        return ''.join([base64.b64encode(c.encode()).decode() if (i + 1) % 3 == 0 else c for i, c in enumerate(s)]).split("==")[0]

    def RandomizeSymb(s):
        symbols = "!@#$%&()-_=+[].?/"
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

    def KeyDerivation(password, length):
        result = password
        result = ApplyTransformations(result)

        originalPart = ''.join([random.choice([c.upper(), c.lower(), c]) for c in password])
        result = result + originalPart[:int(length / 3)]

        if len(result) < length:
            result += ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()", k=length - len(result)))

        return result[:length]

    # ------------------------------------------ Password safety test ---------------------------------------------------------

    def PasswordSafety(password):

        pourcentBar = min(len(password) * 4, 50)

        password    = list(password)

        if any(char.isupper() for char in password):
            pourcentBar += 2.5

        if any(char.islower() for char in password):
            pourcentBar += 2.5

        chiffres = sum(1 for char in password if char.isdigit())
        pourcentBar += chiffres * 3

        symboles = sum(1 for char in password if char in ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", ".", ",", "?", "/"])
        pourcentBar += symboles * 5


        pourcentBar = min(pourcentBar, 100)

        return round(pourcentBar, 2)

    # ---------------------------- Key Derivation (PBKDF2) ------------------------------
    def derKey(password, salt=None, iterations=100000, key_length=32):
        if salt is None:
            salt = os.urandom(16)

        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            iterations,
            dklen=key_length
        )

        return key, salt

    # ------------------------------ Execution logic ------------------------------

    print(f"\n   {Green}>{Yellow}> {Reset}Testing {Blue}{password}{Reset} security...\n")

    dervedKey, salt = derKey(password)

    if PasswordSafety(password) <= 50:
        print(f"\n   {Reset}Password {Red}{password}{Reset} not safe ({Red}{PasswordSafety(password)}{Reset}%)!")


        print(f"   {Green}>{Yellow}> {Reset}Safe password has been generated: {Blue}{KeyDerivation(password, 20)}{Reset})\n")

    elif PasswordSafety(password) > 50 and PasswordSafety(password) < 75:
        print(f"\n   {Green}>{Yellow}> {Reset}Password {Blue}{password}{Reset} score: {Blue}{PasswordSafety(password)}{Reset}% (positive).\n   (New password if you want to be more safe: {Yellow}{KeyDerivation(password, 24)}{Reset})\n")

    else:
        print(f"   {Green}>{Yellow}> {Reset}Password {Blue}{password}{Reset} score: {Green}{PasswordSafety(password)}{Reset}% (very positive)\n")

    print(f"   {Green}>{Yellow}> {Reset}Derived Key has been generated: {Bold}{Magenta}{dervedKey.hex()}{Reset} (using PBKDF2)\n")


executionKeyDer(password)
