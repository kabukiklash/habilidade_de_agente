#!/usr/bin/env python3
"""
Initialize a monorepo structure for AI-assisted platform development.
Usage: python init_monorepo.py <project-name>
"""

import os
import sys
import json
from pathlib import Path

def create_monorepo(project_name):
    """Create monorepo structure for platform development."""
    
    base_path = Path.home() / project_name
    base_path.mkdir(parents=True, exist_ok=True)
    
    # Create directory structure
    dirs = [
        "packages/backend/src/{services,routes,types,config,lib,repositories,__tests__}",
        "packages/backend/prisma/migrations",
        "packages/frontend/src/{components,pages,hooks,lib,contexts}",
        "packages/frontend/public",
        ".github/workflows",
        "docs",
    ]
    
    for dir_path in dirs:
        full_path = base_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
    
    # Create root package.json
    root_package = {
        "name": project_name,
        "version": "1.0.0",
        "private": True,
        "description": f"AI-assisted platform: {project_name}",
        "workspaces": ["packages/backend", "packages/frontend"],
        "scripts": {
            "install-all": "pnpm install",
            "dev": "pnpm -r dev",
            "build": "pnpm -r build",
            "test": "pnpm -r test",
            "lint": "pnpm -r lint"
        }
    }
    
    with open(base_path / "package.json", "w") as f:
        json.dump(root_package, f, indent=2)
    
    # Create .gitignore
    gitignore_content = """
node_modules/
dist/
build/
.env
.env.local
.env.*.local
*.log
.DS_Store
.vscode/
.idea/
*.swp
*.swo
.git/
coverage/
.next/
out/
"""
    
    with open(base_path / ".gitignore", "w") as f:
        f.write(gitignore_content.strip())
    
    # Create README.md
    readme_content = f"""# {project_name}

AI-assisted platform development project.

## Structure

```
{project_name}/
├── packages/
│   ├── backend/    # Node.js + Express + TypeScript
│   └── frontend/   # React + Vite + TypeScript
├── docs/           # Documentation
└── .github/        # GitHub Actions
```

## Quick Start

```bash
pnpm install-all
pnpm dev
```

## Documentation

See `/docs` for detailed documentation.
"""
    
    with open(base_path / "README.md", "w") as f:
        f.write(readme_content)
    
    print(f"✅ Monorepo '{project_name}' created at {base_path}")
    print(f"   - Backend: {base_path}/packages/backend")
    print(f"   - Frontend: {base_path}/packages/frontend")
    print(f"   - Docs: {base_path}/docs")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python init_monorepo.py <project-name>")
        sys.exit(1)
    
    project_name = sys.argv[1]
    create_monorepo(project_name)
