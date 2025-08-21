# Dicionário de dados  

| Nome da Coluna      | Descrição                                                                 | Tipo de Dado |  
|---------------------|---------------------------------------------------------------------------|--------------|  
| `id_aluno`          | Identificador único do aluno (chave primária, numérica e sequencial)      | int64        |  
| `nota_diagnostico`  | Número de acertos no Simulado Diagnóstico (avaliação inicial)             | int64        |  
| `nota_final`        | Número de acertos no Simulado Final (avaliação após o curso)              | int64        |  

**Observação**: os simulados possuem o mesmo número total de questões, e cada questão vale 1 ponto. Portanto, os valores representam o número de acertos (0 até o total de questões).  
