(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_powershell"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/powershell.js":
/*!*****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/powershell.js ***!
  \*****************************************************************************************************/
/***/ ((module) => {

/*
Language: PowerShell
Description: PowerShell is a task-based command-line shell and scripting language built on .NET.
Author: David Mohundro <david@mohundro.com>
Contributors: Nicholas Blumhardt <nblumhardt@nblumhardt.com>, Victor Zhou <OiCMudkips@users.noreply.github.com>, Nicolas Le Gall <contact@nlegall.fr>
Website: https://docs.microsoft.com/en-us/powershell/
*/

function powershell(hljs) {
  const TYPES = [
    "string",
    "char",
    "byte",
    "int",
    "long",
    "bool",
    "decimal",
    "single",
    "double",
    "DateTime",
    "xml",
    "array",
    "hashtable",
    "void"
  ];

  // https://docs.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands
  const VALID_VERBS =
    'Add|Clear|Close|Copy|Enter|Exit|Find|Format|Get|Hide|Join|Lock|' +
    'Move|New|Open|Optimize|Pop|Push|Redo|Remove|Rename|Reset|Resize|' +
    'Search|Select|Set|Show|Skip|Split|Step|Switch|Undo|Unlock|' +
    'Watch|Backup|Checkpoint|Compare|Compress|Convert|ConvertFrom|' +
    'ConvertTo|Dismount|Edit|Expand|Export|Group|Import|Initialize|' +
    'Limit|Merge|Mount|Out|Publish|Restore|Save|Sync|Unpublish|Update|' +
    'Approve|Assert|Build|Complete|Confirm|Deny|Deploy|Disable|Enable|Install|Invoke|' +
    'Register|Request|Restart|Resume|Start|Stop|Submit|Suspend|Uninstall|' +
    'Unregister|Wait|Debug|Measure|Ping|Repair|Resolve|Test|Trace|Connect|' +
    'Disconnect|Read|Receive|Send|Write|Block|Grant|Protect|Revoke|Unblock|' +
    'Unprotect|Use|ForEach|Sort|Tee|Where';

  const COMPARISON_OPERATORS =
    '-and|-as|-band|-bnot|-bor|-bxor|-casesensitive|-ccontains|-ceq|-cge|-cgt|' +
    '-cle|-clike|-clt|-cmatch|-cne|-cnotcontains|-cnotlike|-cnotmatch|-contains|' +
    '-creplace|-csplit|-eq|-exact|-f|-file|-ge|-gt|-icontains|-ieq|-ige|-igt|' +
    '-ile|-ilike|-ilt|-imatch|-in|-ine|-inotcontains|-inotlike|-inotmatch|' +
    '-ireplace|-is|-isnot|-isplit|-join|-le|-like|-lt|-match|-ne|-not|' +
    '-notcontains|-notin|-notlike|-notmatch|-or|-regex|-replace|-shl|-shr|' +
    '-split|-wildcard|-xor';

  const KEYWORDS = {
    $pattern: /-?[A-z\.\-]+\b/,
    keyword:
      'if else foreach return do while until elseif begin for trap data dynamicparam ' +
      'end break throw param continue finally in switch exit filter try process catch ' +
      'hidden static parameter',
    // "echo" relevance has been set to 0 to avoid auto-detect conflicts with shell transcripts
    built_in:
      'ac asnp cat cd CFS chdir clc clear clhy cli clp cls clv cnsn compare copy cp ' +
      'cpi cpp curl cvpa dbp del diff dir dnsn ebp echo|0 epal epcsv epsn erase etsn exsn fc fhx ' +
      'fl ft fw gal gbp gc gcb gci gcm gcs gdr gerr ghy gi gin gjb gl gm gmo gp gps gpv group ' +
      'gsn gsnp gsv gtz gu gv gwmi h history icm iex ihy ii ipal ipcsv ipmo ipsn irm ise iwmi ' +
      'iwr kill lp ls man md measure mi mount move mp mv nal ndr ni nmo npssc nsn nv ogv oh ' +
      'popd ps pushd pwd r rbp rcjb rcsn rd rdr ren ri rjb rm rmdir rmo rni rnp rp rsn rsnp ' +
      'rujb rv rvpa rwmi sajb sal saps sasv sbp sc scb select set shcm si sl sleep sls sort sp ' +
      'spjb spps spsv start stz sujb sv swmi tee trcm type wget where wjb write'
    // TODO: 'validate[A-Z]+' can't work in keywords
  };

  const TITLE_NAME_RE = /\w[\w\d]*((-)[\w\d]+)*/;

  const BACKTICK_ESCAPE = {
    begin: '`[\\s\\S]',
    relevance: 0
  };

  const VAR = {
    className: 'variable',
    variants: [
      {
        begin: /\$\B/
      },
      {
        className: 'keyword',
        begin: /\$this/
      },
      {
        begin: /\$[\w\d][\w\d_:]*/
      }
    ]
  };

  const LITERAL = {
    className: 'literal',
    begin: /\$(null|true|false)\b/
  };

  const QUOTE_STRING = {
    className: "string",
    variants: [
      {
        begin: /"/,
        end: /"/
      },
      {
        begin: /@"/,
        end: /^"@/
      }
    ],
    contains: [
      BACKTICK_ESCAPE,
      VAR,
      {
        className: 'variable',
        begin: /\$[A-z]/,
        end: /[^A-z]/
      }
    ]
  };

  const APOS_STRING = {
    className: 'string',
    variants: [
      {
        begin: /'/,
        end: /'/
      },
      {
        begin: /@'/,
        end: /^'@/
      }
    ]
  };

  const PS_HELPTAGS = {
    className: "doctag",
    variants: [
      /* no paramater help tags */
      {
        begin: /\.(synopsis|description|example|inputs|outputs|notes|link|component|role|functionality)/
      },
      /* one parameter help tags */
      {
        begin: /\.(parameter|forwardhelptargetname|forwardhelpcategory|remotehelprunspace|externalhelp)\s+\S+/
      }
    ]
  };

  const PS_COMMENT = hljs.inherit(
    hljs.COMMENT(null, null),
    {
      variants: [
        /* single-line comment */
        {
          begin: /#/,
          end: /$/
        },
        /* multi-line comment */
        {
          begin: /<#/,
          end: /#>/
        }
      ],
      contains: [ PS_HELPTAGS ]
    }
  );

  const CMDLETS = {
    className: 'built_in',
    variants: [
      {
        begin: '('.concat(VALID_VERBS, ')+(-)[\\w\\d]+')
      }
    ]
  };

  const PS_CLASS = {
    className: 'class',
    beginKeywords: 'class enum',
    end: /\s*[{]/,
    excludeEnd: true,
    relevance: 0,
    contains: [ hljs.TITLE_MODE ]
  };

  const PS_FUNCTION = {
    className: 'function',
    begin: /function\s+/,
    end: /\s*\{|$/,
    excludeEnd: true,
    returnBegin: true,
    relevance: 0,
    contains: [
      {
        begin: "function",
        relevance: 0,
        className: "keyword"
      },
      {
        className: "title",
        begin: TITLE_NAME_RE,
        relevance: 0
      },
      {
        begin: /\(/,
        end: /\)/,
        className: "params",
        relevance: 0,
        contains: [ VAR ]
      }
      // CMDLETS
    ]
  };

  // Using statment, plus type, plus assembly name.
  const PS_USING = {
    begin: /using\s/,
    end: /$/,
    returnBegin: true,
    contains: [
      QUOTE_STRING,
      APOS_STRING,
      {
        className: 'keyword',
        begin: /(using|assembly|command|module|namespace|type)/
      }
    ]
  };

  // Comperison operators & function named parameters.
  const PS_ARGUMENTS = {
    variants: [
      // PS literals are pretty verbose so it's a good idea to accent them a bit.
      {
        className: 'operator',
        begin: '('.concat(COMPARISON_OPERATORS, ')\\b')
      },
      {
        className: 'literal',
        begin: /(-)[\w\d]+/,
        relevance: 0
      }
    ]
  };

  const HASH_SIGNS = {
    className: 'selector-tag',
    begin: /@\B/,
    relevance: 0
  };

  // It's a very general rule so I'll narrow it a bit with some strict boundaries
  // to avoid any possible false-positive collisions!
  const PS_METHODS = {
    className: 'function',
    begin: /\[.*\]\s*[\w]+[ ]??\(/,
    end: /$/,
    returnBegin: true,
    relevance: 0,
    contains: [
      {
        className: 'keyword',
        begin: '('.concat(
          KEYWORDS.keyword.toString().replace(/\s/g, '|'
          ), ')\\b'),
        endsParent: true,
        relevance: 0
      },
      hljs.inherit(hljs.TITLE_MODE, {
        endsParent: true
      })
    ]
  };

  const GENTLEMANS_SET = [
    // STATIC_MEMBER,
    PS_METHODS,
    PS_COMMENT,
    BACKTICK_ESCAPE,
    hljs.NUMBER_MODE,
    QUOTE_STRING,
    APOS_STRING,
    // PS_NEW_OBJECT_TYPE,
    CMDLETS,
    VAR,
    LITERAL,
    HASH_SIGNS
  ];

  const PS_TYPE = {
    begin: /\[/,
    end: /\]/,
    excludeBegin: true,
    excludeEnd: true,
    relevance: 0,
    contains: [].concat(
      'self',
      GENTLEMANS_SET,
      {
        begin: "(" + TYPES.join("|") + ")",
        className: "built_in",
        relevance: 0
      },
      {
        className: 'type',
        begin: /[\.\w\d]+/,
        relevance: 0
      }
    )
  };

  PS_METHODS.contains.unshift(PS_TYPE);

  return {
    name: 'PowerShell',
    aliases: [
      "ps",
      "ps1"
    ],
    case_insensitive: true,
    keywords: KEYWORDS,
    contains: GENTLEMANS_SET.concat(
      PS_CLASS,
      PS_FUNCTION,
      PS_USING,
      PS_ARGUMENTS,
      PS_TYPE
    )
  };
}

module.exports = powershell;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcG93ZXJzaGVsbC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBOztBQUVBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3Bvd2Vyc2hlbGwuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBQb3dlclNoZWxsXG5EZXNjcmlwdGlvbjogUG93ZXJTaGVsbCBpcyBhIHRhc2stYmFzZWQgY29tbWFuZC1saW5lIHNoZWxsIGFuZCBzY3JpcHRpbmcgbGFuZ3VhZ2UgYnVpbHQgb24gLk5FVC5cbkF1dGhvcjogRGF2aWQgTW9odW5kcm8gPGRhdmlkQG1vaHVuZHJvLmNvbT5cbkNvbnRyaWJ1dG9yczogTmljaG9sYXMgQmx1bWhhcmR0IDxuYmx1bWhhcmR0QG5ibHVtaGFyZHQuY29tPiwgVmljdG9yIFpob3UgPE9pQ011ZGtpcHNAdXNlcnMubm9yZXBseS5naXRodWIuY29tPiwgTmljb2xhcyBMZSBHYWxsIDxjb250YWN0QG5sZWdhbGwuZnI+XG5XZWJzaXRlOiBodHRwczovL2RvY3MubWljcm9zb2Z0LmNvbS9lbi11cy9wb3dlcnNoZWxsL1xuKi9cblxuZnVuY3Rpb24gcG93ZXJzaGVsbChobGpzKSB7XG4gIGNvbnN0IFRZUEVTID0gW1xuICAgIFwic3RyaW5nXCIsXG4gICAgXCJjaGFyXCIsXG4gICAgXCJieXRlXCIsXG4gICAgXCJpbnRcIixcbiAgICBcImxvbmdcIixcbiAgICBcImJvb2xcIixcbiAgICBcImRlY2ltYWxcIixcbiAgICBcInNpbmdsZVwiLFxuICAgIFwiZG91YmxlXCIsXG4gICAgXCJEYXRlVGltZVwiLFxuICAgIFwieG1sXCIsXG4gICAgXCJhcnJheVwiLFxuICAgIFwiaGFzaHRhYmxlXCIsXG4gICAgXCJ2b2lkXCJcbiAgXTtcblxuICAvLyBodHRwczovL2RvY3MubWljcm9zb2Z0LmNvbS9lbi11cy9wb3dlcnNoZWxsL3NjcmlwdGluZy9kZXZlbG9wZXIvY21kbGV0L2FwcHJvdmVkLXZlcmJzLWZvci13aW5kb3dzLXBvd2Vyc2hlbGwtY29tbWFuZHNcbiAgY29uc3QgVkFMSURfVkVSQlMgPVxuICAgICdBZGR8Q2xlYXJ8Q2xvc2V8Q29weXxFbnRlcnxFeGl0fEZpbmR8Rm9ybWF0fEdldHxIaWRlfEpvaW58TG9ja3wnICtcbiAgICAnTW92ZXxOZXd8T3BlbnxPcHRpbWl6ZXxQb3B8UHVzaHxSZWRvfFJlbW92ZXxSZW5hbWV8UmVzZXR8UmVzaXplfCcgK1xuICAgICdTZWFyY2h8U2VsZWN0fFNldHxTaG93fFNraXB8U3BsaXR8U3RlcHxTd2l0Y2h8VW5kb3xVbmxvY2t8JyArXG4gICAgJ1dhdGNofEJhY2t1cHxDaGVja3BvaW50fENvbXBhcmV8Q29tcHJlc3N8Q29udmVydHxDb252ZXJ0RnJvbXwnICtcbiAgICAnQ29udmVydFRvfERpc21vdW50fEVkaXR8RXhwYW5kfEV4cG9ydHxHcm91cHxJbXBvcnR8SW5pdGlhbGl6ZXwnICtcbiAgICAnTGltaXR8TWVyZ2V8TW91bnR8T3V0fFB1Ymxpc2h8UmVzdG9yZXxTYXZlfFN5bmN8VW5wdWJsaXNofFVwZGF0ZXwnICtcbiAgICAnQXBwcm92ZXxBc3NlcnR8QnVpbGR8Q29tcGxldGV8Q29uZmlybXxEZW55fERlcGxveXxEaXNhYmxlfEVuYWJsZXxJbnN0YWxsfEludm9rZXwnICtcbiAgICAnUmVnaXN0ZXJ8UmVxdWVzdHxSZXN0YXJ0fFJlc3VtZXxTdGFydHxTdG9wfFN1Ym1pdHxTdXNwZW5kfFVuaW5zdGFsbHwnICtcbiAgICAnVW5yZWdpc3RlcnxXYWl0fERlYnVnfE1lYXN1cmV8UGluZ3xSZXBhaXJ8UmVzb2x2ZXxUZXN0fFRyYWNlfENvbm5lY3R8JyArXG4gICAgJ0Rpc2Nvbm5lY3R8UmVhZHxSZWNlaXZlfFNlbmR8V3JpdGV8QmxvY2t8R3JhbnR8UHJvdGVjdHxSZXZva2V8VW5ibG9ja3wnICtcbiAgICAnVW5wcm90ZWN0fFVzZXxGb3JFYWNofFNvcnR8VGVlfFdoZXJlJztcblxuICBjb25zdCBDT01QQVJJU09OX09QRVJBVE9SUyA9XG4gICAgJy1hbmR8LWFzfC1iYW5kfC1ibm90fC1ib3J8LWJ4b3J8LWNhc2VzZW5zaXRpdmV8LWNjb250YWluc3wtY2VxfC1jZ2V8LWNndHwnICtcbiAgICAnLWNsZXwtY2xpa2V8LWNsdHwtY21hdGNofC1jbmV8LWNub3Rjb250YWluc3wtY25vdGxpa2V8LWNub3RtYXRjaHwtY29udGFpbnN8JyArXG4gICAgJy1jcmVwbGFjZXwtY3NwbGl0fC1lcXwtZXhhY3R8LWZ8LWZpbGV8LWdlfC1ndHwtaWNvbnRhaW5zfC1pZXF8LWlnZXwtaWd0fCcgK1xuICAgICctaWxlfC1pbGlrZXwtaWx0fC1pbWF0Y2h8LWlufC1pbmV8LWlub3Rjb250YWluc3wtaW5vdGxpa2V8LWlub3RtYXRjaHwnICtcbiAgICAnLWlyZXBsYWNlfC1pc3wtaXNub3R8LWlzcGxpdHwtam9pbnwtbGV8LWxpa2V8LWx0fC1tYXRjaHwtbmV8LW5vdHwnICtcbiAgICAnLW5vdGNvbnRhaW5zfC1ub3Rpbnwtbm90bGlrZXwtbm90bWF0Y2h8LW9yfC1yZWdleHwtcmVwbGFjZXwtc2hsfC1zaHJ8JyArXG4gICAgJy1zcGxpdHwtd2lsZGNhcmR8LXhvcic7XG5cbiAgY29uc3QgS0VZV09SRFMgPSB7XG4gICAgJHBhdHRlcm46IC8tP1tBLXpcXC5cXC1dK1xcYi8sXG4gICAga2V5d29yZDpcbiAgICAgICdpZiBlbHNlIGZvcmVhY2ggcmV0dXJuIGRvIHdoaWxlIHVudGlsIGVsc2VpZiBiZWdpbiBmb3IgdHJhcCBkYXRhIGR5bmFtaWNwYXJhbSAnICtcbiAgICAgICdlbmQgYnJlYWsgdGhyb3cgcGFyYW0gY29udGludWUgZmluYWxseSBpbiBzd2l0Y2ggZXhpdCBmaWx0ZXIgdHJ5IHByb2Nlc3MgY2F0Y2ggJyArXG4gICAgICAnaGlkZGVuIHN0YXRpYyBwYXJhbWV0ZXInLFxuICAgIC8vIFwiZWNob1wiIHJlbGV2YW5jZSBoYXMgYmVlbiBzZXQgdG8gMCB0byBhdm9pZCBhdXRvLWRldGVjdCBjb25mbGljdHMgd2l0aCBzaGVsbCB0cmFuc2NyaXB0c1xuICAgIGJ1aWx0X2luOlxuICAgICAgJ2FjIGFzbnAgY2F0IGNkIENGUyBjaGRpciBjbGMgY2xlYXIgY2xoeSBjbGkgY2xwIGNscyBjbHYgY25zbiBjb21wYXJlIGNvcHkgY3AgJyArXG4gICAgICAnY3BpIGNwcCBjdXJsIGN2cGEgZGJwIGRlbCBkaWZmIGRpciBkbnNuIGVicCBlY2hvfDAgZXBhbCBlcGNzdiBlcHNuIGVyYXNlIGV0c24gZXhzbiBmYyBmaHggJyArXG4gICAgICAnZmwgZnQgZncgZ2FsIGdicCBnYyBnY2IgZ2NpIGdjbSBnY3MgZ2RyIGdlcnIgZ2h5IGdpIGdpbiBnamIgZ2wgZ20gZ21vIGdwIGdwcyBncHYgZ3JvdXAgJyArXG4gICAgICAnZ3NuIGdzbnAgZ3N2IGd0eiBndSBndiBnd21pIGggaGlzdG9yeSBpY20gaWV4IGloeSBpaSBpcGFsIGlwY3N2IGlwbW8gaXBzbiBpcm0gaXNlIGl3bWkgJyArXG4gICAgICAnaXdyIGtpbGwgbHAgbHMgbWFuIG1kIG1lYXN1cmUgbWkgbW91bnQgbW92ZSBtcCBtdiBuYWwgbmRyIG5pIG5tbyBucHNzYyBuc24gbnYgb2d2IG9oICcgK1xuICAgICAgJ3BvcGQgcHMgcHVzaGQgcHdkIHIgcmJwIHJjamIgcmNzbiByZCByZHIgcmVuIHJpIHJqYiBybSBybWRpciBybW8gcm5pIHJucCBycCByc24gcnNucCAnICtcbiAgICAgICdydWpiIHJ2IHJ2cGEgcndtaSBzYWpiIHNhbCBzYXBzIHNhc3Ygc2JwIHNjIHNjYiBzZWxlY3Qgc2V0IHNoY20gc2kgc2wgc2xlZXAgc2xzIHNvcnQgc3AgJyArXG4gICAgICAnc3BqYiBzcHBzIHNwc3Ygc3RhcnQgc3R6IHN1amIgc3Ygc3dtaSB0ZWUgdHJjbSB0eXBlIHdnZXQgd2hlcmUgd2piIHdyaXRlJ1xuICAgIC8vIFRPRE86ICd2YWxpZGF0ZVtBLVpdKycgY2FuJ3Qgd29yayBpbiBrZXl3b3Jkc1xuICB9O1xuXG4gIGNvbnN0IFRJVExFX05BTUVfUkUgPSAvXFx3W1xcd1xcZF0qKCgtKVtcXHdcXGRdKykqLztcblxuICBjb25zdCBCQUNLVElDS19FU0NBUEUgPSB7XG4gICAgYmVnaW46ICdgW1xcXFxzXFxcXFNdJyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcblxuICBjb25zdCBWQVIgPSB7XG4gICAgY2xhc3NOYW1lOiAndmFyaWFibGUnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFwkXFxCL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgICAgIGJlZ2luOiAvXFwkdGhpcy9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFwkW1xcd1xcZF1bXFx3XFxkXzpdKi9cbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgY29uc3QgTElURVJBTCA9IHtcbiAgICBjbGFzc05hbWU6ICdsaXRlcmFsJyxcbiAgICBiZWdpbjogL1xcJChudWxsfHRydWV8ZmFsc2UpXFxiL1xuICB9O1xuXG4gIGNvbnN0IFFVT1RFX1NUUklORyA9IHtcbiAgICBjbGFzc05hbWU6IFwic3RyaW5nXCIsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cIi8sXG4gICAgICAgIGVuZDogL1wiL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9AXCIvLFxuICAgICAgICBlbmQ6IC9eXCJAL1xuICAgICAgfVxuICAgIF0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIEJBQ0tUSUNLX0VTQ0FQRSxcbiAgICAgIFZBUixcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndmFyaWFibGUnLFxuICAgICAgICBiZWdpbjogL1xcJFtBLXpdLyxcbiAgICAgICAgZW5kOiAvW15BLXpdL1xuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBBUE9TX1NUUklORyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvJy8sXG4gICAgICAgIGVuZDogLycvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL0AnLyxcbiAgICAgICAgZW5kOiAvXidAL1xuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBQU19IRUxQVEFHUyA9IHtcbiAgICBjbGFzc05hbWU6IFwiZG9jdGFnXCIsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIC8qIG5vIHBhcmFtYXRlciBoZWxwIHRhZ3MgKi9cbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXC4oc3lub3BzaXN8ZGVzY3JpcHRpb258ZXhhbXBsZXxpbnB1dHN8b3V0cHV0c3xub3Rlc3xsaW5rfGNvbXBvbmVudHxyb2xlfGZ1bmN0aW9uYWxpdHkpL1xuICAgICAgfSxcbiAgICAgIC8qIG9uZSBwYXJhbWV0ZXIgaGVscCB0YWdzICovXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFwuKHBhcmFtZXRlcnxmb3J3YXJkaGVscHRhcmdldG5hbWV8Zm9yd2FyZGhlbHBjYXRlZ29yeXxyZW1vdGVoZWxwcnVuc3BhY2V8ZXh0ZXJuYWxoZWxwKVxccytcXFMrL1xuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBQU19DT01NRU5UID0gaGxqcy5pbmhlcml0KFxuICAgIGhsanMuQ09NTUVOVChudWxsLCBudWxsKSxcbiAgICB7XG4gICAgICB2YXJpYW50czogW1xuICAgICAgICAvKiBzaW5nbGUtbGluZSBjb21tZW50ICovXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogLyMvLFxuICAgICAgICAgIGVuZDogLyQvXG4gICAgICAgIH0sXG4gICAgICAgIC8qIG11bHRpLWxpbmUgY29tbWVudCAqL1xuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46IC88Iy8sXG4gICAgICAgICAgZW5kOiAvIz4vXG4gICAgICAgIH1cbiAgICAgIF0sXG4gICAgICBjb250YWluczogWyBQU19IRUxQVEFHUyBdXG4gICAgfVxuICApO1xuXG4gIGNvbnN0IENNRExFVFMgPSB7XG4gICAgY2xhc3NOYW1lOiAnYnVpbHRfaW4nLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnKCcuY29uY2F0KFZBTElEX1ZFUkJTLCAnKSsoLSlbXFxcXHdcXFxcZF0rJylcbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgY29uc3QgUFNfQ0xBU1MgPSB7XG4gICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgIGJlZ2luS2V5d29yZHM6ICdjbGFzcyBlbnVtJyxcbiAgICBlbmQ6IC9cXHMqW3tdLyxcbiAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICBjb250YWluczogWyBobGpzLlRJVExFX01PREUgXVxuICB9O1xuXG4gIGNvbnN0IFBTX0ZVTkNUSU9OID0ge1xuICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICBiZWdpbjogL2Z1bmN0aW9uXFxzKy8sXG4gICAgZW5kOiAvXFxzKlxce3wkLyxcbiAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogXCJmdW5jdGlvblwiLFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIGNsYXNzTmFtZTogXCJrZXl3b3JkXCJcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogXCJ0aXRsZVwiLFxuICAgICAgICBiZWdpbjogVElUTEVfTkFNRV9SRSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcKC8sXG4gICAgICAgIGVuZDogL1xcKS8sXG4gICAgICAgIGNsYXNzTmFtZTogXCJwYXJhbXNcIixcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogWyBWQVIgXVxuICAgICAgfVxuICAgICAgLy8gQ01ETEVUU1xuICAgIF1cbiAgfTtcblxuICAvLyBVc2luZyBzdGF0bWVudCwgcGx1cyB0eXBlLCBwbHVzIGFzc2VtYmx5IG5hbWUuXG4gIGNvbnN0IFBTX1VTSU5HID0ge1xuICAgIGJlZ2luOiAvdXNpbmdcXHMvLFxuICAgIGVuZDogLyQvLFxuICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBRVU9URV9TVFJJTkcsXG4gICAgICBBUE9TX1NUUklORyxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgICAgIGJlZ2luOiAvKHVzaW5nfGFzc2VtYmx5fGNvbW1hbmR8bW9kdWxlfG5hbWVzcGFjZXx0eXBlKS9cbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgLy8gQ29tcGVyaXNvbiBvcGVyYXRvcnMgJiBmdW5jdGlvbiBuYW1lZCBwYXJhbWV0ZXJzLlxuICBjb25zdCBQU19BUkdVTUVOVFMgPSB7XG4gICAgdmFyaWFudHM6IFtcbiAgICAgIC8vIFBTIGxpdGVyYWxzIGFyZSBwcmV0dHkgdmVyYm9zZSBzbyBpdCdzIGEgZ29vZCBpZGVhIHRvIGFjY2VudCB0aGVtIGEgYml0LlxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdvcGVyYXRvcicsXG4gICAgICAgIGJlZ2luOiAnKCcuY29uY2F0KENPTVBBUklTT05fT1BFUkFUT1JTLCAnKVxcXFxiJylcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2xpdGVyYWwnLFxuICAgICAgICBiZWdpbjogLygtKVtcXHdcXGRdKy8sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBIQVNIX1NJR05TID0ge1xuICAgIGNsYXNzTmFtZTogJ3NlbGVjdG9yLXRhZycsXG4gICAgYmVnaW46IC9AXFxCLyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcblxuICAvLyBJdCdzIGEgdmVyeSBnZW5lcmFsIHJ1bGUgc28gSSdsbCBuYXJyb3cgaXQgYSBiaXQgd2l0aCBzb21lIHN0cmljdCBib3VuZGFyaWVzXG4gIC8vIHRvIGF2b2lkIGFueSBwb3NzaWJsZSBmYWxzZS1wb3NpdGl2ZSBjb2xsaXNpb25zIVxuICBjb25zdCBQU19NRVRIT0RTID0ge1xuICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICBiZWdpbjogL1xcWy4qXFxdXFxzKltcXHddK1sgXT8/XFwoLyxcbiAgICBlbmQ6IC8kLyxcbiAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICByZWxldmFuY2U6IDAsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgICAgIGJlZ2luOiAnKCcuY29uY2F0KFxuICAgICAgICAgIEtFWVdPUkRTLmtleXdvcmQudG9TdHJpbmcoKS5yZXBsYWNlKC9cXHMvZywgJ3wnXG4gICAgICAgICAgKSwgJylcXFxcYicpLFxuICAgICAgICBlbmRzUGFyZW50OiB0cnVlLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICBobGpzLmluaGVyaXQoaGxqcy5USVRMRV9NT0RFLCB7XG4gICAgICAgIGVuZHNQYXJlbnQ6IHRydWVcbiAgICAgIH0pXG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IEdFTlRMRU1BTlNfU0VUID0gW1xuICAgIC8vIFNUQVRJQ19NRU1CRVIsXG4gICAgUFNfTUVUSE9EUyxcbiAgICBQU19DT01NRU5ULFxuICAgIEJBQ0tUSUNLX0VTQ0FQRSxcbiAgICBobGpzLk5VTUJFUl9NT0RFLFxuICAgIFFVT1RFX1NUUklORyxcbiAgICBBUE9TX1NUUklORyxcbiAgICAvLyBQU19ORVdfT0JKRUNUX1RZUEUsXG4gICAgQ01ETEVUUyxcbiAgICBWQVIsXG4gICAgTElURVJBTCxcbiAgICBIQVNIX1NJR05TXG4gIF07XG5cbiAgY29uc3QgUFNfVFlQRSA9IHtcbiAgICBiZWdpbjogL1xcWy8sXG4gICAgZW5kOiAvXFxdLyxcbiAgICBleGNsdWRlQmVnaW46IHRydWUsXG4gICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICByZWxldmFuY2U6IDAsXG4gICAgY29udGFpbnM6IFtdLmNvbmNhdChcbiAgICAgICdzZWxmJyxcbiAgICAgIEdFTlRMRU1BTlNfU0VULFxuICAgICAge1xuICAgICAgICBiZWdpbjogXCIoXCIgKyBUWVBFUy5qb2luKFwifFwiKSArIFwiKVwiLFxuICAgICAgICBjbGFzc05hbWU6IFwiYnVpbHRfaW5cIixcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd0eXBlJyxcbiAgICAgICAgYmVnaW46IC9bXFwuXFx3XFxkXSsvLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH1cbiAgICApXG4gIH07XG5cbiAgUFNfTUVUSE9EUy5jb250YWlucy51bnNoaWZ0KFBTX1RZUEUpO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1Bvd2VyU2hlbGwnLFxuICAgIGFsaWFzZXM6IFtcbiAgICAgIFwicHNcIixcbiAgICAgIFwicHMxXCJcbiAgICBdLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgIGNvbnRhaW5zOiBHRU5UTEVNQU5TX1NFVC5jb25jYXQoXG4gICAgICBQU19DTEFTUyxcbiAgICAgIFBTX0ZVTkNUSU9OLFxuICAgICAgUFNfVVNJTkcsXG4gICAgICBQU19BUkdVTUVOVFMsXG4gICAgICBQU19UWVBFXG4gICAgKVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHBvd2Vyc2hlbGw7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=