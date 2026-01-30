#!/usr/bin/env node

/**
 * DesignAudit AI - Project Validation
 * Checks that all required files and configurations are in place
 */

const fs = require('fs');
const path = require('path');

const ROOT = __dirname;

// Color codes
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[36m',
};

function log(msg, type = 'info') {
  const symbol = {
    pass: `${colors.green}✓${colors.reset}`,
    fail: `${colors.red}✗${colors.reset}`,
    warn: `${colors.yellow}⚠${colors.reset}`,
    info: `${colors.blue}ℹ${colors.reset}`,
  };
  const prefix = symbol[type] || '';
  console.log(`${prefix} ${msg}`);
}

function checkFile(filePath) {
  const fullPath = path.join(ROOT, filePath);
  return fs.existsSync(fullPath);
}

function checkDir(dirPath) {
  const fullPath = path.join(ROOT, dirPath);
  return fs.existsSync(fullPath) && fs.statSync(fullPath).isDirectory();
}

function getFileSize(filePath) {
  const fullPath = path.join(ROOT, filePath);
  if (fs.existsSync(fullPath)) {
    const stats = fs.statSync(fullPath);
    return stats.size;
  }
  return 0;
}

async function validate() {
  console.log('\n📋 DesignAudit AI - Project Validation\n');
  console.log(`Location: ${ROOT}\n`);

  let passed = 0;
  let failed = 0;
  let warnings = 0;

  // Frontend checks
  console.log(`${colors.blue}Frontend:${colors.reset}`);
  const frontendFiles = [
    'frontend/package.json',
    'frontend/tsconfig.json',
    'frontend/tailwind.config.js',
    'frontend/postcss.config.js',
    'frontend/next.config.js',
    'frontend/app/globals.css',
    'frontend/app/layout.tsx',
    'frontend/app/page.tsx',
    'frontend/app/audit/[id]/page.tsx',
    'frontend/app/store/audit.ts',
    'frontend/app/lib/api.ts',
    'frontend/app/lib/utils.ts',
    'frontend/app/components/UploadForm.tsx',
    'frontend/app/components/AuditReport.tsx',
    'frontend/app/components/ChatInterface.tsx',
  ];

  for (const file of frontendFiles) {
    if (checkFile(file)) {
      log(`${file.split('/').pop()}`, 'pass');
      passed++;
    } else {
      log(`${file.split('/').pop()}`, 'fail');
      failed++;
    }
  }

  // Backend checks
  console.log(`\n${colors.blue}Backend:${colors.reset}`);
  const backendFiles = [
    'backend/main.py',
    'backend/config.py',
    'backend/models.py',
    'backend/database.py',
    'backend/tasks.py',
    'backend/requirements.txt',
    'backend/Dockerfile',
    'backend/routes/audits.py',
    'backend/services/audit.py',
    'backend/services/storage.py',
  ];

  for (const file of backendFiles) {
    if (checkFile(file)) {
      log(`${file.split('/').pop()}`, 'pass');
      passed++;
    } else {
      log(`${file.split('/').pop()}`, 'fail');
      failed++;
    }
  }

  // Agents checks
  console.log(`\n${colors.blue}AI Agents:${colors.reset}`);
  const agentFiles = [
    'agents/orchestrator.py',
    'agents/inspector/vision_analyzer.py',
    'agents/analyst/rules_engine.py',
    'agents/advisor/feedback_generator.py',
  ];

  for (const file of agentFiles) {
    if (checkFile(file)) {
      log(`${file.split('/').pop()}`, 'pass');
      passed++;
    } else {
      log(`${file.split('/').pop()}`, 'fail');
      failed++;
    }
  }

  // Documentation checks
  console.log(`\n${colors.blue}Documentation:${colors.reset}`);
  const docFiles = [
    'README.md',
    'BLUEPRINT.md',
    'QUICK_START.md',
    'GETTING_STARTED.md',
    'COMPLETION_REPORT.md',
    'docker-compose.yml',
    '.env.example',
  ];

  for (const file of docFiles) {
    if (checkFile(file)) {
      log(`${file}`, 'pass');
      passed++;
    } else {
      log(`${file}`, 'fail');
      failed++;
    }
  }

  // Setup scripts
  console.log(`\n${colors.blue}Setup Scripts:${colors.reset}`);
  const scripts = [
    'setup.sh',
    'setup.bat',
    'dev.js',
  ];

  for (const script of scripts) {
    if (checkFile(script)) {
      log(`${script}`, 'pass');
      passed++;
    } else {
      log(`${script}`, 'fail');
      failed++;
    }
  }

  // Directory checks
  console.log(`\n${colors.blue}Directories:${colors.reset}`);
  const dirs = [
    'frontend/app',
    'frontend/app/components',
    'frontend/app/lib',
    'frontend/app/store',
    'frontend/app/audit',
    'backend/routes',
    'backend/services',
    'agents/inspector',
    'agents/analyst',
    'agents/advisor',
    'docs',
  ];

  for (const dir of dirs) {
    if (checkDir(dir)) {
      log(`${dir}`, 'pass');
      passed++;
    } else {
      log(`${dir}`, 'fail');
      failed++;
    }
  }

  // Environment checks
  console.log(`\n${colors.blue}Environment:${colors.reset}`);
  if (checkFile('.env')) {
    log('.env exists', 'pass');
    passed++;
  } else {
    log('.env missing (run: cp .env.example .env)', 'warn');
    warnings++;
  }

  // Dependencies checks
  console.log(`\n${colors.blue}Dependencies:${colors.reset}`);
  
  if (checkDir('frontend/node_modules')) {
    log('Frontend node_modules installed', 'pass');
    passed++;
  } else {
    log('Frontend dependencies not installed (run: npm install)', 'warn');
    warnings++;
  }

  if (checkDir('backend/venv') || checkFile('backend/venv/pyvenv.cfg')) {
    log('Backend venv created', 'pass');
    passed++;
  } else {
    log('Backend venv not created (run: python -m venv venv)', 'warn');
    warnings++;
  }

  // Summary
  console.log(`\n${colors.blue}Summary:${colors.reset}`);
  console.log(`${colors.green}Passed: ${passed}${colors.reset}`);
  if (warnings > 0) console.log(`${colors.yellow}Warnings: ${warnings}${colors.reset}`);
  if (failed > 0) console.log(`${colors.red}Failed: ${failed}${colors.reset}`);

  // Recommendations
  if (failed === 0 && warnings === 0) {
    console.log(`\n${colors.green}✓ All checks passed! Project is ready.${colors.reset}`);
    console.log('\nNext steps:');
    console.log('1. Update .env with your API keys');
    console.log('2. Run: node dev.js start');
    console.log('3. Open: http://localhost:3000');
    return 0;
  } else if (failed === 0) {
    console.log(`\n${colors.yellow}⚠ Some setup incomplete. Run setup script:${colors.reset}`);
    console.log('  node dev.js setup');
    return 0;
  } else {
    console.log(`\n${colors.red}✗ Some files missing. Check installation.${colors.reset}`);
    return 1;
  }
}

validate().then(code => process.exit(code));
