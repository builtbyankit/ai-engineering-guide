/* Included inside the app closure by build.py. Shares the existing progress store. */
function bookmarkKey(kind, id) { return "bookmark:" + kind + ":" + id; }
function bookmarkButton(kind, id, title) {
  var key = bookmarkKey(kind, id), saved = !!state[key];
  return '<button type="button" class="bookmark-btn" data-bookmark="' + esc(key) + '" aria-pressed="' + saved + '" aria-label="' + esc((saved ? 'Unsave ' : 'Save ') + title) + '">' + (saved ? '★ Saved' : '☆ Save for later') + '</button>';
}
function validLearningKey(id) {
  var match = id.match(/^(.+)-(read|practiced)$/);
  if (match) return !!DONEABLE[match[1]];
  match = id.match(/^bookmark:(page|res):(.+)$/);
  return !!(match && (match[1] === 'page' ? Object.prototype.hasOwnProperty.call(R, match[2]) && !['saved','assessment','projects','progress','resources'].includes(match[2]) : Object.prototype.hasOwnProperty.call(RESBYID, match[2])));
}
function masteryControls(pid) {
  return '<div class="mastery-actions" role="group" aria-label="Learning stages">' + [
    ['read', 'Read', 'I have read and understood the lesson'],
    ['practiced', 'Practiced', 'I have attempted the practical exercises'],
    ['done', 'Completed', 'I meet the readiness or project completion criteria']
  ].map(function (stage) {
    return '<button type="button" class="btn-quiet" data-stage="' + stage[0] + '" data-stage-page="' + pid + '" aria-pressed="' + !!state[pid + '-' + stage[0]] + '" title="' + stage[2] + '">' + (state[pid + '-' + stage[0]] ? '✓ ' : '') + stage[1] + '</button>';
  }).join('') + '</div>';
}
function masterySummary() {
  var pages = countedPages();
  return '<section class="mastery-summary" aria-label="Learning stages"><h2>Reading is a start. Practice makes it stick.</h2><p>Stages are independent and self-reported. Existing completed pages keep their status; reading and practice are never inferred.</p><div class="mastery-counts">' + [['read','Read'],['practiced','Practiced'],['done','Completed']].map(function (stage) {
    return '<span><strong>' + pages.filter(function (pid) { return !!state[pid + '-' + stage[0]]; }).length + '</strong> / ' + pages.length + ' ' + stage[1] + '</span>';
  }).join('') + '</div></section>';
}
function priorityFor(r, pid) {
  var uses = r.uses.filter(function (u) { return !pid || u[0] === pid; });
  if (uses.some(function (u) { return u[1] === 'Start here'; })) return pid ? 'Essential' : 'Essential in a module';
  if (uses.some(function (u) { return u[1] === 'Go deeper'; })) return 'Optional deep dive';
  if (uses.some(function (u) { return u[1] === 'Reference'; })) return 'Reference';
  return 'Project / interview companion';
}
function addResourceTools(root, pid) {
  root.querySelectorAll('li.res').forEach(function (li) {
    if (li.querySelector('.resource-tools')) return;
    var id = li.getAttribute('data-res'), r = RESBYID[id];
    if (!r) return;
    var essential = r.uses.some(function (u) { return (!pid || u[0] === pid) && u[1] === 'Start here'; });
    li.dataset.essential = String(essential);
    li.querySelector('.res-body').insertAdjacentHTML('beforeend', '<div class="resource-tools"><span class="priority-badge' + (essential ? ' essential' : '') + '">' + priorityFor(r, pid) + '</span>' + bookmarkButton('res', id, r.title) + '</div>');
  });
}
function listMarkup(items) { return '<ul>' + items.map(function (text) { return '<li>' + esc(text) + '</li>'; }).join('') + '</ul>'; }
function addLessonOverview(id) {
  var brief = (DATA.learning || {})[id], header = view.querySelector('.page-head');
  if (!header || !R[id]) return;
  if (!['saved','assessment','projects','progress','resources'].includes(id)) header.insertAdjacentHTML('beforeend', '<div class="page-tools">' + bookmarkButton('page', id, R[id].t) + '</div>');
  if (!brief) { addResourceTools(view, id); return; }
  var pre = brief.prerequisite;
  var prereq = pre && R[pre] ? '<a href="#' + pre + '">' + esc(R[pre].t) + '</a>' : 'A little programming experience in any language. No AI background needed.';
  var html = '<section class="lesson-overview" aria-label="Lesson at a glance"><div class="lesson-facts"><div><span class="eyebrow">BEFORE YOU BEGIN</span><p>' + prereq + '</p></div><div><span class="eyebrow">ESTIMATED EFFORT</span><p>' + esc(brief.effort) + '</p><small>Includes learning and hands-on work.</small></div></div>';
  if (brief.outcomes.length) html += '<h2>What you’ll be able to do</h2>' + listMarkup(brief.outcomes);
  if (brief.practice.length) html += '<details class="practice-preview"><summary>Your first practical task</summary>' + listMarkup(brief.practice) + '</details>';
  if (brief.deliverables && brief.deliverables.length) html += '<details><summary>What you’ll ship</summary>' + listMarkup(brief.deliverables) + '</details>';
  html += '<p class="overview-note">Use the full practice, checklist and readiness criteria below before marking this page complete.</p></section>';
  header.insertAdjacentHTML('afterend', html);
  addResourceTools(view, id);
  var resourceLists = view.querySelectorAll('.res-list');
  if (R[id].k === 'module' && resourceLists.length) {
    resourceLists[0].insertAdjacentHTML('beforebegin', '<div class="resource-priority-control"><label><input type="checkbox" id="essential-only"> Focus on essential resources</label><p>Start with the Essential picks. Deep dives and reference material are optional; practice and checklists stay visible.</p><span id="essential-status" role="status"></span></div>');
    document.getElementById('essential-only').addEventListener('change', function (e) {
      var visible = 0;
      view.querySelectorAll('li.res').forEach(function (li) { li.hidden = e.target.checked && li.dataset.essential !== 'true'; if (!li.hidden) visible++; });
      document.getElementById('essential-status').textContent = visible + ' resources shown';
    });
  }
}
var assessmentQuestions = [
  'Can you write and test Python code using functions, collections, exceptions and JSON?',
  'Can you build an API and work with HTTP, SQL, Git and Docker?',
  'Can you explain tokens and sampling, call an LLM, validate structured output and run basic evals?',
  'Have you built and evaluated a RAG pipeline with chunking, embeddings and retrieval?',
  'Can you build a tool-calling agent with bounded execution, memory and approval steps?',
  'Have you built stateful agent workflows and handled retries, handoffs and human review?'
];
function recommendLevel(answers) {
  if (answers[0] !== 'yes' || answers[1] !== 'yes') return 'L0';
  if (answers[2] !== 'yes') return 'L1';
  if (answers[3] !== 'yes') return 'L2';
  if (answers[4] !== 'yes') return 'L3';
  if (answers[5] !== 'yes') return 'L4';
  return 'L5';
}
function renderAssessment() {
  view.innerHTML = '<header class="page-head"><p class="eyebrow">YOUR EXPERIENCE, YOUR PATH</p><h1 tabindex="-1">Find your starting point</h1><p class="standfirst">Six quick self-checks. Choose “Not yet” if you would need a tutorial to do it independently. This recommends a starting level; it does not certify mastery or mark anything complete.</p></header><form id="assessment-form" class="assessment-form">' + assessmentQuestions.map(function (q, i) {
    return '<fieldset><legend><span>' + (i + 1) + ' / 6</span> ' + esc(q) + '</legend><div class="assessment-options"><label><input type="radio" required name="skill-' + i + '" value="yes"> Yes, independently</label><label><input type="radio" required name="skill-' + i + '" value="no"> Not yet / unsure</label></div></fieldset>';
  }).join('') + '<button class="btn" type="submit">Show my starting point →</button></form><section id="assessment-result" class="assessment-result" hidden tabindex="-1" aria-live="polite"></section>';
  document.getElementById('assessment-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var answers = assessmentQuestions.map(function (_, i) { return new FormData(e.target).get('skill-' + i); });
    var lid = recommendLevel(answers), level = LEVELS.find(function (l) { return l.id === lid; });
    var target = level.modules[0], result = document.getElementById('assessment-result');
    result.hidden = false;
    result.innerHTML = '<p class="eyebrow">SUGGESTED START</p><h2>Level ' + level.num + ': ' + esc(level.t) + '</h2><p>' + esc(R[lid].sum || '') + '</p><p>' + (lid === 'L0' ? 'Build confidence in Python and backend fundamentals first.' : 'Start at the first area you have not yet built independently. Review earlier milestones if you find gaps.') + '</p><div class="backup-row"><button type="button" class="btn" id="use-start">Start here →</button><a class="btn-quiet" href="#' + lid + '">Preview this level</a></div><p>Your existing progress stays intact. You can change paths or revisit earlier levels at any time.</p>';
    document.getElementById('use-start').addEventListener('click', function () {
      applyTrack('core', true);
      store('ai-agent-guide:last-page', target);
      location.hash = target;
    });
    result.focus();
  });
}
function renderProjects() {
  var projects = LEVELS.map(function (l) { return l.project; }).concat(['capstone']);
  view.innerHTML = '<header class="page-head"><p class="eyebrow">LEARN BY SHIPPING</p><h1 tabindex="-1">Your project portfolio</h1><p class="standfirst">Eight projects that turn concepts into working software. Explore the expected deliverables and requirements, then use each project’s full rubric to judge your result.</p></header><div class="project-showcase">' + projects.map(function (id) {
    var p = R[id], brief = DATA.learning[id];
    return '<section class="showcase-card"><p class="eyebrow">' + esc(p.e) + ' · ' + esc(brief.effort) + '</p><h2><a href="#' + id + '">' + esc(p.t) + '</a></h2><p>' + esc(p.sum) + '</p><h3>Expected output</h3>' + listMarkup(brief.deliverables || []) + '<details><summary>Completion criteria preview</summary>' + listMarkup(brief.criteria || []) + '<p>These are a preview. Complete the full requirements and review the evaluation rubric on the project page.</p></details><div class="backup-row"><a class="btn" href="#' + id + '">Explore project →</a>' + bookmarkButton('page', id, p.t) + '</div></section>';
  }).join('') + '</div>';
}
function renderSaved() {
  var pages = Object.keys(R).filter(function (id) { return state[bookmarkKey('page', id)]; });
  var resources = RES.filter(function (r) { return state[bookmarkKey('res', r.id)]; });
  view.innerHTML = '<header class="page-head"><p class="eyebrow">YOUR REVISION SHELF</p><h1 tabindex="-1">Saved for later</h1><p class="standfirst">Keep useful lessons and resources close. Bookmarks are stored in this browser and included in your progress backup.</p></header><div class="prose"><h2>Lessons and projects (' + pages.length + ')</h2>' + (pages.length ? '<ul class="saved-pages">' + pages.map(function (id) { return '<li><div><a href="#' + id + '">' + esc(R[id].t) + '</a><p>' + esc(R[id].sum || '') + '</p></div>' + bookmarkButton('page', id, R[id].t) + '</li>'; }).join('') + '</ul>' : '<p>No pages saved yet. Use “Save for later” on a lesson or project. <a href="#home">Explore the learning path</a>.</p>') + '<h2>Resources (' + resources.length + ')</h2>' + (resources.length ? '<ul class="res-list">' + resources.map(resCard).join('') + '</ul>' : '<p>No resources saved yet. <a href="#resources">Browse the resource library</a> to find your first pick.</p>') + '</div>';
  wireTicks(view);
  addResourceTools(view);
  updateProgress();
}
function syncLearningUI() {
  document.querySelectorAll('[data-bookmark]').forEach(function (button) {
    var key = button.dataset.bookmark, saved = !!state[key];
    var parts = key.split(':'), item = parts[1] === 'res' ? RESBYID[parts[2]] : R[parts[2]];
    button.setAttribute('aria-pressed', String(saved));
    button.textContent = saved ? '★ Saved' : '☆ Save for later';
    button.setAttribute('aria-label', (saved ? 'Unsave ' : 'Save ') + (item ? item.t || item.title : 'item'));
  });
  var summary = document.getElementById('mastery-summary');
  if (summary) summary.innerHTML = masterySummary();
}
document.addEventListener('click', function (e) {
  var button = e.target.closest('[data-bookmark]');
  if (button) {
    var key = button.dataset.bookmark;
    if (!validLearningKey(key)) return;
    setTick(key, !state[key]);
    document.getElementById('learning-status').textContent = state[key] ? 'Saved for later.' : 'Removed from saved items.';
    if (currentId() === 'saved') { renderSaved(); view.querySelector('h1').focus(); }
    return;
  }
  button = e.target.closest('[data-stage]');
  if (!button) return;
  var pid = button.dataset.stagePage, stage = button.dataset.stage;
  if (!DONEABLE[pid] || !['read','practiced','done'].includes(stage)) return;
  setTick(pid + '-' + stage, !state[pid + '-' + stage]);
  var next = view.querySelector('[data-stage="' + stage + '"][data-stage-page="' + pid + '"]');
  if (next) next.focus();
  document.getElementById('learning-status').textContent = 'Learning stage updated.';
});
// Keep keyboard focus inside the mobile navigation and make its background inert.
document.addEventListener('keydown', function (e) {
  if (e.key !== 'Tab' || sidebar.getAttribute('data-open') !== 'true') return;
  var focusable = Array.from(sidebar.querySelectorAll('a[href], button, input')).filter(function (el) { return !el.disabled && el.getClientRects().length; });
  var first = focusable[0], last = focusable[focusable.length - 1];
  if (!first) return;
  if (e.shiftKey && (document.activeElement === first || !sidebar.contains(document.activeElement))) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && (document.activeElement === last || !sidebar.contains(document.activeElement))) { e.preventDefault(); first.focus(); }
});
