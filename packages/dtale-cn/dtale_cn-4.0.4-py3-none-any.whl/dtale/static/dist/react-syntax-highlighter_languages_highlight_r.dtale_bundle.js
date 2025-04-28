(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_r"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/r.js":
/*!********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/r.js ***!
  \********************************************************************************************/
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
 * @param {RegExp | string } re
 * @returns {string}
 */
function lookahead(re) {
  return concat('(?=', re, ')');
}

/**
 * @param {...(RegExp | string) } args
 * @returns {string}
 */
function concat(...args) {
  const joined = args.map((x) => source(x)).join("");
  return joined;
}

/*
Language: R
Description: R is a free software environment for statistical computing and graphics.
Author: Joe Cheng <joe@rstudio.org>
Contributors: Konrad Rudolph <konrad.rudolph@gmail.com>
Website: https://www.r-project.org
Category: common,scientific
*/

/** @type LanguageFn */
function r(hljs) {
  // Identifiers in R cannot start with `_`, but they can start with `.` if it
  // is not immediately followed by a digit.
  // R also supports quoted identifiers, which are near-arbitrary sequences
  // delimited by backticks (`…`), which may contain escape sequences. These are
  // handled in a separate mode. See `test/markup/r/names.txt` for examples.
  // FIXME: Support Unicode identifiers.
  const IDENT_RE = /(?:(?:[a-zA-Z]|\.[._a-zA-Z])[._a-zA-Z0-9]*)|\.(?!\d)/;
  const SIMPLE_IDENT = /[a-zA-Z][a-zA-Z_0-9]*/;

  return {
    name: 'R',

    // only in Haskell, not R
    illegal: /->/,
    keywords: {
      $pattern: IDENT_RE,
      keyword:
        'function if in break next repeat else for while',
      literal:
        'NULL NA TRUE FALSE Inf NaN NA_integer_|10 NA_real_|10 ' +
        'NA_character_|10 NA_complex_|10',
      built_in:
        // Builtin constants
        'LETTERS letters month.abb month.name pi T F ' +
        // Primitive functions
        // These are all the functions in `base` that are implemented as a
        // `.Primitive`, minus those functions that are also keywords.
        'abs acos acosh all any anyNA Arg as.call as.character ' +
        'as.complex as.double as.environment as.integer as.logical ' +
        'as.null.default as.numeric as.raw asin asinh atan atanh attr ' +
        'attributes baseenv browser c call ceiling class Conj cos cosh ' +
        'cospi cummax cummin cumprod cumsum digamma dim dimnames ' +
        'emptyenv exp expression floor forceAndCall gamma gc.time ' +
        'globalenv Im interactive invisible is.array is.atomic is.call ' +
        'is.character is.complex is.double is.environment is.expression ' +
        'is.finite is.function is.infinite is.integer is.language ' +
        'is.list is.logical is.matrix is.na is.name is.nan is.null ' +
        'is.numeric is.object is.pairlist is.raw is.recursive is.single ' +
        'is.symbol lazyLoadDBfetch length lgamma list log max min ' +
        'missing Mod names nargs nzchar oldClass on.exit pos.to.env ' +
        'proc.time prod quote range Re rep retracemem return round ' +
        'seq_along seq_len seq.int sign signif sin sinh sinpi sqrt ' +
        'standardGeneric substitute sum switch tan tanh tanpi tracemem ' +
        'trigamma trunc unclass untracemem UseMethod xtfrm',
    },
    compilerExtensions: [
      // allow beforeMatch to act as a "qualifier" for the match
      // the full match begin must be [beforeMatch][begin]
      (mode, parent) => {
        if (!mode.beforeMatch) return;
        // starts conflicts with endsParent which we need to make sure the child
        // rule is not matched multiple times
        if (mode.starts) throw new Error("beforeMatch cannot be used with starts");

        const originalMode = Object.assign({}, mode);
        Object.keys(mode).forEach((key) => { delete mode[key]; });

        mode.begin = concat(originalMode.beforeMatch, lookahead(originalMode.begin));
        mode.starts = {
          relevance: 0,
          contains: [
            Object.assign(originalMode, { endsParent: true })
          ]
        };
        mode.relevance = 0;

        delete originalMode.beforeMatch;
      }
    ],
    contains: [
      // Roxygen comments
      hljs.COMMENT(
        /#'/,
        /$/,
        {
          contains: [
            {
              // Handle `@examples` separately to cause all subsequent code
              // until the next `@`-tag on its own line to be kept as-is,
              // preventing highlighting. This code is example R code, so nested
              // doctags shouldn’t be treated as such. See
              // `test/markup/r/roxygen.txt` for an example.
              className: 'doctag',
              begin: '@examples',
              starts: {
                contains: [
                  { begin: /\n/ },
                  {
                    begin: /#'\s*(?=@[a-zA-Z]+)/,
                    endsParent: true,
                  },
                  {
                    begin: /#'/,
                    end: /$/,
                    excludeBegin: true,
                  }
                ]
              }
            },
            {
              // Handle `@param` to highlight the parameter name following
              // after.
              className: 'doctag',
              begin: '@param',
              end: /$/,
              contains: [
                {
                  className: 'variable',
                  variants: [
                    { begin: IDENT_RE },
                    { begin: /`(?:\\.|[^`\\])+`/ }
                  ],
                  endsParent: true
                }
              ]
            },
            {
              className: 'doctag',
              begin: /@[a-zA-Z]+/
            },
            {
              className: 'meta-keyword',
              begin: /\\[a-zA-Z]+/,
            }
          ]
        }
      ),

      hljs.HASH_COMMENT_MODE,

      {
        className: 'string',
        contains: [hljs.BACKSLASH_ESCAPE],
        variants: [
          hljs.END_SAME_AS_BEGIN({ begin: /[rR]"(-*)\(/, end: /\)(-*)"/ }),
          hljs.END_SAME_AS_BEGIN({ begin: /[rR]"(-*)\{/, end: /\}(-*)"/ }),
          hljs.END_SAME_AS_BEGIN({ begin: /[rR]"(-*)\[/, end: /\](-*)"/ }),
          hljs.END_SAME_AS_BEGIN({ begin: /[rR]'(-*)\(/, end: /\)(-*)'/ }),
          hljs.END_SAME_AS_BEGIN({ begin: /[rR]'(-*)\{/, end: /\}(-*)'/ }),
          hljs.END_SAME_AS_BEGIN({ begin: /[rR]'(-*)\[/, end: /\](-*)'/ }),
          {begin: '"', end: '"', relevance: 0},
          {begin: "'", end: "'", relevance: 0}
        ],
      },
      {
        className: 'number',
        relevance: 0,
        beforeMatch: /([^a-zA-Z0-9._])/, // not part of an identifier
        variants: [
          // TODO: replace with negative look-behind when available
          // { begin: /(?<![a-zA-Z0-9._])0[xX][0-9a-fA-F]+\.[0-9a-fA-F]*[pP][+-]?\d+i?/ },
          // { begin: /(?<![a-zA-Z0-9._])0[xX][0-9a-fA-F]+([pP][+-]?\d+)?[Li]?/ },
          // { begin: /(?<![a-zA-Z0-9._])(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?[Li]?/ }
          {
            // Special case: only hexadecimal binary powers can contain fractions.
            match: /0[xX][0-9a-fA-F]+\.[0-9a-fA-F]*[pP][+-]?\d+i?/,
          },
          {
            match: /0[xX][0-9a-fA-F]+([pP][+-]?\d+)?[Li]?/
          },
          {
            match: /(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?[Li]?/,
          }
        ],
      },
      {
        // infix operator
        begin: '%',
        end: '%'
      },
      // relevance boost for assignment
      {
        begin: concat(SIMPLE_IDENT, "\\s+<-\\s+")
      },
      {
        // escaped identifier
        begin: '`',
        end: '`',
        contains: [
          { begin: /\\./ }
        ]
      }
    ]
  };
}

module.exports = r;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfci5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBLFdBQVcsUUFBUTtBQUNuQixhQUFhO0FBQ2I7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLFdBQVcsdUJBQXVCO0FBQ2xDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEsNkNBQTZDO0FBQzdDLDZDQUE2QyxtQkFBbUI7O0FBRWhFO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsMENBQTBDLGtCQUFrQjtBQUM1RDtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG9CQUFvQixhQUFhO0FBQ2pDO0FBQ0E7QUFDQTtBQUNBLG1CQUFtQjtBQUNuQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHNCQUFzQixpQkFBaUI7QUFDdkMsc0JBQXNCO0FBQ3RCO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG1DQUFtQyxzQ0FBc0M7QUFDekUsbUNBQW1DLG1CQUFtQixXQUFXLFFBQVE7QUFDekUsbUNBQW1DLHNDQUFzQztBQUN6RSxtQ0FBbUMsc0NBQXNDO0FBQ3pFLG1DQUFtQyxtQkFBbUIsV0FBVyxRQUFRO0FBQ3pFLG1DQUFtQyxzQ0FBc0M7QUFDekUsV0FBVyxtQ0FBbUM7QUFDOUMsV0FBVztBQUNYO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGVBQWUsMEVBQTBFO0FBQ3pGLGVBQWUsa0VBQWtFO0FBQ2pGLGVBQWU7QUFDZjtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9yLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogQHBhcmFtIHtzdHJpbmd9IHZhbHVlXG4gKiBAcmV0dXJucyB7UmVnRXhwfVxuICogKi9cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBzb3VyY2UocmUpIHtcbiAgaWYgKCFyZSkgcmV0dXJuIG51bGw7XG4gIGlmICh0eXBlb2YgcmUgPT09IFwic3RyaW5nXCIpIHJldHVybiByZTtcblxuICByZXR1cm4gcmUuc291cmNlO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGxvb2thaGVhZChyZSkge1xuICByZXR1cm4gY29uY2F0KCcoPz0nLCByZSwgJyknKTtcbn1cblxuLyoqXG4gKiBAcGFyYW0gey4uLihSZWdFeHAgfCBzdHJpbmcpIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gY29uY2F0KC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcIlwiKTtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuLypcbkxhbmd1YWdlOiBSXG5EZXNjcmlwdGlvbjogUiBpcyBhIGZyZWUgc29mdHdhcmUgZW52aXJvbm1lbnQgZm9yIHN0YXRpc3RpY2FsIGNvbXB1dGluZyBhbmQgZ3JhcGhpY3MuXG5BdXRob3I6IEpvZSBDaGVuZyA8am9lQHJzdHVkaW8ub3JnPlxuQ29udHJpYnV0b3JzOiBLb25yYWQgUnVkb2xwaCA8a29ucmFkLnJ1ZG9scGhAZ21haWwuY29tPlxuV2Vic2l0ZTogaHR0cHM6Ly93d3cuci1wcm9qZWN0Lm9yZ1xuQ2F0ZWdvcnk6IGNvbW1vbixzY2llbnRpZmljXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gcihobGpzKSB7XG4gIC8vIElkZW50aWZpZXJzIGluIFIgY2Fubm90IHN0YXJ0IHdpdGggYF9gLCBidXQgdGhleSBjYW4gc3RhcnQgd2l0aCBgLmAgaWYgaXRcbiAgLy8gaXMgbm90IGltbWVkaWF0ZWx5IGZvbGxvd2VkIGJ5IGEgZGlnaXQuXG4gIC8vIFIgYWxzbyBzdXBwb3J0cyBxdW90ZWQgaWRlbnRpZmllcnMsIHdoaWNoIGFyZSBuZWFyLWFyYml0cmFyeSBzZXF1ZW5jZXNcbiAgLy8gZGVsaW1pdGVkIGJ5IGJhY2t0aWNrcyAoYOKApmApLCB3aGljaCBtYXkgY29udGFpbiBlc2NhcGUgc2VxdWVuY2VzLiBUaGVzZSBhcmVcbiAgLy8gaGFuZGxlZCBpbiBhIHNlcGFyYXRlIG1vZGUuIFNlZSBgdGVzdC9tYXJrdXAvci9uYW1lcy50eHRgIGZvciBleGFtcGxlcy5cbiAgLy8gRklYTUU6IFN1cHBvcnQgVW5pY29kZSBpZGVudGlmaWVycy5cbiAgY29uc3QgSURFTlRfUkUgPSAvKD86KD86W2EtekEtWl18XFwuWy5fYS16QS1aXSlbLl9hLXpBLVowLTldKil8XFwuKD8hXFxkKS87XG4gIGNvbnN0IFNJTVBMRV9JREVOVCA9IC9bYS16QS1aXVthLXpBLVpfMC05XSovO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1InLFxuXG4gICAgLy8gb25seSBpbiBIYXNrZWxsLCBub3QgUlxuICAgIGlsbGVnYWw6IC8tPi8sXG4gICAga2V5d29yZHM6IHtcbiAgICAgICRwYXR0ZXJuOiBJREVOVF9SRSxcbiAgICAgIGtleXdvcmQ6XG4gICAgICAgICdmdW5jdGlvbiBpZiBpbiBicmVhayBuZXh0IHJlcGVhdCBlbHNlIGZvciB3aGlsZScsXG4gICAgICBsaXRlcmFsOlxuICAgICAgICAnTlVMTCBOQSBUUlVFIEZBTFNFIEluZiBOYU4gTkFfaW50ZWdlcl98MTAgTkFfcmVhbF98MTAgJyArXG4gICAgICAgICdOQV9jaGFyYWN0ZXJffDEwIE5BX2NvbXBsZXhffDEwJyxcbiAgICAgIGJ1aWx0X2luOlxuICAgICAgICAvLyBCdWlsdGluIGNvbnN0YW50c1xuICAgICAgICAnTEVUVEVSUyBsZXR0ZXJzIG1vbnRoLmFiYiBtb250aC5uYW1lIHBpIFQgRiAnICtcbiAgICAgICAgLy8gUHJpbWl0aXZlIGZ1bmN0aW9uc1xuICAgICAgICAvLyBUaGVzZSBhcmUgYWxsIHRoZSBmdW5jdGlvbnMgaW4gYGJhc2VgIHRoYXQgYXJlIGltcGxlbWVudGVkIGFzIGFcbiAgICAgICAgLy8gYC5QcmltaXRpdmVgLCBtaW51cyB0aG9zZSBmdW5jdGlvbnMgdGhhdCBhcmUgYWxzbyBrZXl3b3Jkcy5cbiAgICAgICAgJ2FicyBhY29zIGFjb3NoIGFsbCBhbnkgYW55TkEgQXJnIGFzLmNhbGwgYXMuY2hhcmFjdGVyICcgK1xuICAgICAgICAnYXMuY29tcGxleCBhcy5kb3VibGUgYXMuZW52aXJvbm1lbnQgYXMuaW50ZWdlciBhcy5sb2dpY2FsICcgK1xuICAgICAgICAnYXMubnVsbC5kZWZhdWx0IGFzLm51bWVyaWMgYXMucmF3IGFzaW4gYXNpbmggYXRhbiBhdGFuaCBhdHRyICcgK1xuICAgICAgICAnYXR0cmlidXRlcyBiYXNlZW52IGJyb3dzZXIgYyBjYWxsIGNlaWxpbmcgY2xhc3MgQ29uaiBjb3MgY29zaCAnICtcbiAgICAgICAgJ2Nvc3BpIGN1bW1heCBjdW1taW4gY3VtcHJvZCBjdW1zdW0gZGlnYW1tYSBkaW0gZGltbmFtZXMgJyArXG4gICAgICAgICdlbXB0eWVudiBleHAgZXhwcmVzc2lvbiBmbG9vciBmb3JjZUFuZENhbGwgZ2FtbWEgZ2MudGltZSAnICtcbiAgICAgICAgJ2dsb2JhbGVudiBJbSBpbnRlcmFjdGl2ZSBpbnZpc2libGUgaXMuYXJyYXkgaXMuYXRvbWljIGlzLmNhbGwgJyArXG4gICAgICAgICdpcy5jaGFyYWN0ZXIgaXMuY29tcGxleCBpcy5kb3VibGUgaXMuZW52aXJvbm1lbnQgaXMuZXhwcmVzc2lvbiAnICtcbiAgICAgICAgJ2lzLmZpbml0ZSBpcy5mdW5jdGlvbiBpcy5pbmZpbml0ZSBpcy5pbnRlZ2VyIGlzLmxhbmd1YWdlICcgK1xuICAgICAgICAnaXMubGlzdCBpcy5sb2dpY2FsIGlzLm1hdHJpeCBpcy5uYSBpcy5uYW1lIGlzLm5hbiBpcy5udWxsICcgK1xuICAgICAgICAnaXMubnVtZXJpYyBpcy5vYmplY3QgaXMucGFpcmxpc3QgaXMucmF3IGlzLnJlY3Vyc2l2ZSBpcy5zaW5nbGUgJyArXG4gICAgICAgICdpcy5zeW1ib2wgbGF6eUxvYWREQmZldGNoIGxlbmd0aCBsZ2FtbWEgbGlzdCBsb2cgbWF4IG1pbiAnICtcbiAgICAgICAgJ21pc3NpbmcgTW9kIG5hbWVzIG5hcmdzIG56Y2hhciBvbGRDbGFzcyBvbi5leGl0IHBvcy50by5lbnYgJyArXG4gICAgICAgICdwcm9jLnRpbWUgcHJvZCBxdW90ZSByYW5nZSBSZSByZXAgcmV0cmFjZW1lbSByZXR1cm4gcm91bmQgJyArXG4gICAgICAgICdzZXFfYWxvbmcgc2VxX2xlbiBzZXEuaW50IHNpZ24gc2lnbmlmIHNpbiBzaW5oIHNpbnBpIHNxcnQgJyArXG4gICAgICAgICdzdGFuZGFyZEdlbmVyaWMgc3Vic3RpdHV0ZSBzdW0gc3dpdGNoIHRhbiB0YW5oIHRhbnBpIHRyYWNlbWVtICcgK1xuICAgICAgICAndHJpZ2FtbWEgdHJ1bmMgdW5jbGFzcyB1bnRyYWNlbWVtIFVzZU1ldGhvZCB4dGZybScsXG4gICAgfSxcbiAgICBjb21waWxlckV4dGVuc2lvbnM6IFtcbiAgICAgIC8vIGFsbG93IGJlZm9yZU1hdGNoIHRvIGFjdCBhcyBhIFwicXVhbGlmaWVyXCIgZm9yIHRoZSBtYXRjaFxuICAgICAgLy8gdGhlIGZ1bGwgbWF0Y2ggYmVnaW4gbXVzdCBiZSBbYmVmb3JlTWF0Y2hdW2JlZ2luXVxuICAgICAgKG1vZGUsIHBhcmVudCkgPT4ge1xuICAgICAgICBpZiAoIW1vZGUuYmVmb3JlTWF0Y2gpIHJldHVybjtcbiAgICAgICAgLy8gc3RhcnRzIGNvbmZsaWN0cyB3aXRoIGVuZHNQYXJlbnQgd2hpY2ggd2UgbmVlZCB0byBtYWtlIHN1cmUgdGhlIGNoaWxkXG4gICAgICAgIC8vIHJ1bGUgaXMgbm90IG1hdGNoZWQgbXVsdGlwbGUgdGltZXNcbiAgICAgICAgaWYgKG1vZGUuc3RhcnRzKSB0aHJvdyBuZXcgRXJyb3IoXCJiZWZvcmVNYXRjaCBjYW5ub3QgYmUgdXNlZCB3aXRoIHN0YXJ0c1wiKTtcblxuICAgICAgICBjb25zdCBvcmlnaW5hbE1vZGUgPSBPYmplY3QuYXNzaWduKHt9LCBtb2RlKTtcbiAgICAgICAgT2JqZWN0LmtleXMobW9kZSkuZm9yRWFjaCgoa2V5KSA9PiB7IGRlbGV0ZSBtb2RlW2tleV07IH0pO1xuXG4gICAgICAgIG1vZGUuYmVnaW4gPSBjb25jYXQob3JpZ2luYWxNb2RlLmJlZm9yZU1hdGNoLCBsb29rYWhlYWQob3JpZ2luYWxNb2RlLmJlZ2luKSk7XG4gICAgICAgIG1vZGUuc3RhcnRzID0ge1xuICAgICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgT2JqZWN0LmFzc2lnbihvcmlnaW5hbE1vZGUsIHsgZW5kc1BhcmVudDogdHJ1ZSB9KVxuICAgICAgICAgIF1cbiAgICAgICAgfTtcbiAgICAgICAgbW9kZS5yZWxldmFuY2UgPSAwO1xuXG4gICAgICAgIGRlbGV0ZSBvcmlnaW5hbE1vZGUuYmVmb3JlTWF0Y2g7XG4gICAgICB9XG4gICAgXSxcbiAgICBjb250YWluczogW1xuICAgICAgLy8gUm94eWdlbiBjb21tZW50c1xuICAgICAgaGxqcy5DT01NRU5UKFxuICAgICAgICAvIycvLFxuICAgICAgICAvJC8sXG4gICAgICAgIHtcbiAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAge1xuICAgICAgICAgICAgICAvLyBIYW5kbGUgYEBleGFtcGxlc2Agc2VwYXJhdGVseSB0byBjYXVzZSBhbGwgc3Vic2VxdWVudCBjb2RlXG4gICAgICAgICAgICAgIC8vIHVudGlsIHRoZSBuZXh0IGBAYC10YWcgb24gaXRzIG93biBsaW5lIHRvIGJlIGtlcHQgYXMtaXMsXG4gICAgICAgICAgICAgIC8vIHByZXZlbnRpbmcgaGlnaGxpZ2h0aW5nLiBUaGlzIGNvZGUgaXMgZXhhbXBsZSBSIGNvZGUsIHNvIG5lc3RlZFxuICAgICAgICAgICAgICAvLyBkb2N0YWdzIHNob3VsZG7igJl0IGJlIHRyZWF0ZWQgYXMgc3VjaC4gU2VlXG4gICAgICAgICAgICAgIC8vIGB0ZXN0L21hcmt1cC9yL3JveHlnZW4udHh0YCBmb3IgYW4gZXhhbXBsZS5cbiAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnZG9jdGFnJyxcbiAgICAgICAgICAgICAgYmVnaW46ICdAZXhhbXBsZXMnLFxuICAgICAgICAgICAgICBzdGFydHM6IHtcbiAgICAgICAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgICAgICAgeyBiZWdpbjogL1xcbi8gfSxcbiAgICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgYmVnaW46IC8jJ1xccyooPz1AW2EtekEtWl0rKS8sXG4gICAgICAgICAgICAgICAgICAgIGVuZHNQYXJlbnQ6IHRydWUsXG4gICAgICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgICBiZWdpbjogLyMnLyxcbiAgICAgICAgICAgICAgICAgICAgZW5kOiAvJC8sXG4gICAgICAgICAgICAgICAgICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBdXG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICB7XG4gICAgICAgICAgICAgIC8vIEhhbmRsZSBgQHBhcmFtYCB0byBoaWdobGlnaHQgdGhlIHBhcmFtZXRlciBuYW1lIGZvbGxvd2luZ1xuICAgICAgICAgICAgICAvLyBhZnRlci5cbiAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnZG9jdGFnJyxcbiAgICAgICAgICAgICAgYmVnaW46ICdAcGFyYW0nLFxuICAgICAgICAgICAgICBlbmQ6IC8kLyxcbiAgICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgICBjbGFzc05hbWU6ICd2YXJpYWJsZScsXG4gICAgICAgICAgICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgICAgICAgICAgICB7IGJlZ2luOiBJREVOVF9SRSB9LFxuICAgICAgICAgICAgICAgICAgICB7IGJlZ2luOiAvYCg/OlxcXFwufFteYFxcXFxdKStgLyB9XG4gICAgICAgICAgICAgICAgICBdLFxuICAgICAgICAgICAgICAgICAgZW5kc1BhcmVudDogdHJ1ZVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgXVxuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnZG9jdGFnJyxcbiAgICAgICAgICAgICAgYmVnaW46IC9AW2EtekEtWl0rL1xuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnbWV0YS1rZXl3b3JkJyxcbiAgICAgICAgICAgICAgYmVnaW46IC9cXFxcW2EtekEtWl0rLyxcbiAgICAgICAgICAgIH1cbiAgICAgICAgICBdXG4gICAgICAgIH1cbiAgICAgICksXG5cbiAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG5cbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgY29udGFpbnM6IFtobGpzLkJBQ0tTTEFTSF9FU0NBUEVdLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIGhsanMuRU5EX1NBTUVfQVNfQkVHSU4oeyBiZWdpbjogL1tyUl1cIigtKilcXCgvLCBlbmQ6IC9cXCkoLSopXCIvIH0pLFxuICAgICAgICAgIGhsanMuRU5EX1NBTUVfQVNfQkVHSU4oeyBiZWdpbjogL1tyUl1cIigtKilcXHsvLCBlbmQ6IC9cXH0oLSopXCIvIH0pLFxuICAgICAgICAgIGhsanMuRU5EX1NBTUVfQVNfQkVHSU4oeyBiZWdpbjogL1tyUl1cIigtKilcXFsvLCBlbmQ6IC9cXF0oLSopXCIvIH0pLFxuICAgICAgICAgIGhsanMuRU5EX1NBTUVfQVNfQkVHSU4oeyBiZWdpbjogL1tyUl0nKC0qKVxcKC8sIGVuZDogL1xcKSgtKiknLyB9KSxcbiAgICAgICAgICBobGpzLkVORF9TQU1FX0FTX0JFR0lOKHsgYmVnaW46IC9bclJdJygtKilcXHsvLCBlbmQ6IC9cXH0oLSopJy8gfSksXG4gICAgICAgICAgaGxqcy5FTkRfU0FNRV9BU19CRUdJTih7IGJlZ2luOiAvW3JSXScoLSopXFxbLywgZW5kOiAvXFxdKC0qKScvIH0pLFxuICAgICAgICAgIHtiZWdpbjogJ1wiJywgZW5kOiAnXCInLCByZWxldmFuY2U6IDB9LFxuICAgICAgICAgIHtiZWdpbjogXCInXCIsIGVuZDogXCInXCIsIHJlbGV2YW5jZTogMH1cbiAgICAgICAgXSxcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgYmVmb3JlTWF0Y2g6IC8oW15hLXpBLVowLTkuX10pLywgLy8gbm90IHBhcnQgb2YgYW4gaWRlbnRpZmllclxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIC8vIFRPRE86IHJlcGxhY2Ugd2l0aCBuZWdhdGl2ZSBsb29rLWJlaGluZCB3aGVuIGF2YWlsYWJsZVxuICAgICAgICAgIC8vIHsgYmVnaW46IC8oPzwhW2EtekEtWjAtOS5fXSkwW3hYXVswLTlhLWZBLUZdK1xcLlswLTlhLWZBLUZdKltwUF1bKy1dP1xcZCtpPy8gfSxcbiAgICAgICAgICAvLyB7IGJlZ2luOiAvKD88IVthLXpBLVowLTkuX10pMFt4WF1bMC05YS1mQS1GXSsoW3BQXVsrLV0/XFxkKyk/W0xpXT8vIH0sXG4gICAgICAgICAgLy8geyBiZWdpbjogLyg/PCFbYS16QS1aMC05Ll9dKShcXGQrKFxcLlxcZCopP3xcXC5cXGQrKShbZUVdWystXT9cXGQrKT9bTGldPy8gfVxuICAgICAgICAgIHtcbiAgICAgICAgICAgIC8vIFNwZWNpYWwgY2FzZTogb25seSBoZXhhZGVjaW1hbCBiaW5hcnkgcG93ZXJzIGNhbiBjb250YWluIGZyYWN0aW9ucy5cbiAgICAgICAgICAgIG1hdGNoOiAvMFt4WF1bMC05YS1mQS1GXStcXC5bMC05YS1mQS1GXSpbcFBdWystXT9cXGQraT8vLFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgbWF0Y2g6IC8wW3hYXVswLTlhLWZBLUZdKyhbcFBdWystXT9cXGQrKT9bTGldPy9cbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIG1hdGNoOiAvKFxcZCsoXFwuXFxkKik/fFxcLlxcZCspKFtlRV1bKy1dP1xcZCspP1tMaV0/LyxcbiAgICAgICAgICB9XG4gICAgICAgIF0sXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyBpbmZpeCBvcGVyYXRvclxuICAgICAgICBiZWdpbjogJyUnLFxuICAgICAgICBlbmQ6ICclJ1xuICAgICAgfSxcbiAgICAgIC8vIHJlbGV2YW5jZSBib29zdCBmb3IgYXNzaWdubWVudFxuICAgICAge1xuICAgICAgICBiZWdpbjogY29uY2F0KFNJTVBMRV9JREVOVCwgXCJcXFxccys8LVxcXFxzK1wiKVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gZXNjYXBlZCBpZGVudGlmaWVyXG4gICAgICAgIGJlZ2luOiAnYCcsXG4gICAgICAgIGVuZDogJ2AnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHsgYmVnaW46IC9cXFxcLi8gfVxuICAgICAgICBdXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHI7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=