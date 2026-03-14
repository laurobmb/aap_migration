import os

# A lista de recursos
recursos = [
    "settings", "credentials", "credential_types", "execution_environments",
    "groups", "hosts", "inventory", "inventory_sources", "job_templates",
    "notification_templates", "organizations", "projects", "roles", "teams",
    "users", "workflow_job_templates", "instance_groups", "applications",
    "labels", "schedules"
]

# 1. Gerar os nomes bonitos dos nós (Ex: "AAP Migration - Get Job Templates")
node_names = [f"AAP Migration - Get {r.replace('_', ' ').title()}" for r in recursos]

# 2. Montar a lista de success_nodes para atrelar ao Projeto aap-migration
success_nodes_yaml = "\n".join([f"            - identifier: {name}" for name in node_names])

# 3. Montar os blocos individuais de cada nó do Workflow
nodes_list = []
for name in node_names:
    node = f"""      - identifier: {name}
        all_parents_must_converge: false
        related:
          failure_nodes: []
          always_nodes: []
          credentials: []
          success_nodes: []
        unified_job_template:
          name: {name}
          organization:
            name: "{{{{ orgs }}}}"
          type: job_template
          description: "{{{{ description }}}}" """
    nodes_list.append(node)

nodes_yaml = "\n\n".join(nodes_list)

# 4. Juntar tudo no YAML principal, respeitando a indentação exata do CaC
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

      - identifier: aap-migration
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
{success_nodes_yaml}

{nodes_yaml}
...
"""

# Salva o arquivo gerado
nome_arquivo = "Automation - AAP Migration.yml"
with open(nome_arquivo, "w") as f:
    f.write(final_yaml)

print(f"✅ Arquivo de Workflow gerado com sucesso: {nome_arquivo}")