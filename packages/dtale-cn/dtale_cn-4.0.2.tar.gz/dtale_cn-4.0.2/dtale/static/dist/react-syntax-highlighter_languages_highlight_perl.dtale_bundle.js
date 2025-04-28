(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_perl"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/perl.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/perl.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/**
 * @param {string} value
 * @returns {RegExp}
 * */

/**
 * @param {RegExp | string } re
 * @returns {string}
 */
function source(re) {
  if (!re) return null;
  if (typeof re === "string") return re;

  return re.source;
}

/**
 * @param {...(RegExp | string) } args
 * @returns {string}
 */
function concat(...args) {
  const joined = args.map((x) => source(x)).join("");
  return joined;
}

/**
 * Any of the passed expresssions may match
 *
 * Creates a huge this | this | that | that match
 * @param {(RegExp | string)[] } args
 * @returns {string}
 */
function either(...args) {
  const joined = '(' + args.map((x) => source(x)).join("|") + ")";
  return joined;
}

/*
Language: Perl
Author: Peter Leonov <gojpeg@yandex.ru>
Website: https://www.perl.org
Category: common
*/

/** @type LanguageFn */
function perl(hljs) {
  const KEYWORDS = [
    'abs',
    'accept',
    'alarm',
    'and',
    'atan2',
    'bind',
    'binmode',
    'bless',
    'break',
    'caller',
    'chdir',
    'chmod',
    'chomp',
    'chop',
    'chown',
    'chr',
    'chroot',
    'close',
    'closedir',
    'connect',
    'continue',
    'cos',
    'crypt',
    'dbmclose',
    'dbmopen',
    'defined',
    'delete',
    'die',
    'do',
    'dump',
    'each',
    'else',
    'elsif',
    'endgrent',
    'endhostent',
    'endnetent',
    'endprotoent',
    'endpwent',
    'endservent',
    'eof',
    'eval',
    'exec',
    'exists',
    'exit',
    'exp',
    'fcntl',
    'fileno',
    'flock',
    'for',
    'foreach',
    'fork',
    'format',
    'formline',
    'getc',
    'getgrent',
    'getgrgid',
    'getgrnam',
    'gethostbyaddr',
    'gethostbyname',
    'gethostent',
    'getlogin',
    'getnetbyaddr',
    'getnetbyname',
    'getnetent',
    'getpeername',
    'getpgrp',
    'getpriority',
    'getprotobyname',
    'getprotobynumber',
    'getprotoent',
    'getpwent',
    'getpwnam',
    'getpwuid',
    'getservbyname',
    'getservbyport',
    'getservent',
    'getsockname',
    'getsockopt',
    'given',
    'glob',
    'gmtime',
    'goto',
    'grep',
    'gt',
    'hex',
    'if',
    'index',
    'int',
    'ioctl',
    'join',
    'keys',
    'kill',
    'last',
    'lc',
    'lcfirst',
    'length',
    'link',
    'listen',
    'local',
    'localtime',
    'log',
    'lstat',
    'lt',
    'ma',
    'map',
    'mkdir',
    'msgctl',
    'msgget',
    'msgrcv',
    'msgsnd',
    'my',
    'ne',
    'next',
    'no',
    'not',
    'oct',
    'open',
    'opendir',
    'or',
    'ord',
    'our',
    'pack',
    'package',
    'pipe',
    'pop',
    'pos',
    'print',
    'printf',
    'prototype',
    'push',
    'q|0',
    'qq',
    'quotemeta',
    'qw',
    'qx',
    'rand',
    'read',
    'readdir',
    'readline',
    'readlink',
    'readpipe',
    'recv',
    'redo',
    'ref',
    'rename',
    'require',
    'reset',
    'return',
    'reverse',
    'rewinddir',
    'rindex',
    'rmdir',
    'say',
    'scalar',
    'seek',
    'seekdir',
    'select',
    'semctl',
    'semget',
    'semop',
    'send',
    'setgrent',
    'sethostent',
    'setnetent',
    'setpgrp',
    'setpriority',
    'setprotoent',
    'setpwent',
    'setservent',
    'setsockopt',
    'shift',
    'shmctl',
    'shmget',
    'shmread',
    'shmwrite',
    'shutdown',
    'sin',
    'sleep',
    'socket',
    'socketpair',
    'sort',
    'splice',
    'split',
    'sprintf',
    'sqrt',
    'srand',
    'stat',
    'state',
    'study',
    'sub',
    'substr',
    'symlink',
    'syscall',
    'sysopen',
    'sysread',
    'sysseek',
    'system',
    'syswrite',
    'tell',
    'telldir',
    'tie',
    'tied',
    'time',
    'times',
    'tr',
    'truncate',
    'uc',
    'ucfirst',
    'umask',
    'undef',
    'unless',
    'unlink',
    'unpack',
    'unshift',
    'untie',
    'until',
    'use',
    'utime',
    'values',
    'vec',
    'wait',
    'waitpid',
    'wantarray',
    'warn',
    'when',
    'while',
    'write',
    'x|0',
    'xor',
    'y|0'
  ];

  // https://perldoc.perl.org/perlre#Modifiers
  const REGEX_MODIFIERS = /[dualxmsipngr]{0,12}/; // aa and xx are valid, making max length 12
  const PERL_KEYWORDS = {
    $pattern: /[\w.]+/,
    keyword: KEYWORDS.join(" ")
  };
  const SUBST = {
    className: 'subst',
    begin: '[$@]\\{',
    end: '\\}',
    keywords: PERL_KEYWORDS
  };
  const METHOD = {
    begin: /->\{/,
    end: /\}/
    // contains defined later
  };
  const VAR = {
    variants: [
      {
        begin: /\$\d/
      },
      {
        begin: concat(
          /[$%@](\^\w\b|#\w+(::\w+)*|\{\w+\}|\w+(::\w*)*)/,
          // negative look-ahead tries to avoid matching patterns that are not
          // Perl at all like $ident$, @ident@, etc.
          `(?![A-Za-z])(?![@$%])`
        )
      },
      {
        begin: /[$%@][^\s\w{]/,
        relevance: 0
      }
    ]
  };
  const STRING_CONTAINS = [
    hljs.BACKSLASH_ESCAPE,
    SUBST,
    VAR
  ];
  const REGEX_DELIMS = [
    /!/,
    /\//,
    /\|/,
    /\?/,
    /'/,
    /"/, // valid but infrequent and weird
    /#/ // valid but infrequent and weird
  ];
  /**
   * @param {string|RegExp} prefix
   * @param {string|RegExp} open
   * @param {string|RegExp} close
   */
  const PAIRED_DOUBLE_RE = (prefix, open, close = '\\1') => {
    const middle = (close === '\\1')
      ? close
      : concat(close, open);
    return concat(
      concat("(?:", prefix, ")"),
      open,
      /(?:\\.|[^\\\/])*?/,
      middle,
      /(?:\\.|[^\\\/])*?/,
      close,
      REGEX_MODIFIERS
    );
  };
  /**
   * @param {string|RegExp} prefix
   * @param {string|RegExp} open
   * @param {string|RegExp} close
   */
  const PAIRED_RE = (prefix, open, close) => {
    return concat(
      concat("(?:", prefix, ")"),
      open,
      /(?:\\.|[^\\\/])*?/,
      close,
      REGEX_MODIFIERS
    );
  };
  const PERL_DEFAULT_CONTAINS = [
    VAR,
    hljs.HASH_COMMENT_MODE,
    hljs.COMMENT(
      /^=\w/,
      /=cut/,
      {
        endsWithParent: true
      }
    ),
    METHOD,
    {
      className: 'string',
      contains: STRING_CONTAINS,
      variants: [
        {
          begin: 'q[qwxr]?\\s*\\(',
          end: '\\)',
          relevance: 5
        },
        {
          begin: 'q[qwxr]?\\s*\\[',
          end: '\\]',
          relevance: 5
        },
        {
          begin: 'q[qwxr]?\\s*\\{',
          end: '\\}',
          relevance: 5
        },
        {
          begin: 'q[qwxr]?\\s*\\|',
          end: '\\|',
          relevance: 5
        },
        {
          begin: 'q[qwxr]?\\s*<',
          end: '>',
          relevance: 5
        },
        {
          begin: 'qw\\s+q',
          end: 'q',
          relevance: 5
        },
        {
          begin: '\'',
          end: '\'',
          contains: [ hljs.BACKSLASH_ESCAPE ]
        },
        {
          begin: '"',
          end: '"'
        },
        {
          begin: '`',
          end: '`',
          contains: [ hljs.BACKSLASH_ESCAPE ]
        },
        {
          begin: /\{\w+\}/,
          relevance: 0
        },
        {
          begin: '-?\\w+\\s*=>',
          relevance: 0
        }
      ]
    },
    {
      className: 'number',
      begin: '(\\b0[0-7_]+)|(\\b0x[0-9a-fA-F_]+)|(\\b[1-9][0-9_]*(\\.[0-9_]+)?)|[0_]\\b',
      relevance: 0
    },
    { // regexp container
      begin: '(\\/\\/|' + hljs.RE_STARTERS_RE + '|\\b(split|return|print|reverse|grep)\\b)\\s*',
      keywords: 'split return print reverse grep',
      relevance: 0,
      contains: [
        hljs.HASH_COMMENT_MODE,
        {
          className: 'regexp',
          variants: [
            // allow matching common delimiters
            { begin: PAIRED_DOUBLE_RE("s|tr|y", either(...REGEX_DELIMS)) },
            // and then paired delmis
            { begin: PAIRED_DOUBLE_RE("s|tr|y", "\\(", "\\)") },
            { begin: PAIRED_DOUBLE_RE("s|tr|y", "\\[", "\\]") },
            { begin: PAIRED_DOUBLE_RE("s|tr|y", "\\{", "\\}") }
          ],
          relevance: 2
        },
        {
          className: 'regexp',
          variants: [
            {
              // could be a comment in many languages so do not count
              // as relevant
              begin: /(m|qr)\/\//,
              relevance: 0
            },
            // prefix is optional with /regex/
            { begin: PAIRED_RE("(?:m|qr)?", /\//, /\//)},
            // allow matching common delimiters
            { begin: PAIRED_RE("m|qr", either(...REGEX_DELIMS), /\1/)},
            // allow common paired delmins
            { begin: PAIRED_RE("m|qr", /\(/, /\)/)},
            { begin: PAIRED_RE("m|qr", /\[/, /\]/)},
            { begin: PAIRED_RE("m|qr", /\{/, /\}/)}
          ]
        }
      ]
    },
    {
      className: 'function',
      beginKeywords: 'sub',
      end: '(\\s*\\(.*?\\))?[;{]',
      excludeEnd: true,
      relevance: 5,
      contains: [ hljs.TITLE_MODE ]
    },
    {
      begin: '-\\w\\b',
      relevance: 0
    },
    {
      begin: "^__DATA__$",
      end: "^__END__$",
      subLanguage: 'mojolicious',
      contains: [
        {
          begin: "^@@.*",
          end: "$",
          className: "comment"
        }
      ]
    }
  ];
  SUBST.contains = PERL_DEFAULT_CONTAINS;
  METHOD.contains = PERL_DEFAULT_CONTAINS;

  return {
    name: 'Perl',
    aliases: [
      'pl',
      'pm'
    ],
    keywords: PERL_KEYWORDS,
    contains: PERL_DEFAULT_CONTAINS
  };
}

module.exports = perl;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcGVybC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBLFdBQVcsUUFBUTtBQUNuQixhQUFhO0FBQ2I7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBLFdBQVcsdUJBQXVCO0FBQ2xDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVyxzQkFBc0I7QUFDakMsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtB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RDtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQSxjQUFjLDBDQUEwQztBQUN4RDtBQUNBLGNBQWMsd0RBQXdEO0FBQ3RFO0FBQ0EsY0FBYyxxQ0FBcUM7QUFDbkQsY0FBYyxxQ0FBcUM7QUFDbkQsY0FBYyw0QkFBNEIsTUFBTTtBQUNoRDtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0EsK0JBQStCO0FBQy9CO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9wZXJsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogQHBhcmFtIHtzdHJpbmd9IHZhbHVlXG4gKiBAcmV0dXJucyB7UmVnRXhwfVxuICogKi9cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBzb3VyY2UocmUpIHtcbiAgaWYgKCFyZSkgcmV0dXJuIG51bGw7XG4gIGlmICh0eXBlb2YgcmUgPT09IFwic3RyaW5nXCIpIHJldHVybiByZTtcblxuICByZXR1cm4gcmUuc291cmNlO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7Li4uKFJlZ0V4cCB8IHN0cmluZykgfSBhcmdzXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBjb25jYXQoLi4uYXJncykge1xuICBjb25zdCBqb2luZWQgPSBhcmdzLm1hcCgoeCkgPT4gc291cmNlKHgpKS5qb2luKFwiXCIpO1xuICByZXR1cm4gam9pbmVkO1xufVxuXG4vKipcbiAqIEFueSBvZiB0aGUgcGFzc2VkIGV4cHJlc3NzaW9ucyBtYXkgbWF0Y2hcbiAqXG4gKiBDcmVhdGVzIGEgaHVnZSB0aGlzIHwgdGhpcyB8IHRoYXQgfCB0aGF0IG1hdGNoXG4gKiBAcGFyYW0geyhSZWdFeHAgfCBzdHJpbmcpW10gfSBhcmdzXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBlaXRoZXIoLi4uYXJncykge1xuICBjb25zdCBqb2luZWQgPSAnKCcgKyBhcmdzLm1hcCgoeCkgPT4gc291cmNlKHgpKS5qb2luKFwifFwiKSArIFwiKVwiO1xuICByZXR1cm4gam9pbmVkO1xufVxuXG4vKlxuTGFuZ3VhZ2U6IFBlcmxcbkF1dGhvcjogUGV0ZXIgTGVvbm92IDxnb2pwZWdAeWFuZGV4LnJ1PlxuV2Vic2l0ZTogaHR0cHM6Ly93d3cucGVybC5vcmdcbkNhdGVnb3J5OiBjb21tb25cbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBwZXJsKGhsanMpIHtcbiAgY29uc3QgS0VZV09SRFMgPSBbXG4gICAgJ2FicycsXG4gICAgJ2FjY2VwdCcsXG4gICAgJ2FsYXJtJyxcbiAgICAnYW5kJyxcbiAgICAnYXRhbjInLFxuICAgICdiaW5kJyxcbiAgICAnYmlubW9kZScsXG4gICAgJ2JsZXNzJyxcbiAgICAnYnJlYWsnLFxuICAgICdjYWxsZXInLFxuICAgICdjaGRpcicsXG4gICAgJ2NobW9kJyxcbiAgICAnY2hvbXAnLFxuICAgICdjaG9wJyxcbiAgICAnY2hvd24nLFxuICAgICdjaHInLFxuICAgICdjaHJvb3QnLFxuICAgICdjbG9zZScsXG4gICAgJ2Nsb3NlZGlyJyxcbiAgICAnY29ubmVjdCcsXG4gICAgJ2NvbnRpbnVlJyxcbiAgICAnY29zJyxcbiAgICAnY3J5cHQnLFxuICAgICdkYm1jbG9zZScsXG4gICAgJ2RibW9wZW4nLFxuICAgICdkZWZpbmVkJyxcbiAgICAnZGVsZXRlJyxcbiAgICAnZGllJyxcbiAgICAnZG8nLFxuICAgICdkdW1wJyxcbiAgICAnZWFjaCcsXG4gICAgJ2Vsc2UnLFxuICAgICdlbHNpZicsXG4gICAgJ2VuZGdyZW50JyxcbiAgICAnZW5kaG9zdGVudCcsXG4gICAgJ2VuZG5ldGVudCcsXG4gICAgJ2VuZHByb3RvZW50JyxcbiAgICAnZW5kcHdlbnQnLFxuICAgICdlbmRzZXJ2ZW50JyxcbiAgICAnZW9mJyxcbiAgICAnZXZhbCcsXG4gICAgJ2V4ZWMnLFxuICAgICdleGlzdHMnLFxuICAgICdleGl0JyxcbiAgICAnZXhwJyxcbiAgICAnZmNudGwnLFxuICAgICdmaWxlbm8nLFxuICAgICdmbG9jaycsXG4gICAgJ2ZvcicsXG4gICAgJ2ZvcmVhY2gnLFxuICAgICdmb3JrJyxcbiAgICAnZm9ybWF0JyxcbiAgICAnZm9ybWxpbmUnLFxuICAgICdnZXRjJyxcbiAgICAnZ2V0Z3JlbnQnLFxuICAgICdnZXRncmdpZCcsXG4gICAgJ2dldGdybmFtJyxcbiAgICAnZ2V0aG9zdGJ5YWRkcicsXG4gICAgJ2dldGhvc3RieW5hbWUnLFxuICAgICdnZXRob3N0ZW50JyxcbiAgICAnZ2V0bG9naW4nLFxuICAgICdnZXRuZXRieWFkZHInLFxuICAgICdnZXRuZXRieW5hbWUnLFxuICAgICdnZXRuZXRlbnQnLFxuICAgICdnZXRwZWVybmFtZScsXG4gICAgJ2dldHBncnAnLFxuICAgICdnZXRwcmlvcml0eScsXG4gICAgJ2dldHByb3RvYnluYW1lJyxcbiAgICAnZ2V0cHJvdG9ieW51bWJlcicsXG4gICAgJ2dldHByb3RvZW50JyxcbiAgICAnZ2V0cHdlbnQnLFxuICAgICdnZXRwd25hbScsXG4gICAgJ2dldHB3dWlkJyxcbiAgICAnZ2V0c2VydmJ5bmFtZScsXG4gICAgJ2dldHNlcnZieXBvcnQnLFxuICAgICdnZXRzZXJ2ZW50JyxcbiAgICAnZ2V0c29ja25hbWUnLFxuICAgICdnZXRzb2Nrb3B0JyxcbiAgICAnZ2l2ZW4nLFxuICAgICdnbG9iJyxcbiAgICAnZ210aW1lJyxcbiAgICAnZ290bycsXG4gICAgJ2dyZXAnLFxuICAgICdndCcsXG4gICAgJ2hleCcsXG4gICAgJ2lmJyxcbiAgICAnaW5kZXgnLFxuICAgICdpbnQnLFxuICAgICdpb2N0bCcsXG4gICAgJ2pvaW4nLFxuICAgICdrZXlzJyxcbiAgICAna2lsbCcsXG4gICAgJ2xhc3QnLFxuICAgICdsYycsXG4gICAgJ2xjZmlyc3QnLFxuICAgICdsZW5ndGgnLFxuICAgICdsaW5rJyxcbiAgICAnbGlzdGVuJyxcbiAgICAnbG9jYWwnLFxuICAgICdsb2NhbHRpbWUnLFxuICAgICdsb2cnLFxuICAgICdsc3RhdCcsXG4gICAgJ2x0JyxcbiAgICAnbWEnLFxuICAgICdtYXAnLFxuICAgICdta2RpcicsXG4gICAgJ21zZ2N0bCcsXG4gICAgJ21zZ2dldCcsXG4gICAgJ21zZ3JjdicsXG4gICAgJ21zZ3NuZCcsXG4gICAgJ215JyxcbiAgICAnbmUnLFxuICAgICduZXh0JyxcbiAgICAnbm8nLFxuICAgICdub3QnLFxuICAgICdvY3QnLFxuICAgICdvcGVuJyxcbiAgICAnb3BlbmRpcicsXG4gICAgJ29yJyxcbiAgICAnb3JkJyxcbiAgICAnb3VyJyxcbiAgICAncGFjaycsXG4gICAgJ3BhY2thZ2UnLFxuICAgICdwaXBlJyxcbiAgICAncG9wJyxcbiAgICAncG9zJyxcbiAgICAncHJpbnQnLFxuICAgICdwcmludGYnLFxuICAgICdwcm90b3R5cGUnLFxuICAgICdwdXNoJyxcbiAgICAncXwwJyxcbiAgICAncXEnLFxuICAgICdxdW90ZW1ldGEnLFxuICAgICdxdycsXG4gICAgJ3F4JyxcbiAgICAncmFuZCcsXG4gICAgJ3JlYWQnLFxuICAgICdyZWFkZGlyJyxcbiAgICAncmVhZGxpbmUnLFxuICAgICdyZWFkbGluaycsXG4gICAgJ3JlYWRwaXBlJyxcbiAgICAncmVjdicsXG4gICAgJ3JlZG8nLFxuICAgICdyZWYnLFxuICAgICdyZW5hbWUnLFxuICAgICdyZXF1aXJlJyxcbiAgICAncmVzZXQnLFxuICAgICdyZXR1cm4nLFxuICAgICdyZXZlcnNlJyxcbiAgICAncmV3aW5kZGlyJyxcbiAgICAncmluZGV4JyxcbiAgICAncm1kaXInLFxuICAgICdzYXknLFxuICAgICdzY2FsYXInLFxuICAgICdzZWVrJyxcbiAgICAnc2Vla2RpcicsXG4gICAgJ3NlbGVjdCcsXG4gICAgJ3NlbWN0bCcsXG4gICAgJ3NlbWdldCcsXG4gICAgJ3NlbW9wJyxcbiAgICAnc2VuZCcsXG4gICAgJ3NldGdyZW50JyxcbiAgICAnc2V0aG9zdGVudCcsXG4gICAgJ3NldG5ldGVudCcsXG4gICAgJ3NldHBncnAnLFxuICAgICdzZXRwcmlvcml0eScsXG4gICAgJ3NldHByb3RvZW50JyxcbiAgICAnc2V0cHdlbnQnLFxuICAgICdzZXRzZXJ2ZW50JyxcbiAgICAnc2V0c29ja29wdCcsXG4gICAgJ3NoaWZ0JyxcbiAgICAnc2htY3RsJyxcbiAgICAnc2htZ2V0JyxcbiAgICAnc2htcmVhZCcsXG4gICAgJ3NobXdyaXRlJyxcbiAgICAnc2h1dGRvd24nLFxuICAgICdzaW4nLFxuICAgICdzbGVlcCcsXG4gICAgJ3NvY2tldCcsXG4gICAgJ3NvY2tldHBhaXInLFxuICAgICdzb3J0JyxcbiAgICAnc3BsaWNlJyxcbiAgICAnc3BsaXQnLFxuICAgICdzcHJpbnRmJyxcbiAgICAnc3FydCcsXG4gICAgJ3NyYW5kJyxcbiAgICAnc3RhdCcsXG4gICAgJ3N0YXRlJyxcbiAgICAnc3R1ZHknLFxuICAgICdzdWInLFxuICAgICdzdWJzdHInLFxuICAgICdzeW1saW5rJyxcbiAgICAnc3lzY2FsbCcsXG4gICAgJ3N5c29wZW4nLFxuICAgICdzeXNyZWFkJyxcbiAgICAnc3lzc2VlaycsXG4gICAgJ3N5c3RlbScsXG4gICAgJ3N5c3dyaXRlJyxcbiAgICAndGVsbCcsXG4gICAgJ3RlbGxkaXInLFxuICAgICd0aWUnLFxuICAgICd0aWVkJyxcbiAgICAndGltZScsXG4gICAgJ3RpbWVzJyxcbiAgICAndHInLFxuICAgICd0cnVuY2F0ZScsXG4gICAgJ3VjJyxcbiAgICAndWNmaXJzdCcsXG4gICAgJ3VtYXNrJyxcbiAgICAndW5kZWYnLFxuICAgICd1bmxlc3MnLFxuICAgICd1bmxpbmsnLFxuICAgICd1bnBhY2snLFxuICAgICd1bnNoaWZ0JyxcbiAgICAndW50aWUnLFxuICAgICd1bnRpbCcsXG4gICAgJ3VzZScsXG4gICAgJ3V0aW1lJyxcbiAgICAndmFsdWVzJyxcbiAgICAndmVjJyxcbiAgICAnd2FpdCcsXG4gICAgJ3dhaXRwaWQnLFxuICAgICd3YW50YXJyYXknLFxuICAgICd3YXJuJyxcbiAgICAnd2hlbicsXG4gICAgJ3doaWxlJyxcbiAgICAnd3JpdGUnLFxuICAgICd4fDAnLFxuICAgICd4b3InLFxuICAgICd5fDAnXG4gIF07XG5cbiAgLy8gaHR0cHM6Ly9wZXJsZG9jLnBlcmwub3JnL3BlcmxyZSNNb2RpZmllcnNcbiAgY29uc3QgUkVHRVhfTU9ESUZJRVJTID0gL1tkdWFseG1zaXBuZ3JdezAsMTJ9LzsgLy8gYWEgYW5kIHh4IGFyZSB2YWxpZCwgbWFraW5nIG1heCBsZW5ndGggMTJcbiAgY29uc3QgUEVSTF9LRVlXT1JEUyA9IHtcbiAgICAkcGF0dGVybjogL1tcXHcuXSsvLFxuICAgIGtleXdvcmQ6IEtFWVdPUkRTLmpvaW4oXCIgXCIpXG4gIH07XG4gIGNvbnN0IFNVQlNUID0ge1xuICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICBiZWdpbjogJ1skQF1cXFxceycsXG4gICAgZW5kOiAnXFxcXH0nLFxuICAgIGtleXdvcmRzOiBQRVJMX0tFWVdPUkRTXG4gIH07XG4gIGNvbnN0IE1FVEhPRCA9IHtcbiAgICBiZWdpbjogLy0+XFx7LyxcbiAgICBlbmQ6IC9cXH0vXG4gICAgLy8gY29udGFpbnMgZGVmaW5lZCBsYXRlclxuICB9O1xuICBjb25zdCBWQVIgPSB7XG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCRcXGQvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogY29uY2F0KFxuICAgICAgICAgIC9bJCVAXShcXF5cXHdcXGJ8I1xcdysoOjpcXHcrKSp8XFx7XFx3K1xcfXxcXHcrKDo6XFx3KikqKS8sXG4gICAgICAgICAgLy8gbmVnYXRpdmUgbG9vay1haGVhZCB0cmllcyB0byBhdm9pZCBtYXRjaGluZyBwYXR0ZXJucyB0aGF0IGFyZSBub3RcbiAgICAgICAgICAvLyBQZXJsIGF0IGFsbCBsaWtlICRpZGVudCQsIEBpZGVudEAsIGV0Yy5cbiAgICAgICAgICBgKD8hW0EtWmEtel0pKD8hW0AkJV0pYFxuICAgICAgICApXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1skJUBdW15cXHNcXHd7XS8sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF1cbiAgfTtcbiAgY29uc3QgU1RSSU5HX0NPTlRBSU5TID0gW1xuICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICBTVUJTVCxcbiAgICBWQVJcbiAgXTtcbiAgY29uc3QgUkVHRVhfREVMSU1TID0gW1xuICAgIC8hLyxcbiAgICAvXFwvLyxcbiAgICAvXFx8LyxcbiAgICAvXFw/LyxcbiAgICAvJy8sXG4gICAgL1wiLywgLy8gdmFsaWQgYnV0IGluZnJlcXVlbnQgYW5kIHdlaXJkXG4gICAgLyMvIC8vIHZhbGlkIGJ1dCBpbmZyZXF1ZW50IGFuZCB3ZWlyZFxuICBdO1xuICAvKipcbiAgICogQHBhcmFtIHtzdHJpbmd8UmVnRXhwfSBwcmVmaXhcbiAgICogQHBhcmFtIHtzdHJpbmd8UmVnRXhwfSBvcGVuXG4gICAqIEBwYXJhbSB7c3RyaW5nfFJlZ0V4cH0gY2xvc2VcbiAgICovXG4gIGNvbnN0IFBBSVJFRF9ET1VCTEVfUkUgPSAocHJlZml4LCBvcGVuLCBjbG9zZSA9ICdcXFxcMScpID0+IHtcbiAgICBjb25zdCBtaWRkbGUgPSAoY2xvc2UgPT09ICdcXFxcMScpXG4gICAgICA/IGNsb3NlXG4gICAgICA6IGNvbmNhdChjbG9zZSwgb3Blbik7XG4gICAgcmV0dXJuIGNvbmNhdChcbiAgICAgIGNvbmNhdChcIig/OlwiLCBwcmVmaXgsIFwiKVwiKSxcbiAgICAgIG9wZW4sXG4gICAgICAvKD86XFxcXC58W15cXFxcXFwvXSkqPy8sXG4gICAgICBtaWRkbGUsXG4gICAgICAvKD86XFxcXC58W15cXFxcXFwvXSkqPy8sXG4gICAgICBjbG9zZSxcbiAgICAgIFJFR0VYX01PRElGSUVSU1xuICAgICk7XG4gIH07XG4gIC8qKlxuICAgKiBAcGFyYW0ge3N0cmluZ3xSZWdFeHB9IHByZWZpeFxuICAgKiBAcGFyYW0ge3N0cmluZ3xSZWdFeHB9IG9wZW5cbiAgICogQHBhcmFtIHtzdHJpbmd8UmVnRXhwfSBjbG9zZVxuICAgKi9cbiAgY29uc3QgUEFJUkVEX1JFID0gKHByZWZpeCwgb3BlbiwgY2xvc2UpID0+IHtcbiAgICByZXR1cm4gY29uY2F0KFxuICAgICAgY29uY2F0KFwiKD86XCIsIHByZWZpeCwgXCIpXCIpLFxuICAgICAgb3BlbixcbiAgICAgIC8oPzpcXFxcLnxbXlxcXFxcXC9dKSo/LyxcbiAgICAgIGNsb3NlLFxuICAgICAgUkVHRVhfTU9ESUZJRVJTXG4gICAgKTtcbiAgfTtcbiAgY29uc3QgUEVSTF9ERUZBVUxUX0NPTlRBSU5TID0gW1xuICAgIFZBUixcbiAgICBobGpzLkhBU0hfQ09NTUVOVF9NT0RFLFxuICAgIGhsanMuQ09NTUVOVChcbiAgICAgIC9ePVxcdy8sXG4gICAgICAvPWN1dC8sXG4gICAgICB7XG4gICAgICAgIGVuZHNXaXRoUGFyZW50OiB0cnVlXG4gICAgICB9XG4gICAgKSxcbiAgICBNRVRIT0QsXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgIGNvbnRhaW5zOiBTVFJJTkdfQ09OVEFJTlMsXG4gICAgICB2YXJpYW50czogW1xuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46ICdxW3F3eHJdP1xcXFxzKlxcXFwoJyxcbiAgICAgICAgICBlbmQ6ICdcXFxcKScsXG4gICAgICAgICAgcmVsZXZhbmNlOiA1XG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogJ3FbcXd4cl0/XFxcXHMqXFxcXFsnLFxuICAgICAgICAgIGVuZDogJ1xcXFxdJyxcbiAgICAgICAgICByZWxldmFuY2U6IDVcbiAgICAgICAgfSxcbiAgICAgICAge1xuICAgICAgICAgIGJlZ2luOiAncVtxd3hyXT9cXFxccypcXFxceycsXG4gICAgICAgICAgZW5kOiAnXFxcXH0nLFxuICAgICAgICAgIHJlbGV2YW5jZTogNVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46ICdxW3F3eHJdP1xcXFxzKlxcXFx8JyxcbiAgICAgICAgICBlbmQ6ICdcXFxcfCcsXG4gICAgICAgICAgcmVsZXZhbmNlOiA1XG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogJ3FbcXd4cl0/XFxcXHMqPCcsXG4gICAgICAgICAgZW5kOiAnPicsXG4gICAgICAgICAgcmVsZXZhbmNlOiA1XG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogJ3F3XFxcXHMrcScsXG4gICAgICAgICAgZW5kOiAncScsXG4gICAgICAgICAgcmVsZXZhbmNlOiA1XG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogJ1xcJycsXG4gICAgICAgICAgZW5kOiAnXFwnJyxcbiAgICAgICAgICBjb250YWluczogWyBobGpzLkJBQ0tTTEFTSF9FU0NBUEUgXVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46ICdcIicsXG4gICAgICAgICAgZW5kOiAnXCInXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogJ2AnLFxuICAgICAgICAgIGVuZDogJ2AnLFxuICAgICAgICAgIGNvbnRhaW5zOiBbIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSBdXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogL1xce1xcdytcXH0vLFxuICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46ICctP1xcXFx3K1xcXFxzKj0+JyxcbiAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgfVxuICAgICAgXVxuICAgIH0sXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICAgIGJlZ2luOiAnKFxcXFxiMFswLTdfXSspfChcXFxcYjB4WzAtOWEtZkEtRl9dKyl8KFxcXFxiWzEtOV1bMC05X10qKFxcXFwuWzAtOV9dKyk/KXxbMF9dXFxcXGInLFxuICAgICAgcmVsZXZhbmNlOiAwXG4gICAgfSxcbiAgICB7IC8vIHJlZ2V4cCBjb250YWluZXJcbiAgICAgIGJlZ2luOiAnKFxcXFwvXFxcXC98JyArIGhsanMuUkVfU1RBUlRFUlNfUkUgKyAnfFxcXFxiKHNwbGl0fHJldHVybnxwcmludHxyZXZlcnNlfGdyZXApXFxcXGIpXFxcXHMqJyxcbiAgICAgIGtleXdvcmRzOiAnc3BsaXQgcmV0dXJuIHByaW50IHJldmVyc2UgZ3JlcCcsXG4gICAgICByZWxldmFuY2U6IDAsXG4gICAgICBjb250YWluczogW1xuICAgICAgICBobGpzLkhBU0hfQ09NTUVOVF9NT0RFLFxuICAgICAgICB7XG4gICAgICAgICAgY2xhc3NOYW1lOiAncmVnZXhwJyxcbiAgICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgICAgLy8gYWxsb3cgbWF0Y2hpbmcgY29tbW9uIGRlbGltaXRlcnNcbiAgICAgICAgICAgIHsgYmVnaW46IFBBSVJFRF9ET1VCTEVfUkUoXCJzfHRyfHlcIiwgZWl0aGVyKC4uLlJFR0VYX0RFTElNUykpIH0sXG4gICAgICAgICAgICAvLyBhbmQgdGhlbiBwYWlyZWQgZGVsbWlzXG4gICAgICAgICAgICB7IGJlZ2luOiBQQUlSRURfRE9VQkxFX1JFKFwic3x0cnx5XCIsIFwiXFxcXChcIiwgXCJcXFxcKVwiKSB9LFxuICAgICAgICAgICAgeyBiZWdpbjogUEFJUkVEX0RPVUJMRV9SRShcInN8dHJ8eVwiLCBcIlxcXFxbXCIsIFwiXFxcXF1cIikgfSxcbiAgICAgICAgICAgIHsgYmVnaW46IFBBSVJFRF9ET1VCTEVfUkUoXCJzfHRyfHlcIiwgXCJcXFxce1wiLCBcIlxcXFx9XCIpIH1cbiAgICAgICAgICBdLFxuICAgICAgICAgIHJlbGV2YW5jZTogMlxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgY2xhc3NOYW1lOiAncmVnZXhwJyxcbiAgICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgICAge1xuICAgICAgICAgICAgICAvLyBjb3VsZCBiZSBhIGNvbW1lbnQgaW4gbWFueSBsYW5ndWFnZXMgc28gZG8gbm90IGNvdW50XG4gICAgICAgICAgICAgIC8vIGFzIHJlbGV2YW50XG4gICAgICAgICAgICAgIGJlZ2luOiAvKG18cXIpXFwvXFwvLyxcbiAgICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgICB9LFxuICAgICAgICAgICAgLy8gcHJlZml4IGlzIG9wdGlvbmFsIHdpdGggL3JlZ2V4L1xuICAgICAgICAgICAgeyBiZWdpbjogUEFJUkVEX1JFKFwiKD86bXxxcik/XCIsIC9cXC8vLCAvXFwvLyl9LFxuICAgICAgICAgICAgLy8gYWxsb3cgbWF0Y2hpbmcgY29tbW9uIGRlbGltaXRlcnNcbiAgICAgICAgICAgIHsgYmVnaW46IFBBSVJFRF9SRShcIm18cXJcIiwgZWl0aGVyKC4uLlJFR0VYX0RFTElNUyksIC9cXDEvKX0sXG4gICAgICAgICAgICAvLyBhbGxvdyBjb21tb24gcGFpcmVkIGRlbG1pbnNcbiAgICAgICAgICAgIHsgYmVnaW46IFBBSVJFRF9SRShcIm18cXJcIiwgL1xcKC8sIC9cXCkvKX0sXG4gICAgICAgICAgICB7IGJlZ2luOiBQQUlSRURfUkUoXCJtfHFyXCIsIC9cXFsvLCAvXFxdLyl9LFxuICAgICAgICAgICAgeyBiZWdpbjogUEFJUkVEX1JFKFwibXxxclwiLCAvXFx7LywgL1xcfS8pfVxuICAgICAgICAgIF1cbiAgICAgICAgfVxuICAgICAgXVxuICAgIH0sXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgYmVnaW5LZXl3b3JkczogJ3N1YicsXG4gICAgICBlbmQ6ICcoXFxcXHMqXFxcXCguKj9cXFxcKSk/Wzt7XScsXG4gICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgcmVsZXZhbmNlOiA1LFxuICAgICAgY29udGFpbnM6IFsgaGxqcy5USVRMRV9NT0RFIF1cbiAgICB9LFxuICAgIHtcbiAgICAgIGJlZ2luOiAnLVxcXFx3XFxcXGInLFxuICAgICAgcmVsZXZhbmNlOiAwXG4gICAgfSxcbiAgICB7XG4gICAgICBiZWdpbjogXCJeX19EQVRBX18kXCIsXG4gICAgICBlbmQ6IFwiXl9fRU5EX18kXCIsXG4gICAgICBzdWJMYW5ndWFnZTogJ21vam9saWNpb3VzJyxcbiAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogXCJeQEAuKlwiLFxuICAgICAgICAgIGVuZDogXCIkXCIsXG4gICAgICAgICAgY2xhc3NOYW1lOiBcImNvbW1lbnRcIlxuICAgICAgICB9XG4gICAgICBdXG4gICAgfVxuICBdO1xuICBTVUJTVC5jb250YWlucyA9IFBFUkxfREVGQVVMVF9DT05UQUlOUztcbiAgTUVUSE9ELmNvbnRhaW5zID0gUEVSTF9ERUZBVUxUX0NPTlRBSU5TO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1BlcmwnLFxuICAgIGFsaWFzZXM6IFtcbiAgICAgICdwbCcsXG4gICAgICAncG0nXG4gICAgXSxcbiAgICBrZXl3b3JkczogUEVSTF9LRVlXT1JEUyxcbiAgICBjb250YWluczogUEVSTF9ERUZBVUxUX0NPTlRBSU5TXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gcGVybDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==