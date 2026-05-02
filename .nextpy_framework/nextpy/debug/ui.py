"""
NextPy Debug UI System
Modular UI components for debug panel
"""

from typing import Dict, Any, Optional, List
from .core import debug_core


class DebugUI:
    """Clean UI system for debug panel"""
    
    def __init__(self):
        self.visible = False
        self.position = "bottom-right"
        self.theme = "dark"
        self.size = {"width": 450, "height": 600}
        
    def generate_html(self, page_props: Optional[Dict[str, Any]] = None) -> str:
        """Generate debug panel HTML"""
        return '''
        <!-- NextPy Debug Panel - Modular Architecture -->
        <div class="nextpy-debug-overlay" id="nextpy-debug-overlay">
            <!-- Debug Icon -->
            <div class="nextpy-debug-icon" id="nextpy-debug-icon" onclick="nextpyDebugUI.toggle()">
                <span class="nextpy-debug-text">NP</span>
                <span class="nextpy-debug-badge" id="nextpy-debug-badge">0</span>
            </div>
            
            <!-- Debug Panel -->
            <div class="nextpy-debug-panel" id="nextpy-debug-panel" style="display: none;">
                <!-- Header -->
                <div class="nextpy-debug-header">
                    <div class="nextpy-debug-title">
                        <h3>NextPy Debug</h3>
                        <span class="nextpy-debug-version">v3.0</span>
                    </div>
                    <button class="nextpy-debug-close" onclick="nextpyDebugUI.toggle()">×</button>
                </div>
                
                <!-- Content Container -->
                <div class="nextpy-debug-content">
                    <!-- Session Info -->
                    <div class="nextpy-debug-section">
                        <h4>Session <span class="nextpy-debug-count" id="nextpy-session-id">None</span></h4>
                        <div class="nextpy-debug-info">
                            <div class="nextpy-debug-row">
                                <span class="nextpy-debug-label">Status:</span>
                                <span class="nextpy-debug-value" id="nextpy-session-status">Inactive</span>
                            </div>
                            <div class="nextpy-debug-row">
                                <span class="nextpy-debug-label">Duration:</span>
                                <span class="nextpy-debug-value" id="nextpy-session-duration">0s</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Component States -->
                    <div class="nextpy-debug-section">
                        <h4>Components <span class="nextpy-debug-count" id="nextpy-component-count">0</span></h4>
                        <div class="nextpy-debug-components" id="nextpy-debug-components">
                            <div class="nextpy-debug-empty">No components tracked</div>
                        </div>
                    </div>
                    
                    <!-- Recent Events -->
                    <div class="nextpy-debug-section">
                        <h4>Events <span class="nextpy-debug-count" id="nextpy-event-count">0</span></h4>
                        <div class="nextpy-debug-events" id="nextpy-debug-events">
                            <div class="nextpy-debug-empty">No events tracked</div>
                        </div>
                    </div>
                    
                    <!-- Performance -->
                    <div class="nextpy-debug-section">
                        <h4>Performance</h4>
                        <div class="nextpy-debug-performance" id="nextpy-debug-performance">
                            <div class="nextpy-debug-empty">No metrics available</div>
                        </div>
                    </div>
                    
                    <!-- WebSocket Status -->
                    <div class="nextpy-debug-section">
                        <h4>WebSocket</h4>
                        <div class="nextpy-debug-websocket" id="nextpy-debug-websocket">
                            <div class="nextpy-debug-row">
                                <span class="nextpy-debug-label">Status:</span>
                                <span class="nextpy-debug-value" id="nextpy-ws-status">Disconnected</span>
                            </div>
                            <div class="nextpy-debug-row">
                                <span class="nextpy-debug-label">Client ID:</span>
                                <span class="nextpy-debug-value" id="nextpy-ws-client-id">None</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tools -->
                    <div class="nextpy-debug-section">
                        <h4>Tools</h4>
                        <div class="nextpy-debug-tools">
                            <button class="nextpy-debug-tool-btn" onclick="nextpyDebugUI.startSession()">Start Session</button>
                            <button class="nextpy-debug-tool-btn" onclick="nextpyDebugUI.endSession()">End Session</button>
                            <button class="nextpy-debug-tool-btn" onclick="nextpyDebugUI.exportData()">Export</button>
                            <button class="nextpy-debug-tool-btn" onclick="nextpyDebugUI.clearData()">Clear</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        '''
    
    def generate_javascript(self) -> str:
        """Generate debug panel JavaScript"""
        return '''
        // NextPy Debug UI - Modular Architecture
        (function() {
            'use strict';
                     
            // Debug UI Controller
            window.nextpyDebugUI = {
                visible: false,
                sessionActive: false,
                updateInterval: null,
                
                // Toggle panel visibility
                toggle: function() {
                    const panel = document.getElementById('nextpy-debug-panel');
                    const icon = document.getElementById('nextpy-debug-icon');
                    
                    if (!panel || !icon) return;
                    
                    this.visible = !this.visible;
                    
                    if (this.visible) {
                        panel.style.display = 'block';
                        icon.classList.add('active');
                        this.startUpdates();
                    } else {
                        panel.style.display = 'none';
                        icon.classList.remove('active');
                        this.stopUpdates();
                    }
                },
                
                // Start debug session
                startSession: function() {
                    if (this.sessionActive) return;
                    
                    // Call backend to start session
                    this.fetchAPI('/__nextpy/debug/start', 'POST')
                        .then(data => {
                            this.sessionActive = true;
                            this.updateSessionInfo(data);
                            this.log('INFO', 'Debug session started');
                        })
                        .catch(error => {
                            this.log('ERROR', 'Failed to start session: ' + error.message);
                        });
                },
                
                // End debug session
                endSession: function() {
                    if (!this.sessionActive) return;
                    
                    this.fetchAPI('/__nextpy/debug/end', 'POST')
                        .then(data => {
                            this.sessionActive = false;
                            this.updateSessionInfo(null);
                            this.log('INFO', 'Debug session ended');
                            if (data && data.summary) {
                                console.log('Session Summary:', data.summary);
                            }
                        })
                        .catch(error => {
                            this.log('ERROR', 'Failed to end session: ' + error.message);
                        });
                },
                
                // Export debug data
                exportData: function() {
                    this.fetchAPI('/__nextpy/debug/export', 'GET')
                        .then(data => {
                            const blob = new Blob([JSON.stringify(data, null, 2)], {
                                type: 'application/json'
                            });
                            const url = URL.createObjectURL(blob);
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = 'nextpy-debug-' + Date.now() + '.json';
                            a.click();
                            URL.revokeObjectURL(url);
                            this.log('INFO', 'Debug data exported');
                        })
                        .catch(error => {
                            this.log('ERROR', 'Failed to export data: ' + error.message);
                        });
                },
                
                // Clear debug data
                clearData: function() {
                    this.fetchAPI('/__nextpy/debug/clear', 'POST')
                        .then(() => {
                            this.updateDisplays();
                            this.log('INFO', 'Debug data cleared');
                        })
                        .catch(error => {
                            this.log('ERROR', 'Failed to clear data: ' + error.message);
                        });
                },
                
                // Update displays
                updateDisplays: function() {
                    this.updateSessionInfo();
                    this.updateComponents();
                    this.updateEvents();
                    this.updatePerformance();
                    this.updateWebSocket();
                },
                
                // Update session info
                updateSessionInfo: function(sessionData) {
                    const sessionId = document.getElementById('nextpy-session-id');
                    const status = document.getElementById('nextpy-session-status');
                    const duration = document.getElementById('nextpy-session-duration');
                    
                    if (sessionData) {
                        if (sessionId) sessionId.textContent = sessionData.session_id || 'Active';
                        if (status) {
                            status.textContent = 'Active';
                            status.style.color = '#4ade80';
                        }
                        if (duration) {
                            const durationSec = Math.floor((Date.now() / 1000) - sessionData.start_time);
                            duration.textContent = durationSec + 's';
                        }
                    } else {
                        if (sessionId) sessionId.textContent = 'None';
                        if (status) {
                            status.textContent = 'Inactive';
                            status.style.color = '#ff4444';
                        }
                        if (duration) duration.textContent = '0s';
                    }
                },
                
                // Update components display
                updateComponents: function() {
                    this.fetchAPI('/__nextpy/debug/components', 'GET')
                        .then(data => {
                            const container = document.getElementById('nextpy-debug-components');
                            const count = document.getElementById('nextpy-component-count');
                            
                            if (!container) return;
                            
                            if (Object.keys(data).length === 0) {
                                container.innerHTML = '<div class="nextpy-debug-empty">No components tracked</div>';
                                if (count) count.textContent = '0';
                                return;
                            }
                            
                            let html = '';
                            for (const [componentId, state] of Object.entries(data)) {
                                html += '<div class="nextpy-debug-component-item">' +
                                    '<div class="nextpy-debug-component-id">' + componentId + '</div>' +
                                    '<div class="nextpy-debug-component-state">' + 
                                        JSON.stringify(state, null, 2) + 
                                    '</div>' +
                                    '</div>';
                            }
                            
                            container.innerHTML = html;
                            if (count) count.textContent = Object.keys(data).length;
                        })
                        .catch(error => {
                            console.error('Failed to update components:', error);
                        });
                },
                
                // Update events display
                updateEvents: function() {
                    this.fetchAPI('/__nextpy/debug/events', 'GET')
                        .then(data => {
                            const container = document.getElementById('nextpy-debug-events');
                            const count = document.getElementById('nextpy-event-count');
                            
                            if (!container) return;
                            
                            if (data.length === 0) {
                                container.innerHTML = '<div class="nextpy-debug-empty">No events tracked</div>';
                                if (count) count.textContent = '0';
                                return;
                            }
                            
                            let html = '';
                            const recentEvents = data.slice(-20).reverse(); // Show last 20 events
                            
                            for (const event of recentEvents) {
                                const time = new Date(event.timestamp * 1000).toLocaleTimeString();
                                html += '<div class="nextpy-debug-event-item">' +
                                    '<span class="nextpy-debug-event-time">' + time + '</span>' +
                                    '<span class="nextpy-debug-event-type">' + event.type + '</span>' +
                                    '<span class="nextpy-debug-event-source">' + event.source + '</span>' +
                                    '</div>';
                            }
                            
                            container.innerHTML = html;
                            if (count) count.textContent = data.length;
                        })
                        .catch(error => {
                            console.error('Failed to update events:', error);
                        });
                },
                
                // Update performance display
                updatePerformance: function() {
                    this.fetchAPI('/__nextpy/debug/performance', 'GET')
                        .then(data => {
                            const container = document.getElementById('nextpy-debug-performance');
                            
                            if (!container) return;
                            
                            if (Object.keys(data).length === 0) {
                                container.innerHTML = '<div class="nextpy-debug-empty">No metrics available</div>';
                                return;
                            }
                            
                            let html = '';
                            for (const [metric, info] of Object.entries(data)) {
                                html += '<div class="nextpy-debug-row">' +
                                    '<span class="nextpy-debug-label">' + metric + ':</span>' +
                                    '<span class="nextpy-debug-value">' + info.value + '</span>' +
                                    '</div>';
                            }
                            
                            container.innerHTML = html;
                        })
                        .catch(error => {
                            console.error('Failed to update performance:', error);
                        });
                },
                
                // Update WebSocket display
                updateWebSocket: function() {
                    this.fetchAPI('/__nextpy/debug/websocket', 'GET')
                        .then(data => {
                            const status = document.getElementById('nextpy-ws-status');
                            const clientId = document.getElementById('nextpy-ws-client-id');
                            
                            if (status) {
                                status.textContent = data.connected ? 'Connected' : 'Disconnected';
                                status.style.color = data.connected ? '#4ade80' : '#ff4444';
                            }
                            if (clientId) clientId.textContent = data.client_id || 'None';
                        })
                        .catch(error => {
                            // Handle WebSocket API unavailability gracefully
                            const status = document.getElementById('nextpy-ws-status');
                            const clientId = document.getElementById('nextpy-ws-client-id');
                            
                            if (status) {
                                status.textContent = 'Server Offline';
                                status.style.color = '#ffa500'; // Orange warning color
                            }
                            if (clientId) clientId.textContent = 'N/A';
                            
                            // Don't spam console with WebSocket errors
                            if (!this.wsErrorLogged) {
                                console.warn('WebSocket server not available - debug features limited');
                                this.wsErrorLogged = true;
                            }
                        });
                },
                
                // Start auto updates
                startUpdates: function() {
                    this.stopUpdates(); // Clear any existing interval
                    this.updateDisplays(); // Initial update
                    
                    this.updateInterval = setInterval(() => {
                        this.updateDisplays();
                    }, 2000);
                },
                
                // Stop auto updates
                stopUpdates: function() {
                    if (this.updateInterval) {
                        clearInterval(this.updateInterval);
                        this.updateInterval = null;
                    }
                },
                
                // Log message
                log: function(level, message) {
                    console.log('[NextPy Debug][' + level + '] ' + message);
                },
                
                // Simple fetch API wrapper
                fetchAPI: function(url, method, data) {
                    return fetch(url, {
                        method: method,
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: data ? JSON.stringify(data) : undefined
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('HTTP ' + response.status);
                        }
                        return response.json();
                    });
                }
            };
            
            // Initialize
            console.log('[NextPy Debug] UI module loaded');
            
            // Ensure debug icon is visible
            setTimeout(() => {
                const icon = document.getElementById('nextpy-debug-icon');
                const overlay = document.getElementById('nextpy-debug-overlay');
                
                if (icon) {
                    console.log('[NextPy Debug] Debug icon found:', icon);
                    // Force icon to be visible
                    icon.style.display = 'flex';
                    icon.style.visibility = 'visible';
                    icon.style.opacity = '1';
                    icon.style.pointerEvents = 'all';
                } else {
                    console.warn('[NextPy Debug] Debug icon not found');
                }
                
                if (overlay) {
                    console.log('[NextPy Debug] Debug overlay found:', overlay);
                } else {
                    console.warn('[NextPy Debug] Debug overlay not found');
                }
            }, 100);
        })();
        '''
    
    def generate_css(self) -> str:
        """Generate debug panel CSS"""
        return '''
        /* NextPy Debug UI - Modular Architecture */
        .nextpy-debug-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
        }
        
        .nextpy-debug-icon {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 48px;
            height: 48px;
            background: #1a1a1a;
            border: 2px solid #333;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-family: 'SF Mono', 'Monaco', monospace;
            font-size: 12px;
            font-weight: bold;
            color: #fff;
            transition: all 0.2s ease;
            pointer-events: all;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            user-select: none;
        }
        
        .nextpy-debug-icon:hover {
            background: #333;
            border-color: #555;
            transform: scale(1.1);
        }
        
        .nextpy-debug-icon.active {
            background: #0070f3;
            border-color: #0051cc;
        }
        
        .nextpy-debug-badge {
            position: absolute;
            top: -8px;
            right: -8px;
            min-width: 18px;
            height: 18px;
            background: #ffaa00;
            color: white;
            border-radius: 50%;
            font-size: 10px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid #1a1a1a;
        }
        
        .nextpy-debug-panel {
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 450px;
            max-height: 80vh;
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            overflow: hidden;
            pointer-events: all;
            font-family: 'SF Mono', 'Monaco', monospace;
            font-size: 12px;
            color: #fff;
            display: flex;
            flex-direction: column;
        }
        
        .nextpy-debug-header {
            background: #2a2a2a;
            padding: 12px 16px;
            border-bottom: 1px solid #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .nextpy-debug-title h3 {
            margin: 0;
            font-size: 14px;
            font-weight: 600;
            color: #fff;
        }
        
        .nextpy-debug-version {
            background: #0070f3;
            color: white;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 500;
        }
        
        .nextpy-debug-close {
            background: none;
            border: none;
            color: #999;
            font-size: 18px;
            cursor: pointer;
            padding: 0;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            transition: all 0.2s ease;
        }
        
        .nextpy-debug-close:hover {
            background: #ff4444;
            color: white;
        }
        
        .nextpy-debug-content {
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        
        .nextpy-debug-section {
            border-bottom: 1px solid #333;
            padding: 12px 16px;
            flex-shrink: 0;
        }
        
        .nextpy-debug-section:last-child {
            border-bottom: none;
        }
        
        .nextpy-debug-section h4 {
            margin: 0 0 8px 0;
            font-size: 12px;
            font-weight: 600;
            color: #ccc;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .nextpy-debug-count {
            background: #0070f3;
            color: white;
            padding: 2px 6px;
            border-radius: 10px;
            font-size: 9px;
            font-weight: 500;
            margin-left: 8px;
        }
        
        .nextpy-debug-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 2px 0;
        }
        
        .nextpy-debug-label {
            color: #999;
            font-size: 11px;
        }
        
        .nextpy-debug-value {
            color: #fff;
            font-weight: 500;
            font-size: 11px;
        }
        
        .nextpy-debug-components,
        .nextpy-debug-events {
            max-height: 200px;
            overflow-y: auto;
        }
        
        .nextpy-debug-component-item {
            margin-bottom: 8px;
            padding: 8px;
            background: rgba(76, 175, 80, 0.1);
            border-radius: 4px;
            border-left: 3px solid #4caf50;
        }
        
        .nextpy-debug-component-id {
            color: #4caf50;
            font-weight: 600;
            font-size: 10px;
            margin-bottom: 4px;
        }
        
        .nextpy-debug-component-state {
            color: #ccc;
            font-size: 9px;
            font-family: monospace;
            white-space: pre-wrap;
            word-break: break-all;
        }
        
        .nextpy-debug-event-item {
            display: flex;
            gap: 8px;
            padding: 4px 8px;
            border-radius: 2px;
            font-size: 10px;
            align-items: center;
        }
        
        .nextpy-debug-event-time {
            color: #666;
            min-width: 60px;
        }
        
        .nextpy-debug-event-type {
            color: #0070f3;
            font-weight: 500;
            min-width: 80px;
        }
        
        .nextpy-debug-event-source {
            color: #ffa500;
            flex: 1;
        }
        
        .nextpy-debug-empty {
            color: #666;
            font-style: italic;
            text-align: center;
            padding: 20px;
        }
        
        .nextpy-debug-tools {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }
        
        .nextpy-debug-tool-btn {
            background: #2a2a2a;
            border: 1px solid #444;
            color: #ccc;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: inherit;
        }
        
        .nextpy-debug-tool-btn:hover {
            background: #3a3a3a;
            border-color: #666;
            color: #fff;
        }
        
        @media (max-width: 480px) {
            .nextpy-debug-panel {
                width: calc(100vw - 40px);
                right: 20px;
                left: 20px;
                max-height: 70vh;
            }
            
            .nextpy-debug-tools {
                grid-template-columns: 1fr;
            }
        }
        '''


# Global UI instance
debug_ui = DebugUI()


def inject_debug_ui(html_content: str, page_props: Optional[Dict[str, Any]] = None) -> str:
    """Inject debug UI into HTML content"""
    ui = debug_ui
    
    debug_html = ui.generate_html(page_props)
    debug_js = ui.generate_javascript()
    debug_css = ui.generate_css()
    
    # Create complete debug system with proper structure
    debug_system = f"""
{debug_html}
<style>
{debug_css}
</style>
<script>
{debug_js}
</script>
"""
    
    # Insert before closing body tag
    if "</body>" in html_content:
        parts = html_content.split("</body>")
        html_content = parts[0] + debug_system + "</body>" + parts[1] if len(parts) > 1 else parts[0] + debug_system + "</body>"
    else:
        html_content += debug_system
    
    return html_content
