import os

JAR_PATH_DIR = '$HOME/.vscode'
INSTALLED_VERSION = 'codeforiserver-1.0.0-alpha-4.jar'
INSTALLED = True

class ServerComponent(object):
    installed = INSTALLED
    
    @staticmethod
    def get_init_command() -> str:
        return f"java -jar {JAR_PATH_DIR}/{INSTALLED_VERSION} && exit"
        
    staticmethod
    def _get_component_path() -> str:
        # TODO: check installed version
        jar_name = ServerComponent._get_component_name()
        if ServerComponent.installed:
            return os.path.join(JAR_PATH_DIR, jar_name)
    
    @staticmethod
    def _get_component_name() -> str:
        return INSTALLED_VERSION
    
        
        
        