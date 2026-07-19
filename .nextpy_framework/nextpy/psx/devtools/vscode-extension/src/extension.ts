import * as vscode from 'vscode';
import { LanguageClient, LanguageClientOptions, ServerOptions } from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: vscode.ExtensionContext) {
    console.log('PSX extension is now active!');
    
    // Language server options
    const serverOptions: ServerOptions = {
        command: getServerPath(),
        args: [],
        options: {
            cwd: vscode.workspace.rootPath
        }
    };
    
    // Client options
    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'psx' }],
        synchronize: {
            configurationSection: 'psx',
            fileEvents: vscode.workspace.createFileSystemWatcher('**/.clientrc')
        }
    };
    
    // Create and start the client
    client = new LanguageClient(
        'psxLanguageServer',
        'PSX Language Server',
        serverOptions,
        clientOptions
    );
    
    // Start the client
    client.start();
    
    // Register commands
    const restartCommand = vscode.commands.registerCommand('psx.restartServer', () => {
        if (client) {
            client.stop();
            client.start();
            vscode.window.showInformationMessage('PSX Language Server restarted');
        }
    });
    
    const formatCommand = vscode.commands.registerCommand('psx.formatDocument', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            vscode.commands.executeCommand('editor.action.format');
        }
    });
    
    context.subscriptions.push(restartCommand, formatCommand);
    
    // Register status bar item
    const statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    statusBarItem.text = '$(symbol-method) PSX';
    statusBarItem.tooltip = 'PSX Language Server Active';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
}

function getServerPath(): string {
    const config = vscode.workspace.getConfiguration('psx');
    const serverPath = config.get<string>('languageServer.path');
    
    if (serverPath) {
        return serverPath;
    }
    
    // Default to python script
    return 'python3';
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
