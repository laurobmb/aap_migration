import os

# A sua lista de recursos
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
    # 1. Corrige o plural do inventory para bater com a role
    nome_seguro = "inventories" if recurso == "inventory" else recurso
    
    # 2. Cria um nome bonito (Title Case) para a interface do AAP
    # Exemplo: "credential_types" vira "Credential Types"
    nome_exibicao = nome_seguro.replace('_', ' ').title()

    # Define o nome do arquivo que será salvo na sua pasta do Git
    nome_arquivo = f"jt_export_{nome_seguro}.yml"
    
    # 3. Substitui o Nome do Job Template
    novo_conteudo = conteudo_base.replace(
        'name: "AAP Migration - Get Templates"',
        f'name: "AAP Migration - Get {nome_exibicao}"'
    )
    
    # 4. Substitui o nome do Playbook que o Job Template vai executar
    novo_conteudo = novo_conteudo.replace(
        'playbook: "main_export_create_job_templates.yml"',
        f'playbook: "main_export_create_{nome_seguro}.yml"'
    )
    
    # Grava o novo arquivo YAML
    with open(nome_arquivo, "w") as f:
        f.write(novo_conteudo)
        
    print(f"✅ Arquivo gerado: {nome_arquivo} -> Playbook vinculado: main_export_create_{nome_seguro}.yml")

print("\n🎉 Todos os 20 Job Templates de CaC foram gerados com sucesso!")