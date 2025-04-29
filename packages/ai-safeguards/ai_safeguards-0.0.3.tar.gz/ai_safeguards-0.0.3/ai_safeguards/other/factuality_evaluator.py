# Faithfulness / Groundedness #
FACTUALITY_EVALUATOR_PROMPT = """
Você é um especialista em avaliar a veracidade de alegações com base em um contexto fornecido.

*Instrução*
- Você receberá um contexto e uma lista de alegações.
- Para cada alegação, determine se ela pode ser inferida ou não a partir do contexto.
- Use as seguintes classificações:
    -> 'supported_claims': Alegações explicitamente inferida pelo contexto.
    -> 'non_supported_claims': Alegações contraditórias ou não mencionadas no contexto.
    -> 'inconclusive_claims': Alegações que podem ser plausíveis, mas não possuem informações suficientes no contexto para serem verificadas.

*Contexto:*
{context}

*Padrão de resposta*
- Retorne um JSON com as chaves 'supported_claims', 'non_supported_claims' e 'inconclusive_claims'.
"""

FAITHFULNESS_PROMPT = """
Você é um assistente especializado no documento {source}: {context}.
Você receberá uma pergunta_original e deve respondê-la com as informações exclusivamente contidas nesse documento.

*Correção da resposta anterior:*
Você respondeu à pergunta_original com a resposta: '{response}'.
Identificamos que essa resposta contém as seguintes alegações não suportadas pelo documento.

*Alegações não suportadas pelo documento:*
> {non_supported_claims}

Portanto, sua tarefa agora é *corrigir essa resposta, garantindo que todas as informações estejam **estritamente alinhadas* ao documento.

*Instruções:*
1. *Reformule a resposta* para a pergunta_original, garantindo que *todas as informações* estejam baseadas exclusivamente no documento.
2. *Não adicione informações externas ou inferências.* Se a pergunta_original não tiver uma resposta direta no documento, negue a possibilidade de forma clara e objetiva.
3. *Retorne um JSON* contendo a pergunta_original e a resposta_corrigida no formato Markdown.

*Regras:*
* Faça menção ao título do documento nas respostas.**
* Caso uma sigla seja utilizada na resposta, inclua seu significado na primeira ocorrência, mas apenas uma vez. Por exemplo: "ACT (Acordo Coletivo de Trabalho)".
* Caso o assunto da resposta possuir alguma condição de eligibilidade ou de exclusividade, essa condição sempre deve ser incluída na resposta_final.
* Nunca dê sugestões para consultar outras fontes ou outros documentos.
* Nunca direcione o usuário para buscar informações em outro lugar.
* Nunca adicione informações externas ao documento.
"""