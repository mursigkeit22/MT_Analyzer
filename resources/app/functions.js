const { PythonShell } = require('python-shell');
const fs = require('fs');
const logger = require('electron-log/renderer');

var currentFolder = 1;

function getDirectory() {
  return `${__dirname}\\tempFiles\\${currentFolder}`;
}

function makeLog(name) {
  logger.info(name);
}
function writeLog(name) {
  fs.appendFileSync(`LOGS_JS.txt`, `${name}\n`, 'utf8');
}

let fromTextArea;
const options = {
  pythonPath: `${__dirname}/python/python.exe`,
  args: [],
};

const buttonFileCycle = document.getElementById('go');
buttonFileCycle.addEventListener('click', () => {
  const textOpt = fs.readFileSync(`${__dirname}/tempFiles/options.args.txt`, 'utf8');
  writeLog(`TEXT_OPT: ${textOpt}`);
  const textByLine = textOpt.split('?');
  for (const strr of textByLine) {
    options.args.push(strr);
  }
  fromTextArea = document.getElementById('googleText').value;
  writeLog(`FROMTEXTAREA: ${fromTextArea}`);
  writeLog(`CURRENTFOLDER: ${currentFolder}`);
  // options.args.push(currentFolder);
  options.args.push(fromTextArea);
  options.args.push(getDirectory());

  fs.mkdir(`${__dirname}/tempFiles/${currentFolder}`, (err) => {
    if (err) {
      alert(err);
      writeLog(`FS.MKDIR ERROR: ${err}`);
    }
  });

  PythonShell.run(`${__dirname}/get_the_job_done2.py`, options, (err, results) => {
    makeLog(`options: ${options.args}`);
    writeLog(`PYTHONSHELLRUN OPTIONS.ARGS: ${options.args}`);
    if (err) {
      makeLog(`PYTHONSHELLRUN ERROR: ${err}`);
      alert(err);
      writeLog(`PYTHONSHELLRUN ERROR: ${err}`);
    }


    // fs.writeFileSync(`${__dirname}/tempFiles/${currentFolder}/second_window.html`, '');
    const text = fs.readFileSync(`${__dirname}/tempFiles/${currentFolder}/text_second_window.txt`, 'utf8');
    fs.writeFileSync(`${__dirname}/tempFiles/${currentFolder}/second_window.html`, text);

    window.open(`${__dirname}/tempFiles/${currentFolder}/second_window.html`, '', 'width=1200,height=600');
    document.getElementById('reset').style.display = 'inline';
    document.body.style.cursor = 'auto';
    document.getElementById('wait').style.display = 'none';
    for (const res of results) {
      makeLog(res);
      writeLog(`RESULT: ${res}`);
    }
  });
});

buttonFileCycle.addEventListener('click', () => {
  document.getElementById('leftwriting').style.display = 'none';
  document.getElementById('inputLabel').style.display = 'none';
  document.getElementById('rightbox').style.display = 'none';
  document.getElementById('nameList').style.display = 'none';
  document.getElementById('googleText').style.display = 'none';
  document.getElementById('forText').style.display = 'none';
  document.getElementById('go').style.display = 'none';
  document.body.style.cursor = 'wait';
  document.getElementById('wait').style.display = 'inline';
});
const buttonReset = document.getElementById('reset');
buttonReset.addEventListener('click', () => {
  document.getElementById('leftwriting').style.display = 'inline';
  document.getElementById('inputLabel').style.display = 'block';
  document.getElementById('rightbox').style.display = 'inline';
  document.getElementById('nameList').innerHTML = '';
  document.getElementById('nameList').style.display = 'inline';
  document.getElementById('googleText').value = '';
  document.getElementById('googleText').style.display = 'inline';
  document.getElementById('forText').style.display = 'inline';
  document.getElementById('go').style.display = 'inline';
  document.getElementById('reset').style.display = 'none';
  options.args.length = 0;
  currentFolder++;
});
