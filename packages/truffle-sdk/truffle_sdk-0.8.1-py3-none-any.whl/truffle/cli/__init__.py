"""CLI package initialization"""

from .commands.init import InitCommand
from .commands.build import BuildCommand
from .commands.upload import UploadCommand
from ..utils.logger import log
import sys
import difflib

def main():
    """CLI entry point"""
    try:
        # Show help for help or no args
        if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
            from ..utils.help import HelpMenu
            HelpMenu(show_banner=True).show_help()
            sys.exit(0)
            
        # Initialize commands
        init_cmd = InitCommand()
        build_cmd = BuildCommand()
        upload_cmd = UploadCommand()
        
        # Parse command
        command = sys.argv[1]
        
        # Execute command
        if command == "init":            
            # Execute init command with all arguments
            init_cmd.execute()     
        elif command == "build":
            build_cmd.execute(sys.argv[2] if len(sys.argv) > 2 else None)
        elif command == "upload":
            upload_cmd.execute(sys.argv[2] if len(sys.argv) > 2 else None)
        else:
            # 'cutoff` sets the minimum similarity ratio
            close_match = difflib.get_close_matches(command, ["init", "build", "upload"], n=1, cutoff=0.6)

            # If there is a close match then the user probably made a typo, no need to show the help menu
            if close_match:
                log.error(f"'{command}' is not a truffle command. See 'truffle --help'")
                log.detail(f"The most similar command is '{close_match[0]}'")
            else:
                # Show help for unknown command without printing banner again
                from ..utils.help import HelpMenu
                HelpMenu(show_banner=True).show_help()
                print()
                log.error(f"'{command}' is not a truffle command")

            sys.exit(1)
            
    except KeyboardInterrupt:
        log.warning("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        log.error("Unexpected error")
        log.detail(str(e))
        sys.exit(1) 

