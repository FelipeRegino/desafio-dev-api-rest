# Como rodar

Para rodar o projeto é necessario ter o Docker e o docker-compose instalados na maquina

iniciar o projeto:
``` docker compose up ```

para ter acesso aos endpoints no seu navegador acesse:
``` http://localhost:8000/docs ```

rodar testes unitarios:
``` pytest ```

# Interagindo

Para o **Portador** é possivel criar, buscar e desativar.
- Para criar basta passar um CPF valido e um nome. Exemplo:

```aiignore
{
  "cpf": "392.572.850-30", # Pode ser enviado sem formatação tambem
  "name": "Felipe Regino"
}
```

- Para buscar basta passar o CPF do portador.

- Para desativar tambem basta passar o CPF do portador.

Para a **conta digital Dock** é possivel buscar todas de um portador, por id, criar, fechar bloquear e desbloquear
- Para buscar todas basta passar o CPF do portador.
- Para buscar por id basta passar o CPF do portador e o id da conta.
- Para criar basta passar o CPF do portador.
- Para fechar, bloquear e desbloquear basta passar o CPF do portador e o id da conta.

Para as **Transações** é posivel consultar o extrato, saque e depósito
- Para consultar o extrato basta passar o id da conta e caso queira filtrar por período, filtros de data. Exemplo:
```aiignore
dock_account_id="[id da conta]"
start_date=2024-01-01 # opcional
end_date=2024-01-30 # opcional
```

- Para o saque e o depósito é necessario passar o id da conta, o tipo de transação e o valor. Exemplo:
```aiignore
{
  "dock_account": "[id da conta]",
  "type": "DEPOSIT", # [DEPOSIT=depósito, WITHDRAWAL=saque]
  "amount": 100,
}
```

# Cenário

A Dock está crescendo e expandindo seus negócios, gerando novas oportunidades de revolucionar o mercado financeiro e criar produtos diferenciados.
Nossa próxima missão é construir uma nova conta digital Dock para nossos clientes utilizarem através de endpoints, onde receberemos requisições em um novo backend que deverá gerenciar as contas e seus portadores (os donos das contas digitais).

# Requisitos

- Deve ser possível criar e remover **portadores**
    - Um **portador** deve conter apenas seu *nome completo* e *CPF*
    - O *CPF* deve ser válido e único no cadastro de **portadores**
- As **contas digital Dock** devem conter as seguintes funcionalidades:
    - A conta deve ser criada utilizando o *CPF* do **portador**
    - Uma conta deve ter seu *saldo*, *número* e *agência* disponíveis para consulta
    - Necessário ter funcionalidade para fazer a *consulta de extrato* da conta *por período*
    - Um **portador** pode fechar a **conta digital Dock** a qualquer instante
    - Executar as operações de *saque* e *depósito*
        - *Depósito* é liberado para todas as *contas ativas* e *desbloqueadas*
        - *Saque* é permitido para todas as *contas ativas* e *desbloqueadas* desde que haja *saldo disponível* e não ultrapasse o limite diário de *2 mil reais*

## Regulação obrigatória

- Precisamos *bloquear* e *desbloquear* a **conta digital Dock** a qualquer momento
- A **conta digital Dock** nunca poderá ter o *saldo negativo*


#  Orientações

Utilize qualquer uma das linguagens de programação:
- Java
- Javascript
- Typescript
- Python
- Kotlin
- Golang

Desenvolva o case seguindo as melhores práticas que julgar necessário, aplique todos os conceitos, se atente a qualidade, utilize toda e qualquer forma de governança de código válido. Vamos considerar toda e qualquer implementação, trecho de código, documentação e/ou intenção compartilhada conosco. Esperamos também que o desafio seja feito dentro do tempo disponibilizado e que esteja condizente com a posição pretendida.

É necessário ter o desafio 100% funcional contendo informações e detalhes sobre: como iniciar a aplicação, interagir com as funcionalidades disponíveis e qualquer outro ponto adicional.

## Diferenciais

- Práticas, padrões e conceitos de microservices será considerado um diferencial para nós por existir uma variedade de produtos e serviços dentro da Dock.
- Temos 100% das nossas aplicações e infraestrutura na nuvem, consideramos um diferencial, caso o desafio seja projeto para ser executado na nuvem.
- Nossos times são autônomos e têm liberdade para definir arquiteturas e soluções. Por este motivo será considerado diferencial toda: arquitetura, design, paradigma e documentação detalhando a sua abordagem.

### Instruções
      1. Faça o fork do desafio;
      2. Crie um repositório privado no seu github para o projeto e adicione como colaborador, os usuários informados no email pelo time de recrutameto ;
      3. Após concluir seu trabalho faça um push; 
      4. Envie um e-mail à pessoa que está mantendo o contato com você durante o processo notificando a finalização do desafio para validação.
