"""NextPy Debug Icon Component - Development overlay similar to Next.js debug icon"""

def DebugIcon(props = None):
    """Floating debug icon with development information and controls"""
    props = props or {}
    
    # Component state (in real implementation, this would use React hooks)
    is_open = props.get("is_open", False)
    has_errors = props.get("has_errors", False)
    has_warnings = props.get("has_warnings", False)
    current_route = props.get("current_route", "/")
    render_time = props.get("render_time", 0)
    error_count = props.get("error_count", 0)
    warning_count = props.get("warning_count", 0)
    
    return jsx("""
        <div class="nextpy-debug-overlay">
            <!-- Debug Icon Button -->
            <div 
                class="nextpy-debug-icon"
                onclick="toggleDebugPanel()"
                title="NextPy Debug Panel"
            >
                <span class="nextpy-debug-text">NP</span>
                """ + (jsx(f'<span class="nextpy-debug-badge nextpy-debug-error">{error_count}</span>') if error_count > 0 else "") + (jsx(f'<span class="nextpy-debug-badge nextpy-debug-warning">{warning_count}</span>') if warning_count > 0 and error_count == 0 else "") + """
            </div>
            
            <!-- Debug Panel -->
            """ + (jsx(f"""
                <div class="nextpy-debug-panel" style="display: {'block' if is_open else 'none'}">
                    <!-- Header -->
                    <div class="nextpy-debug-header">
                        <div class="nextpy-debug-title">
                            <h3>NextPy Debug</h3>
                            <span class="nextpy-debug-version">v2.0.0</span>
                        </div>
                        <button 
                            class="nextpy-debug-close"
                            onclick="toggleDebugPanel()"
                            title="Close"
                        >
                            ×
                        </button>
                    </div>
                    
                    <!-- Current Route Info -->
                    <div class="nextpy-debug-section">
                        <h4>📍 Current Route</h4>
                        <div class="nextpy-debug-info">
                            <div class="nextpy-debug-row">
                                <span class="nextpy-debug-label">Path:</span>
                                <span class="nextpy-debug-value">{current_route}</span>
                            </div>
                            <div class="nextpy-debug-row">
                                <span class="nextpy-debug-label">Render Time:</span>
                                <span class="nextpy-debug-value">{render_time}ms</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Performance Metrics -->
                    <div class="nextpy-debug-section">
                        <h4>Performance</h4>
                        <div class="nextpy-debug-metrics">
                            <div class="nextpy-debug-row">
                                <span class="nextpy-debug-label">Components:</span>
                                <span class="nextpy-debug-value">{props.get("component_count", 0)}</span>
                            </div>
                            <div class="nextpy-debug-row">
                                <span class="nextpy-debug-label">Re-renders:</span>
                                <span class="nextpy-debug-value">{props.get("rerender_count", 0)}</span>
                            </div>
                            <div class="nextpy-debug-row">
                                <span class="nextpy-debug-label">API Calls:</span>
                                <span class="nextpy-debug-value">{props.get("api_calls", 0)}</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Development Tools -->
                    <div class="nextpy-debug-section">
                        <h4>Tools</h4>
                        <div class="nextpy-debug-tools">
                            <button 
                                class="nextpy-debug-tool-btn"
                                onclick="toggleComponentBoundaries()"
                                title="Toggle component boundaries"
                            >
                                Boundaries
                            </button>
                            <button 
                                class="nextpy-debug-tool-btn"
                                onclick="toggleRerenderHighlight()"
                                title="Highlight re-renders"
                            >
                                Re-renders
                            </button>
                            <button 
                                class="nextpy-debug-tool-btn"
                                onclick="toggleVerboseLogging()"
                                title="Enable verbose logging"
                            >
                                Verbose
                            </button>
                            <button 
                                class="nextpy-debug-tool-btn"
                                onclick="clearDebugLogs()"
                                title="Clear debug logs"
                            >
                                Clear
                            </button>
                        </div>
                    </div>
                </div>
            """) if is_open else "") + """
        </div>
    """)


# JavaScript functions for interactivity
DEBUG_JS = """
// Toggle debug panel
function toggleDebugPanel() {
    const panel = document.querySelector('.nextpy-debug-panel');
    const icon = document.querySelector('.nextpy-debug-icon');
    
    if (panel.style.display === 'block') {
        panel.style.display = 'none';
        icon.classList.remove('active');
    } else {
        panel.style.display = 'block';
        icon.classList.add('active');
    }
}

// Toggle component boundaries
function toggleComponentBoundaries() {
    const btn = event.target;
    btn.classList.toggle('active');
    console.log('Component boundaries', btn.classList.contains('active') ? 'enabled' : 'disabled');
}

// Toggle re-render highlights
function toggleRerenderHighlight() {
    const btn = event.target;
    btn.classList.toggle('active');
    console.log('Re-render highlights', btn.classList.contains('active') ? 'enabled' : 'disabled');
}

// Toggle verbose logging
function toggleVerboseLogging() {
    const btn = event.target;
    btn.classList.toggle('active');
    console.log('Verbose logging', btn.classList.contains('active') ? 'enabled' : 'disabled');
}

// Clear debug logs
function clearDebugLogs() {
    console.log('Debug logs cleared');
}

// Capture console logs
const originalLog = console.log;
const originalWarn = console.warn;
const originalError = console.error;

console.log = function(...args) {
    originalLog.apply(console, args);
    addDebugLog('INFO', args.join(' '));
};

console.warn = function(...args) {
    originalWarn.apply(console, args);
    addDebugLog('WARN', args.join(' '));
};

console.error = function(...args) {
    originalError.apply(console, args);
    addDebugLog('ERROR', args.join(' '));
};

function addDebugLog(level, message) {
    console.log(`[${level}] ${message}`);
}

// Capture unhandled errors
window.addEventListener('error', function(event) {
    addDebugLog('ERROR', event.message + ' at ' + event.filename + ':' + event.lineno);
});

window.addEventListener('unhandledrejection', function(event) {
    addDebugLog('ERROR', 'Unhandled promise rejection: ' + event.reason);
});

// Make debug panel draggable
let isDragging = false;
let currentX;
let currentY;
let initialX;
let initialY;
let xOffset = 0;
let yOffset = 0;

document.addEventListener('DOMContentLoaded', function() {
    const debugIcon = document.querySelector('.nextpy-debug-icon');
    if (debugIcon) {
        debugIcon.addEventListener('mousedown', dragStart);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', dragEnd);
    }
});

function dragStart(e) {
    if (e.target.classList.contains('nextpy-debug-icon')) {
        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;
        isDragging = true;
    }
}

function dragEnd(e) {
    initialX = currentX;
    initialY = currentY;
    isDragging = false;
}

function drag(e) {
    if (isDragging) {
        e.preventDefault();
        currentX = e.clientX - initialX;
        currentY = e.clientY - initialY;
        xOffset = currentX;
        yOffset = currentY;

        const debugIcon = document.querySelector('.nextpy-debug-icon');
        if (debugIcon) {
            debugIcon.style.transform = `translate(${currentX}px, ${currentY}px)`;
        }
    }
}
"""


default = DebugIcon
