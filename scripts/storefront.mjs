import { fileURLToPath } from 'node:url';
import { runPreview } from './preview-runtime.mjs';
const root = fileURLToPath(new URL('../', import.meta.url));
try { process.exitCode = await runPreview(root); }
catch (error) { console.error(error.message); process.exitCode = 1; }
