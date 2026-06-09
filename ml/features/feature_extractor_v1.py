# Bibliotecas necessárias
from urllib.parse import urlparse
import ipaddress

def extract_features(url):

    parsed = urlparse(url)

    hostname = parsed.hostname or ""
    path = parsed.path
    query = parsed.query

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

    except:
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
        main_domain in path
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
    # Double Slash
    # =========================
    # DoubleSlashInPath (indica se há '//' no caminho) - Binária
    features['DoubleSlashInPath'] = int(
        '//' in path
    )
    
    return features
