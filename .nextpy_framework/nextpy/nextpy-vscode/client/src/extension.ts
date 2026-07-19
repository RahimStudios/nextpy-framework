import * as vscode from 'vscode';
import { LanguageClient, LanguageClientOptions, ServerOptions, TransportKind } from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: vscode.ExtensionContext) {
    console.log('NextPy extension is now active!');

    // Server setup
    const serverModule = context.asAbsolutePath('../server/out/server.js');
    const debugOptions = { execArgv: ['--nolazy', '--inspect=6009'] };
    const serverOptions: ServerOptions = {
        run: { module: serverModule, transport: TransportKind.ipc },
        debug: { module: serverModule, transport: TransportKind.ipc, options: debugOptions }
    };

    // Client options
    const clientOptions: LanguageClientOptions = {
        documentSelector: [
            { scheme: 'file', language: 'nextpy' },
            { scheme: 'file', language: 'python' }
        ],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.py.jsx')
        },
        initializationOptions: {
            enableIntelliSense: vscode.workspace.getConfiguration('nextpy').get('enableIntelliSense', true),
            enableJSXHighlighting: vscode.workspace.getConfiguration('nextpy').get('enableJSXHighlighting', true)
        }
    };

    // Create and start the client
    client = new LanguageClient(
        'nextpyLanguageServer',
        'NextPy Language Server',
        serverOptions,
        clientOptions
    );
    client.start();
    context.subscriptions.push(client); // Push client, not Promise

    // Completion provider
    const completionProvider = vscode.languages.registerCompletionItemProvider(
        { language: 'nextpy' },
        new NextPyCompletionProvider(),
        '.', '<' // trigger characters
    );
    context.subscriptions.push(completionProvider);

    // Hover provider
    const hoverProvider = vscode.languages.registerHoverProvider(
        { language: 'nextpy' },
        new NextPyHoverProvider()
    );
    context.subscriptions.push(hoverProvider);
}

// Deactivate properly
export function deactivate(): Thenable<void> {
    if (!client) {
        return Promise.resolve();
    }
    return client.stop();
}

// Completion provider
class NextPyCompletionProvider implements vscode.CompletionItemProvider {
    provideCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position
    ): vscode.CompletionItem[] | Thenable<vscode.CompletionItem[]> {

        const linePrefix = document.lineAt(position.line).text.substring(0, position.character);

        const completions: vscode.CompletionItem[] = [
            { label: 'Button', kind: vscode.CompletionItemKind.Class, insertText: 'Button' },
            { label: 'Card', kind: vscode.CompletionItemKind.Class, insertText: 'Card' },
            { label: 'Modal', kind: vscode.CompletionItemKind.Class, insertText: 'Modal' },
            { label: 'Input', kind: vscode.CompletionItemKind.Class, insertText: 'Input' },
            { label: 'Layout', kind: vscode.CompletionItemKind.Class, insertText: 'Layout' },
            { label: 'def', kind: vscode.CompletionItemKind.Keyword, insertText: 'def ' },
            { label: 'return', kind: vscode.CompletionItemKind.Keyword, insertText: 'return' },
            { label: 'import', kind: vscode.CompletionItemKind.Keyword, insertText: 'import ' },
            { label: 'from', kind: vscode.CompletionItemKind.Keyword, insertText: 'from ' },
            { label: 'className', kind: vscode.CompletionItemKind.Property, insertText: 'className=' },
            { label: 'onClick', kind: vscode.CompletionItemKind.Property, insertText: 'onClick=' },
            { label: 'onChange', kind: vscode.CompletionItemKind.Property, insertText: 'onChange=' },
            { label: 'className="container"', kind: vscode.CompletionItemKind.Snippet, insertText: 'className="container"' },
            { label: 'className="btn btn-primary"', kind: vscode.CompletionItemKind.Snippet, insertText: 'className="btn btn-primary"' },
            { label: 'className="flex"', kind: vscode.CompletionItemKind.Snippet, insertText: 'className="flex"' }
        ];

        return completions.filter(item => {
            const labelText = typeof item.label === 'string' ? item.label : item.label.label;
            return labelText.toLowerCase().startsWith(linePrefix.toLowerCase());
        });
    }
}

// Hover provider
class NextPyHoverProvider implements vscode.HoverProvider {
    provideHover(
        document: vscode.TextDocument,
        position: vscode.Position
    ): vscode.Hover | undefined {

        const wordRange = document.getWordRangeAtPosition(position);
        if (!wordRange) return undefined;

        const word = document.getText(wordRange);

        const componentDocs: { [key: string]: string } = {
            'Button': 'NextPy Button component\n\nProps: variant, size, disabled, onClick, className',
            'Card': 'NextPy Card component\n\nProps: title, children, className',
            'Modal': 'NextPy Modal component\n\nProps: isOpen, onClose, title, children',
            'Input': 'NextPy Input component\n\nProps: type, placeholder, value, onChange, error',
            'Layout': 'NextPy Layout component\n\nProps: children, className'
        };

        if (componentDocs[word]) {
            return new vscode.Hover(componentDocs[word]);
        }

        return undefined;
    }
}
