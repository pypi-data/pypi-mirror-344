(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_aspectj"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/aspectj.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/aspectj.js ***!
  \**************************************************************************************************/
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

/*
Language: AspectJ
Author: Hakan Ozler <ozler.hakan@gmail.com>
Website: https://www.eclipse.org/aspectj/
Description: Syntax Highlighting for the AspectJ Language which is a general-purpose aspect-oriented extension to the Java programming language.
Audit: 2020
*/

/** @type LanguageFn */
function aspectj(hljs) {
  const KEYWORDS =
    'false synchronized int abstract float private char boolean static null if const ' +
    'for true while long throw strictfp finally protected import native final return void ' +
    'enum else extends implements break transient new catch instanceof byte super volatile case ' +
    'assert short package default double public try this switch continue throws privileged ' +
    'aspectOf adviceexecution proceed cflowbelow cflow initialization preinitialization ' +
    'staticinitialization withincode target within execution getWithinTypeName handler ' +
    'thisJoinPoint thisJoinPointStaticPart thisEnclosingJoinPointStaticPart declare parents ' +
    'warning error soft precedence thisAspectInstance';
  const SHORTKEYS = 'get set args call';

  return {
    name: 'AspectJ',
    keywords: KEYWORDS,
    illegal: /<\/|#/,
    contains: [
      hljs.COMMENT(
        /\/\*\*/,
        /\*\//,
        {
          relevance: 0,
          contains: [
            {
              // eat up @'s in emails to prevent them to be recognized as doctags
              begin: /\w+@/,
              relevance: 0
            },
            {
              className: 'doctag',
              begin: /@[A-Za-z]+/
            }
          ]
        }
      ),
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      {
        className: 'class',
        beginKeywords: 'aspect',
        end: /[{;=]/,
        excludeEnd: true,
        illegal: /[:;"\[\]]/,
        contains: [
          {
            beginKeywords: 'extends implements pertypewithin perthis pertarget percflowbelow percflow issingleton'
          },
          hljs.UNDERSCORE_TITLE_MODE,
          {
            begin: /\([^\)]*/,
            end: /[)]+/,
            keywords: KEYWORDS + ' ' + SHORTKEYS,
            excludeEnd: false
          }
        ]
      },
      {
        className: 'class',
        beginKeywords: 'class interface',
        end: /[{;=]/,
        excludeEnd: true,
        relevance: 0,
        keywords: 'class interface',
        illegal: /[:"\[\]]/,
        contains: [
          {
            beginKeywords: 'extends implements'
          },
          hljs.UNDERSCORE_TITLE_MODE
        ]
      },
      {
        // AspectJ Constructs
        beginKeywords: 'pointcut after before around throwing returning',
        end: /[)]/,
        excludeEnd: false,
        illegal: /["\[\]]/,
        contains: [
          {
            begin: concat(hljs.UNDERSCORE_IDENT_RE, /\s*\(/),
            returnBegin: true,
            contains: [ hljs.UNDERSCORE_TITLE_MODE ]
          }
        ]
      },
      {
        begin: /[:]/,
        returnBegin: true,
        end: /[{;]/,
        relevance: 0,
        excludeEnd: false,
        keywords: KEYWORDS,
        illegal: /["\[\]]/,
        contains: [
          {
            begin: concat(hljs.UNDERSCORE_IDENT_RE, /\s*\(/),
            keywords: KEYWORDS + ' ' + SHORTKEYS,
            relevance: 0
          },
          hljs.QUOTE_STRING_MODE
        ]
      },
      {
        // this prevents 'new Name(...), or throw ...' from being recognized as a function definition
        beginKeywords: 'new throw',
        relevance: 0
      },
      {
        // the function class is a bit different for AspectJ compared to the Java language
        className: 'function',
        begin: /\w+ +\w+(\.\w+)?\s*\([^\)]*\)\s*((throws)[\w\s,]+)?[\{;]/,
        returnBegin: true,
        end: /[{;=]/,
        keywords: KEYWORDS,
        excludeEnd: true,
        contains: [
          {
            begin: concat(hljs.UNDERSCORE_IDENT_RE, /\s*\(/),
            returnBegin: true,
            relevance: 0,
            contains: [ hljs.UNDERSCORE_TITLE_MODE ]
          },
          {
            className: 'params',
            begin: /\(/,
            end: /\)/,
            relevance: 0,
            keywords: KEYWORDS,
            contains: [
              hljs.APOS_STRING_MODE,
              hljs.QUOTE_STRING_MODE,
              hljs.C_NUMBER_MODE,
              hljs.C_BLOCK_COMMENT_MODE
            ]
          },
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE
        ]
      },
      hljs.C_NUMBER_MODE,
      {
        // annotation is also used in this language
        className: 'meta',
        begin: /@[A-Za-z]+/
      }
    ]
  };
}

module.exports = aspectj;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYXNwZWN0ai5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBLFdBQVcsUUFBUTtBQUNuQixhQUFhO0FBQ2I7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBLFdBQVcsdUJBQXVCO0FBQ2xDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQjtBQUNqQjtBQUNBLHFCQUFxQjtBQUNyQjtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxpQkFBaUI7QUFDakI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxpQkFBaUI7QUFDakI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsdUVBQXVFO0FBQ3ZFO0FBQ0EsaUJBQWlCO0FBQ2pCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2FzcGVjdGouanMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHsuLi4oUmVnRXhwIHwgc3RyaW5nKSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGNvbmNhdCguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9IGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJcIik7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qXG5MYW5ndWFnZTogQXNwZWN0SlxuQXV0aG9yOiBIYWthbiBPemxlciA8b3psZXIuaGFrYW5AZ21haWwuY29tPlxuV2Vic2l0ZTogaHR0cHM6Ly93d3cuZWNsaXBzZS5vcmcvYXNwZWN0ai9cbkRlc2NyaXB0aW9uOiBTeW50YXggSGlnaGxpZ2h0aW5nIGZvciB0aGUgQXNwZWN0SiBMYW5ndWFnZSB3aGljaCBpcyBhIGdlbmVyYWwtcHVycG9zZSBhc3BlY3Qtb3JpZW50ZWQgZXh0ZW5zaW9uIHRvIHRoZSBKYXZhIHByb2dyYW1taW5nIGxhbmd1YWdlLlxuQXVkaXQ6IDIwMjBcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBhc3BlY3RqKGhsanMpIHtcbiAgY29uc3QgS0VZV09SRFMgPVxuICAgICdmYWxzZSBzeW5jaHJvbml6ZWQgaW50IGFic3RyYWN0IGZsb2F0IHByaXZhdGUgY2hhciBib29sZWFuIHN0YXRpYyBudWxsIGlmIGNvbnN0ICcgK1xuICAgICdmb3IgdHJ1ZSB3aGlsZSBsb25nIHRocm93IHN0cmljdGZwIGZpbmFsbHkgcHJvdGVjdGVkIGltcG9ydCBuYXRpdmUgZmluYWwgcmV0dXJuIHZvaWQgJyArXG4gICAgJ2VudW0gZWxzZSBleHRlbmRzIGltcGxlbWVudHMgYnJlYWsgdHJhbnNpZW50IG5ldyBjYXRjaCBpbnN0YW5jZW9mIGJ5dGUgc3VwZXIgdm9sYXRpbGUgY2FzZSAnICtcbiAgICAnYXNzZXJ0IHNob3J0IHBhY2thZ2UgZGVmYXVsdCBkb3VibGUgcHVibGljIHRyeSB0aGlzIHN3aXRjaCBjb250aW51ZSB0aHJvd3MgcHJpdmlsZWdlZCAnICtcbiAgICAnYXNwZWN0T2YgYWR2aWNlZXhlY3V0aW9uIHByb2NlZWQgY2Zsb3diZWxvdyBjZmxvdyBpbml0aWFsaXphdGlvbiBwcmVpbml0aWFsaXphdGlvbiAnICtcbiAgICAnc3RhdGljaW5pdGlhbGl6YXRpb24gd2l0aGluY29kZSB0YXJnZXQgd2l0aGluIGV4ZWN1dGlvbiBnZXRXaXRoaW5UeXBlTmFtZSBoYW5kbGVyICcgK1xuICAgICd0aGlzSm9pblBvaW50IHRoaXNKb2luUG9pbnRTdGF0aWNQYXJ0IHRoaXNFbmNsb3NpbmdKb2luUG9pbnRTdGF0aWNQYXJ0IGRlY2xhcmUgcGFyZW50cyAnICtcbiAgICAnd2FybmluZyBlcnJvciBzb2Z0IHByZWNlZGVuY2UgdGhpc0FzcGVjdEluc3RhbmNlJztcbiAgY29uc3QgU0hPUlRLRVlTID0gJ2dldCBzZXQgYXJncyBjYWxsJztcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdBc3BlY3RKJyxcbiAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgaWxsZWdhbDogLzxcXC98Iy8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ09NTUVOVChcbiAgICAgICAgL1xcL1xcKlxcKi8sXG4gICAgICAgIC9cXCpcXC8vLFxuICAgICAgICB7XG4gICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICB7XG4gICAgICAgICAgICAgIC8vIGVhdCB1cCBAJ3MgaW4gZW1haWxzIHRvIHByZXZlbnQgdGhlbSB0byBiZSByZWNvZ25pemVkIGFzIGRvY3RhZ3NcbiAgICAgICAgICAgICAgYmVnaW46IC9cXHcrQC8sXG4gICAgICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnZG9jdGFnJyxcbiAgICAgICAgICAgICAgYmVnaW46IC9AW0EtWmEtel0rL1xuICAgICAgICAgICAgfVxuICAgICAgICAgIF1cbiAgICAgICAgfVxuICAgICAgKSxcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdjbGFzcycsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdhc3BlY3QnLFxuICAgICAgICBlbmQ6IC9bezs9XS8sXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGlsbGVnYWw6IC9bOjtcIlxcW1xcXV0vLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luS2V5d29yZHM6ICdleHRlbmRzIGltcGxlbWVudHMgcGVydHlwZXdpdGhpbiBwZXJ0aGlzIHBlcnRhcmdldCBwZXJjZmxvd2JlbG93IHBlcmNmbG93IGlzc2luZ2xldG9uJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgaGxqcy5VTkRFUlNDT1JFX1RJVExFX01PREUsXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IC9cXChbXlxcKV0qLyxcbiAgICAgICAgICAgIGVuZDogL1spXSsvLFxuICAgICAgICAgICAga2V5d29yZHM6IEtFWVdPUkRTICsgJyAnICsgU0hPUlRLRVlTLFxuICAgICAgICAgICAgZXhjbHVkZUVuZDogZmFsc2VcbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2NsYXNzJyxcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ2NsYXNzIGludGVyZmFjZScsXG4gICAgICAgIGVuZDogL1t7Oz1dLyxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBrZXl3b3JkczogJ2NsYXNzIGludGVyZmFjZScsXG4gICAgICAgIGlsbGVnYWw6IC9bOlwiXFxbXFxdXS8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW5LZXl3b3JkczogJ2V4dGVuZHMgaW1wbGVtZW50cydcbiAgICAgICAgICB9LFxuICAgICAgICAgIGhsanMuVU5ERVJTQ09SRV9USVRMRV9NT0RFXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIEFzcGVjdEogQ29uc3RydWN0c1xuICAgICAgICBiZWdpbktleXdvcmRzOiAncG9pbnRjdXQgYWZ0ZXIgYmVmb3JlIGFyb3VuZCB0aHJvd2luZyByZXR1cm5pbmcnLFxuICAgICAgICBlbmQ6IC9bKV0vLFxuICAgICAgICBleGNsdWRlRW5kOiBmYWxzZSxcbiAgICAgICAgaWxsZWdhbDogL1tcIlxcW1xcXV0vLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiBjb25jYXQoaGxqcy5VTkRFUlNDT1JFX0lERU5UX1JFLCAvXFxzKlxcKC8pLFxuICAgICAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgICAgICBjb250YWluczogWyBobGpzLlVOREVSU0NPUkVfVElUTEVfTU9ERSBdXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1s6XS8sXG4gICAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICBlbmQ6IC9beztdLyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBleGNsdWRlRW5kOiBmYWxzZSxcbiAgICAgICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgICAgICBpbGxlZ2FsOiAvW1wiXFxbXFxdXS8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IGNvbmNhdChobGpzLlVOREVSU0NPUkVfSURFTlRfUkUsIC9cXHMqXFwoLyksXG4gICAgICAgICAgICBrZXl3b3JkczogS0VZV09SRFMgKyAnICcgKyBTSE9SVEtFWVMsXG4gICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICB9LFxuICAgICAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gdGhpcyBwcmV2ZW50cyAnbmV3IE5hbWUoLi4uKSwgb3IgdGhyb3cgLi4uJyBmcm9tIGJlaW5nIHJlY29nbml6ZWQgYXMgYSBmdW5jdGlvbiBkZWZpbml0aW9uXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICduZXcgdGhyb3cnLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIHRoZSBmdW5jdGlvbiBjbGFzcyBpcyBhIGJpdCBkaWZmZXJlbnQgZm9yIEFzcGVjdEogY29tcGFyZWQgdG8gdGhlIEphdmEgbGFuZ3VhZ2VcbiAgICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgICBiZWdpbjogL1xcdysgK1xcdysoXFwuXFx3Kyk/XFxzKlxcKFteXFwpXSpcXClcXHMqKCh0aHJvd3MpW1xcd1xccyxdKyk/W1xceztdLyxcbiAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgIGVuZDogL1t7Oz1dLyxcbiAgICAgICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiBjb25jYXQoaGxqcy5VTkRFUlNDT1JFX0lERU5UX1JFLCAvXFxzKlxcKC8pLFxuICAgICAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgICAgICBjb250YWluczogWyBobGpzLlVOREVSU0NPUkVfVElUTEVfTU9ERSBdXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgICAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICAgICAgZW5kOiAvXFwpLyxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICAgICAgICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgICAgICAgICAgaGxqcy5DX05VTUJFUl9NT0RFLFxuICAgICAgICAgICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFXG4gICAgICAgICAgICBdXG4gICAgICAgICAgfSxcbiAgICAgICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAgaGxqcy5DX05VTUJFUl9NT0RFLFxuICAgICAge1xuICAgICAgICAvLyBhbm5vdGF0aW9uIGlzIGFsc28gdXNlZCBpbiB0aGlzIGxhbmd1YWdlXG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogL0BbQS1aYS16XSsvXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGFzcGVjdGo7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=