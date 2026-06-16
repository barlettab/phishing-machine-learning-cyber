# Bibliotecas necessárias
from urllib.parse import urlparse
import ipaddress
from collections import Counter
from math import log2

def entropy(text):

    if not text:
        return 0

    counts = Counter(text)

    probs = [
        count / len(text)
        for count in counts.values()
    ]

    return -sum(
        p * log2(p)
        for p in probs
    )

def has_random_token(hostname):

    parts = hostname.split(".")

    for part in parts:

        if len(part) >= 8:

            vowels = sum(
                c in "aeiou"
                for c in part.lower()
            )

            ratio = vowels / len(part)

            if ratio < 0.2:
                return 1

    return 0

def extract_features(url):

    parsed = urlparse(url)

    hostname = parsed.hostname or ""
    path = parsed.path
    query = parsed.query

    # =========================
    # Phishing Keywords
    # =========================

    url_lower = url.lower()

    PHISHING_WORDS = [
        "login",
        "verify",
        "secure",
        "account",
        "update",
        "confirm",
        "signin",
        "bank",
        "payment",
        "wallet",
        "password",
        "security",
        "support"
    ]

    features = {}

    # =========================
    # Estrutura da URL
    # =========================

    # NumDots (qnt de pontos na URL) - discreta
    features['NumDots'] = url.count('.')

    # SubdomainLevel (nível de subdomínio, ou seja, número de subdomínios) - Numérica discreta
    features['SubdomainLevel'] = (
        hostname.count('.') - 1
        if hostname.count('.') > 1
        else 0
    )

    # PathLevel (nível do caminho) - Numérica discreta
    features['PathLevel'] = (
        path.count('/')
    )

    # UrlLength (comprimento da URL) - Numérica Discreta
    features['UrlLength'] = len(url)

    # NumDash (número de hífens na URL) - Numérica discreta
    features['NumDash'] = url.count('-') 

    # NumDashInHostname (número de hífens no hostname) - Numérica discreta
    features['NumDashInHostname'] = hostname.count('-')

    # AtSymbol (número de '@' na URL) - Binária 
    features['AtSymbol'] = int('@' in url)

    # TildeSymbol (número de '~' na URL) - Binária 
    features['TildeSymbol'] = int('~' in url)

    # NumUnderscore (número de '_' na URL) - Numérica discreta
    features['NumUnderscore'] = url.count('_')

    # NumPercent (número de '%' na URL) - Numérica discreta
    features['NumPercent'] = url.count('%')

    # NumQueryComponents (número de componentes na query string) - Numérica discreta
    features['NumQueryComponents'] = (
        len(query.split('&'))
        if query
        else 0
    )

    # NumAmpersand (número de '&' na URL) - Numérica discreta
    features['NumAmpersand'] = url.count('&')

    # NumHash (número de '#' na URL) - Numérica discreta
    features['NumHash'] = url.count('#')

    # NumNumericChars (número de caracteres numéricos na URL) - Numérica discreta
    features['NumNumericChars'] = sum(
        c.isdigit()
        for c in url
    )

    features['PctNumericChars'] = (
    features['NumNumericChars'] / len(url)
    if len(url) > 0
    else 0
    )

    # =========================
    # HTTPS
    # =========================

    # NoHttps (indica se a URL não usa HTTPS) - Binária
    features['NoHttps'] = int(
        parsed.scheme != 'https'
    )

    # =========================
    # IP Address
    # =========================

    # IpAddress (indica se o hostname é um endereço IP)
    try:
        ipaddress.ip_address(hostname)
        features['IpAddress'] = 1

    except ValueError:
        features['IpAddress'] = 0

    # =========================
    # Domínio em locais suspeitos
    # =========================

    domain_parts = hostname.split('.')

    main_domain = (
        domain_parts[-2]
        if len(domain_parts) >= 2
        else hostname
    )

    subdomains = domain_parts[:-2]

    features['DomainInSubdomains'] = int(
        main_domain in ''.join(subdomains)
    )

    features['DomainInPaths'] = int(
        main_domain.lower() in path.lower()
    )

    # =========================
    # Comprimentos
    # =========================

    # HostnameLength (comprimento do hostname) - Numérica discreta
    features['HostnameLength'] = len(hostname) 

    # PathLength (comprimento do caminho) - Numérica discreta
    features['PathLength'] = len(path)

    # QueryLength (comprimento da query string) - Numérica discreta
    features['QueryLength'] = len(query)


    # =========================
    # Hostname suspeito
    # =========================

    features['HttpsInHostname'] = int(
        'https' in hostname.lower()
    )

    features['HostnameHasDigit'] = int(
        any(
            c.isdigit()
            for c in hostname
        )
    )

    features['HostnameDigitCount'] = sum(
        c.isdigit()
        for c in hostname
    )

    features['NumSensitiveWords'] = sum(
        word in url_lower
        for word in PHISHING_WORDS
    )

    # =========================
    # Double Slash
    # =========================
    # DoubleSlashInPath (indica se há '//' no caminho) - Binária
    features['DoubleSlashInPath'] = int(
        '//' in path
    )

    for word in PHISHING_WORDS:
        features[f"Has_{word}"] = int(
            word in url_lower
        )

    SUSPICIOUS_TLDS = {
        "tk",
        "ml",
        "cf",
        "ga",
        "gq",
        "xyz",
        "top",
        "click",
        "work",
        "sbs",
        "cfd",
        "buzz",
        "monster",
        "cam",
        "rest",
        "fit",
        "country"
    }

    tld = (
        hostname.split(".")[-1]
        if "." in hostname
        else ""
    )

    features["SuspiciousTLD"] = int(
        tld in SUSPICIOUS_TLDS
    )

    features["ManySubdomains"] = int(
    features["SubdomainLevel"] >= 2
    )   

    main_domain = (
        domain_parts[-2]
        if len(domain_parts) >= 2
        else hostname
    )

    KNOWN_BRANDS = [

        # Big Tech
        "google",
        "gmail",
        "youtube",
        "microsoft",
        "office",
        "outlook",
        "onedrive",
        "apple",
        "icloud",

        # Social
        "facebook",
        "instagram",
        "whatsapp",
        "telegram",
        "linkedin",
        "twitter",
        "x",

        # Streaming
        "netflix",
        "spotify",
        "disney",
        "disneyplus",
        "primevideo",

        # E-commerce
        "amazon",
        "aliexpress",
        "mercadolivre",
        "mercadolibre",
        "ebay",
        "allegro",
        "allegrolokalnie",
        "shopee",
        "magalu",

        # Financeiro
        "paypal",
        "wise",
        "nubank",
        "itau",
        "bradesco",
        "santander",
        "caixa",
        "bb",
        "bancodobrasil",
        "inter",
        "c6bank",
        "picpay",
        "mercadopago",

        # Crypto
        "binance",
        "coinbase",
        "metamask",
        "ledger",
        "trezor",
        "trustwallet",
        "blockchain",

        # Cloud / Dev
        "github",
        "gitlab",
        "docker",
        "aws",
        "azure",
        "gcp",
        "cloudflare",

        # Governo BR
        "gov",
        "govbr",
        "receita",
        "receitafederal",
        "senado",
        "inss",

        # Universidades BR
        "usp",
        "unicamp",
        "ufmg",
        "ufrj",
        "ufpr",
        "ufsc",
        "ufpe",

        # Correios / logística
        "correios",
        "fedex",
        "dhl",
        "ups",

    ]

    features["KnownBrandInURL"] = int(
        any(
            brand in url_lower
            for brand in KNOWN_BRANDS
        )
        and
        not any(
            brand == main_domain.lower()
            for brand in KNOWN_BRANDS
        )
    )

    # =========================
    # Brand Features
    # =========================

    features["BrandInSubdomain"] = int(
        any(
            brand in ".".join(subdomains).lower()
            for brand in KNOWN_BRANDS
        )
    )

    features["BrandInPath"] = int(
        any(
            brand in path.lower()
            for brand in KNOWN_BRANDS
        )
    )

    features["BrandMismatch"] = int(
        any(
            brand in url_lower
            for brand in KNOWN_BRANDS
        )
        and
        main_domain.lower() not in KNOWN_BRANDS
    )

    features["SpecialCharRatio"] = (
        (
            url.count("-")
            + url.count("_")
            + url.count("%")
            + url.count("@")
        )
        / len(url)
        if len(url) > 0
        else 0
    )

    features["SpecialCharRatio"] = (
        (
            url.count("-")
            + url.count("_")
            + url.count("%")
            + url.count("@")
        )
        / len(url)
        if len(url) > 0
        else 0
    )

    features["LongURL"] = int(
        len(url) > 75
    )

    features["VeryLongURL"] = int(
    len(url) > 120
    )

    features["UrlEntropy"] = entropy(url)


    FREE_HOSTING = [
        "netlify.app",
        "vercel.app",
        "wixsite.com",
        "wixstudio.com",
        "github.io",
        "pages.dev",
        "web.app",
        "firebaseapp.com"
    ]

    features["FreeHosting"] = int(
        any(
            host in hostname.lower()
            for host in FREE_HOSTING
        )
    )
    
    features["RandomLookingHostname"] = (
        has_random_token(hostname)
    )

    return features



