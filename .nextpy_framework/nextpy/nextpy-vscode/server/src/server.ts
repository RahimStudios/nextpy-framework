import {
    createConnection,
    TextDocuments,
    ProposedFeatures,
    InitializeParams,
    CompletionItem,
    CompletionItemKind,
    Hover,
    TextDocumentPositionParams
} from 'vscode-languageserver/node';
import { spawn } from 'child_process';
import { TextDocument } from 'vscode-languageserver-textdocument';

const connection = createConnection(ProposedFeatures.all);
const documents: TextDocuments<TextDocument> = new TextDocuments(TextDocument);

// Python bridge for autocomplete
function getPythonCompletions(code: string, line: number, column: number): CompletionItem[] {
    return new Promise((resolve) => {
        const python = spawn('python', ['-c', `
import jedi
import sys
import json

code = """${code.replace(/"/g, '\\"')}"""
script = jedi.Script(code)
try:
    completions = script.complete(${line}, ${column})
    result = []
    for comp in completions:
        result.append({
            "label": comp.name,
            "kind": "function" if comp.type == "function" else "variable",
            "insertText": comp.name
        })
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({"error": str(e)}))
        `]);

        let output = '';
        python.stdout.on('data', (data) => {
            output += data.toString();
        });

        python.on('close', (code) => {
            if (code === 0) {
                try {
                    const completions = JSON.parse(output);
                    resolve(completions.map((c: any) => ({
                        label: c.label,
                        kind: c.kind === 'function' ? CompletionItemKind.Function : CompletionItemKind.Variable,
                        insertText: c.insertText
                    })));
                } catch (e) {
                    resolve([]);
                }
            } else {
                resolve([]);
            }
        });
    });
}

connection.onInitialize((params: InitializeParams) => {
    return {
        capabilities: {
            textDocumentSync: documents.syncKind,
            completionProvider: {
                resolveProvider: true
            },
            hoverProvider: true
        }
    };
});

// Extract Python code from JSX for analysis
function extractPythonCode(document: TextDocument): string {
    const text = document.getText();
    // Simple extraction - remove JSX tags for Python analysis
    const pythonCode = text
        .replace(/<[^>]*>/g, '') // Remove opening tags
        .replace(/<\/[^>]*>/g, '') // Remove closing tags
        .replace(/\{[^}]*\}/g, '""'); // Replace JSX expressions with empty strings
    
    return pythonCode;
}

connection.onCompletion(async (textDocumentPosition: TextDocumentPositionParams) => {
    const { textDocument, position } = textDocumentPosition;
    const doc = documents.get(textDocument.uri);
    
    if (!doc) return [];

    const text = doc.getText();
    const offset = doc.offsetAt(position);
    const line = position.line;
    const column = position.character;

    // Get completions from Python analysis
    const pythonCode = extractPythonCode(doc);
    const pythonCompletions = await getPythonCompletions(pythonCode, line, column);

    // Add NextPy-specific completions
    const nextpyCompletions: CompletionItem[] = [
        { label: 'Button', kind: CompletionItemKind.Class, insertText: 'Button' },
        { label: 'Card', kind: CompletionItemKind.Class, insertText: 'Card' },
        { label: 'Modal', kind: CompletionItemKind.Class, insertText: 'Modal' },
        { label: 'Input', kind: CompletionItemKind.Class, insertText: 'Input' },
        { label: 'Layout', kind: CompletionItemKind.Class, insertText: 'Layout' },
        { label: 'useState', kind: CompletionItemKind.Function, insertText: 'useState' },
        { label: 'useEffect', kind: CompletionItemKind.Function, insertText: 'useEffect' },
        { label: 'className', kind: CompletionItemKind.Property, insertText: 'className=' },
        { label: 'onClick', kind: CompletionItemKind.Property, insertText: 'onClick=' },
        { label: 'onChange', kind: CompletionItemKind.Property, insertText: 'onChange=' }
    ];

    return [...pythonCompletions, ...nextpyCompletions];
});

connection.onHover((textDocumentPosition: TextDocumentPositionParams) => {
    const { textDocument, position } = textDocumentPosition;
    const doc = documents.get(textDocument.uri);
    
    if (!doc) return undefined;

    const wordRange = doc.getWordRangeAtPosition(position);
    const word = doc.getText(wordRange);

    const componentDocs: { [key: string]: string } = {
        'Button': 'NextPy Button component\n\nProps: variant, size, disabled, onClick, className',
        'Card': 'NextPy Card component\n\nProps: title, children, className',
        'Modal': 'NextPy Modal component\n\nProps: isOpen, onClose, title, children',
        'Input': 'NextPy Input component\n\nProps: type, placeholder, value, onChange, error',
        'Layout': 'NextPy Layout component\n\nProps: children, className',
        'useState': 'React-like state hook\n\nUsage: const [state, setState] = useState(initialValue)',
        'useEffect': 'React-like effect hook\n\nUsage: useEffect(() => {}, [dependencies])'
    };

    if (componentDocs[word]) {
        return {
            contents: componentDocs[word]
        };
    }

    return undefined;
});

documents.listen(connection);
connection.listen();
