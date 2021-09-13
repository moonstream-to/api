"""
Collect secrets from AWS SSM Parameter Store and output as environment variable exports.
"""
import argparse
from dataclasses import dataclass
import sys
from typing import Any, Dict, Iterable, List, Optional

import boto3


@dataclass
class EnvironmentVariable:
    name: str
    value: str


def get_parameters(path: str) -> List[Dict[str, Any]]:
    """
    Retrieve parameters from AWS SSM Parameter Store. Decrypts any encrypted parameters.

    Relies on the appropriate environment variables to authenticate against AWS:
    https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html
    """
    ssm = boto3.client("ssm")
    next_token: Optional[bool] = True
    parameters: List[Dict[str, Any]] = []
    while next_token is not None:
        kwargs = {"Path": path, "Recursive": False, "WithDecryption": True}
        if next_token is not True:
            kwargs["NextToken"] = next_token
        response = ssm.get_parameters_by_path(**kwargs)
        new_parameters = response.get("Parameters", [])
        parameters.extend(new_parameters)
        next_token = response.get("NextToken")

    return parameters


def parameter_to_env(parameter_object: Dict[str, Any]) -> EnvironmentVariable:
    """
    Transforms parameters returned by the AWS SSM API into EnvironmentVariables.
    """
    parameter_path = parameter_object.get("Name")
    if parameter_path is None:
        raise ValueError('Did not find "Name" in parameter object')
    name = parameter_path.split("/")[-1].upper()

    value = parameter_object.get("Value")
    if value is None:
        raise ValueError('Did not find "Value" in parameter object')

    return EnvironmentVariable(name, value)


def env_string(env_vars: Iterable[EnvironmentVariable], with_export: bool) -> str:
    """
    Produces a string which, when executed in a shell, exports the desired environment variables as
    specified by env_vars.
    """
    prefix = "export " if with_export else ""
    return "\n".join([f'{prefix}{var.name}="{var.value}"' for var in env_vars])


def extract_handler(args: argparse.Namespace) -> None:
    """
    Save environment variables to file.
    """
    result = env_string(map(parameter_to_env, get_parameters(args.path)), args.export)
    with args.outfile as ofp:
        print(result, file=ofp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Materialize environment variables from AWS SSM Parameter Store"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Parameters commands")

    parser_extract = subcommands.add_parser(
        "extract", description="Parameters extract commands"
    )
    parser_extract.set_defaults(func=lambda _: parser_extract.print_help())
    parser_extract.add_argument(
        "-o", "--outfile", type=argparse.FileType("w"), default=sys.stdout
    )
    parser_extract.add_argument(
        "--export",
        action="store_true",
        help="Set to output environment strings with export statements",
    )
    parser_extract.add_argument(
        "-p",
        "--path",
        default=None,
        help="SSM path from which to pull environment variables (pull is NOT recursive)",
    )
    parser_extract.set_defaults(func=extract_handler)

    args = parser.parse_args()
    args.func(args)
