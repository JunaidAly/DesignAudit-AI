#!/usr/bin/env node

/**
 * DesignAudit AI - Development CLI
 * Convenient commands for common development tasks
 *
 * Usage: node dev.js <command>
 * Examples:
 *   node dev.js start        - Start all services
 *   node dev.js setup        - Install dependencies
 *   node dev.js backend      - Start only backend
 *   node dev.js frontend     - Start only frontend
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const ROOT = __dirname;
const BACKEND_DIR = path.join(ROOT, 'backend');
const FRONTEND_DIR = path.join(ROOT, 'frontend');

const commands = {
  setup: 'Install all dependencies',
  start: 'Start all services (Docker)',
  backend: 'Start backend only (manual)',
  frontend: 'Start frontend only (manual)',
  stop: 'Stop all Docker services',
  logs: 'View Docker service logs',
  db: 'Start PostgreSQL only',
  redis: 'Start Redis only',
  clean: 'Remove all node_modules and venv',
  env: 'Copy and setup .env file',
  help: 'Show this help message',
};

function log(msg, type = 'info') {
  const colors = {
    info: '\x1b[36m',    // Cyan
    success: '\x1b[32m', // Green
    error: '\x1b[31m',   // Red
    warn: '\x1b[33m',    // Yellow
    reset: '\x1b[0m'
  };
  const symbol = {
    info: 'ℹ ',
    success: '✓ ',
    error: '✗ ',
    warn: '⚠ '
  };
  console.log(`${colors[type]}${symbol[type]}${msg}${colors.reset}`);
}

function runCommand(cmd, args, options = {}) {
  return new Promise((resolve, reject) => {
    const proc = spawn(cmd, args, {
      stdio: 'inherit',
      shell: true,
      cwd: options.cwd || ROOT,
      ...options
    });
    
    proc.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Command failed with code ${code}`));
      }
    });
  });
}

async function main() {
  const cmd = process.argv[2] || 'help';

  try {
    switch (cmd) {
      case 'setup':
        log('Installing dependencies...');
        log('Backend dependencies...', 'info');
        if (process.platform === 'win32') {
          await runCommand('cmd', ['/c', 'pip install -r requirements.txt'], { cwd: BACKEND_DIR });
        } else {
          await runCommand('bash', ['-c', 'source venv/bin/activate && pip install -r requirements.txt'], { cwd: BACKEND_DIR });
        }
        log('Frontend dependencies...', 'info');
        await runCommand('npm', ['install'], { cwd: FRONTEND_DIR });
        log('Dependencies installed successfully!', 'success');
        break;

      case 'start':
        log('Starting services with Docker Compose...', 'info');
        await runCommand('docker-compose', ['up', '-d']);
        log('Services started! Open http://localhost:3000', 'success');
        break;

      case 'stop':
        log('Stopping Docker services...', 'info');
        await runCommand('docker-compose', ['down']);
        log('Services stopped.', 'success');
        break;

      case 'logs':
        log('Showing Docker logs...', 'info');
        await runCommand('docker-compose', ['logs', '-f']);
        break;

      case 'backend':
        log('Starting backend server...', 'info');
        log('Backend running at http://localhost:8000', 'success');
        if (process.platform === 'win32') {
          await runCommand('cmd', ['/c', 'venv\\Scripts\\activate && python main.py'], { cwd: BACKEND_DIR });
        } else {
          await runCommand('bash', ['-c', 'source venv/bin/activate && python main.py'], { cwd: BACKEND_DIR });
        }
        break;

      case 'frontend':
        log('Starting frontend development server...', 'info');
        log('Frontend running at http://localhost:3000', 'success');
        await runCommand('npm', ['run', 'dev'], { cwd: FRONTEND_DIR });
        break;

      case 'db':
        log('Starting PostgreSQL...', 'info');
        await runCommand('docker-compose', ['up', '-d', 'postgres']);
        log('PostgreSQL started on localhost:5432', 'success');
        break;

      case 'redis':
        log('Starting Redis...', 'info');
        await runCommand('docker-compose', ['up', '-d', 'redis']);
        log('Redis started on localhost:6379', 'success');
        break;

      case 'env':
        if (!fs.existsSync('.env')) {
          log('Creating .env file...', 'info');
          if (fs.existsSync('.env.example')) {
            fs.copyFileSync('.env.example', '.env');
            log('.env created from .env.example', 'success');
            log('Please update .env with your API keys', 'warn');
          }
        } else {
          log('.env already exists', 'warn');
        }
        break;

      case 'clean':
        log('Cleaning up...', 'info');
        const dirs = [
          path.join(FRONTEND_DIR, 'node_modules'),
          path.join(BACKEND_DIR, 'venv'),
          path.join(BACKEND_DIR, '__pycache__'),
          '.next'
        ];
        
        for (const dir of dirs) {
          if (fs.existsSync(dir)) {
            log(`Removing ${dir}...`, 'info');
            if (process.platform === 'win32') {
              await runCommand('rmdir', ['/s', '/q', dir]);
            } else {
              await runCommand('rm', ['-rf', dir]);
            }
          }
        }
        log('Cleanup complete!', 'success');
        break;

      case 'help':
      case '-h':
      case '--help':
        console.log('\n📋 DesignAudit AI - Development Commands\n');
        console.log('Usage: node dev.js <command>\n');
        console.log('Available commands:');
        Object.entries(commands).forEach(([cmd, desc]) => {
          console.log(`  ${cmd.padEnd(15)} - ${desc}`);
        });
        console.log('\nExamples:');
        console.log('  node dev.js start       # Start all services with Docker');
        console.log('  node dev.js setup       # Install dependencies');
        console.log('  node dev.js backend     # Start backend server only');
        console.log('  node dev.js frontend    # Start frontend server only');
        console.log('\nDocumentation:');
        console.log('  - GETTING_STARTED.md    # Complete setup guide');
        console.log('  - QUICK_START.md        # Quick reference');
        console.log('  - docs/API.md           # API documentation\n');
        break;

      default:
        log(`Unknown command: ${cmd}`, 'error');
        log(`Run 'node dev.js help' for available commands`, 'info');
        process.exit(1);
    }
  } catch (error) {
    log(error.message, 'error');
    process.exit(1);
  }
}

main();
