(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_php"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/php.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/php.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: PHP
Author: Victor Karamzin <Victor.Karamzin@enterra-inc.com>
Contributors: Evgeny Stepanischev <imbolk@gmail.com>, Ivan Sagalaev <maniac@softwaremaniacs.org>
Website: https://www.php.net
Category: common
*/

/**
 * @param {HLJSApi} hljs
 * @returns {LanguageDetail}
 * */
function php(hljs) {
  const VARIABLE = {
    className: 'variable',
    begin: '\\$+[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*' +
      // negative look-ahead tries to avoid matching patterns that are not
      // Perl at all like $ident$, @ident@, etc.
      `(?![A-Za-z0-9])(?![$])`
  };
  const PREPROCESSOR = {
    className: 'meta',
    variants: [
      { begin: /<\?php/, relevance: 10 }, // boost for obvious PHP
      { begin: /<\?[=]?/ },
      { begin: /\?>/ } // end php tag
    ]
  };
  const SUBST = {
    className: 'subst',
    variants: [
      { begin: /\$\w+/ },
      { begin: /\{\$/, end: /\}/ }
    ]
  };
  const SINGLE_QUOTED = hljs.inherit(hljs.APOS_STRING_MODE, {
    illegal: null,
  });
  const DOUBLE_QUOTED = hljs.inherit(hljs.QUOTE_STRING_MODE, {
    illegal: null,
    contains: hljs.QUOTE_STRING_MODE.contains.concat(SUBST),
  });
  const HEREDOC = hljs.END_SAME_AS_BEGIN({
    begin: /<<<[ \t]*(\w+)\n/,
    end: /[ \t]*(\w+)\b/,
    contains: hljs.QUOTE_STRING_MODE.contains.concat(SUBST),
  });
  const STRING = {
    className: 'string',
    contains: [hljs.BACKSLASH_ESCAPE, PREPROCESSOR],
    variants: [
      hljs.inherit(SINGLE_QUOTED, {
        begin: "b'", end: "'",
      }),
      hljs.inherit(DOUBLE_QUOTED, {
        begin: 'b"', end: '"',
      }),
      DOUBLE_QUOTED,
      SINGLE_QUOTED,
      HEREDOC
    ]
  };
  const NUMBER = {
    className: 'number',
    variants: [
      { begin: `\\b0b[01]+(?:_[01]+)*\\b` }, // Binary w/ underscore support
      { begin: `\\b0o[0-7]+(?:_[0-7]+)*\\b` }, // Octals w/ underscore support
      { begin: `\\b0x[\\da-f]+(?:_[\\da-f]+)*\\b` }, // Hex w/ underscore support
      // Decimals w/ underscore support, with optional fragments and scientific exponent (e) suffix.
      { begin: `(?:\\b\\d+(?:_\\d+)*(\\.(?:\\d+(?:_\\d+)*))?|\\B\\.\\d+)(?:e[+-]?\\d+)?` }
    ],
    relevance: 0
  };
  const KEYWORDS = {
    keyword:
    // Magic constants:
    // <https://www.php.net/manual/en/language.constants.predefined.php>
    '__CLASS__ __DIR__ __FILE__ __FUNCTION__ __LINE__ __METHOD__ __NAMESPACE__ __TRAIT__ ' +
    // Function that look like language construct or language construct that look like function:
    // List of keywords that may not require parenthesis
    'die echo exit include include_once print require require_once ' +
    // These are not language construct (function) but operate on the currently-executing function and can access the current symbol table
    // 'compact extract func_get_arg func_get_args func_num_args get_called_class get_parent_class ' +
    // Other keywords:
    // <https://www.php.net/manual/en/reserved.php>
    // <https://www.php.net/manual/en/language.types.type-juggling.php>
    'array abstract and as binary bool boolean break callable case catch class clone const continue declare ' +
    'default do double else elseif empty enddeclare endfor endforeach endif endswitch endwhile enum eval extends ' +
    'final finally float for foreach from global goto if implements instanceof insteadof int integer interface ' +
    'isset iterable list match|0 mixed new object or private protected public real return string switch throw trait ' +
    'try unset use var void while xor yield',
    literal: 'false null true',
    built_in:
    // Standard PHP library:
    // <https://www.php.net/manual/en/book.spl.php>
    'Error|0 ' + // error is too common a name esp since PHP is case in-sensitive
    'AppendIterator ArgumentCountError ArithmeticError ArrayIterator ArrayObject AssertionError BadFunctionCallException BadMethodCallException CachingIterator CallbackFilterIterator CompileError Countable DirectoryIterator DivisionByZeroError DomainException EmptyIterator ErrorException Exception FilesystemIterator FilterIterator GlobIterator InfiniteIterator InvalidArgumentException IteratorIterator LengthException LimitIterator LogicException MultipleIterator NoRewindIterator OutOfBoundsException OutOfRangeException OuterIterator OverflowException ParentIterator ParseError RangeException RecursiveArrayIterator RecursiveCachingIterator RecursiveCallbackFilterIterator RecursiveDirectoryIterator RecursiveFilterIterator RecursiveIterator RecursiveIteratorIterator RecursiveRegexIterator RecursiveTreeIterator RegexIterator RuntimeException SeekableIterator SplDoublyLinkedList SplFileInfo SplFileObject SplFixedArray SplHeap SplMaxHeap SplMinHeap SplObjectStorage SplObserver SplObserver SplPriorityQueue SplQueue SplStack SplSubject SplSubject SplTempFileObject TypeError UnderflowException UnexpectedValueException UnhandledMatchError ' +
    // Reserved interfaces:
    // <https://www.php.net/manual/en/reserved.interfaces.php>
    'ArrayAccess Closure Generator Iterator IteratorAggregate Serializable Stringable Throwable Traversable WeakReference WeakMap ' +
    // Reserved classes:
    // <https://www.php.net/manual/en/reserved.classes.php>
    'Directory __PHP_Incomplete_Class parent php_user_filter self static stdClass'
  };
  return {
    aliases: ['php3', 'php4', 'php5', 'php6', 'php7', 'php8'],
    case_insensitive: true,
    keywords: KEYWORDS,
    contains: [
      hljs.HASH_COMMENT_MODE,
      hljs.COMMENT('//', '$', {contains: [PREPROCESSOR]}),
      hljs.COMMENT(
        '/\\*',
        '\\*/',
        {
          contains: [
            {
              className: 'doctag',
              begin: '@[A-Za-z]+'
            }
          ]
        }
      ),
      hljs.COMMENT(
        '__halt_compiler.+?;',
        false,
        {
          endsWithParent: true,
          keywords: '__halt_compiler'
        }
      ),
      PREPROCESSOR,
      {
        className: 'keyword', begin: /\$this\b/
      },
      VARIABLE,
      {
        // swallow composed identifiers to avoid parsing them as keywords
        begin: /(::|->)+[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*/
      },
      {
        className: 'function',
        relevance: 0,
        beginKeywords: 'fn function', end: /[;{]/, excludeEnd: true,
        illegal: '[$%\\[]',
        contains: [
          {
            beginKeywords: 'use',
          },
          hljs.UNDERSCORE_TITLE_MODE,
          {
            begin: '=>', // No markup, just a relevance booster
            endsParent: true
          },
          {
            className: 'params',
            begin: '\\(', end: '\\)',
            excludeBegin: true,
            excludeEnd: true,
            keywords: KEYWORDS,
            contains: [
              'self',
              VARIABLE,
              hljs.C_BLOCK_COMMENT_MODE,
              STRING,
              NUMBER
            ]
          }
        ]
      },
      {
        className: 'class',
        variants: [
          { beginKeywords: "enum", illegal: /[($"]/ },
          { beginKeywords: "class interface trait", illegal: /[:($"]/ }
        ],
        relevance: 0,
        end: /\{/,
        excludeEnd: true,
        contains: [
          {beginKeywords: 'extends implements'},
          hljs.UNDERSCORE_TITLE_MODE
        ]
      },
      {
        beginKeywords: 'namespace',
        relevance: 0,
        end: ';',
        illegal: /[.']/,
        contains: [hljs.UNDERSCORE_TITLE_MODE]
      },
      {
        beginKeywords: 'use',
        relevance: 0,
        end: ';',
        contains: [hljs.UNDERSCORE_TITLE_MODE]
      },
      STRING,
      NUMBER
    ]
  };
}

module.exports = php;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcGhwLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyxTQUFTO0FBQ3BCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxRQUFRLGdDQUFnQztBQUN4QyxRQUFRLGtCQUFrQjtBQUMxQixRQUFRLGVBQWU7QUFDdkI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFFBQVEsZ0JBQWdCO0FBQ3hCLFFBQVEsVUFBVSxhQUFhO0FBQy9CO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsR0FBRztBQUNIO0FBQ0E7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBO0FBQ0E7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsUUFBUSxtQ0FBbUM7QUFDM0MsUUFBUSxxQ0FBcUM7QUFDN0MsUUFBUSwyQ0FBMkM7QUFDbkQ7QUFDQSxRQUFRO0FBQ1I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSwrQkFBK0IseUJBQXlCO0FBQ3hEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsNEJBQTRCO0FBQzVCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSwrQ0FBK0M7QUFDL0M7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLFlBQVkseUNBQXlDO0FBQ3JELFlBQVk7QUFDWjtBQUNBO0FBQ0EsZ0JBQWdCO0FBQ2hCO0FBQ0E7QUFDQSxXQUFXLG9DQUFvQztBQUMvQztBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGVBQWU7QUFDZjtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGVBQWU7QUFDZjtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9waHAuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBQSFBcbkF1dGhvcjogVmljdG9yIEthcmFtemluIDxWaWN0b3IuS2FyYW16aW5AZW50ZXJyYS1pbmMuY29tPlxuQ29udHJpYnV0b3JzOiBFdmdlbnkgU3RlcGFuaXNjaGV2IDxpbWJvbGtAZ21haWwuY29tPiwgSXZhbiBTYWdhbGFldiA8bWFuaWFjQHNvZnR3YXJlbWFuaWFjcy5vcmc+XG5XZWJzaXRlOiBodHRwczovL3d3dy5waHAubmV0XG5DYXRlZ29yeTogY29tbW9uXG4qL1xuXG4vKipcbiAqIEBwYXJhbSB7SExKU0FwaX0gaGxqc1xuICogQHJldHVybnMge0xhbmd1YWdlRGV0YWlsfVxuICogKi9cbmZ1bmN0aW9uIHBocChobGpzKSB7XG4gIGNvbnN0IFZBUklBQkxFID0ge1xuICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICBiZWdpbjogJ1xcXFwkK1thLXpBLVpfXFx4N2YtXFx4ZmZdW2EtekEtWjAtOV9cXHg3Zi1cXHhmZl0qJyArXG4gICAgICAvLyBuZWdhdGl2ZSBsb29rLWFoZWFkIHRyaWVzIHRvIGF2b2lkIG1hdGNoaW5nIHBhdHRlcm5zIHRoYXQgYXJlIG5vdFxuICAgICAgLy8gUGVybCBhdCBhbGwgbGlrZSAkaWRlbnQkLCBAaWRlbnRALCBldGMuXG4gICAgICBgKD8hW0EtWmEtejAtOV0pKD8hWyRdKWBcbiAgfTtcbiAgY29uc3QgUFJFUFJPQ0VTU09SID0ge1xuICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7IGJlZ2luOiAvPFxcP3BocC8sIHJlbGV2YW5jZTogMTAgfSwgLy8gYm9vc3QgZm9yIG9idmlvdXMgUEhQXG4gICAgICB7IGJlZ2luOiAvPFxcP1s9XT8vIH0sXG4gICAgICB7IGJlZ2luOiAvXFw/Pi8gfSAvLyBlbmQgcGhwIHRhZ1xuICAgIF1cbiAgfTtcbiAgY29uc3QgU1VCU1QgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3Vic3QnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7IGJlZ2luOiAvXFwkXFx3Ky8gfSxcbiAgICAgIHsgYmVnaW46IC9cXHtcXCQvLCBlbmQ6IC9cXH0vIH1cbiAgICBdXG4gIH07XG4gIGNvbnN0IFNJTkdMRV9RVU9URUQgPSBobGpzLmluaGVyaXQoaGxqcy5BUE9TX1NUUklOR19NT0RFLCB7XG4gICAgaWxsZWdhbDogbnVsbCxcbiAgfSk7XG4gIGNvbnN0IERPVUJMRV9RVU9URUQgPSBobGpzLmluaGVyaXQoaGxqcy5RVU9URV9TVFJJTkdfTU9ERSwge1xuICAgIGlsbGVnYWw6IG51bGwsXG4gICAgY29udGFpbnM6IGhsanMuUVVPVEVfU1RSSU5HX01PREUuY29udGFpbnMuY29uY2F0KFNVQlNUKSxcbiAgfSk7XG4gIGNvbnN0IEhFUkVET0MgPSBobGpzLkVORF9TQU1FX0FTX0JFR0lOKHtcbiAgICBiZWdpbjogLzw8PFsgXFx0XSooXFx3KylcXG4vLFxuICAgIGVuZDogL1sgXFx0XSooXFx3KylcXGIvLFxuICAgIGNvbnRhaW5zOiBobGpzLlFVT1RFX1NUUklOR19NT0RFLmNvbnRhaW5zLmNvbmNhdChTVUJTVCksXG4gIH0pO1xuICBjb25zdCBTVFJJTkcgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBjb250YWluczogW2hsanMuQkFDS1NMQVNIX0VTQ0FQRSwgUFJFUFJPQ0VTU09SXSxcbiAgICB2YXJpYW50czogW1xuICAgICAgaGxqcy5pbmhlcml0KFNJTkdMRV9RVU9URUQsIHtcbiAgICAgICAgYmVnaW46IFwiYidcIiwgZW5kOiBcIidcIixcbiAgICAgIH0pLFxuICAgICAgaGxqcy5pbmhlcml0KERPVUJMRV9RVU9URUQsIHtcbiAgICAgICAgYmVnaW46ICdiXCInLCBlbmQ6ICdcIicsXG4gICAgICB9KSxcbiAgICAgIERPVUJMRV9RVU9URUQsXG4gICAgICBTSU5HTEVfUVVPVEVELFxuICAgICAgSEVSRURPQ1xuICAgIF1cbiAgfTtcbiAgY29uc3QgTlVNQkVSID0ge1xuICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHsgYmVnaW46IGBcXFxcYjBiWzAxXSsoPzpfWzAxXSspKlxcXFxiYCB9LCAvLyBCaW5hcnkgdy8gdW5kZXJzY29yZSBzdXBwb3J0XG4gICAgICB7IGJlZ2luOiBgXFxcXGIwb1swLTddKyg/Ol9bMC03XSspKlxcXFxiYCB9LCAvLyBPY3RhbHMgdy8gdW5kZXJzY29yZSBzdXBwb3J0XG4gICAgICB7IGJlZ2luOiBgXFxcXGIweFtcXFxcZGEtZl0rKD86X1tcXFxcZGEtZl0rKSpcXFxcYmAgfSwgLy8gSGV4IHcvIHVuZGVyc2NvcmUgc3VwcG9ydFxuICAgICAgLy8gRGVjaW1hbHMgdy8gdW5kZXJzY29yZSBzdXBwb3J0LCB3aXRoIG9wdGlvbmFsIGZyYWdtZW50cyBhbmQgc2NpZW50aWZpYyBleHBvbmVudCAoZSkgc3VmZml4LlxuICAgICAgeyBiZWdpbjogYCg/OlxcXFxiXFxcXGQrKD86X1xcXFxkKykqKFxcXFwuKD86XFxcXGQrKD86X1xcXFxkKykqKSk/fFxcXFxCXFxcXC5cXFxcZCspKD86ZVsrLV0/XFxcXGQrKT9gIH1cbiAgICBdLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuICBjb25zdCBLRVlXT1JEUyA9IHtcbiAgICBrZXl3b3JkOlxuICAgIC8vIE1hZ2ljIGNvbnN0YW50czpcbiAgICAvLyA8aHR0cHM6Ly93d3cucGhwLm5ldC9tYW51YWwvZW4vbGFuZ3VhZ2UuY29uc3RhbnRzLnByZWRlZmluZWQucGhwPlxuICAgICdfX0NMQVNTX18gX19ESVJfXyBfX0ZJTEVfXyBfX0ZVTkNUSU9OX18gX19MSU5FX18gX19NRVRIT0RfXyBfX05BTUVTUEFDRV9fIF9fVFJBSVRfXyAnICtcbiAgICAvLyBGdW5jdGlvbiB0aGF0IGxvb2sgbGlrZSBsYW5ndWFnZSBjb25zdHJ1Y3Qgb3IgbGFuZ3VhZ2UgY29uc3RydWN0IHRoYXQgbG9vayBsaWtlIGZ1bmN0aW9uOlxuICAgIC8vIExpc3Qgb2Yga2V5d29yZHMgdGhhdCBtYXkgbm90IHJlcXVpcmUgcGFyZW50aGVzaXNcbiAgICAnZGllIGVjaG8gZXhpdCBpbmNsdWRlIGluY2x1ZGVfb25jZSBwcmludCByZXF1aXJlIHJlcXVpcmVfb25jZSAnICtcbiAgICAvLyBUaGVzZSBhcmUgbm90IGxhbmd1YWdlIGNvbnN0cnVjdCAoZnVuY3Rpb24pIGJ1dCBvcGVyYXRlIG9uIHRoZSBjdXJyZW50bHktZXhlY3V0aW5nIGZ1bmN0aW9uIGFuZCBjYW4gYWNjZXNzIHRoZSBjdXJyZW50IHN5bWJvbCB0YWJsZVxuICAgIC8vICdjb21wYWN0IGV4dHJhY3QgZnVuY19nZXRfYXJnIGZ1bmNfZ2V0X2FyZ3MgZnVuY19udW1fYXJncyBnZXRfY2FsbGVkX2NsYXNzIGdldF9wYXJlbnRfY2xhc3MgJyArXG4gICAgLy8gT3RoZXIga2V5d29yZHM6XG4gICAgLy8gPGh0dHBzOi8vd3d3LnBocC5uZXQvbWFudWFsL2VuL3Jlc2VydmVkLnBocD5cbiAgICAvLyA8aHR0cHM6Ly93d3cucGhwLm5ldC9tYW51YWwvZW4vbGFuZ3VhZ2UudHlwZXMudHlwZS1qdWdnbGluZy5waHA+XG4gICAgJ2FycmF5IGFic3RyYWN0IGFuZCBhcyBiaW5hcnkgYm9vbCBib29sZWFuIGJyZWFrIGNhbGxhYmxlIGNhc2UgY2F0Y2ggY2xhc3MgY2xvbmUgY29uc3QgY29udGludWUgZGVjbGFyZSAnICtcbiAgICAnZGVmYXVsdCBkbyBkb3VibGUgZWxzZSBlbHNlaWYgZW1wdHkgZW5kZGVjbGFyZSBlbmRmb3IgZW5kZm9yZWFjaCBlbmRpZiBlbmRzd2l0Y2ggZW5kd2hpbGUgZW51bSBldmFsIGV4dGVuZHMgJyArXG4gICAgJ2ZpbmFsIGZpbmFsbHkgZmxvYXQgZm9yIGZvcmVhY2ggZnJvbSBnbG9iYWwgZ290byBpZiBpbXBsZW1lbnRzIGluc3RhbmNlb2YgaW5zdGVhZG9mIGludCBpbnRlZ2VyIGludGVyZmFjZSAnICtcbiAgICAnaXNzZXQgaXRlcmFibGUgbGlzdCBtYXRjaHwwIG1peGVkIG5ldyBvYmplY3Qgb3IgcHJpdmF0ZSBwcm90ZWN0ZWQgcHVibGljIHJlYWwgcmV0dXJuIHN0cmluZyBzd2l0Y2ggdGhyb3cgdHJhaXQgJyArXG4gICAgJ3RyeSB1bnNldCB1c2UgdmFyIHZvaWQgd2hpbGUgeG9yIHlpZWxkJyxcbiAgICBsaXRlcmFsOiAnZmFsc2UgbnVsbCB0cnVlJyxcbiAgICBidWlsdF9pbjpcbiAgICAvLyBTdGFuZGFyZCBQSFAgbGlicmFyeTpcbiAgICAvLyA8aHR0cHM6Ly93d3cucGhwLm5ldC9tYW51YWwvZW4vYm9vay5zcGwucGhwPlxuICAgICdFcnJvcnwwICcgKyAvLyBlcnJvciBpcyB0b28gY29tbW9uIGEgbmFtZSBlc3Agc2luY2UgUEhQIGlzIGNhc2UgaW4tc2Vuc2l0aXZlXG4gICAgJ0FwcGVuZEl0ZXJhdG9yIEFyZ3VtZW50Q291bnRFcnJvciBBcml0aG1ldGljRXJyb3IgQXJyYXlJdGVyYXRvciBBcnJheU9iamVjdCBBc3NlcnRpb25FcnJvciBCYWRGdW5jdGlvbkNhbGxFeGNlcHRpb24gQmFkTWV0aG9kQ2FsbEV4Y2VwdGlvbiBDYWNoaW5nSXRlcmF0b3IgQ2FsbGJhY2tGaWx0ZXJJdGVyYXRvciBDb21waWxlRXJyb3IgQ291bnRhYmxlIERpcmVjdG9yeUl0ZXJhdG9yIERpdmlzaW9uQnlaZXJvRXJyb3IgRG9tYWluRXhjZXB0aW9uIEVtcHR5SXRlcmF0b3IgRXJyb3JFeGNlcHRpb24gRXhjZXB0aW9uIEZpbGVzeXN0ZW1JdGVyYXRvciBGaWx0ZXJJdGVyYXRvciBHbG9iSXRlcmF0b3IgSW5maW5pdGVJdGVyYXRvciBJbnZhbGlkQXJndW1lbnRFeGNlcHRpb24gSXRlcmF0b3JJdGVyYXRvciBMZW5ndGhFeGNlcHRpb24gTGltaXRJdGVyYXRvciBMb2dpY0V4Y2VwdGlvbiBNdWx0aXBsZUl0ZXJhdG9yIE5vUmV3aW5kSXRlcmF0b3IgT3V0T2ZCb3VuZHNFeGNlcHRpb24gT3V0T2ZSYW5nZUV4Y2VwdGlvbiBPdXRlckl0ZXJhdG9yIE92ZXJmbG93RXhjZXB0aW9uIFBhcmVudEl0ZXJhdG9yIFBhcnNlRXJyb3IgUmFuZ2VFeGNlcHRpb24gUmVjdXJzaXZlQXJyYXlJdGVyYXRvciBSZWN1cnNpdmVDYWNoaW5nSXRlcmF0b3IgUmVjdXJzaXZlQ2FsbGJhY2tGaWx0ZXJJdGVyYXRvciBSZWN1cnNpdmVEaXJlY3RvcnlJdGVyYXRvciBSZWN1cnNpdmVGaWx0ZXJJdGVyYXRvciBSZWN1cnNpdmVJdGVyYXRvciBSZWN1cnNpdmVJdGVyYXRvckl0ZXJhdG9yIFJlY3Vyc2l2ZVJlZ2V4SXRlcmF0b3IgUmVjdXJzaXZlVHJlZUl0ZXJhdG9yIFJlZ2V4SXRlcmF0b3IgUnVudGltZUV4Y2VwdGlvbiBTZWVrYWJsZUl0ZXJhdG9yIFNwbERvdWJseUxpbmtlZExpc3QgU3BsRmlsZUluZm8gU3BsRmlsZU9iamVjdCBTcGxGaXhlZEFycmF5IFNwbEhlYXAgU3BsTWF4SGVhcCBTcGxNaW5IZWFwIFNwbE9iamVjdFN0b3JhZ2UgU3BsT2JzZXJ2ZXIgU3BsT2JzZXJ2ZXIgU3BsUHJpb3JpdHlRdWV1ZSBTcGxRdWV1ZSBTcGxTdGFjayBTcGxTdWJqZWN0IFNwbFN1YmplY3QgU3BsVGVtcEZpbGVPYmplY3QgVHlwZUVycm9yIFVuZGVyZmxvd0V4Y2VwdGlvbiBVbmV4cGVjdGVkVmFsdWVFeGNlcHRpb24gVW5oYW5kbGVkTWF0Y2hFcnJvciAnICtcbiAgICAvLyBSZXNlcnZlZCBpbnRlcmZhY2VzOlxuICAgIC8vIDxodHRwczovL3d3dy5waHAubmV0L21hbnVhbC9lbi9yZXNlcnZlZC5pbnRlcmZhY2VzLnBocD5cbiAgICAnQXJyYXlBY2Nlc3MgQ2xvc3VyZSBHZW5lcmF0b3IgSXRlcmF0b3IgSXRlcmF0b3JBZ2dyZWdhdGUgU2VyaWFsaXphYmxlIFN0cmluZ2FibGUgVGhyb3dhYmxlIFRyYXZlcnNhYmxlIFdlYWtSZWZlcmVuY2UgV2Vha01hcCAnICtcbiAgICAvLyBSZXNlcnZlZCBjbGFzc2VzOlxuICAgIC8vIDxodHRwczovL3d3dy5waHAubmV0L21hbnVhbC9lbi9yZXNlcnZlZC5jbGFzc2VzLnBocD5cbiAgICAnRGlyZWN0b3J5IF9fUEhQX0luY29tcGxldGVfQ2xhc3MgcGFyZW50IHBocF91c2VyX2ZpbHRlciBzZWxmIHN0YXRpYyBzdGRDbGFzcydcbiAgfTtcbiAgcmV0dXJuIHtcbiAgICBhbGlhc2VzOiBbJ3BocDMnLCAncGhwNCcsICdwaHA1JywgJ3BocDYnLCAncGhwNycsICdwaHA4J10sXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNPTU1FTlQoJy8vJywgJyQnLCB7Y29udGFpbnM6IFtQUkVQUk9DRVNTT1JdfSksXG4gICAgICBobGpzLkNPTU1FTlQoXG4gICAgICAgICcvXFxcXConLFxuICAgICAgICAnXFxcXCovJyxcbiAgICAgICAge1xuICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICB7XG4gICAgICAgICAgICAgIGNsYXNzTmFtZTogJ2RvY3RhZycsXG4gICAgICAgICAgICAgIGJlZ2luOiAnQFtBLVphLXpdKydcbiAgICAgICAgICAgIH1cbiAgICAgICAgICBdXG4gICAgICAgIH1cbiAgICAgICksXG4gICAgICBobGpzLkNPTU1FTlQoXG4gICAgICAgICdfX2hhbHRfY29tcGlsZXIuKz87JyxcbiAgICAgICAgZmFsc2UsXG4gICAgICAgIHtcbiAgICAgICAgICBlbmRzV2l0aFBhcmVudDogdHJ1ZSxcbiAgICAgICAgICBrZXl3b3JkczogJ19faGFsdF9jb21waWxlcidcbiAgICAgICAgfVxuICAgICAgKSxcbiAgICAgIFBSRVBST0NFU1NPUixcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAna2V5d29yZCcsIGJlZ2luOiAvXFwkdGhpc1xcYi9cbiAgICAgIH0sXG4gICAgICBWQVJJQUJMRSxcbiAgICAgIHtcbiAgICAgICAgLy8gc3dhbGxvdyBjb21wb3NlZCBpZGVudGlmaWVycyB0byBhdm9pZCBwYXJzaW5nIHRoZW0gYXMga2V5d29yZHNcbiAgICAgICAgYmVnaW46IC8oOjp8LT4pK1thLXpBLVpfXFx4N2YtXFx4ZmZdW2EtekEtWjAtOV9cXHg3Zi1cXHhmZl0qL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdmbiBmdW5jdGlvbicsIGVuZDogL1s7e10vLCBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICBpbGxlZ2FsOiAnWyQlXFxcXFtdJyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbktleXdvcmRzOiAndXNlJyxcbiAgICAgICAgICB9LFxuICAgICAgICAgIGhsanMuVU5ERVJTQ09SRV9USVRMRV9NT0RFLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnPT4nLCAvLyBObyBtYXJrdXAsIGp1c3QgYSByZWxldmFuY2UgYm9vc3RlclxuICAgICAgICAgICAgZW5kc1BhcmVudDogdHJ1ZVxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAncGFyYW1zJyxcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXCgnLCBlbmQ6ICdcXFxcKScsXG4gICAgICAgICAgICBleGNsdWRlQmVnaW46IHRydWUsXG4gICAgICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICAgICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAgJ3NlbGYnLFxuICAgICAgICAgICAgICBWQVJJQUJMRSxcbiAgICAgICAgICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgICAgICAgU1RSSU5HLFxuICAgICAgICAgICAgICBOVU1CRVJcbiAgICAgICAgICAgIF1cbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2NsYXNzJyxcbiAgICAgICAgdmFyaWFudHM6IFtcbiAgICAgICAgICB7IGJlZ2luS2V5d29yZHM6IFwiZW51bVwiLCBpbGxlZ2FsOiAvWygkXCJdLyB9LFxuICAgICAgICAgIHsgYmVnaW5LZXl3b3JkczogXCJjbGFzcyBpbnRlcmZhY2UgdHJhaXRcIiwgaWxsZWdhbDogL1s6KCRcIl0vIH1cbiAgICAgICAgXSxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBlbmQ6IC9cXHsvLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtiZWdpbktleXdvcmRzOiAnZXh0ZW5kcyBpbXBsZW1lbnRzJ30sXG4gICAgICAgICAgaGxqcy5VTkRFUlNDT1JFX1RJVExFX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ25hbWVzcGFjZScsXG4gICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgZW5kOiAnOycsXG4gICAgICAgIGlsbGVnYWw6IC9bLiddLyxcbiAgICAgICAgY29udGFpbnM6IFtobGpzLlVOREVSU0NPUkVfVElUTEVfTU9ERV1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICd1c2UnLFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIGVuZDogJzsnLFxuICAgICAgICBjb250YWluczogW2hsanMuVU5ERVJTQ09SRV9USVRMRV9NT0RFXVxuICAgICAgfSxcbiAgICAgIFNUUklORyxcbiAgICAgIE5VTUJFUlxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBwaHA7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=