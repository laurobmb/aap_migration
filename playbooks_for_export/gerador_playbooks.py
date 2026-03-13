import os

# A sua lista exata de recursos
recursos = [
    "settings", "credentials", "credential_types", "execution_environments",
    "groups", "hosts", "inventory", "inventory_sources", "job_templates",
    "notification_templates", "organizations", "projects", "roles", "teams",
    "users", "workflow_job_templates", "instance_groups", "applications",
    "labels", "schedules"
]

arquivo_base = "template.yml"

# Lê o conteúdo do seu template
with open(arquivo_base, "r") as f:
    conteudo_base = f.read()

for recurso in recursos:
    # 🚨 Correção amigável: Sua lista tem "inventory", mas a role exige "inventories" no plural
    nome_seguro = "inventories" if recurso == "inventory" else recurso

    nome_arquivo = f"main_export_create_{nome_seguro}.yml"
    
    # 1. Altera o NOME do playbook lá no topo para facilitar a leitura no log do AAP
    novo_conteudo = conteudo_base.replace(
        "Controller file create dump job_templates",
        f"Controller file create dump {nome_seguro}"
    )
    
    # 2. Altera a TAG. 
    # Adicionamos o prefixo 'controller_' porque a role exige isso para funcionar (ex: controller_credentials)
    novo_conteudo = novo_conteudo.replace(
        "input_tag:\n      - job_templates",
        f"input_tag:\n      - {nome_seguro}"
    )
    
    # Grava o novo playbook
    with open(nome_arquivo, "w") as f:
        f.write(novo_conteudo)
        
    print(f"✅ Arquivo gerado: {nome_arquivo}")

print("\n🎉 Todos os playbooks foram gerados com sucesso!")