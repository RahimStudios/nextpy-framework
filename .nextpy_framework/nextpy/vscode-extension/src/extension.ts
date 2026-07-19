import * as vscode from 'vscode';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
    console.log('NextPy PSX extension is now active!');

    // Register commands
    const createComponentCommand = vscode.commands.registerCommand('nextpy-psx.createComponent', () => {
        createPSXComponent();
    });

    const createPageCommand = vscode.commands.registerCommand('nextpy-psx.createPage', () => {
        createPSXPage();
    });

    const togglePythonLogicCommand = vscode.commands.registerCommand('nextpy-psx.togglePythonLogic', () => {
        togglePythonLogicHighlighting();
    });

    const showDocumentationCommand = vscode.commands.registerCommand('nextpy-psx.showDocumentation', () => {
        showDocumentation();
    });

    context.subscriptions.push(
        createComponentCommand,
        createPageCommand,
        togglePythonLogicCommand,
        showDocumentationCommand
    );

    // Register completion provider
    const completionProvider = vscode.languages.registerCompletionItemProvider(
        { language: 'nextpy-psx' },
        new PSXCompletionProvider(),
        '<', '{', ' ', '\n'
    );

    context.subscriptions.push(completionProvider);

    // Register hover provider
    const hoverProvider = vscode.languages.registerHoverProvider(
        { language: 'nextpy-psx' },
        new PSXHoverProvider()
    );

    context.subscriptions.push(hoverProvider);

    // Show activation message
    vscode.window.showInformationMessage(
        'NextPy PSX extension activated! Use Ctrl+Shift+P to access PSX commands.'
    );
}

class PSXCompletionProvider implements vscode.CompletionItemProvider {
    provideCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken,
        context: vscode.CompletionContext
    ): vscode.CompletionItem[] {
        const items: vscode.CompletionItem[] = [];

        // PSX elements
        const psxElements = [
            'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'button', 'input', 'form', 'label', 'textarea', 'select',
            'ul', 'ol', 'li', 'a', 'img', 'br', 'hr',
            'section', 'article', 'header', 'footer', 'nav', 'aside',
            'table', 'thead', 'tbody', 'tr', 'th', 'td'
        ];

        psxElements.forEach(element => {
            const item = new vscode.CompletionItem(element, vscode.CompletionItemKind.Class);
            item.insertText = new vscode.SnippetString(`<${element}>$1</${element}>`);
            item.documentation = new vscode.MarkdownString(`PSX \`${element}\` element`);
            items.push(item);
        });

        // PSX logic blocks
        const logicBlocks = [
            { name: 'for', snippet: '{for $1 in $2:\n    $3\n}' },
            { name: 'if', snippet: '{if $1:\n    $2\n}' },
            { name: 'try', snippet: '{try:\n    $1\n}{except $2:\n    $3\n}' },
            { name: 'python', snippet: '{python:\n    $1\n}' }
        ];

        logicBlocks.forEach(block => {
            const item = new vscode.CompletionItem(block.name, vscode.CompletionItemKind.Snippet);
            item.insertText = new vscode.SnippetString(block.snippet);
            item.documentation = new vscode.MarkdownString(`PSX \`${block.name}\` logic block`);
            items.push(item);
        });

        // NextPy components
        const nextpyComponents = [
            { name: 'Link', snippet: '<Link href="$1">$2</Link>' },
            { name: 'Head', snippet: '<Head>\n    $1\n</Head>' },
            { name: 'Fragment', snippet: '<>\n    $1\n</>' }
        ];

        nextpyComponents.forEach(component => {
            const item = new vscode.CompletionItem(component.name, vscode.CompletionItemKind.Class);
            item.insertText = new vscode.SnippetString(component.snippet);
            item.documentation = new vscode.MarkdownString(`NextPy \`${component.name}\` component`);
            items.push(item);
        });

        return items;
    }
}

class PSXHoverProvider implements vscode.HoverProvider {
    provideHover(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken
    ): vscode.Hover | undefined {
        const range = document.getWordRangeAtPosition(position);
        if (!range) return undefined;

        const word = document.getText(range);
        
        const documentation: { [key: string]: string } = {
            'psx': 'PSX - Python Syntax eXtension for NextPy\n\nWrite JSX-like syntax in Python with revolutionary features like real Python logic blocks.',
            'for': 'PSX For Loop\n\n```psx\n{for item in items:\n    <div>{item}</div>\n}\n```',
            'if': 'PSX If Condition\n\n```psx\n{if condition:\n    <div>Content</div>\n}\n```',
            'try': 'PSX Try-Catch\n\n```psx\n{try:\n    <div>{risky()}</div>\n}{except Error as e:\n    <div>Error: {e}</div>\n}\n```',
            'python': 'PSX Python Logic\n\n```psx\n{python:\n    # Any Python code\n    result = complex_logic()\n    return psx("<div>{result}</div>")\n}\n```',
            'component': 'PSX Component Decorator\n\n```python\n@component\ndef MyComponent(props):\n    return psx("<div>{props.get(\'text\')}</div>")\n```',
            'useState': 'useState Hook\n\n```python\nvalue, setValue = useState(initial_value)\n```',
            'useEffect': 'useEffect Hook\n\n```python\nuseEffect(lambda: () => {\n    # Side effect logic\n}, [dependencies])\n```'
        };

        if (documentation[word]) {
            return new vscode.Hover(new vscode.MarkdownString(documentation[word]));
        }

        return undefined;
    }
}

function createPSXComponent() {
    const componentName = vscode.window.showInputBox({
        prompt: 'Enter component name',
        placeHolder: 'MyComponent'
    });

    componentName.then(name => {
        if (name) {
            const workspaceFolders = vscode.workspace.workspaceFolders;
            if (workspaceFolders) {
                const componentPath = path.join(workspaceFolders[0].uri.fsPath, 'components', `${name}.py`);
                
                const componentTemplate = `"""
${name} PSX Component
"""

from nextpy.psx import psx, component

@component
def ${name}(props):
    """${name} component"""
    
    return psx(
        "<div className=\"${name.toLowerCase()}\">",
        "    <h1>{props.get('title', '${name}')}</h1>",
        "    <p>{props.get('description', 'Default description')}</p>",
        "</div>"
    )
`;

                vscode.workspace.fs.writeFile(vscode.Uri.file(componentPath), Buffer.from(componentTemplate))
                    .then(() => {
                        vscode.window.showInformationMessage(`Component ${name} created successfully!`);
                        vscode.workspace.openTextDocument(componentPath);
                    });
            }
        }
    });
}

function createPSXPage() {
    const pageName = vscode.window.showInputBox({
        prompt: 'Enter page name',
        placeHolder: 'my-page'
    });

    pageName.then(name => {
        if (name) {
            const workspaceFolders = vscode.workspace.workspaceFolders;
            if (workspaceFolders) {
                const pagePath = path.join(workspaceFolders[0].uri.fsPath, 'pages', `${name}.py`);
                
                const pageTemplate = `"""
${name} Page
"""

from nextpy.psx import psx, component

@component
def Page(props):
    """${name} page"""
    
    return psx(
        "<div className=\"page\">",
        "    <h1>${name.replace('-', ' ').replace(/\b\w/g, (l: string) => l.toUpperCase())}</h1>",
        "    <p>Welcome to the ${name} page!</p>",
        "</div>"
    )
`;

                vscode.workspace.fs.writeFile(vscode.Uri.file(pagePath), Buffer.from(pageTemplate))
                    .then(() => {
                        vscode.window.showInformationMessage(`Page ${name} created successfully!`);
                        vscode.workspace.openTextDocument(pagePath);
                    });
            }
        }
    });
}

function togglePythonLogicHighlighting() {
    const config = vscode.workspace.getConfiguration('nextpyPsx');
    const currentValue = config.get('pythonLogicHighlighting', true);
    
    config.update('pythonLogicHighlighting', !currentValue).then(() => {
        vscode.window.showInformationMessage(
            `Python logic highlighting ${!currentValue ? 'enabled' : 'disabled'}`
        );
    });
}

function showDocumentation() {
    const uri = vscode.Uri.parse('https://github.com/nextpy-framework/nextpy');
    vscode.env.openExternal(uri);
}

export function deactivate() {
    console.log('NextPy PSX extension deactivated');
}
