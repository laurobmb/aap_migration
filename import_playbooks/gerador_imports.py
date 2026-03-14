import os

# Mapeamento estrito da Ordem de Dependência do AAP
# Tupla: ("Nome do Arquivo/Recurso", "Variável Exata do Dispatch")
recursos_import = [
    ("organizations", "controller_organizations"),
    ("teams", "controller_teams"),
    ("users", "controller_user_accounts"),
    ("execution_environments", "controller_execution_environments"),
    ("credential_types", "controller_credential_types"),
    ("credentials", "controller_credentials"),
    ("notification_templates", "controller_notification_templates"),
    ("projects", "controller_projects"),
    ("inventories", "controller_inventories"),
    ("inventory_sources", "controller_inventory_sources"),
    ("instance_groups", "controller_instance_groups"),
    ("hosts", "controller_hosts"),
    ("groups", "controller_groups"),
    ("applications", "controller_applications"),
    ("job_templates", "controller_templates"),
    ("workflow_job_templates", "controller_workflows"),
    ("schedules", "controller_schedules"),
    ("roles", "controller_roles"),
    ("labels", "controller_labels")
]

arquivo_base = "template_import.yml"

with open(arquivo_base, "r") as f:
    conteudo_base = f.read()

print("Gerando Playbooks de Importação Individuais...")

for nome_arquivo_ref, nome_variavel in recursos_import:
    nome_arquivo = f"main_import_apply_{nome_arquivo_ref}.yml"
    
    # Substitui os placeholders do template
    novo_conteudo = conteudo_base.replace("RESOURCE_FILE_NAME", nome_arquivo_ref)
    novo_conteudo = novo_conteudo.replace("RESOURCE_VAR_NAME", nome_variavel)
    
    with open(nome_arquivo, "w") as f:
        f.write(novo_conteudo)
        
    print(f"✅ Criado: {nome_arquivo}")

# =========================================================
# GERADOR DO WORKFLOW SEQUENCIAL DE IMPORTAÇÃO
# =========================================================
print("\nGerando Workflow Sequencial de Importação...")

def formatar_nome(recurso):
    return f"AAP Migration - Apply {recurso.replace('_', ' ').title()}"

nodes_list = []

# O primeiro nó sincroniza o projeto Git
primeiro_recurso = formatar_nome(recursos_import[0][0])
nodes_list.append(f"""      - identifier: aap-migration-sync
        unified_job_template:
          organization:
            name: "{{{{ orgs }}}}"
          name: aap-migration
          type: project
        related:
          failure_nodes: []
          always_nodes: []
          credentials: []
          success_nodes:
            - identifier: {primeiro_recurso}""")

# Cria os nós sequenciais formando uma "Corrente"
for i in range(len(recursos_import)):
    nome_atual = formatar_nome(recursos_import[i][0])
    
    # Se não for o último, aponta pro próximo. Se for o último, fica vazio.
    if i < len(recursos_import) - 1:
        nome_proximo = formatar_nome(recursos_import[i+1][0])
        succ_nodes = f"\n            - identifier: {nome_proximo}"
    else:
        succ_nodes = " []"

    nodes_list.append(f"""      - identifier: {nome_atual}
        all_parents_must_converge: false
        related:
          failure_nodes: []
          always_nodes: []
          credentials: []
          success_nodes:{succ_nodes}
        unified_job_template:
          name: {nome_atual}
          organization:
            name: "{{{{ orgs }}}}"
          type: job_template
          description: "Aplica as configurações de {nome_atual}" """)

nodes_yaml = "\n\n".join(nodes_list)

workflow_yaml = f"""---
controller_workflows:
  - name: Automation - AAP Apply Configuration (Sequential)
    description: "Restaura o ambiente na ordem correta de dependências"
    organization: "{{{{ orgs }}}}"
    extra_vars:
      target_org: 'ALL'
    inventory: 'Default Blank Localhost Only'
    allow_simultaneous: false
    ask_variables_on_launch: true
    schedules: []
    workflow_nodes:

{nodes_yaml}
...
"""

nome_wf = "wf_import_aap_migration.yml"
with open(nome_wf, "w") as f:
    f.write(workflow_yaml)

print(f"✅ Workflow Sequencial Gerado: {nome_wf}")