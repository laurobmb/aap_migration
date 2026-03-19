import yaml
from awx.main.models import Credential
from awx.main.utils.encryption import get_encryption_key, decrypt_value

cofre = {}
credenciais = Credential.objects.all()

for cred in credenciais:
    inputs = cred.inputs
    if inputs:
        cofre_cred = {}
        for key, value in inputs.items():
            if isinstance(value, str) and value.startswith('$encrypted$'):
                try:
                    enc_key = get_encryption_key(key, pk=cred.pk)
                    decrypted = decrypt_value(enc_key, value)
                    cofre_cred[key] = decrypted
                except Exception as e:
                    cofre_cred[key] = f"FALHA: {str(e)}"
            else:
                cofre_cred[key] = value
                
        cofre[cred.name] = cofre_cred

caminho_arquivo = '/tmp/senhas_descriptografadas.yml'
with open(caminho_arquivo, 'w') as f:
    yaml.dump(cofre, f, default_flow_style=False, allow_unicode=True)

print(f"Sucesso! Senhas salvas em {caminho_arquivo}")