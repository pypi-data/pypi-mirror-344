import questionary
from git import Repo
import os
import shutil
import subprocess
from project_initializer.utils import log, RequiredValidator, edit_line_containing, success, error

def get_packages(selected_features: list[str]) -> str:
    """
    Get the list of packages to be installed based on the selected features.
    """
    # Default packages
    python_packages = [
        "djangorestframework",
        "django",
        "django-cors-headers",
        "python-dotenv",
    ]
    react_packages = [
        "react-router",
        "axios",
        "tailwindcss",
        "@tailwindcss/vite",
    ]
    # Adding packages based on selected features
    for feature in selected_features:
        match feature:
            case "Authentication":
                python_packages.append("djangorestframework_simplejwt")
                react_packages.append("zustand")
            
    return " ".join(python_packages), " ".join(react_packages)

def init_project(project_name: str, selected_features: list[str]):
    """
    Initialize the project with packages for selected features.
    """
    log("Initializing the project...")
    python_str_packages, react_str_packages = get_packages(selected_features)
    # Django project initialization
    os.makedirs(f"{project_name}/backend")
    subprocess.run(
        f"\
        python -m venv .venv\
        && source .venv/bin/activate\
        && pip install --upgrade pip\
        && pip install {python_str_packages}\
        && pip freeze > requirements.txt\
        && django-admin startproject {project_name} .\
        ",
        shell=True,
        cwd=f"{project_name}/backend"
    )
    shutil.move("template_repo/backend/utils", f"{project_name}/backend/utils")
    shutil.move("template_repo/backend/.gitignore", f"{project_name}/backend/.gitignore")
    os.remove(f"{project_name}/backend/{project_name}/settings.py")
    os.mkdir(f"{project_name}/backend/{project_name}/settings")
    shutil.move("template_repo/backend/backend/settings/__init__.py", f"{project_name}/backend/{project_name}/settings/__init__.py")
    shutil.move("template_repo/backend/backend/settings/base.py", f"{project_name}/backend/{project_name}/settings/base.py")
    with open(f"{project_name}/backend/.env", "w") as file:
       pass
    with open(f"{project_name}/backend/{project_name}/settings/settings.py", "w") as file:
        file.write("from .base import *\n")
    edit_line_containing(
        f"{project_name}/backend/{project_name}/asgi.py",
        [f"os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"{project_name}.settings\")"],
        [f"os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"{project_name}.settings.settings\")\n"]
    )
    edit_line_containing(
        f"{project_name}/backend/{project_name}/wsgi.py",
        [f"os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"{project_name}.settings\")"],
        [f"os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"{project_name}.settings.settings\")\n"]
    )
    edit_line_containing(
        f"{project_name}/backend/manage.py",
        [f"os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"{project_name}.settings\")"],
        [f"    os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"{project_name}.settings.settings\")\n"]
    )
    edit_line_containing(
        f"{project_name}/backend/{project_name}/urls.py",
        ["from django.urls import path"],
        ["from django.urls import path, include\n"]
    )
   
    # React project initialization
    os.makedirs(f"{project_name}/frontend")
    subprocess.run(f"\
        yarn create vite . --template react-swc-ts\
        && yarn add {react_str_packages}\
        ",
        shell=True,
        cwd=f"{project_name}/frontend"
    )
    shutil.move("template_repo/frontend/vite.config.ts", f"{project_name}/frontend/vite.config.ts")
    shutil.move("template_repo/frontend/.gitignore", f"{project_name}/frontend/.gitignore")
    shutil.move("template_repo/frontend/.env", f"{project_name}/frontend/.env")
    shutil.move("template_repo/frontend/src/index.css", f"{project_name}/frontend/src/index.css")
    shutil.move("template_repo/frontend/src/main.tsx", f"{project_name}/frontend/src/main.tsx")
    shutil.move("template_repo/frontend/src/PATHS.tsx", f"{project_name}/frontend/src/PATHS.tsx")
    os.mkdir(f"{project_name}/frontend/src/components")
    os.mkdir(f"{project_name}/frontend/src/features")
    os.mkdir(f"{project_name}/frontend/src/hooks")
    shutil.move("template_repo/frontend/src/hooks/useAxios.tsx", f"{project_name}/frontend/src/hooks/useAxios.tsx")
    os.mkdir(f"{project_name}/frontend/src/pages")
    os.mkdir(f"{project_name}/frontend/src/services")
    shutil.move("template_repo/frontend/src/services/backend.tsx", f"{project_name}/frontend/src/services/backend.tsx")
    os.mkdir(f"{project_name}/frontend/src/stores")
    os.mkdir(f"{project_name}/frontend/src/types")
    os.mkdir(f"{project_name}/frontend/src/layouts")
    os.remove(f"{project_name}/frontend/src/assets/react.svg")
    os.remove(f"{project_name}/frontend/src/App.css")

    success("Project initialized successfully.")
    
def add_features(project_name: str, selected_features: list[str]):
    """
    Add files based on selected features.
    """
    SRC_BACKEND_DIR = "template_repo/backend"
    DST_BACKEND_DIR = f"{project_name}/backend"
    SRC_FRONTEND_DIR = "template_repo/frontend/src"
    DST_FRONTEND_DIR = f"{project_name}/frontend/src"

    for feature in FEATURES:
        # Adding files based on selected features
        if feature in selected_features:
            log(f"Adding {feature} feature...")
            match feature:
                case "Authentication":
                    # Backend
                    shutil.move(f"{SRC_BACKEND_DIR}/auth", f"{DST_BACKEND_DIR}/auth")
                    shutil.move(f"{SRC_BACKEND_DIR}/backend/settings/auth.py", f"{DST_BACKEND_DIR}/{project_name}/settings/auth.py")
                    with open(f"{DST_BACKEND_DIR}/{project_name}/settings/settings.py", "a") as file:
                        file.write("from .auth import *\n")
                    edit_line_containing(
                        f"{project_name}/backend/{project_name}/urls.py",
                        ["]"],
                        ["    path(\"auth/\", include(\"auth.urls\")),\n]"]
                    )
                    # Frontend
                    shutil.move(f"{SRC_FRONTEND_DIR}/components/Logout.tsx", f"{DST_FRONTEND_DIR}/components/Logout.tsx")
                    shutil.move(f"{SRC_FRONTEND_DIR}/components/ProtectedRoute.tsx", f"{DST_FRONTEND_DIR}/components/ProtectedRoute.tsx")
                    shutil.move(f"{SRC_FRONTEND_DIR}/features/auth", f"{DST_FRONTEND_DIR}/features/auth")
                    shutil.move(f"{SRC_FRONTEND_DIR}/pages/Home.tsx", f"{DST_FRONTEND_DIR}/pages/Home.tsx")
                    shutil.move(f"{SRC_FRONTEND_DIR}/pages/Login.tsx", f"{DST_FRONTEND_DIR}/pages/Login.tsx")
                    shutil.move(f"{SRC_FRONTEND_DIR}/stores/useUserStore.tsx", f"{DST_FRONTEND_DIR}/stores/useUserStore.tsx")
                    shutil.move(f"{SRC_FRONTEND_DIR}/types/User.tsx", f"{DST_FRONTEND_DIR}/types/User.tsx")
                    shutil.move(f"{SRC_FRONTEND_DIR}/App.tsx", f"{DST_FRONTEND_DIR}/App.tsx")
                case "API":
                    # Backend
                    shutil.move(f"{SRC_BACKEND_DIR}/api", f"{DST_BACKEND_DIR}/api")
                    shutil.move(f"{SRC_BACKEND_DIR}/backend/settings/api.py", f"{DST_BACKEND_DIR}/{project_name}/settings/api.py")
                    with open(f"{DST_BACKEND_DIR}/{project_name}/settings/settings.py", "a") as file:
                        file.write("from .api import *\n")
                    edit_line_containing(
                        f"{project_name}/backend/{project_name}/urls.py",
                        ["]"],
                        ["    path(\"api/\", include(\"api.urls\")),\n]"]
                    )
            success(f"{feature} feature added successfully.")

                    

def main():
    global FEATURES
    FEATURES = [
        "Authentication", 
        "API",
    ]

    answers = questionary.form(
        project_name = questionary.text("What is the name of your project?", validate=RequiredValidator),
        features = questionary.checkbox("Select the features you want to include in your project:", choices=FEATURES)
    ).ask()

    project_name = answers['project_name']
    selected_features = answers['features']

    try:
        log("Cloning the repository...")
        Repo.clone_from("https://github.com/Soulflys02/web-dev-framework.git", "template_repo")
        success("Repository cloned successfully.")
        init_project(project_name, selected_features)
        add_features(project_name, selected_features)
        shutil.rmtree("template_repo")
        success("Project setup completed successfully.")
    except Exception as e:
        error(e)
    
if __name__ == "__main__":
    main()