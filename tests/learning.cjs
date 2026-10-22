// Run after python build.py: node tests/learning.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('site/index.html', 'utf8');
const data = JSON.parse(html.match(/<script id="site-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const app = fs.readFileSync('template.html', 'utf8');
const learning = fs.readFileSync('learning.js', 'utf8');
function source(text, name, indent) {
  const start = text.indexOf(indent + 'function ' + name + '(');
  assert.ok(start >= 0, name);
  return text.slice(start, text.indexOf('\n' + indent + '}', start) + indent.length + 2);
}
const elements = {};
const context = {
  DATA: data, R: data.routes, LEVELS: data.levels, state: {},
  DONEABLE: Object.fromEntries(data.doneable.map(id => [id, true])),
  RESBYID: Object.fromEntries(data.resources.map(r => [r.id, r])),
  GATES: data.gates, TASKS: data.tasks, IV: data.interview,
  APP_ID: 'ai-agent-engineering-guide', track: 'core',
  inTrack: () => true, save() {}, updateProgress() {},
  document: {getElementById: id => elements[id] ||= {}},
  view: {innerHTML: ''},
  countedPages: () => data.levels.flatMap(l => l.modules.concat(l.project)).concat('capstone')
};
vm.createContext(context);
vm.runInContext(['esc','validId','tickedIds','describe','backupJson','setTick','renderDone','isDone'].map(n => source(app,n,'  ')).join('\n'),context);
vm.runInContext(['bookmarkKey','bookmarkButton','validLearningKey','masteryControls','masterySummary','priorityFor','listMarkup','recommendLevel','renderProjects'].map(n=>source(learning,n,'')).join('\n'),context);
// Earliest prerequisite gap wins, even with advanced experience elsewhere.
for (let mask = 0; mask < 64; mask++) {
  const answers = Array.from({length:6},(_,i)=>mask & (1<<i) ? 'yes':'no');
  const expected = answers[0]!=='yes'||answers[1]!=='yes' ? 'L0' : 'L'+Math.min(answers.slice(2).findIndex(v=>v!=='yes')===-1 ? 5 : answers.slice(2).findIndex(v=>v!=='yes')+1,5);
  assert.equal(context.recommendLevel(answers),expected);
}
const pid = data.doneable[0], resource = data.resources[0];
context.state[pid+'-done'] = true; // Existing users keep completion; no invented mastery.
let controls = context.masteryControls(pid);
assert.match(controls,/data-stage="read"[^>]*aria-pressed="false"/);
assert.match(controls,/data-stage="practiced"[^>]*aria-pressed="false"/);
assert.match(controls,/data-stage="done"[^>]*aria-pressed="true"/);
context.setTick(pid+'-read',true);
context.setTick(pid+'-practiced',true);
context.setTick(pid+'-done',false);
assert.equal(context.state[pid+'-read'],true);
assert.equal(context.state[pid+'-practiced'],true);
assert.equal(context.isDone(pid),false);
context.setTick(context.bookmarkKey('page',pid),true);
context.setTick(context.bookmarkKey('res',resource.id),true);
context.state['nonexistent-read']=true;
context.state['bookmark:page:nonexistent']=true;
context.state['bookmark:res:nonexistent']=true;
const backup=JSON.parse(context.backupJson());
assert.equal(backup.version,2);
assert.equal(backup.checks.length,4);
for(const key of backup.checks) assert.equal(context.validId(key),true);
assert.equal(context.validId(pid+'-done'),true); // v1 completion keys still restore.
assert.match(context.describe(backup.checks),/2 learning stages and 2 bookmarks/);
context.state={};
for(const key of backup.checks.filter(context.validId)) context.setTick(key,true);
assert.match(context.bookmarkButton('page',pid,data.routes[pid].t),/aria-pressed="true"/);
context.setTick(context.bookmarkKey('page',pid),false);
assert.match(context.bookmarkButton('page',pid,data.routes[pid].t),/aria-pressed="false"/);
const mixed={uses:[['a','Start here'],['b','Reference']]};
assert.equal(context.priorityFor(mixed,'a'),'Essential');
assert.equal(context.priorityFor(mixed,'b'),'Reference');
assert.equal(context.priorityFor(mixed),'Essential in a module');
context.renderProjects();
assert.equal((context.view.innerHTML.match(/class="showcase-card"/g)||[]).length,8);
for(const level of data.levels) assert.ok(context.view.innerHTML.includes('href="#'+level.project+'"'));
for(const [id,brief] of Object.entries(data.learning)) {
  assert.ok(brief.effort && brief.practice.length,id);
  if(brief.prerequisite) assert.ok(data.routes[brief.prerequisite],id+' prerequisite');
  if(brief.deliverables) assert.ok(brief.deliverables.length && brief.criteria.length,id);
  else assert.ok(brief.outcomes.length,id);
}
console.log('Learning checks passed: 64 assessment combinations, independent stages, legacy completion keys, backup round trip, bookmarks, contextual priorities, all 8 projects and 43 lesson briefs.');
