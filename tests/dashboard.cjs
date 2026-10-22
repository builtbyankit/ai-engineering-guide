// Run after python build.py: node tests/dashboard.cjs
// Exercise the real dashboard functions against the generated curriculum data.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('site/index.html', 'utf8');
const data = JSON.parse(html.match(/<script id="site-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const template = fs.readFileSync('template.html', 'utf8');
function functionSource(name) {
  const start = template.indexOf('  function ' + name + '(');
  assert.ok(start >= 0, name);
  return template.slice(start, template.indexOf('\n  }', start) + 4);
}
const elements = {};
const element = id => elements[id] ||= {style: {}};
const context = {
  LEVELS: data.levels, R: data.routes, state: {}, track: 'core', last: null,
  OPT: Object.fromEntries(data.optional.map(id => [id, true])),
  FAST: Object.fromEntries(data.fastSkip.map(id => [id, true])),
  document: {getElementById: element, querySelectorAll: selector => [element(selector)]},
  read: () => context.last,
  setAll: (selector, value) => { element(selector).textContent = value; }
};
vm.createContext(context);
vm.runInContext(['inTrack', 'countedPages', 'isDone', 'countDone', 'levelPages', 'pct', 'updateDashboard'].map(functionSource).join('\n'), context);
function update() { context.updateDashboard(); return element('continue-link'); }
assert.equal(update().href, '#l0-python-for-ai');
context.state['l0-python-for-ai-done'] = true;
assert.notEqual(update().href, '#l0-python-for-ai');
context.last = 'l3-agent-loop';
assert.equal(update().href, '#l3-agent-loop');
context.state['l3-agent-loop-done'] = true;
assert.notEqual(update().href, '#l3-agent-loop');
context.track = 'fast';
context.last = data.fastSkip[0];
assert.ok(!data.fastSkip.includes(update().href.slice(1)));
context.track = 'core';
context.last = data.optional[0];
assert.ok(!data.optional.includes(update().href.slice(1)));
context.track = 'full';
assert.equal(update().href, '#' + data.optional[0]);
context.last = 'unknown-old-route';
assert.doesNotThrow(update);
context.last = data.interview[0];
assert.notEqual(update().href, '#' + context.last);
for (const id of context.countedPages()) context.state[id + '-done'] = true;
assert.equal(update().href, '#interview');
for (const level of data.levels) assert.equal(element('[data-card-bar="' + level.id + '"]').style.width, '100%');
context.state = {};
assert.equal(update().href, '#l0-python-for-ai');
assert.equal(element('[data-card-bar="L0"]').style.width, '0%');
console.log('Dashboard checks passed: new learner, resume, completion, all three tracks, stale route, interview exclusion, complete path and reset.');
