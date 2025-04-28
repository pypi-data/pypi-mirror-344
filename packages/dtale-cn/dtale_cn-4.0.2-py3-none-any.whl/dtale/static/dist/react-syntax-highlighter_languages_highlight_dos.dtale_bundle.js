(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_dos"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/dos.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/dos.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: Batch file (DOS)
Author: Alexander Makarov <sam@rmcreative.ru>
Contributors: Anton Kochkov <anton.kochkov@gmail.com>
Website: https://en.wikipedia.org/wiki/Batch_file
*/

/** @type LanguageFn */
function dos(hljs) {
  const COMMENT = hljs.COMMENT(
    /^\s*@?rem\b/, /$/,
    {
      relevance: 10
    }
  );
  const LABEL = {
    className: 'symbol',
    begin: '^\\s*[A-Za-z._?][A-Za-z0-9_$#@~.?]*(:|\\s+label)',
    relevance: 0
  };
  return {
    name: 'Batch file (DOS)',
    aliases: [
      'bat',
      'cmd'
    ],
    case_insensitive: true,
    illegal: /\/\*/,
    keywords: {
      keyword:
        'if else goto for in do call exit not exist errorlevel defined ' +
        'equ neq lss leq gtr geq',
      built_in:
        'prn nul lpt3 lpt2 lpt1 con com4 com3 com2 com1 aux ' +
        'shift cd dir echo setlocal endlocal set pause copy ' +
        'append assoc at attrib break cacls cd chcp chdir chkdsk chkntfs cls cmd color ' +
        'comp compact convert date dir diskcomp diskcopy doskey erase fs ' +
        'find findstr format ftype graftabl help keyb label md mkdir mode more move path ' +
        'pause print popd pushd promt rd recover rem rename replace restore rmdir shift ' +
        'sort start subst time title tree type ver verify vol ' +
        // winutils
        'ping net ipconfig taskkill xcopy ren del'
    },
    contains: [
      {
        className: 'variable',
        begin: /%%[^ ]|%[^ ]+?%|![^ ]+?!/
      },
      {
        className: 'function',
        begin: LABEL.begin,
        end: 'goto:eof',
        contains: [
          hljs.inherit(hljs.TITLE_MODE, {
            begin: '([_a-zA-Z]\\w*\\.)*([_a-zA-Z]\\w*:)?[_a-zA-Z]\\w*'
          }),
          COMMENT
        ]
      },
      {
        className: 'number',
        begin: '\\b\\d+',
        relevance: 0
      },
      COMMENT
    ]
  };
}

module.exports = dos;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZG9zLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2Rvcy5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IEJhdGNoIGZpbGUgKERPUylcbkF1dGhvcjogQWxleGFuZGVyIE1ha2Fyb3YgPHNhbUBybWNyZWF0aXZlLnJ1PlxuQ29udHJpYnV0b3JzOiBBbnRvbiBLb2Noa292IDxhbnRvbi5rb2Noa292QGdtYWlsLmNvbT5cbldlYnNpdGU6IGh0dHBzOi8vZW4ud2lraXBlZGlhLm9yZy93aWtpL0JhdGNoX2ZpbGVcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBkb3MoaGxqcykge1xuICBjb25zdCBDT01NRU5UID0gaGxqcy5DT01NRU5UKFxuICAgIC9eXFxzKkA/cmVtXFxiLywgLyQvLFxuICAgIHtcbiAgICAgIHJlbGV2YW5jZTogMTBcbiAgICB9XG4gICk7XG4gIGNvbnN0IExBQkVMID0ge1xuICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgYmVnaW46ICdeXFxcXHMqW0EtWmEtei5fP11bQS1aYS16MC05XyQjQH4uP10qKDp8XFxcXHMrbGFiZWwpJyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnQmF0Y2ggZmlsZSAoRE9TKScsXG4gICAgYWxpYXNlczogW1xuICAgICAgJ2JhdCcsXG4gICAgICAnY21kJ1xuICAgIF0sXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBpbGxlZ2FsOiAvXFwvXFwqLyxcbiAgICBrZXl3b3Jkczoge1xuICAgICAga2V5d29yZDpcbiAgICAgICAgJ2lmIGVsc2UgZ290byBmb3IgaW4gZG8gY2FsbCBleGl0IG5vdCBleGlzdCBlcnJvcmxldmVsIGRlZmluZWQgJyArXG4gICAgICAgICdlcXUgbmVxIGxzcyBsZXEgZ3RyIGdlcScsXG4gICAgICBidWlsdF9pbjpcbiAgICAgICAgJ3BybiBudWwgbHB0MyBscHQyIGxwdDEgY29uIGNvbTQgY29tMyBjb20yIGNvbTEgYXV4ICcgK1xuICAgICAgICAnc2hpZnQgY2QgZGlyIGVjaG8gc2V0bG9jYWwgZW5kbG9jYWwgc2V0IHBhdXNlIGNvcHkgJyArXG4gICAgICAgICdhcHBlbmQgYXNzb2MgYXQgYXR0cmliIGJyZWFrIGNhY2xzIGNkIGNoY3AgY2hkaXIgY2hrZHNrIGNoa250ZnMgY2xzIGNtZCBjb2xvciAnICtcbiAgICAgICAgJ2NvbXAgY29tcGFjdCBjb252ZXJ0IGRhdGUgZGlyIGRpc2tjb21wIGRpc2tjb3B5IGRvc2tleSBlcmFzZSBmcyAnICtcbiAgICAgICAgJ2ZpbmQgZmluZHN0ciBmb3JtYXQgZnR5cGUgZ3JhZnRhYmwgaGVscCBrZXliIGxhYmVsIG1kIG1rZGlyIG1vZGUgbW9yZSBtb3ZlIHBhdGggJyArXG4gICAgICAgICdwYXVzZSBwcmludCBwb3BkIHB1c2hkIHByb210IHJkIHJlY292ZXIgcmVtIHJlbmFtZSByZXBsYWNlIHJlc3RvcmUgcm1kaXIgc2hpZnQgJyArXG4gICAgICAgICdzb3J0IHN0YXJ0IHN1YnN0IHRpbWUgdGl0bGUgdHJlZSB0eXBlIHZlciB2ZXJpZnkgdm9sICcgK1xuICAgICAgICAvLyB3aW51dGlsc1xuICAgICAgICAncGluZyBuZXQgaXBjb25maWcgdGFza2tpbGwgeGNvcHkgcmVuIGRlbCdcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICAgICAgYmVnaW46IC8lJVteIF18JVteIF0rPyV8IVteIF0rPyEvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgICAgIGJlZ2luOiBMQUJFTC5iZWdpbixcbiAgICAgICAgZW5kOiAnZ290bzplb2YnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuaW5oZXJpdChobGpzLlRJVExFX01PREUsIHtcbiAgICAgICAgICAgIGJlZ2luOiAnKFtfYS16QS1aXVxcXFx3KlxcXFwuKSooW19hLXpBLVpdXFxcXHcqOik/W19hLXpBLVpdXFxcXHcqJ1xuICAgICAgICAgIH0pLFxuICAgICAgICAgIENPTU1FTlRcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICAgICAgYmVnaW46ICdcXFxcYlxcXFxkKycsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIENPTU1FTlRcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gZG9zO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9