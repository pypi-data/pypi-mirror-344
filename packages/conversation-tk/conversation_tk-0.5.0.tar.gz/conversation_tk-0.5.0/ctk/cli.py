"""
@file cli.py
@brief ctk command-line tool for managing and analyzing chat logs.

This script provides subcommands to import, list, merge, run jmespath queries, etc.
"""

import argparse
import json
import os
import sys
import AlgoTree
from rich.console import Console
from rich.json import JSON
from importlib.metadata import version
import webbrowser
import logging
import zipfile
from .utils import (load_conversations, save_conversations, pretty_print_conversation,
                    query_conversations_search, query_conversations_jmespath, path_value,
                    list_conversations, ensure_libdir_structure, print_json_as_table,
                    generate_unique_filename)
from .merge import union_libs, intersect_libs, diff_libs

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

console = Console()

################################################################################
# COMMAND-LINE INTERFACE (argparse)
################################################################################

def main():
    """
    @brief Main entry point for the ctk CLI.
    @return None
    """
    parser = argparse.ArgumentParser(
        description="ctk: A command-line tool for chat log management and analysis."
    )
    parser.add_argument("--version", action="version",
                        version=version("conversation-tk"))

    subparsers = parser.add_subparsers(
        dest="command", help="Subcommand to run")

    # Subcommand: search
    regex_parser = subparsers.add_parser(
        "search", help="Run a search using regex against the ctk lib on the specified fields")
    regex_parser.add_argument(
        "libdir", help="Path to the conversation library directory")
    regex_parser.add_argument("expression", help="Regex expression")
    regex_parser.add_argument(
        "--fields", nargs="+", help="Field paths to apply the regex", default=["title"])
    regex_parser.add_argument(
        "--json", action="store_true", help="Output as JSON. Default: False")
    regex_parser.add_argument(
        "--no-payload", action="store_true", help="Do not show payload in the output. Default: False")

    # Subcommand: conv-stats
    tree_parser = subparsers.add_parser(
        "conv-stats", help="Compute conversation tree statistics")
    tree_parser.add_argument(
        "libdir", help="Path to the conversation library directory")
    tree_parser.add_argument(
        "index", type=int, help="Index of conversation tree")
    tree_parser.add_argument(
        "--json", action="store_true", help="Output as JSON. Default: False")
    tree_parser.add_argument("--no-payload", action="store_true",
                             help="Do not show payload in the output. Default: False")

    # Subcommand: tree
    tree_parser = subparsers.add_parser(
        "tree", help="Conversation tree visualization")
    tree_parser.add_argument(
        "libdir", help="Path to the conversation library directory")
    tree_parser.add_argument(
        "index", type=int, help="Index of conversation tree to visualize")
    tree_parser.add_argument("--label-fields", nargs="+",
                             type=str, default=['id', 'message.content.parts'],
                             help="When showing the tree, use this field as the node's label")
    tree_parser.add_argument("--label-lambda", type=str, default=None,
                             help="Lambda function to apply to a node to determine its label")

    tree_parser.add_argument(
        "--truncate", type=int, default=8, help="Truncate each field to this length. Default: 8")

    # Subcommand: conv
    conv_parser = subparsers.add_parser(
        "conv", help="Print conversation based on a particular node id. Defaults to using `current_node` for the corresponding conversation tree.")
    conv_parser.add_argument(
        "libdir", help="Path to the conversation library directory")
    conv_parser.add_argument(
        "indices", nargs="+", type=int, help="Indices of conversations to print")
    conv_parser.add_argument(
        "--node", default=None, help="Node id that indicates the terminal node of a conversation path")
    conv_parser.add_argument(
        "--json", action="store_true", help="Output as JSON")
    conv_parser.add_argument("--msg-limit", type=int, default=1000,
                             help="Limit the number of messages to display. Default: 1000")
    conv_parser.add_argument("--msg-roles", type=str, nargs="+", default=[
                             "user", "assistant"], help="Roles to include in message output")
    conv_parser.add_argument("--msg-start-index", type=int, default=0,
                             help="Start index for messages to display. Default: 0")
    conv_parser.add_argument("--msg-end-index", type=int, default=-1,
                             help="End index for messages to display. Default: -1 (end of list). Use negative values to count from the end.")

    # Subcommand: remove
    remove_parser = subparsers.add_parser(
        "remove", help="Remove a conversation from the ctk lib")
    remove_parser.add_argument(
        "libdir", help="Path to the conversation library directory")
    remove_parser.add_argument(
        "indices", type=int, nargs="+", help="Indices of conversations to remove")

    # Subcommand: share
    export_parser = subparsers.add_parser(
        "export", help="Export a conversation from the ctk lib")
    export_parser.add_argument(
        "libdir", help="Path to the conversation library directory")
    export_parser.add_argument("--indices", type=int, nargs="+", default=None,
                               help="Indices of conversations to export. Default: all")
    export_parser.add_argument(
        "--format", choices=["json", "markdown", "hugo", "zip"], default="json", help="Output format")

    # Subcommand: list
    list_parser = subparsers.add_parser(
        "list", help="List conversations in the ctk lib")
    list_parser.add_argument("libdir", help="Path to the ctk library")
    list_parser.add_argument("--indices", nargs="+", default=None,
                             type=int, help="Indices of conversations to list. Default: all")
    list_parser.add_argument("--fields", nargs="+", default=[
                             "title", "create_time"], help="Path fields to include in the output")

    # Subcommand: merge (union, intersection, difference)
    merge_parser = subparsers.add_parser(
        "merge", help="Merge multiple ctk libs into one")
    merge_parser.add_argument("operation", choices=["union", "intersection", "difference"],
                              help="Type of merge operation")
    merge_parser.add_argument("libdirs", nargs="+",
                              help="List of library directories")
    merge_parser.add_argument(
        "-o", "--output", required=True, help="Output library directory")

    # Subcommand: jmespath
    jmespath_parser = subparsers.add_parser(
        "jmespath", help="Run a JMESPath query on the ctk lib")
    jmespath_parser.add_argument(
        "libdir", help="Path to the conversation library directory")
    jmespath_parser.add_argument("query", help="JMESPath expression")

    # Subcommand: purge
    purge_parser = subparsers.add_parser(
        'purge', help='Purge dead links from the conversation library')
    purge_parser.add_argument(
        'libdir', type=str, help='Directory of the ctk library to purge')

    # Subcommand: web
    web_parser = subparsers.add_parser(
        'web', help='View a conversation in the OpenAI chat interface')
    web_parser.add_argument(
        'libdir', type=str, help='Directory of the ctk library to visit')
    web_parser.add_argument('index', type=int, nargs='+',
                            help='Indices of the conversations to view in the browser')

    # Subcommand: about
    about_parser = subparsers.add_parser(
        'about', help='Print information about ctk')

    args = parser.parse_args()

    if args.command == "list":
        list_conversations(args.libdir, args.fields, args.indices)

    elif args.command == "search":
        results = query_conversations_search(
            args.libdir, args.expression, args.fields)
        if args.json:
            # pretty JSON
            console.print(JSON(json.dumps(results, indent=2)))
        else:
            if args.no_payload:
                for i, conv in results:
                    console.print(f"[bold]Conversation {i}[/bold]: {conv['title']}")
            else:
                for i, conv in results:
                    # print a header that tells us the index
                    console.print(f"[bold]Conversation {i}[/bold]: {conv['title']}")
                    pretty_print_conversation(conv)

    elif args.command == "remove":
        convs = load_conversations(args.libdir)
        for index in sorted(args.indices, reverse=True):
            del convs[index]
        save_conversations(args.libdir, convs)
        logger.debug(f"Removed {len(args.indices)} conversations")

    elif args.command == "export":
        convs = load_conversations(args.libdir)
        if args.indices is None:
            indices = range(len(convs))
        else:
            indices = args.indices
        convs = [convs[i] for i in indices if i < len(convs) and i >= 0]

        if args.format == "zip":
            zipfile_name = generate_unique_filename(args.libdir + ".zip") 
            with zipfile.ZipFile(zipfile_name, "w") as zf:
                zf.writestr("conversations.json",
                            json.dumps(convs, indent=2))
                # now we copy the directory of the libdir, which contains the conversations.json, with the exception of copying the conversations.json file
                for root, dirs, files in os.walk(args.libdir):
                    for file in files:
                        if file == "conversations.json":
                            continue
                        # write the file to the zip file in the zip file, replicating the same structure
                        arcname = os.path.relpath(
                            os.path.join(root, file), start=args.libdir)
                        zf.write(os.path.join(root, file), arcname=arcname)

        elif args.format == "json":
            print(json.dumps(convs, indent=2))

    elif args.command == "jmespath":
        result = query_conversations_jmespath(args.libdir, args.query)
        # pretty print
        console.print(JSON(json.dumps(result, indent=2)))

    elif args.command == "conv-stats":
        convs = load_conversations(args.libdir)
        if args.index >= len(convs):
            console.debug(f"[red]Error: Index {index} out of range.[/red]")
        conv = convs[args.index]

        cur_node_name = conv.get("current_node")

        tree_map = conv.get("mapping")
        t = AlgoTree.FlatForest(tree_map)
        cur_node = t.node(cur_node_name)
        ancestors = AlgoTree.utils.ancestors(cur_node)
        cur_conv_ids = [node.name for node in ancestors] + [cur_node_name]

        stats = {}
        metadata = conv
        metadata.pop("mapping", None)

        stats['metadata'] = metadata
        stats["num_paths"] = len(AlgoTree.utils.leaves(t.root))
        stats["num_nodes"] = AlgoTree.utils.size(t.root)
        stats["max_path"] = AlgoTree.utils.height(t.root)

        def walk(node, the_id, the_parent_id):
            node_dict = {}
            node_dict["siblings"] = [
                node.name for node in AlgoTree.utils.siblings(node)]
            node_dict["children"] = [child.name for child in node.children]
            node_dict["is_leaf"] = AlgoTree.utils.is_leaf(node)
            node_dict["is_root"] = AlgoTree.utils.is_root(node)
            node_dict["is_current"] = node.name in cur_conv_ids
            node_dict["num_children"] = len(node.children)
            node_dict['num_siblings'] = len(node_dict['siblings'])
            node_dict["depth"] = AlgoTree.utils.depth(node)
            node_dict["num_descendants"] = AlgoTree.utils.size(node)
            node_dict["num_ancestors"] = len(AlgoTree.utils.ancestors(node))
            node_dict["parent_id"] = node.parent.name if node.parent else None
            if not args.no_payload:
                node_dict['payload'] = node.payload

            stats[(the_id, the_parent_id)] = node_dict

            the_parent_id = the_id
            the_id = the_id + 1
            for child in node.children:
                walk(child, the_id, the_parent_id)
                the_id += 1

        walk(t.root, 0, None)
        if args.json:
            console.print(JSON(json.dumps(stats, indent=2)))
        else:
            print_json_as_table(stats, table_title=conv['title'])

    elif args.command == "tree":
        convs = load_conversations(args.libdir)
        if args.index >= len(convs):
            console.debug(f"[red]Error: Index {index} out of range.[/red]")
            sys.exit(1)
        conv = convs[args.index]
        tree_map = conv.get("mapping", {})
        t = AlgoTree.FlatForest(tree_map)

        def generate_label_fn():
            paths = []
            for field in args.label_fields:
                paths.append(field.split('.'))

            def label_fn(node):
                results = []
                for path in paths:
                    value = path_value(node.payload, path)
                    value = value[:args.truncate]
                    results.append(value)

                label = " ".join(results)
                return label

            return label_fn

        if args.label_lambda is None:
            label_fn = generate_label_fn()
            console.print(AlgoTree.pretty_tree(t, node_name=label_fn))
        else:
            label_fn = eval(args.label_lambda)
            label_fallback_fn = generate_label_fn()

            def wrapper_lambda(node):
                try:
                    return label_fn(node)
                except Exception as e:
                    print("Error in label_fn:", e)
                    return label_fallback_fn(node)

            # label_fn should be a function that takes a conversation node and returns a string
            console.print(AlgoTree.pretty_tree(t, node_name=wrapper_lambda))
    elif args.command == "purge":
        print("TODO: Implement purge command. This swill remove any local files that are dead links in the library.")

    elif args.command == "chat":
        chat_llm(args.libdir)

    elif args.command == "conv":

        if args.node is not None and len(args.indices) > 1:
            console.print(
                "[red]Error: If you specify a node, you can only print one conversation at a time.[/red]")
            sys.exit(1)

        convs = load_conversations(args.libdir)
        json_obj = []

        for idx in args.indices:
            if idx >= len(convs):
                console.debug(
                    f"[red]Error: Index {idx} in indices out of range.[/red]. Skipping.")
                continue

            if args.json:
                json_obj.append(convs[idx])
            else:
                pretty_print_conversation(
                    convs[idx],
                    terminal_node=args.node,
                    msg_limit=args.msg_limit,
                    msg_roles=args.msg_roles,
                    msg_start_index=args.msg_start_index,
                    msg_end_index=args.msg_end_index)

        if args.json:
            console.print(JSON(json.dumps(json_obj, indent=2)))

    elif args.command == "about":
        console.print("[bold cyan]ctk[/bold cyan]: A command-line toolkit for working with conversation trees, "
                      "typically derived from exported LLM interaction data.\n")
        console.print("[dim]Developed by:[/dim] [bold white]Alex Towell[/bold white]  \n"
                      "[dim]Contact:[/dim] [link=mailto:lex@metafunctor.com]lex@metafunctor.com[/link]  \n"
                      "[dim]Source Code:[/dim] [link=https://github.com/queelius/ctk]https://github.com/queelius/ctk[/link]\n")
        console.print("[bold]Features:[/bold]")
        console.print("• Parse and analyze ChatGPT-like conversation trees.")
        console.print(
            "• Export, transform, and query structured conversation data.")
        console.print("• Visualize conversation trees and relationships.")
        console.print("• Query conversation trees using JMESPath.")
        console.print(
            "• Lightweight and designed for command-line efficiency.")
        console.print(
            "\n[bold green]Usage:[/bold green] Run `ctk --help` for available commands.")

    elif args.command == "web":
        convs = load_conversations(args.libdir)
        for idx in args.index:
            if idx < 0 or idx >= len(convs):
                console.debug(
                    f"[red]Error: Index {idx} out of range.[/red]. Skipping.")
                continue

            conv = convs[idx]
            link = f"https://chat.openai.com/c/{conv['id']}"
            webbrowser.open_new_tab(link)

    elif args.command == "merge":
        ensure_libdir_structure(args.output)
        if args.operation == "union":
            union_libs(args.libdirs, args.output)
            logger.debug(f"Merged {len(args.libdirs)} libs into {args.output}")
        elif args.operation == "intersection":
            intersect_libs(args.libdirs, args.output)
            logger.debug(f"Merged {len(args.libdirs)} libs into {args.output}")
        elif args.operation == "difference":
            diff_libs(args.libdirs, args.output)
            logger.debug(f"Merged {len(args.libdirs)} libs into {args.output}")
        logger.debug(f"Merged {len(args.libdirs)} libs into {args.output}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
