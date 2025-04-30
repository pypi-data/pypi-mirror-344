from pylintsql.utils.arg_utils import parse_arguments
from pylintsql import process_all_files_in_directory
from .utils.config_utils import get_sqlfluff_config, get_excluded_paths

def main():
    # Parse arguments using the existing parser logic
    args = parse_arguments()

    # Get the SQLFluff configuration
    config = get_sqlfluff_config(
        search_path=args.path,
        config_path=args.config
    )

    # Get the matcher for excluded paths - pass the config_path
    excluded_matcher = get_excluded_paths(args.path, args.config)

    # Process the directory
    process_all_files_in_directory(args.path, args.mode, config, excluded_matcher)

if __name__ == "__main__":
    main()