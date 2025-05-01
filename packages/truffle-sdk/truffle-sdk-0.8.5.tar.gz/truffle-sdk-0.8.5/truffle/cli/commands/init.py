"""Initialize new Truffle projects"""

from pathlib import Path
from typing import Optional
from ...utils.logger import log, Colors
from ...utils import argparse
from ...utils.banner import get_truffle_banner
from ..project.finder import ProjectFinder
from ..project.creator import ProjectCreator
import sys

class InitCommand:
    """Handles 'truffle init' command"""
    
    def __init__(self):
        self.finder = ProjectFinder()
        self.creator = ProjectCreator()
        
    def execute(self, name: Optional[str] = None, path: Optional[str] = None, description: Optional[str] = None) -> None:
        """Execute init command non-interactively.
        
        Flags -n, -d, -p are captured and passed as potential overrides or targets 
        to the ProjectCreator.
        """
        try:
            # Parse command line arguments
            # Note: The function signature args (name, path, description) are likely unused now
            #       if this command is only ever called via CLI entrypoint.
            #       Keeping them for now preserves the signature but they could be removed
            #       if programmatic calls are not intended.
            parser = argparse.TruffleArgumentParser(description='Initialize a new Truffle project structure.')
            parser.add_argument('-n', '--name', help='Override the inferred app name.')
            parser.add_argument('-p', '--path', help='Path where to create the project structure (defaults to current directory).')
            parser.add_argument('-d', '--description', help='Override the description from the @truffle.app decorator.')
            
            # Get the args after 'init' command
            cli_args = sys.argv[2:] if len(sys.argv) > 2 else []
            parsed_args = parser.parse_args(cli_args)
            
            # Store flag values directly
            name_override = parsed_args.name
            path_flag_value = parsed_args.path # Path from -p flag, if provided
            description_override = parsed_args.description
            
            # --- Determine proposed project path --- 
            if path_flag_value:
                proposed_path = Path(path_flag_value)
            elif name_override:
                # Path not given, but name override is -> propose subdir with that name in CWD
                proposed_path = Path.cwd() / name_override
            else:
                # Neither path nor name override given -> propose default subdir in CWD
                DEFAULT_PROJECT_DIR_NAME = "TruffleApp" # Define the default name
                proposed_path = Path.cwd() / DEFAULT_PROJECT_DIR_NAME

            # --- Confirm path with user --- 
            log.detail(f"\nProject will be created at: {proposed_path.resolve()}")
            log.prompt("Press Enter to confirm, or enter a different path", end="")
            try:
                custom_path_str = input().strip()
                final_path_str = custom_path_str if custom_path_str else str(proposed_path)
            except KeyboardInterrupt:
                print() # Ensure error appears on new line
                raise # Re-raise to be caught by outer handler

            # No more interactive prompts for name or description.

            # Create project structure and store overrides
            # ProjectCreator now receives the final, confirmed path.
            project_path = self.creator.create(
                path=final_path_str, # Pass the final, confirmed path string
                name_override=name_override, 
                description_override=description_override
            )
            
            # Restore simpler success message
            log.success("App initialized successfully")
            # Provide guidance only if the created path is not the current directory
            if project_path.resolve() != Path.cwd().resolve():
                 try:
                     # Try to show relative path
                     relative_path = project_path.relative_to(Path.cwd())
                     log.detail(f"Run \'cd {relative_path}\' to start working")
                 except ValueError:
                     # Fallback to absolute path if not relative
                     log.detail(f"Project created at {project_path}. Run \'cd {project_path}\' to start working.")
            log.detail("Run 'truffle build' when ready to build your app")

            # Removed the more verbose logging about main.py and @truffle.app
            sys.exit(0)

        except KeyboardInterrupt:
            log.warning("Initialization cancelled by user")
            sys.exit(1)
        except FileNotFoundError as e:
            log.error("Initialization failed")
            log.detail(str(e))
            sys.exit(1)
        except Exception as e:
            log.error("Initialization failed")
            log.detail(str(e))
            sys.exit(1) 