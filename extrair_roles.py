import yaml
from django.contrib.auth.models import User
from awx.main.models import Team

# Mapeia os nomes internos do banco para o padrão que o CaC (GitOps) exige
type_map = {
    'jobtemplate': 'job_templates',
    'project': 'projects',
    'inventory': 'inventories',
    'credential': 'credentials',
    'organization': 'organizations',
    'workflowjobtemplate': 'workflow_job_templates'
}

grouped_roles = {}

# Função para agrupar as roles em blocos limpos
def add_role(actor_type, actor_name, role_name, res_type, res_name):
    key = (actor_type, actor_name, role_name)
    if key not in grouped_roles:
        grouped_roles[key] = {}
    if res_type not in grouped_roles[key]:
        grouped_roles[key][res_type] = []
    if res_name not in grouped_roles[key][res_type]:
        grouped_roles[key][res_type].append(res_name)

# 1. Varre as permissões amarradas a TIMES
for team in Team.objects.all():
    for role in team.roles.all():
        if role.content_object and role.content_type.model in type_map:
            # Tira o sufixo "_role" (ex: "execute_role" vira "execute")
            nome_role_limpo = role.role_field.replace('_role', '')
            res_type = type_map[role.content_type.model]
            add_role('team', team.name, nome_role_limpo, res_type, role.content_object.name)

# 2. Varre as permissões amarradas a USUÁRIOS (Ignorando system)
for user in User.objects.filter(is_superuser=False).exclude(username='system'):
    for role in user.roles.all():
        if role.content_object and role.content_type.model in type_map:
            nome_role_limpo = role.role_field.replace('_role', '')
            res_type = type_map[role.content_type.model]
            add_role('user', user.username, nome_role_limpo, res_type, role.content_object.name)

# Converte o dicionário agrupado para a lista final do CaC
cac_roles = []
for (actor_type, actor_name, role_name), resources in grouped_roles.items():
    role_dict = {
        actor_type: actor_name,
        'role': role_name
    }
    role_dict.update(resources) # Adiciona a lista de templates/inventários
    cac_roles.append(role_dict)

# Salva no disco
caminho_arquivo = '/tmp/roles_exportadas.yml'
with open(caminho_arquivo, 'w') as f:
    yaml.dump({'controller_roles': cac_roles}, f, default_flow_style=False, sort_keys=False)

print(f"✅ Sucesso! 22.000 permissões brutas foram otimizadas para {len(cac_roles)} blocos limpos em {caminho_arquivo}")