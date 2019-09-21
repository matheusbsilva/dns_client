## Instalação

1. Instale as dependências do projeto através do comando:
```
pip install -r requirements.txt
```

Foi utilizado como depedência externa a biblioteca [bitstring](https://pypi.org/project/bitstring/), para auxiliar no parse das informações da requisição.

## Execução

Para utilizar a aplicação execute na raiz do projeto:
```
python dns.py hostname dns_server_ip
```

Exemplo:

```
python dns.py www.google.com 8.8.8.8 
```
