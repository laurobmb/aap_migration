import os
import re

# A sua lista de recursos (Idêntica ao que a role exige)
recursos = [
    "settings", "credentials", "credential_types", "execution_environments",
    "groups", "hosts", "inventory", "inventory_sources", "job_templates",
    "notification_templates", "organizations", "projects", "roles", "teams",
    "users", "workflow_job_templates", "instance_groups", "applications",
    "labels", "schedules"
]

arquivo_base = "template_jt.yml"

# Lê o conteúdo do seu template
with open(arquivo_base, "r") as f:
    conteudo_base = f.read()

for recurso in recursos:
    # Cria um nome bonito (Title Case) para a interface do AAP
    # Exemplo: "credential_types" vira "Credential Types"
    nome_exibicao = recurso.replace('_', ' ').title()

    # Define o nome do arquivo que será salvo na sua pasta do Git
    nome_arquivo = f"jt_export_{recurso}.yml"
    
    # 1. Substitui o Nome do Job Template de forma dinâmica
    novo_conteudo = re.sub(
        r'name: "AAP Migration - Get .*"',
        f'name: "AAP Migration - Get {nome_exibicao}"',
        conteudo_base
    )
    
    # 2. Substitui o nome do Playbook que o Job Template vai executar de forma dinâmica
    novo_conteudo = re.sub(
        r'playbook: ".*\.yml"',
        f'playbook: "export_playbooks/main_export_create_{recurso}.yml"',
        novo_conteudo
    )
    
    # Grava o novo arquivo YAML
    with open(nome_arquivo, "w") as f:
        f.write(novo_conteudo)
        
    print(f"✅ Arquivo gerado: {nome_arquivo} -> Playbook vinculado: export_playbooks/main_export_create_{recurso}.yml")

print("\n🎉 Todos os 20 Job Templates de CaC foram gerados com sucesso e alinhados no singular!")