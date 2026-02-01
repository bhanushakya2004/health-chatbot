/**
 * Smart Logging System for Frontend
 * Provides structured logging with levels and optional backend syncing
 */

export enum LogLevel {
  DEBUG = 'DEBUG',
  INFO = 'INFO',
  WARN = 'WARN',
  ERROR = 'ERROR',
}

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  context?: Record<string, any>;
  error?: Error;
}

class Logger {
  private static instance: Logger;
  private logs: LogEntry[] = [];
  private maxLogs: number = 1000;
  private enableConsole: boolean = true;
  private enableStorage: boolean = true;

  private constructor() {
    this.loadFromStorage();
  }

  static getInstance(): Logger {
    if (!Logger.instance) {
      Logger.instance = new Logger();
    }
    return Logger.instance;
  }

  private loadFromStorage() {
    if (!this.enableStorage) return;
    
    try {
      const stored = localStorage.getItem('app_logs');
      if (stored) {
        this.logs = JSON.parse(stored);
      }
    } catch (error) {
      console.warn('Failed to load logs from storage:', error);
    }
  }

  private saveToStorage() {
    if (!this.enableStorage) return;
    
    try {
      // Keep only last 1000 logs in storage
      const logsToStore = this.logs.slice(-this.maxLogs);
      localStorage.setItem('app_logs', JSON.stringify(logsToStore));
    } catch (error) {
      console.warn('Failed to save logs to storage:', error);
    }
  }

  private log(level: LogLevel, message: string, context?: Record<string, any>, error?: Error) {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context,
      error,
    };

    this.logs.push(entry);
    
    // Trim logs if exceeding max
    if (this.logs.length > this.maxLogs) {
      this.logs = this.logs.slice(-this.maxLogs);
    }

    this.saveToStorage();

    if (this.enableConsole) {
      this.logToConsole(entry);
    }
  }

  private logToConsole(entry: LogEntry) {
    const { timestamp, level, message, context, error } = entry;
    const time = new Date(timestamp).toLocaleTimeString();
    const prefix = `[${time}] [${level}]`;

    const styles = {
      [LogLevel.DEBUG]: 'color: #6B7280',
      [LogLevel.INFO]: 'color: #10B981',
      [LogLevel.WARN]: 'color: #F59E0B',
      [LogLevel.ERROR]: 'color: #EF4444; font-weight: bold',
    };

    switch (level) {
      case LogLevel.DEBUG:
        console.debug(`%c${prefix}`, styles[level], message, context || '');
        break;
      case LogLevel.INFO:
        console.info(`%c${prefix}`, styles[level], message, context || '');
        break;
      case LogLevel.WARN:
        console.warn(`%c${prefix}`, styles[level], message, context || '');
        break;
      case LogLevel.ERROR:
        console.error(`%c${prefix}`, styles[level], message, context || '', error || '');
        break;
    }
  }

  debug(message: string, context?: Record<string, any>) {
    this.log(LogLevel.DEBUG, message, context);
  }

  info(message: string, context?: Record<string, any>) {
    this.log(LogLevel.INFO, message, context);
  }

  warn(message: string, context?: Record<string, any>) {
    this.log(LogLevel.WARN, message, context);
  }

  error(message: string, error?: Error, context?: Record<string, any>) {
    this.log(LogLevel.ERROR, message, context, error);
  }

  // Specialized logging methods
  apiRequest(method: string, url: string, status: number, duration: number) {
    this.info(`API Request: ${method} ${url}`, { status, duration });
  }

  apiError(method: string, url: string, error: Error) {
    this.error(`API Error: ${method} ${url}`, error);
  }

  userAction(action: string, details?: Record<string, any>) {
    this.info(`User Action: ${action}`, details);
  }

  componentMount(componentName: string) {
    this.debug(`Component Mounted: ${componentName}`);
  }

  componentUnmount(componentName: string) {
    this.debug(`Component Unmounted: ${componentName}`);
  }

  // Get logs
  getLogs(level?: LogLevel): LogEntry[] {
    if (level) {
      return this.logs.filter(log => log.level === level);
    }
    return this.logs;
  }

  // Clear logs
  clearLogs() {
    this.logs = [];
    localStorage.removeItem('app_logs');
    this.info('Logs cleared');
  }

  // Export logs
  exportLogs(): string {
    return JSON.stringify(this.logs, null, 2);
  }

  // Download logs as file
  downloadLogs() {
    const dataStr = this.exportLogs();
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `app-logs-${new Date().toISOString()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  // Configure logger
  configure(options: {
    enableConsole?: boolean;
    enableStorage?: boolean;
    maxLogs?: number;
  }) {
    if (options.enableConsole !== undefined) {
      this.enableConsole = options.enableConsole;
    }
    if (options.enableStorage !== undefined) {
      this.enableStorage = options.enableStorage;
    }
    if (options.maxLogs !== undefined) {
      this.maxLogs = options.maxLogs;
    }
  }
}

// Export singleton instance
export const logger = Logger.getInstance();

// Convenience exports
export const debug = (message: string, context?: Record<string, any>) => 
  logger.debug(message, context);

export const info = (message: string, context?: Record<string, any>) => 
  logger.info(message, context);

export const warn = (message: string, context?: Record<string, any>) => 
  logger.warn(message, context);

export const error = (message: string, err?: Error, context?: Record<string, any>) => 
  logger.error(message, err, context);

export const logApiRequest = (method: string, url: string, status: number, duration: number) =>
  logger.apiRequest(method, url, status, duration);

export const logApiError = (method: string, url: string, err: Error) =>
  logger.apiError(method, url, err);

export const logUserAction = (action: string, details?: Record<string, any>) =>
  logger.userAction(action, details);

export default logger;
