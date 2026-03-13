import os

# A sua lista exata de recursos (Idêntica ao que a role exige)
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
    # Usamos a variável pura, sem conversões!
    nome_arquivo = f"main_export_create_{recurso}.yml"
    
    # 1. Altera o NOME do playbook lá no topo para facilitar a leitura no log do AAP
    novo_conteudo = conteudo_base.replace(
        "Controller file create dump job_templates",
        f"Controller file create dump {recurso}"
    )
    
    # 2. Altera a TAG para bater exatamente com a lista
    novo_conteudo = novo_conteudo.replace(
        "input_tag:\n      - job_templates",
        f"input_tag:\n      - {recurso}"
    )
    
    # Grava o novo playbook
    with open(nome_arquivo, "w") as f:
        f.write(novo_conteudo)
        
    print(f"✅ Arquivo gerado: {nome_arquivo} (Tag: {recurso})")

print("\n🎉 Todos os playbooks foram gerados com sucesso e com as tags corretas!")