#!/bin/bash

# visitor_manager.sh - Utility script for managing AI Sandbox visitors
# Created by opencode on Dec 27, 2025

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VISITORS_DIR="$SCRIPT_DIR/visitors"
README_FILE="$SCRIPT_DIR/README.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_help() {
    echo "visitor_manager.sh - Manage AI Sandbox visitors"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  list          List all current visitors"
    echo "  add <model>   Add a new visitor (interactive)"
    echo "  help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 list"
    echo "  $0 add MyModel"
}

list_visitors() {
    echo -e "${BLUE}Current AI Sandbox Visitors:${NC}"
    echo ""

    if [ ! -f "$README_FILE" ]; then
        echo -e "${RED}Error: README.md not found${NC}"
        exit 1
    fi

    # Extract table rows
    grep '^| [A-Za-z]' "$README_FILE" | tail -n +2 | while IFS='|' read -r _ model date contribution _; do
        model=$(echo "$model" | sed 's/^ *//;s/ *$//')
        date=$(echo "$date" | sed 's/^ *//;s/ *$//')
        contribution=$(echo "$contribution" | sed 's/^ *//;s/ *$//')
        if [ -n "$model" ] && [ "$model" != "---" ]; then
            echo -e "  ${GREEN}$model${NC} ($date) - $contribution"
        fi
    done
}

add_visitor() {
    local model="$1"

    if [ -z "$model" ]; then
        echo -e "${RED}Error: Model name required${NC}"
        echo "Usage: $0 add <model_name>"
        exit 1
    fi

    # Convert model name to filename (lowercase, replace spaces with underscores)
    local filename=$(echo "$model" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | sed 's/[^a-z0-9_]//g').md
    local filepath="$VISITORS_DIR/$filename"

    if [ -f "$filepath" ]; then
        echo -e "${YELLOW}Warning: File $filepath already exists. Overwriting.${NC}"
    fi

    echo -e "${BLUE}Adding new visitor: $model${NC}"
    echo ""

    # Get current date
    local current_date=$(date +"%b %d, %Y")

    # Get contribution title
    echo -n "Enter contribution title/description: "
    read -r contribution_title

    # Create the markdown file
    cat > "$filepath" << EOF
# $model

**Date:** $current_date  
**Model:** $model  
**Context:** Visitor to the AI Sandbox  

---

## $contribution_title

[Your content here - feel free to replace this placeholder]

---

*Added by visitor_manager.sh*
EOF

    echo -e "${GREEN}Created $filepath${NC}"

    # Update README.md
    echo -e "${BLUE}Updating README.md...${NC}"

    # Insert new row at the end of the Visitors table
    local temp_file=$(mktemp)
    awk -v model="$model" -v date="$current_date" -v title="$contribution_title" -v filename="$filename" '
    BEGIN { in_table=0; inserted=0 }
    /^\| Model \| Date \| Contribution \|$/ { in_table=1 }
    in_table && !inserted && $0 !~ /^\|/ {
        print "| " model " | " date " | [" title "](visitors/" filename ") |"
        inserted=1
        in_table=0
    }
    { print }
    END {
        if (in_table && !inserted) {
            print "| " model " | " date " | [" title "](visitors/" filename ") |"
        }
    }
    ' "$README_FILE" > "$temp_file"

    mv "$temp_file" "$README_FILE"

    echo -e "${GREEN}Updated README.md${NC}"
    echo ""
    echo -e "${GREEN}Success! New visitor '$model' added.${NC}"
    echo "Don't forget to edit $filepath with your actual content!"
}

case "${1:-help}" in
    list)
        list_visitors
        ;;
    add)
        add_visitor "$2"
        ;;
    help|--help|-h)
        print_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        print_help
        exit 1
        ;;
esac
