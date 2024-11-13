from oauthenticator.generic import LocalGenericOAuthenticator
import os
import shutil

c.JupyterHub.authenticator_class = LocalGenericOAuthenticator
c.LocalGenericOAuthenticator.client_id = 'jhub'
c.LocalGenericOAuthenticator.token_url = 'https://kdp-ediaqi.know-center.at/keycloak/realms/master/protocol/openid-connect/token'
c.LocalGenericOAuthenticator.userdata_url = 'https://kdp-ediaqi.know-center.at/keycloak/realms/master/protocol/openid-connect/userinfo'
c.LocalGenericOAuthenticator.userdata_method = 'GET'
c.LocalGenericOAuthenticator.userdata_params = {"state": "state"}
c.LocalGenericOAuthenticator.username_key = "preferred_username"
c.LocalGenericOAuthenticator.tls_verify = True
c.LocalAuthenticator.create_system_users = True
c.LocalGenericOAuthenticator.auto_login = True
c.LocalGenericOAuthenticator.allow_all = True
c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner' #only for localhost
c.JupyterHub.cookie_max_age_days = 1
c.JupyterHub.tornado_settings = {'slow_spawn_timeout': 90}
c.Spawner.http_timeout = 90
c.Spawner.start_timeout = 90
c.LocalGenericOAuthenticator.admin_users = {'admin'}
c.LocalProcessSpawner.cpu_limit = 1  # Limit each user to 1 CPU core
c.LocalProcessSpawner.mem_limit = '2G'  # Limit each user to 2GB of memory


def copy_notebooks(spawner):
    """Copy example notebooks to the user's directory after spawn"""
    # Path to the notebook folder in the container
    source_dir = '/srv/notebooks'
    # Path to the user's home directory
    user_home_dir = os.path.expanduser(f"~{spawner.user.name}")
    target_dir = os.path.join(user_home_dir, 'notebooks')
    
    # Check if target directory exists, if not, copy the notebooks
    if not os.path.exists(target_dir):
        shutil.copytree(source_dir, target_dir)

# Attach the hook to the spawner
c.Spawner.pre_spawn_hook = copy_notebooks