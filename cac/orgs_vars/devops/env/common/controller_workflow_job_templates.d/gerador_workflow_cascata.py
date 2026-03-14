import os
from itertools import zip_longest

# A lista de recursos exata
recursos = [
    "settings", "credentials", "credential_types", "execution_environments",
    "groups", "hosts", "inventory", "inventory_sources", "job_templates",
    "notification_templates", "organizations", "projects", "roles", "teams",
    "users", "workflow_job_templates", "instance_groups", "applications",
    "labels", "schedules"
]

def formatar_nome(recurso):
    return f"AAP Migration - Get {recurso.replace('_', ' ').title()}"

# 1. Separar as Organizações (Nó raiz da coleta, base do AAP)
recurso_raiz = "organizations"
recursos_restantes = [r for r in recursos if r != recurso_raiz]

# 2. Dividir os 19 restantes perfeitamente ao meio
metade = (len(recursos_restantes) + 1) // 2
grupo_a = recursos_restantes[:metade]
grupo_b = recursos_restantes[metade:]

nodes_list = []

# --- NÓ 0: PROJETO GITHUB ---
nome_raiz = formatar_nome(recurso_raiz)
nodes_list.append(f"""      - identifier: aap-migration
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
            - identifier: {nome_raiz}""")

# --- NÓ 1: ORGANIZAÇÕES (Chama todo o Grupo A ao mesmo tempo) ---
succ_org = "\n".join([f"            - identifier: {formatar_nome(r)}" for r in grupo_a])
nodes_list.append(f"""      - identifier: {nome_raiz}
        all_parents_must_converge: false
        related:
          failure_nodes: []
          always_nodes: []
          credentials: []
          success_nodes:
{succ_org}
        unified_job_template:
          name: {nome_raiz}
          organization:
            name: "{{{{ orgs }}}}"
          type: job_template
          description: "{{{{ description }}}}" """)

# --- NÓS DO GRUPO A e GRUPO B (Emparelhados perfeitamente) ---
# zip_longest garante que mesmo que o Grupo B seja menor, o loop não quebre
for item_a, item_b in zip_longest(grupo_a, grupo_b):
    
    # Processa o nó do Grupo A
    # Se houver um par correspondente no Grupo B, ele aciona. Se não, fica vazio.
    succ_a = f"\n            - identifier: {formatar_nome(item_b)}" if item_b else " []"
    
    nodes_list.append(f"""      - identifier: {formatar_nome(item_a)}
        all_parents_must_converge: false
        related:
          failure_nodes: []
          always_nodes: []
          credentials: []
          success_nodes:{succ_a}
        unified_job_template:
          name: {formatar_nome(item_a)}
          organization:
            name: "{{{{ orgs }}}}"
          type: job_template
          description: "{{{{ description }}}}" """)
          
    # Processa o nó do Grupo B (Sempre o fim da linha, não aciona mais nada)
    if item_b:
        nodes_list.append(f"""      - identifier: {formatar_nome(item_b)}
        all_parents_must_converge: false
        related:
          failure_nodes: []
          always_nodes: []
          credentials: []
          success_nodes: []
        unified_job_template:
          name: {formatar_nome(item_b)}
          organization:
            name: "{{{{ orgs }}}}"
          type: job_template
          description: "{{{{ description }}}}" """)

nodes_yaml = "\n\n".join(nodes_list)

# --- JUNTAR TUDO NO YAML FINAL ---
final_yaml = f"""---
controller_workflows:
  - name: Automation - AAP Migration
    description: "{{{{ description }}}}"
    organization: "{{{{ orgs }}}}"
    extra_vars:
      teste_var: 'xxx'
    inventory: 'Default Blank Localhost Only'
    limit: ''
    scm_branch: ''
    webhook_service: ''
    webhook_credential: ''
    survey_enabled: false
    allow_simultaneous: false
    ask_limit_on_launch: True
    ask_inventory_on_launch: True
    ask_tags_on_launch: True
    ask_credential_on_launch: true
    schedules: []
    workflow_nodes:

{nodes_yaml}
...
"""

# Salva o arquivo de forma limpa
nome_arquivo = "Automation - AAP Migration.yml"
with open(nome_arquivo, "w") as f:
    f.write(final_yaml)

print(f"✅ Workflow em Cascata gerado com sucesso: {nome_arquivo}")