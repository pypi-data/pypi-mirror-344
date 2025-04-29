from jira.client import JIRA

jira_options={'server': 'https://jira.globaldevtools.bbva.com'}

attr_ticket_dict = {
    "summary" : "summary",
    "status" : "status",
    "issuetype" : "issuetype",
    "priority" : "priority",
    "labels" : "labels",
    "customfield_13300" : "team_backlog",
    "customfield_20201" : "tb_geography",
    "customfield_20200" : "workspace_geography",
    "customfield_10004" : "feature_link",
    "customfield_10270" : "item_type",
    "customfield_18001" : "tech_stack",
    "customfield_10601" : "dor",
    "customfield_10600" : "dod",
    "customfield_10260" : "acceptance_criteria",
    "customfield_10002" : "story_points",
    "customfield_10272" : "sprint_estimate",
    "description" : "description",
    "creator" : "creator",
    "subtasks" : "subtasks"
}

labels_dict = {
    'visado' : ['#TTV_Visado'],
    'volcado' : ['#TTV_Dictamen'],
    'correcion' : ['#TTV_Correccion']
}

def get_attr_jira(issue_code: str, jira_obj):
  dict_attr = {}
  print(f"********** Leyendo Ticket {issue_code} **********")
  issue = jira_obj.issue(issue_code)

  # Mostrar todos los campos disponibles
  for field, value in vars(issue.fields).items():
    if value is not None:
      dict_attr[field] = value
  return dict_attr

def get_attr_subtask(subtasks_code: str, jira_obj):
  subtask_list = []
  list_keys_validation = ['summary', 'issuetype','priority','resolution','labels','assignee', 'parent','reporter','description','creator','customfield_13300']
  for subtask in subtasks_code:
    aux_dicct = {}
    for key, value in get_attr_jira(subtask.key, jira_obj).items():
      if key in list_keys_validation:
        if key == 'parent':
          aux_dicct[key] = value.key
        elif key == 'resolution':
          aux_dicct[key] = value.name
        elif key == 'assignee':
          aux_dicct[key] = value.name
        elif key == 'reporter':
          aux_dicct[key] = value.name
        elif key == 'issuetype':
          aux_dicct[key] = value.name
        elif key == 'priority':
          aux_dicct[key] = value.name
        elif key == 'creator':
          aux_dicct[key] = value.name
        elif key == 'customfield_13300':
          aux_dicct['team_backlog'] = vars(jira_obj.issue(value[0]).fields)['customfield_13702']
        else:
          aux_dicct[key] = value
    subtask_list.append(aux_dicct)

  return subtask_list

def rename_keys(subtasks_attr):
  return {new_key: subtasks_attr[old_key] for old_key, new_key in attr_ticket_dict.items() if old_key in subtasks_attr}

def clean_values(dict_jira_prev, jira_obj):
  dict_final = {}
  for key, value in dict_jira_prev.items():
    if key == 'status' or key == 'issuetype' or key == 'priority' or key == 'creator':
      dict_final[key] = value.name
    elif key == 'tb_geography' or key == 'workspace_geography' or key == 'item_type' or key == 'tech_stack' or key == 'sprint_estimate':
      dict_final[key] = value.value
    else:
      dict_final[key] = value
    if key == 'team_backlog':
      dict_final[key] = vars(jira_obj.issue(value[0]).fields)['customfield_13702']
  return dict_final

# Validar Campos y valores de la Story
def validate_subtask(subtasks):
  for subtask in subtasks:
    pref = subtask['summary'].upper().split('-')[0].strip()
    validation_list = {}
    print(f"\nValidando subtask {subtask['summary'].upper()}\n")
    aux_label = None
    if 'VISADO' in subtask['summary'].upper():
      print(f"CORRECTO -> Nombre de la subtask es correcta : {subtask['summary']}")
      aux_label = 'visado'
    elif 'VOLCADO' in subtask['summary'].upper():
      print(f"CORRECTO -> Nombre de la subtask es correcta : {subtask['summary']}")
      aux_label = 'volcado'
    elif 'CORRECION' in subtask['summary'].upper():
      print(f"CORRECTO -> Nombre de la subtask es correcta : {subtask['summary']}")
      aux_label = 'correcion'
    else:
      print(f"INCORRECTO -> Nombre de la subtask no es correcta, deberia ser de tipo Visado, Volcado o de Correcion")

    if subtask['issuetype'].upper() == 'SUBTAREA':
      print(f"CORRECTO -> El tipo de Issue es correcta: {subtask['issuetype']}")
    else:
      print(f"INCORRECTO -> El tipo de Issue debe ser subtarea")

    if subtask['priority'].upper() == 'MEDIUM':
      print(f"CORRECTO -> El tipo de prioridad es correcta: {subtask['priority']}")
    else:
      print(f"INCORRECTO -> El tipo de prioridad deberia ser medium")

    if subtask['resolution'].upper() == 'NUEVO':
      print(f"CORRECTO -> El tipo de estado es correcta: {subtask['resolution']}")
    else:
      print(f"INCORRECTO -> El tipo de estado deberia ser new")

    if subtask['team_backlog'].upper() == 'PE DATA MODELLING':
      print(f"CORRECTO -> Esta asociado al backlog {subtask['team_backlog']}")
    else:
      print(f"INCORRECTO -> No esta asociado al backlog PE DATA MODELLING")
    for label in subtask['labels']:
      if label in (f"{labels_dict[aux_label][0]}",f"{pref}_DM"):
        print(f"CORRECTO -> El label {label} es correcto")
      else:
        print(f"INCORRECTO -> El label {label} no es correcto")

# Validando los campos principales de la Historia
def validate_history(dict_final):
  print(f"\nRevisando el ticket {dict_final['summary']}\n")
  if dict_final['issuetype'].upper() == 'HISTORIA':
    print(f"CORRECTO -> La Issue es de tipo {dict_final['issuetype']}")
  else:
    print(f"INCORRECTO -> La Issue no es de tipo Historia")

  if dict_final['team_backlog'].upper() == 'PE DATA MODELLING':
    print(f"CORRECTO -> La Issue esta en el tablero {dict_final['team_backlog']}")
  else:
    print(f"INCORRECTO -> La Issue no esta en el tablero PE DATA MODELLING")

  print("\nLa issue tiene las siguientes subtask:")
  for subtask in dict_final['subtasks']:
    print(f" -> {subtask['summary']}")
  validate_subtask(dict_final['subtasks'])

def validate_ticket(username: str, token: str):
  
  jira_obj=JIRA(options=jira_options, auth=(username,token))
  
  link_issue = input("Ingrese link de jira: ")
  issue_code = link_issue.split('/')[-1]
  subtasks_attr = get_attr_jira(issue_code, jira_obj)
  subtasks_code = subtasks_attr['subtasks']
  subtasks_value = get_attr_subtask(subtasks_code, jira_obj)

  subtasks_attr['subtasks'] = subtasks_value

  dict_jira_prev = rename_keys(subtasks_attr)
  dict_final = clean_values(dict_jira_prev, jira_obj)
  validate_history(dict_final)