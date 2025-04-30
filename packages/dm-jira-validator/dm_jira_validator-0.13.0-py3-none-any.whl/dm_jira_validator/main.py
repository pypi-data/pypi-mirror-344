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
  issue = jira_obj.issue(issue_code)

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

def validate_history(dict_final, issue_code):
    html = f"""
    <h2>Validación de Historia</h2>
    <h3>{dict_final['summary']} ({issue_code})</h3>
    <table border="1" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr>
                <th>Campo Validado</th>
                <th>Resultado</th>
            </tr>
        </thead>
        <tbody>
    """

    # Validar tipo de Issue
    if dict_final['issuetype'].upper() == 'HISTORIA':
        html += f"""
        <tr style="background-color: #d4edda; color: black;">
            <td>Tipo de Issue</td>
            <td>CORRECTO - Es de tipo Historia</td>
        </tr>
        """
    else:
        html += f"""
        <tr style="background-color: #f8d7da; color: black;">
            <td>Tipo de Issue</td>
            <td>INCORRECTO - No es de tipo Historia</td>
        </tr>
        """

    # Validar backlog
    if dict_final['team_backlog'].upper() == 'PE DATA MODELLING':
        html += f"""
        <tr style="background-color: #d4edda; color: black;">
            <td>Backlog</td>
            <td>CORRECTO - Está asociado al backlog PE DATA MODELLING</td>
        </tr>
        """
    else:
        html += f"""
        <tr style="background-color: #f8d7da; color: black;">
            <td>Backlog</td>
            <td>INCORRECTO - No está asociado al backlog PE DATA MODELLING</td>
        </tr>
        """

    # Listar subtasks
    html += """
        </tbody>
    </table>
    <h3>Subtasks</h3>
    """
    html += validate_subtask(dict_final['subtasks'])  # Reutiliza la función validate_subtask para subtasks

    return html


def validate_subtask(subtasks):
    html = """
    <table border="1" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr>
                <th>Subtask</th>
                <th>Campo Validado</th>
                <th>Resultado</th>
            </tr>
        </thead>
        <tbody>
    """
    labels_dict = {
        'visado': ['VISADO_LABEL'],
        'volcado': ['VOLCADO_LABEL'],
        'correcion': ['CORRECION_LABEL']
    }

    for subtask in subtasks:
        pref = subtask['summary'].upper().split('-')[0].strip()
        aux_label = None

        # Validar nombre de la subtask
        if 'VISADO' in subtask['summary'].upper():
            aux_label = 'visado'
            html += f"""
            <tr style="background-color: #d4edda; color: black;">
                <td>{subtask['summary']}</td>
                <td>Nombre de la subtask</td>
                <td>CORRECTO - Tipo: Visado</td>
            </tr>
            """
        elif 'VOLCADO' in subtask['summary'].upper():
            aux_label = 'volcado'
            html += f"""
            <tr style="background-color: #d4edda; color: black;">
                <td>{subtask['summary']}</td>
                <td>Nombre de la subtask</td>
                <td>CORRECTO - Tipo: Volcado</td>
            </tr>
            """
        elif 'CORRECION' in subtask['summary'].upper():
            aux_label = 'correcion'
            html += f"""
            <tr style="background-color: #d4edda; color: black;">
                <td>{subtask['summary']}</td>
                <td>Nombre de la subtask</td>
                <td>CORRECTO - Tipo: Corrección</td>
            </tr>
            """
        else:
            html += f"""
            <tr style="background-color: #f8d7da; color: black;">
                <td>{subtask['summary']}</td>
                <td>Nombre de la subtask</td>
                <td>INCORRECTO - Debe ser Visado, Volcado o Corrección</td>
            </tr>
            """

        # Validar tipo de Issue
        if subtask['issuetype'].upper() == 'SUBTAREA':
            html += f"""
            <tr style="background-color: #d4edda; color: black;">
                <td>{subtask['summary']}</td>
                <td>Tipo de Issue</td>
                <td>CORRECTO - Tipo: Subtarea</td>
            </tr>
            """
        else:
            html += f"""
            <tr style="background-color: #f8d7da; color: black;">
                <td>{subtask['summary']}</td>
                <td>Tipo de Issue</td>
                <td>INCORRECTO - Debe ser subtarea</td>
            </tr>
            """

        # Validar prioridad
        if subtask['priority'].upper() == 'MEDIUM':
            html += f"""
            <tr style="background-color: #d4edda; color: black;">
                <td>{subtask['summary']}</td>
                <td>Prioridad</td>
                <td>CORRECTO - Prioridad: Medium</td>
            </tr>
            """
        else:
            html += f"""
            <tr style="background-color: #f8d7da; color: black;">
                <td>{subtask['summary']}</td>
                <td>Prioridad</td>
                <td>INCORRECTO - Debe ser Medium</td>
            </tr>
            """

        # Validar resolución
        if subtask['resolution'].upper() == 'NUEVO':
            html += f"""
            <tr style="background-color: #d4edda; color: black;">
                <td>{subtask['summary']}</td>
                <td>Estado</td>
                <td>CORRECTO - Estado: Nuevo</td>
            </tr>
            """
        else:
            html += f"""
            <tr style="background-color: #f8d7da; color: black;">
                <td>{subtask['summary']}</td>
                <td>Estado</td>
                <td>INCORRECTO - Debe ser Nuevo</td>
            </tr>
            """

        # Validar backlog
        if subtask['team_backlog'].upper() == 'PE DATA MODELLING':
            html += f"""
            <tr style="background-color: #d4edda; color: black;">
                <td>{subtask['summary']}</td>
                <td>Backlog</td>
                <td>CORRECTO - Asociado a PE DATA MODELLING</td>
            </tr>
            """
        else:
            html += f"""
            <tr style="background-color: #f8d7da; color: black;">
                <td>{subtask['summary']}</td>
                <td>Backlog</td>
                <td>INCORRECTO - No asociado a PE DATA MODELLING</td>
            </tr>
            """

        # Validar etiquetas
        for label in subtask['labels']:
            if label in (f"{labels_dict[aux_label][0]}", f"{pref}_DM"):
                html += f"""
                <tr style="background-color: #d4edda; color: black;">
                    <td>{subtask['summary']}</td>
                    <td>Etiqueta</td>
                    <td>CORRECTO - Etiqueta: {label}</td>
                </tr>
                """
            else:
                html += f"""
                <tr style="background-color: #f8d7da; color: black;">
                    <td>{subtask['summary']}</td>
                    <td>Etiqueta</td>
                    <td>INCORRECTO - Etiqueta: {label} no es válida</td>
                </tr>
                """

    html += """
        </tbody>
    </table>
    """
    return html


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
  html_report = validate_history(dict_final, issue_code)
  return html_report