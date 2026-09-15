#!/usr/bin/env node
/** 扫描：六人在 vault 中的全部相关文档（用于回答"是否用到了所有内容"） */
import fs from 'node:fs';
import path from 'node:path';

const VAULT = process.cwd();
const NAMES = ['赵问竹', '阳隽豪', '宋俊豪', '刘弈帆', '王麒睿', '郑森'];
const CATS = [
  ['问卷作答', /问卷/],
  ['本人书写(回忆/评价/自述)', /书面|回忆|自述|评价/],
  ['特征分析(性格/外貌/行为)', /特征分析|多维度|行为侧写|形象深度|描写素材|画像|侧写/],
  ['履历/时间线/成长', /履历|时间线|成长|生平|年表/],
  ['证据/核验', /证据|核验|核证|审计/],
];

function walk(dir, acc = []) {
  let entries = [];
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return acc; }
  for (const e of entries) {
    if (e.name.startsWith('.') || e.name === 'node_modules') continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, acc);
    else if (e.name.endsWith('.md')) acc.push(path.relative(VAULT, p).split(path.sep).join('/'));
  }
  return acc;
}

const all = walk(VAULT);
const summary = {};
for (const n of NAMES) {
  const hit = all.filter(f => f.includes(n));
  const groups = {};
  for (const f of hit) {
    let k = '其他';
    for (const [label, re] of CATS) if (re.test(f)) { k = label; break; }
    (groups[k] = groups[k] || []).push(f);
  }
  summary[n] = groups;
}

for (const n of NAMES) {
  const g = summary[n];
  const total = Object.values(g).reduce((s, a) => s + a.length, 0);
  console.log(`■ ${n}  相关文档 ${total} 篇`);
  for (const [label] of CATS) {
    const arr = g[label] || [];
    if (!arr.length) continue;
    console.log(`   [${label}] ${arr.length} 篇`);
    arr.slice(0, 3).forEach(f => console.log(`        · ${f}`));
  }
  const other = g['其他'] || [];
  if (other.length) {
    console.log(`   [其他] ${other.length} 篇`);
    other.slice(0, 3).forEach(f => console.log(`        · ${f}`));
  }
  console.log('');
}
fs.writeFileSync(path.join(VAULT, '..', 'mneme-web', 'ft-dataset-v5', 'vault-scan.json'), JSON.stringify(summary, null, 2));
