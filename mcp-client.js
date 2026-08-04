const { spawn, execSync } = require('child_process');
const readline = require('readline');
const fs = require('fs');
const path = require('path');

class MCPClient {
  constructor() {
    this.pending = new Map();
    this.messageId = 1;
  }

  async start(chromePort = 9226) {
    // Start headless Chrome
    const userDataDir = path.join(require('os').tmpdir(), 'chrome-mcp-' + Date.now());
    fs.mkdirSync(userDataDir, { recursive: true });
    this.chromeProc = spawn(
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      [
        `--remote-debugging-port=${chromePort}`,
        `--user-data-dir=${userDataDir}`,
        '--no-first-run',
        '--headless=new',
        '--disable-gpu',
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
      ],
      { stdio: 'ignore' }
    );
    await new Promise((resolve, reject) => {
      let ready = false;
      const check = setInterval(() => {
        try { if (JSON.parse(execSync(`curl -s http://127.0.0.1:${chromePort}/json/version`, { timeout: 1000 })).Browser) { clearInterval(check); ready = true; resolve(); } }
        catch (e) {}
      }, 500);
      setTimeout(() => { if (!ready) { clearInterval(check); reject('timeout'); } }, 15000);
    });

    // Start MCP
    this.proc = spawn('npx', [
      'chrome-devtools-mcp@latest',
      '--browserUrl', `http://127.0.0.1:${chromePort}`,
      '--no-usage-statistics'
    ], { stdio: ['pipe', 'pipe', 'pipe'] });

    this.rl = readline.createInterface({ input: this.proc.stdout, terminal: false });
    this.rl.on('line', (line) => { try { const msg = JSON.parse(line); if (msg.id && this.pending.has(msg.id)) { const r = this.pending.get(msg.id); this.pending.delete(msg.id); r(msg.result || msg.error); } } catch(e){} });
    await new Promise(r => setTimeout(r, 3000));
    await this.send({ jsonrpc: '2.0', method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'test', version: '1.0' } } });
    this.proc.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) + '\n');
    await this.send({ jsonrpc: '2.0', method: 'tools/list', params: {} });

    // Create new page
    console.log('Creating page...');
    await this.send({ jsonrpc: '2.0', method: 'tools/call', params: { name: 'new_page', arguments: {} } });
    await new Promise(r => setTimeout(r, 2000));

    // List and select page
    var pages = await this.send({ jsonrpc: '2.0', method: 'tools/call', params: { name: 'list_pages', arguments: {} } });
    console.log('Pages:', JSON.stringify(pages));
    if (pages.content && pages.content[0].text) {
      var pm = pages.content[0].text.match(/url="([^"]+)"/);
      if (pm) {
        var pageUrl = pm[1];
        console.log('Selecting page:', pageUrl);
        await this.send({ jsonrpc: '2.0', method: 'tools/call', params: { name: 'select_page', arguments: { url: pageUrl } } });
      }
    }
  }

  send(msg) {
    const id = this.messageId++;
    return new Promise((resolve) => {
      this.pending.set(id, resolve);
      this.proc.stdin.write(JSON.stringify({ ...msg, id }) + '\n');
      setTimeout(() => { if (this.pending.has(id)) { this.pending.delete(id); resolve('timeout'); } }, 30000);
    });
  }

  async tool(name, args) { return this.send({ jsonrpc: '2.0', method: 'tools/call', params: { name, arguments: args } }); }
  stop() { if (this.proc) this.proc.kill(); if (this.chromeProc) this.chromeProc.kill(); }
}

function parseJson(text) {
  try { var m = text.match(/```json\n([\s\S]*?)\n```/); return m ? JSON.parse(m[1]) : null; } catch (e) { return null; }
}

async function main() {
  const client = new MCPClient();
  const results = [];
  try {
    await client.start(9226);

    // LINKEDIN - remote architekt
    console.log('\n=== LINKEDIN: architekt remote ===');
    await client.tool('navigate_page', { url: 'https://www.linkedin.com/jobs/search?keywords=architekt&location=Polska&f_WT=2' });
    await new Promise(r => setTimeout(r, 10000));

    var r = await client.tool('evaluate_script', {
      function: `() => {
        var jobs = [];
        var items = document.querySelectorAll('.jobs-search__results-list li, [data-job-id]');
        for (var i = 0; i < Math.min(items.length, 25); i++) {
          var el = items[i];
          var titleEl = el.querySelector('h3, .job-card-list__title');
          var title = titleEl ? titleEl.textContent.trim() : '';
          var companyEl = el.querySelector('h4, .base-search-card__subtitle');
          var company = companyEl ? companyEl.textContent.trim() : '';
          var locEl = el.querySelector('.job-search-card__location');
          var location = locEl ? locEl.textContent.trim() : '';
          var linkEl = el.querySelector('a');
          var link = linkEl ? linkEl.href : '';
          if (title.toLowerCase().indexOf('architekt') > -1) {
            jobs.push({ title: title, company: company, location: location, link: link });
          }
        }
        return jobs;
      }`
    });
    console.log('LinkedIn results:', JSON.stringify(r, null, 2));
    var linkedinJobs = parseJson(r.content ? r.content[0].text : '');

    // Check LinkedIn jobs for ArchiCAD
    if (Array.isArray(linkedinJobs)) {
      for (var k = 0; k < Math.min(linkedinJobs.length, 6); k++) {
        var lj = linkedinJobs[k];
        if (!lj.link) continue;
        console.log('\n--- LinkedIn checking: ' + lj.title + ' ---');
        await client.tool('navigate_page', { url: lj.link });
        await new Promise(r => setTimeout(r, 6000));
        r = await client.tool('evaluate_script', {
          function: `() => {
            var text = document.body.innerText.toLowerCase();
            var desc = document.querySelector('.description__text, .show-more-less-html__markup');
            return {
              hasArchicad: text.indexOf('archicad') > -1,
              hasRevit: text.indexOf('revit') > -1,
              snippet: desc ? desc.innerText.substring(0, 1500) : document.body.innerText.substring(0, 1500)
            };
          }`
        });
        var ld = parseJson(r.content ? r.content[0].text : '');
        console.log(JSON.stringify(ld));
        if (ld && ld.hasArchicad) {
          results.push({ ...lj, ...ld, source: 'LinkedIn' });
        }
      }
    }

    // JUSTJOIN.IT - architecture remote
    console.log('\n=== JUSTJOIN.IT: architecture remote ===');
    await client.tool('navigate_page', { url: 'https://justjoin.it/job-offers/remote/architecture' });
    await new Promise(r => setTimeout(r, 8000));

    r = await client.tool('evaluate_script', {
      function: `() => {
        var jobs = [];
        var items = document.querySelectorAll('[data-testid="job-title"], a[href*="/job-offer/"]');
        for (var i = 0; i < Math.min(items.length, 30); i++) {
          var el = items[i];
          var title = el.textContent.trim();
          var link = el.href || '';
          var parent = el.closest('div, article');
          var desc = parent ? parent.textContent.toLowerCase() : '';
          if (desc.indexOf('archicad') > -1 || title.toLowerCase().indexOf('archicad') > -1 || title.toLowerCase().indexOf('architekt') > -1) {
            jobs.push({ title: title, link: link });
          }
        }
        return jobs.length > 0 ? jobs : { pageTitle: document.title, snippet: document.body.innerText.substring(0, 500) };
      }`
    });
    console.log('JustJoin:', JSON.stringify(r, null, 2));

    // GOOGLE - search for archicad architect remote poland
    console.log('\n=== GOOGLE SEARCH ===');
    await client.tool('navigate_page', { url: 'https://www.google.com/search?q=architekt+archicad+praca+zdalna+Polska' });
    await new Promise(r => setTimeout(r, 8000));

    r = await client.tool('evaluate_script', {
      function: `() => {
        var results = [];
        var items = document.querySelectorAll('div.g, .g');
        for (var i = 0; i < items.length && results.length < 15; i++) {
          var el = items[i];
          var linkEl = el.querySelector('a[href^="http"]');
          if (!linkEl) continue;
          var link = linkEl.href;
          var titleEl = el.querySelector('h3');
          var title = titleEl ? titleEl.textContent.trim() : '';
          var snippetEl = el.querySelector('.VwiC3b, .s3v94d');
          var snippet = snippetEl ? snippetEl.textContent.trim() : '';
          if (link.indexOf('google.com') === -1 && (title.toLowerCase().indexOf('architekt') > -1 || title.toLowerCase().indexOf('archicad') > -1 || snippet.toLowerCase().indexOf('archicad') > -1)) {
            results.push({ title: title, link: link, snippet: snippet.substring(0, 200) });
          }
        }
        return results;
      }`
    });
    console.log('Google:', JSON.stringify(r, null, 2));

    console.log('\n\n=== FINAL ARCHICAD REMOTE RESULTS ===');
    console.log(JSON.stringify(results, null, 2));

  } catch (err) {
    console.error('Error:', err);
  } finally {
    client.stop();
  }
}

main();
