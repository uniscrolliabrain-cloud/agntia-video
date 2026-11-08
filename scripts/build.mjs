import { readdir, readFile, mkdir, writeFile } from 'node:fs/promises';
import { stripTypeScriptTypes } from 'node:module';
import { fileURLToPath } from 'node:url';

const root = new URL('../', import.meta.url);
await mkdir(new URL('dist/', root), { recursive: true });
for (const filename of await readdir(new URL('typescript/', root))) {
  if (!filename.endsWith('.ts')) continue;
  const source = await readFile(new URL(`typescript/${filename}`, root), 'utf8');
  const code = stripTypeScriptTypes(source, { mode: 'strip' }).replaceAll(/(from\s+['"]\.\/[^'"]+)\.ts(['"])/g, '$1.js$2');
  await writeFile(new URL(`dist/${filename.replace(/\.ts$/, '.js')}`, root), code);
}
console.log(`Agntia SDK built: ${fileURLToPath(new URL('dist/', root))}`);
