import yaml
from django.contrib.auth.models import User
from awx.main.models import Team

type_map = {
    'jobtemplate': 'job_templates',
    'project': 'projects',
    'inventory': 'inventories',
    'credential': 'credentials',
    'organization': 'organizations',
    'workflowjobtemplate': 'workflow_job_templates'
}

grouped_roles = {}

def add_role(actor_type, actor_name, role_name, res_type, res_name):
    key = (actor_type, actor_name, role_name)
    if key not in grouped_roles:
        grouped_roles[key] = {}
    if res_type not in grouped_roles[key]:
        grouped_roles[key][res_type] = []
    if res_name not in grouped_roles[key][res_type]:
        grouped_roles[key][res_type].append(res_name)

# 1. Varre os TIMES navegando pela árvore de permissões "filhas"
for team in Team.objects.all():
    if team.member_role:
        for role in team.member_role.children.all():
            if role.content_object and role.content_type and role.content_type.model in type_map:
                nome_role_limpo = role.role_field.replace('_role', '')
                res_type = type_map[role.content_type.model]
                add_role('team', team.name, nome_role_limpo, res_type, role.content_object.name)

# 2. Varre os USUÁRIOS (Ignorando system) com relacionamento direto
for user in User.objects.filter(is_superuser=False).exclude(username='system'):
    for role in user.roles.all():
        if role.content_object and role.content_type and role.content_type.model in type_map:
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
    role_dict.update(resources) 
    cac_roles.append(role_dict)

# Salva na "casa" do awx para evitar o bloqueio do SELinux/PrivateTmp
caminho_arquivo = '/var/lib/awx/roles_exportadas.yml'
with open(caminho_arquivo, 'w') as f:
    yaml.dump({'controller_roles': cac_roles}, f, default_flow_style=False, sort_keys=False)

print(f"✅ BINGO! {len(cac_roles)} blocos de Roles extraídos com sucesso para {caminho_arquivo}")