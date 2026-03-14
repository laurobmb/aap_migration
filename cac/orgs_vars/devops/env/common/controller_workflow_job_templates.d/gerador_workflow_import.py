import os

# A ordem EXATA E INQUEBRÁVEL de dependências para a importação no AAP
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

def formatar_nome(recurso):
    return f"AAP Migration - Apply {recurso.replace('_', ' ').title()}"

nodes_list = []

# --- NÓ 0: PROJETO GITHUB (Sincroniza o repositório CaC antes de começar a aplicar) ---
primeiro_recurso = formatar_nome(recursos_import[0])
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

# --- NÓS SEQUENCIAIS (Linha de Montagem) ---
for i in range(len(recursos_import)):
    nome_atual = formatar_nome(recursos_import[i])
    
    # Define quem é o próximo nó na corrente
    if i < len(recursos_import) - 1:
        nome_proximo = formatar_nome(recursos_import[i+1])
        succ_nodes = f"\n            - identifier: {nome_proximo}"
    else:
        # Se for o último (labels), ele não aciona mais nada
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
          description: "{{{{ description }}}}" """)

nodes_yaml = "\n\n".join(nodes_list)

# --- JUNTAR TUDO NO YAML FINAL ---
final_yaml = f"""---
controller_workflows:
  - name: Automation - AAP Apply Migration (Import)
    description: "{{{{ description }}}}"
    organization: "{{{{ orgs }}}}"
    
    # 🚨 MÁGICA DA ORG: Define a variável padrão e permite que o usuário troque na hora de rodar
    extra_vars:
      target_org: 'ALL'
    ask_variables_on_launch: true
    
    inventory: 'Default Blank Localhost Only'
    limit: ''
    scm_branch: ''
    webhook_service: ''
    webhook_credential: ''
    survey_enabled: false
    allow_simultaneous: false
    ask_limit_on_launch: false
    ask_inventory_on_launch: false
    ask_tags_on_launch: false
    ask_credential_on_launch: false
    schedules: []
    workflow_nodes:

{nodes_yaml}
...
"""

# Salva o arquivo de forma limpa
nome_arquivo = "Automation - AAP Apply Migration.yml"
with open(nome_arquivo, "w") as f:
    f.write(final_yaml)

print(f"✅ Workflow Sequencial de Importação gerado com sucesso: {nome_arquivo}")