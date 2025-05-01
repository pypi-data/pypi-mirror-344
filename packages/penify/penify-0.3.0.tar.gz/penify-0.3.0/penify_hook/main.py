import argparse
import sys
import time


def main():
    """Main function to handle command-line interface (CLI) interactions with
    Penify services.

    This tool provides a command-line interface for generating smart commit
    messages, configuring local-LLM and JIRA, and generating code
    documentation. It supports basic commands that do not require login and
    advanced commands that require user authentication. The `--version` flag
    can be used to display the version information.

    Returns:
        int: Exit status of the program (0 for success, 1 for error).
    """

    parser = argparse.ArgumentParser(
        description="""Penify CLI tool for:
1. AI commit message generation with JIRA integration to enhance commit messages.
2. Generating Code Documentation, it requires SignUp to Penify
3. For more information, visit https://penify.wiki/dpc1""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Add version flag
    parser.add_argument('--version', '-v', action='store_true', help='Show version information')

    subparsers = parser.add_subparsers(title="options", dest="subcommands")

    # Group commands logically
    basic_title = "Basic Commands (No login required)"
    advanced_title = "Advanced Commands (Login required)"

    # Create grouped subparsers (visually separated in help output)
    parser.add_argument_group(basic_title)
    parser.add_argument_group(advanced_title)
    
    # Set up subparsers with proper imports upfront
    commit_parser = subparsers.add_parser("commit", help="Generate smart commit messages using local-LLM(no login required).")
    from .commands.commit_commands import setup_commit_parser
    setup_commit_parser(commit_parser)
    
    config_parser = subparsers.add_parser("config", help="Configure local-LLM and JIRA.")
    from .config_command import setup_config_parser
    setup_config_parser(config_parser)
    
    login_parser = subparsers.add_parser("login", help="Log in to Penify to use advanced features like 'docgen' generation.")
    from .login_command import setup_login_parser
    setup_login_parser(login_parser)
    
    docgen_parser = subparsers.add_parser("docgen", help="[REQUIRES LOGIN] Generate code documentation for the Git diff, file or folder.")
    from .commands.doc_commands import setup_docgen_parser
    setup_docgen_parser(docgen_parser)
    
    # Parse args without validation first to check for simple flags like --version
    if '--version' in sys.argv or '-v' in sys.argv:
        from importlib.metadata import version
        try:
            print(f"penify version {version('penify')}")
        except:
            print("penify version 0.2.2")
        return 0
    
    # Parse the arguments to determine which command was requested
    args = parser.parse_args()    
    # Handle the commands
    if args.subcommands == "commit":
        from penify_hook.ui_utils import print_info
        print_info("Please wait while we generate the commit message...")
        from .commands.commit_commands import handle_commit
        return handle_commit(args)
    elif args.subcommands == "config":
        from .config_command import handle_config
        return handle_config(args)
    elif args.subcommands == "login":
        from .login_command import handle_login
        return handle_login(args)
    elif args.subcommands == "docgen":
        from .commands.doc_commands import handle_docgen
        return handle_docgen(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
