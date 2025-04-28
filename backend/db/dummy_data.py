import psycopg2
from faker import Faker
from datetime import datetime, timedelta
import random
from typing import List, Dict
import uuid
from dateutil.relativedelta import relativedelta
import json

fake = Faker()

# Database connection parameters - you should move these to a config file in production
DB_PARAMS = {
    "dbname": "neuratask_db",
    "user": "neuratask_admin",
    "password": "root",
    "host": "localhost",
    "port": "5432"
}

def generate_users(num_users: int = 10) -> List[Dict]:
    users = []
    for _ in range(num_users):
        user = {
            'id': str(uuid.uuid4()),
            'auth0_sub': f'auth0|{fake.uuid4()}',
            'name': fake.name(),
            'email': fake.email(),
            'avatar_url': fake.image_url(),
        }
        users.append(user)
    return users

def generate_workspaces(users: List[Dict], num_workspaces: int = 5) -> List[Dict]:
    workspaces = []
    for _ in range(num_workspaces):
        workspace = {
            'id': str(uuid.uuid4()),
            'owner_id': random.choice(users)['id'],
            'name': fake.company(),
        }
        workspaces.append(workspace)
    return workspaces

def generate_projects(workspaces: List[Dict], num_projects_per_workspace: int = 3) -> List[Dict]:
    projects = []
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF']
    
    for workspace in workspaces:
        for i in range(num_projects_per_workspace):
            project = {
                'id': str(uuid.uuid4()),
                'workspace_id': workspace['id'],
                'name': fake.catch_phrase(),
                'color': random.choice(colors),
                'sort_order': i,
                'is_archived': random.random() < 0.1,
            }
            projects.append(project)
    return projects

def generate_tasks(projects: List[Dict], users: List[Dict], num_tasks_per_project: int = 5) -> List[Dict]:
    tasks = []
    statuses = ['TODO', 'DOING', 'DONE']
    
    for project in projects:
        # Generate main tasks
        for i in range(num_tasks_per_project):
            task = {
                'id': str(uuid.uuid4()),
                'project_id': project['id'],
                'parent_task_id': None,
                'title': fake.sentence(nb_words=6),
                'description': fake.paragraph(),
                'status': random.choice(statuses),
                'priority': random.randint(1, 4),
                'due_date': (datetime.now() + timedelta(days=random.randint(1, 30))).date(),
                'start_date': (datetime.now() + timedelta(days=random.randint(-5, 5))).date(),
                'completed_at': datetime.now() if random.random() < 0.3 else None,
                'created_by': random.choice(users)['id'],
                'assigned_to': random.choice(users)['id'] if random.random() < 0.8 else None,
                'is_recurring': random.random() < 0.2,
                'recurrence_rule': 'FREQ=WEEKLY' if random.random() < 0.2 else None,
            }
            tasks.append(task)
            
            # Generate subtasks (30% probability)
            if random.random() < 0.3:
                for _ in range(random.randint(1, 3)):
                    subtask = {
                        'id': str(uuid.uuid4()),
                        'project_id': project['id'],
                        'parent_task_id': task['id'],
                        'title': fake.sentence(nb_words=4),
                        'description': fake.sentence(),
                        'status': random.choice(statuses),
                        'priority': random.randint(1, 4),
                        'due_date': task['due_date'],
                        'start_date': task['start_date'],
                        'completed_at': datetime.now() if random.random() < 0.3 else None,
                        'created_by': task['created_by'],
                        'assigned_to': task['assigned_to'],
                        'is_recurring': False,
                        'recurrence_rule': None,
                    }
                    tasks.append(subtask)
    return tasks

def generate_labels(workspaces: List[Dict], num_labels_per_workspace: int = 4) -> List[Dict]:
    labels = []
    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF']
    label_names = ['Important', 'Urgent', 'Bug', 'Feature', 'Documentation', 'Meeting', 'Planning', 'Research']
    
    for workspace in workspaces:
        for _ in range(num_labels_per_workspace):
            label = {
                'id': str(uuid.uuid4()),
                'workspace_id': workspace['id'],
                'name': random.choice(label_names),
                'color': random.choice(colors),
            }
            labels.append(label)
    return labels

def generate_task_labels(tasks: List[Dict], labels: List[Dict]) -> List[Dict]:
    task_labels = []
    for task in tasks:
        if random.random() < 0.7:  # 70% chance of having labels
            num_labels = random.randint(1, 3)
            task_labels_subset = random.sample(labels, num_labels)
            for label in task_labels_subset:
                task_label = {
                    'task_id': task['id'],
                    'label_id': label['id'],
                }
                task_labels.append(task_label)
    return task_labels

def generate_comments(tasks: List[Dict], users: List[Dict], max_comments_per_task: int = 3) -> List[Dict]:
    comments = []
    for task in tasks:
        num_comments = random.randint(0, max_comments_per_task)
        for _ in range(num_comments):
            comment = {
                'id': str(uuid.uuid4()),
                'task_id': task['id'],
                'author_id': random.choice(users)['id'],
                'body': fake.paragraph(),
                'edited_at': datetime.now() if random.random() < 0.2 else None,
            }
            comments.append(comment)
    return comments

def generate_reminders(tasks: List[Dict], users: List[Dict]) -> List[Dict]:
    reminders = []
    channels = ['PUSH', 'EMAIL', 'WEB']
    
    for task in tasks:
        if random.random() < 0.4:  # 40% chance of having a reminder
            reminder = {
                'id': str(uuid.uuid4()),
                'task_id': task['id'],
                'user_id': task['assigned_to'] or task['created_by'],
                'remind_at': datetime.now() + timedelta(days=random.randint(1, 7)),
                'channel': random.choice(channels),
            }
            reminders.append(reminder)
    return reminders

def generate_activity_logs(users: List[Dict], tasks: List[Dict], num_activities: int = 50) -> List[Dict]:
    activities = []
    actions = ['CREATE', 'UPDATE', 'DELETE', 'COMPLETE', 'ASSIGN', 'COMMENT']
    entity_types = ['TASK', 'PROJECT', 'COMMENT', 'LABEL']
    
    for _ in range(num_activities):
        activity = {
            'id': str(uuid.uuid4()),
            'entity_type': random.choice(entity_types),
            'entity_id': random.choice(tasks)['id'],
            'action': random.choice(actions),
            'actor_id': random.choice(users)['id'],
            'payload': json.dumps({'detail': fake.sentence()}),  # Convertir a string JSON
        }
        activities.append(activity)
    return activities

def insert_data(conn, table: str, data: List[Dict]):
    if not data:
        return
    
    cursor = conn.cursor()
    columns = data[0].keys()
    values_template = ','.join(['%s'] * len(columns))
    query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({values_template})"
    
    for item in data:
        values = [item[column] for column in columns]
        cursor.execute(query, values)
    
    conn.commit()
    cursor.close()

def main():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        
        # Generate and insert data in order of dependencies
        users = generate_users(10)
        insert_data(conn, 'users', users)
        print("✓ Users inserted")
        
        workspaces = generate_workspaces(users, 5)
        insert_data(conn, 'workspaces', workspaces)
        print("✓ Workspaces inserted")
        
        projects = generate_projects(workspaces)
        insert_data(conn, 'projects', projects)
        print("✓ Projects inserted")
        
        tasks = generate_tasks(projects, users)
        insert_data(conn, 'tasks', tasks)
        print("✓ Tasks inserted")
        
        labels = generate_labels(workspaces)
        insert_data(conn, 'labels', labels)
        print("✓ Labels inserted")
        
        task_labels = generate_task_labels(tasks, labels)
        insert_data(conn, 'task_labels', task_labels)
        print("✓ Task labels inserted")
        
        comments = generate_comments(tasks, users)
        insert_data(conn, 'comments', comments)
        print("✓ Comments inserted")
        
        reminders = generate_reminders(tasks, users)
        insert_data(conn, 'reminders', reminders)
        print("✓ Reminders inserted")
        
        activity_logs = generate_activity_logs(users, tasks)
        insert_data(conn, 'activity_log', activity_logs)
        print("✓ Activity logs inserted")
        
        print("\nDummy data generation completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()