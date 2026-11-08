#!/usr/bin/env node
import { openAsBlob } from 'node:fs';
import { readFile as read } from 'node:fs/promises';
import { basename } from 'node:path';
import { AgntiaClient } from '../dist/client.js';
import { createAgntiaTools } from '../dist/agents.js';

const [command = 'help', name, input = '{}'] = process.argv.slice(2);
if (command === 'help') {
  console.log('pnpm agntia tools | call <tool_name> <json-or-@file> | upload <project_id> <file>');
  console.log('Set AGNTIA_BASE_URL and AGNTIA_ACCESS_TOKEN in the process environment. Never put tokens in commands.');
} else {
  try {
    const client = new AgntiaClient({ baseUrl: process.env.AGNTIA_BASE_URL || 'http://127.0.0.1:8000', token: process.env.AGNTIA_ACCESS_TOKEN });
    const tools = createAgntiaTools(client);
    let result;
    if (command === 'tools') result = tools.definitions;
    else if (command === 'call' && name) result = await tools.execute(name, JSON.parse(input.startsWith('@') ? await read(input.slice(1), 'utf8') : input));
    else if (command === 'upload' && name && input !== '{}') result = await client.upload(name, await openAsBlob(input), basename(input));
    else throw new Error('Unknown command. Run pnpm agntia help.');
    console.log(JSON.stringify(result, null, 2));
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
