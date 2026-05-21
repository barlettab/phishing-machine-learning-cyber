# Dicionário de Dados

| Variável                             | Descrição                                                                       | Tipo               |
| ------------------------------------ | ------------------------------------------------------------------------------- | ------------------ |
| `id`                                 | Identificador único de cada registro/URL no dataset.                            | Identificador      |
| `NumDots`                            | Quantidade de pontos (`.`) presentes na URL.                                    | Numérica discreta  |
| `SubdomainLevel`                     | Quantidade de níveis de subdomínio presentes na URL.                            | Numérica discreta  |
| `PathLevel`                          | Quantidade de níveis no caminho (`path`) da URL.                                | Numérica discreta  |
| `UrlLength`                          | Comprimento total da URL em caracteres.                                         | Numérica contínua  |
| `NumDash`                            | Quantidade de hífens (`-`) presentes na URL.                                    | Numérica discreta  |
| `NumDashInHostname`                  | Quantidade de hífens presentes no hostname/domínio.                             | Numérica discreta  |
| `AtSymbol`                           | Indica presença do símbolo `@` na URL.                                          | Binária            |
| `TildeSymbol`                        | Indica presença do símbolo `~` na URL.                                          | Binária            |
| `NumUnderscore`                      | Quantidade de underscores (`_`) na URL.                                         | Numérica discreta  |
| `NumPercent`                         | Quantidade de símbolos `%` na URL.                                              | Numérica discreta  |
| `NumQueryComponents`                 | Quantidade de componentes/parâmetros na query da URL.                           | Numérica discreta  |
| `NumAmpersand`                       | Quantidade de caracteres `&` na URL.                                            | Numérica discreta  |
| `NumHash`                            | Quantidade de símbolos `#` na URL.                                              | Numérica discreta  |
| `NumNumericChars`                    | Quantidade de caracteres numéricos presentes na URL.                            | Numérica discreta  |
| `NoHttps`                            | Indica ausência do protocolo HTTPS.                                             | Binária            |
| `RandomString`                       | Indica presença de cadeias de caracteres aparentemente aleatórias.              | Binária            |
| `IpAddress`                          | Indica utilização de endereço IP em vez de domínio textual.                     | Binária            |
| `DomainInSubdomains`                 | Indica presença do domínio principal em subdomínios.                            | Binária            |
| `DomainInPaths`                      | Indica presença do domínio dentro do caminho da URL.                            | Binária            |
| `HttpsInHostname`                    | Indica presença da palavra “https” dentro do hostname.                          | Binária            |
| `HostnameLength`                     | Comprimento do hostname/domínio da URL.                                         | Numérica contínua  |
| `PathLength`                         | Comprimento do caminho (`path`) da URL.                                         | Numérica contínua  |
| `QueryLength`                        | Comprimento da query string da URL.                                             | Numérica contínua  |
| `DoubleSlashInPath`                  | Indica presença de `//` no caminho da URL.                                      | Binária            |
| `NumSensitiveWords`                  | Quantidade de palavras sensíveis relacionadas a phishing presentes na URL.      | Numérica discreta  |
| `EmbeddedBrandName`                  | Indica presença de nomes de marcas embutidos na URL.                            | Binária            |
| `PctExtHyperlinks`                   | Percentual de hyperlinks externos presentes na página.                          | Numérica contínua  |
| `PctExtResourceUrls`                 | Percentual de recursos externos carregados pela página.                         | Numérica contínua  |
| `ExtFavicon`                         | Indica utilização de favicon externo.                                           | Binária            |
| `InsecureForms`                      | Indica presença de formulários inseguros.                                       | Binária            |
| `RelativeFormAction`                 | Indica utilização de ações de formulário relativas.                             | Binária            |
| `ExtFormAction`                      | Indica formulários enviando dados para domínios externos.                       | Binária            |
| `AbnormalFormAction`                 | Indica comportamento anormal em ações de formulário.                            | Binária            |
| `PctNullSelfRedirectHyperlinks`      | Percentual de hyperlinks nulos ou autorredirecionáveis.                         | Numérica contínua  |
| `FrequentDomainNameMismatch`         | Indica inconsistência frequente entre domínios referenciados.                   | Binária            |
| `FakeLinkInStatusBar`                | Indica presença de links falsos na barra de status.                             | Binária            |
| `RightClickDisabled`                 | Indica desativação do clique direito na página.                                 | Binária            |
| `PopUpWindow`                        | Indica utilização de janelas pop-up.                                            | Binária            |
| `SubmitInfoToEmail`                  | Indica envio de informações diretamente para e-mail.                            | Binária            |
| `IframeOrFrame`                      | Indica utilização de `iframe` ou `frame` na página.                             | Binária            |
| `MissingTitle`                       | Indica ausência de título na página web.                                        | Binária            |
| `ImagesOnlyInForm`                   | Indica formulários contendo apenas imagens.                                     | Binária            |
| `SubdomainLevelRT`                   | Versão categorizada/heurística da quantidade de subdomínios.                    | Categórica ordinal |
| `UrlLengthRT`                        | Versão categorizada/heurística do comprimento da URL.                           | Categórica ordinal |
| `PctExtResourceUrlsRT`               | Versão categorizada/heurística do percentual de recursos externos.              | Categórica ordinal |
| `AbnormalExtFormActionR`             | Versão categorizada/heurística de ações externas anormais em formulários.       | Categórica ordinal |
| `ExtMetaScriptLinkRT`                | Avaliação heurística de links externos em metadados/scripts.                    | Categórica ordinal |
| `PctExtNullSelfRedirectHyperlinksRT` | Versão categorizada/heurística de hyperlinks nulos ou autorredirecionáveis.     | Categórica ordinal |
| `CLASS_LABEL`                        | Variável alvo do modelo: `0` representa URL legítima e `1` representa phishing. | Binária            |
