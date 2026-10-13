import { spawn } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import net from 'node:net';
import { join } from 'node:path';

export const REQUIRED_NODE = '22.23.1';
export const REQUIRED_CLI = '4.9.0';

export function readPreviewConfiguration(root) {
  const text = readFileSync(join(root, 'shopify.theme.toml'), 'utf8');
  const section = text.match(/^\[environments\.dev\]\s*\r?\n([\s\S]*?)(?=^\[|$(?![\s\S]))/m);
  if (!section) throw new Error('Missing [environments.dev] in shopify.theme.toml. No Shopify command started.');
  const config = {};
  for (const line of section[1].split(/\r?\n/)) {
    if (!line.trim() || line.trim().startsWith('#')) continue;
    const match = line.match(/^\s*(store|host|port)\s*=\s*(?:"([^"\r\n]*)"|(\d+))\s*(?:#.*)?$/);
    if (!match || Object.hasOwn(config, match[1])) throw new Error('The dev environment must contain only one store, host and port; no theme, credential or account override.');
    config[match[1]] = match[2] ?? Number(match[3]);
  }
  if (!/^[a-z0-9][a-z0-9-]*\.myshopify\.com$/.test(config.store ?? '') || config.host !== '127.0.0.1' || !Number.isInteger(config.port) || config.port < 1024 || config.port > 65535) {
    throw new Error('Invalid dev store/host/port. Expected a myshopify.com store, 127.0.0.1 and a fixed nonprivileged port.');
  }
  return config;
}

export function resolvePreviewCli(root, nodeVersion = process.versions.node) {
  if (nodeVersion !== REQUIRED_NODE) throw new Error(`Use the project Node ${REQUIRED_NODE} pin in this terminal; current Node is ${nodeVersion}. No global runtime or authentication change was attempted.`);
  const packagePath = join(root, 'node_modules', '@shopify', 'cli', 'package.json');
  const entry = join(root, 'node_modules', '@shopify', 'cli', 'bin', 'run.js');
  if (!existsSync(packagePath) || !existsSync(entry)) throw new Error('Project Shopify CLI is missing. Install the locked dependencies with lifecycle hooks disabled; no global or npx fallback was attempted.');
  const installed = JSON.parse(readFileSync(packagePath, 'utf8'));
  const declared = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8'));
  if (installed.version !== REQUIRED_CLI || declared.devDependencies?.['@shopify/cli'] !== REQUIRED_CLI) throw new Error(`Project Shopify CLI must be exactly ${REQUIRED_CLI}; no automatic upgrade or fallback was attempted.`);
  return { version: installed.version, entry };
}

export function rejectTargetOverrides(env, config) {
  const expected = { SHOPIFY_FLAG_STORE: config.store, SHOPIFY_FLAG_HOST: config.host, SHOPIFY_FLAG_PORT: String(config.port), SHOPIFY_FLAG_ENVIRONMENT: 'dev' };
  for (const name of ['SHOPIFY_FLAG_STORE', 'SHOPIFY_FLAG_HOST', 'SHOPIFY_FLAG_PORT', 'SHOPIFY_FLAG_ENVIRONMENT', 'SHOPIFY_FLAG_THEME_ID', 'SHOPIFY_FLAG_THEME', 'SHOPIFY_FLAG_AUTH_ALIAS', 'SHOPIFY_FLAG_THEME_EDITOR_SYNC', 'SHOPIFY_FLAG_ALLOW_LIVE', 'SHOPIFY_FLAG_FORCE']) {
    if (env[name] && (!Object.hasOwn(expected, name) || String(env[name]) !== expected[name])) throw new Error(`Conflicting inherited ${name}. Clear that variable only in this project terminal after reviewing its purpose. No Shopify command started; its value was not printed.`);
  }
}

export function previewChildEnvironment(parent, config, { unattended = false, interactionParent = parent } = {}) {
  rejectTargetOverrides(parent, config);
  const env = { ...parent, SHOPIFY_CLI_NO_ANALYTICS: '1' };
  for (const name of ['SHOPIFY_FLAG_STORE','SHOPIFY_FLAG_HOST','SHOPIFY_FLAG_PORT','SHOPIFY_FLAG_ENVIRONMENT','SHOPIFY_FLAG_THEME_ID','SHOPIFY_FLAG_THEME','SHOPIFY_FLAG_AUTH_ALIAS','SHOPIFY_FLAG_THEME_EDITOR_SYNC','SHOPIFY_FLAG_ALLOW_LIVE','SHOPIFY_FLAG_FORCE','SHOPIFY_FLAG_VERBOSE']) delete env[name];
  // Manual npm launches inherit their terminal's interaction settings. Project
  // credential adapters must not silently turn that terminal into CI either.
  for (const name of ['CI', 'CLOUD_SHELL', 'SHOPIFY_FLAG_NO_INPUT', 'SHOPIFY_FLAG_OPEN']) {
    if (interactionParent[name] === undefined) delete env[name];
    else env[name] = interactionParent[name];
  }
  if (env.SHOPIFY_FLAG_OPEN === undefined) env.SHOPIFY_FLAG_OPEN = 'false';
  if (unattended) Object.assign(env, { CI:'true', CLOUD_SHELL:'true', SHOPIFY_FLAG_OPEN:'false', SHOPIFY_FLAG_NO_INPUT:'true' });
  return env;
}

// Preserve TinyRigCo's existing optional token source, only for an explicitly
// invoked real launch. Offline dry-run never opens a filled environment file.
export function optionalDotEnv(root, parent) {
  const env = { ...parent };
  const file = join(root, '.env');
  if (!existsSync(file)) return env;
  for (const line of readFileSync(file, 'utf8').split(/\r?\n/)) {
    const match = line.trim().match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/);
    if (!match) continue;
    let value = match[2];
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) value = value.slice(1, -1);
    if (env[match[1]] === undefined) env[match[1]] = value;
  }
  return env;
}

export function probePort(port, host) {
  return new Promise((resolve, reject) => {
    const probe = net.createServer();
    probe.once('error', error => reject(new Error(`Preview port ${port} is unavailable (${error.code}). Reuse the existing preview; no second process or authentication started.`)));
    probe.listen({ port, host, exclusive: true }, () => probe.close(error => error ? reject(error) : resolve()));
  });
}

export function preparePreview(root, { argv = process.argv.slice(2), env = process.env, nodeVersion = process.versions.node } = {}) {
  if (argv.includes('--force-reauth')) throw new Error('Automatic reauthentication is disabled. Request a separate explicit authentication task; no shared sessions were read, deleted or changed.');
  if (argv.some(arg => !['--dry-run','--unattended'].includes(arg)) || new Set(argv).size !== argv.length) throw new Error('Only --dry-run and --unattended are accepted. Store, Development-theme selection, host and port are fixed by [environments.dev].');
  const config = readPreviewConfiguration(root);
  rejectTargetOverrides(env, config);
  const cli = resolvePreviewCli(root, nodeVersion);
  const unattended = argv.includes('--unattended');
  const args = ['theme', 'dev', '--environment=dev', `--store=${config.store}`, `--host=${config.host}`, `--port=${config.port}`];
  if (unattended) args.push('--no-input');
  return { root, config, cli, args, dryRun: argv.includes('--dry-run'), unattended };
}

export function printPreviewPlan(plan, output = process.stdout) {
  output.write(`${JSON.stringify({ node: process.versions.node, executable: process.execPath, cli: plan.cli.version, cliEntry: plan.cli.entry, cwd: plan.root, store: plan.config.store, theme: 'CLI Development theme (no theme ID override)', host: plan.config.host, port: plan.config.port, environment: 'dev', dryRun: plan.dryRun, unattended: plan.unattended })}\n`);
}

export function spawnPreview(plan, env, spawnProcess = spawn) {
  return new Promise((resolve, reject) => {
    const child = spawnProcess(process.execPath, [plan.cli.entry, ...plan.args], { cwd: plan.root, env, stdio: 'inherit', shell: false });
    child.once('error', reject);
    child.once('exit', (code, signal) => {
      if (signal) { process.stderr.write(`Shopify CLI exited with signal ${signal}.\n`); resolve(signal === 'SIGINT' ? 130 : signal === 'SIGTERM' ? 143 : 1); }
      else resolve(code ?? 1);
    });
  });
}

export async function runPreview(root, { argv = process.argv.slice(2), env = process.env, beforeStart = () => {}, transformEnvironment = (_, child) => child, dotEnv = false, probe = probePort, spawnProcess = spawn, output = process.stdout } = {}) {
  const plan = preparePreview(root, { argv, env });
  printPreviewPlan(plan, output);
  if (plan.dryRun) return 0;
  beforeStart();
  await probe(plan.config.port, plan.config.host);
  const parent = dotEnv ? optionalDotEnv(root, env) : env;
  const transformed = transformEnvironment(plan.args, previewChildEnvironment(parent, plan.config, { unattended: plan.unattended }));
  const child = previewChildEnvironment(transformed, plan.config, { unattended: plan.unattended, interactionParent: parent });
  return spawnPreview(plan, child, spawnProcess);
}
