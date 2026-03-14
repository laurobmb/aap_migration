import os
import re

# A lista de recursos na ORDEM EXATA de importação do AAP
recursos_import = [
    "organizations",
    "teams",
    "users",
    "execution_environments",
    "credential_types",
    "credentials",
    "projects",
    "inventories",
    "inventory_sources",
    "instance_groups",
    "hosts",
    "groups",
    "applications",
    "job_templates",
    "workflow_job_templates",
    "schedules",
    "roles",
    "labels"
]

arquivo_base = "template_jt_import.yml"

# Lê o conteúdo do seu template base
with open(arquivo_base, "r") as f:
    conteudo_base = f.read()

print("Gerando YAMLs dos Job Templates de Importação (CaC)...")

for recurso in recursos_import:
    # Cria um nome bonito (Title Case) para a interface do AAP
    # Exemplo: "credential_types" vira "Credential Types"
    nome_exibicao = recurso.replace('_', ' ').title()

    # Define o nome do arquivo que será salvo na sua pasta do Git
    nome_arquivo = f"jt_import_{recurso}.yml"
    
    # 1. Substitui o Nome do Job Template (Muda "Get" ou qualquer outra coisa para "Apply")
    # count=1 garante que ele não mexa no nome de outras coisas (como o nome do projeto)
    novo_conteudo = re.sub(
        r'name: "AAP Migration - [a-zA-Z0-9\s\-]*"',
        f'name: "AAP Migration - Apply {nome_exibicao}"',
        conteudo_base,
        count=1 
    )
    
    # 2. Substitui o nome do Playbook que o Job Template vai executar
    # Apontando para os playbooks de import criados no passo anterior
    novo_conteudo = re.sub(
        r'playbook: ".*\.yml"',
        f'playbook: "import_playbooks/main_import_apply_{recurso}.yml"',
        novo_conteudo
    )
    
    # Grava o novo arquivo YAML
    with open(nome_arquivo, "w") as f:
        f.write(novo_conteudo)
        
    print(f"✅ Arquivo gerado: {nome_arquivo} -> Playbook vinculado: import_playbooks/main_import_apply_{recurso}.yml")

print("\n🎉 Todos os 18 Job Templates de Importação foram gerados com sucesso!")