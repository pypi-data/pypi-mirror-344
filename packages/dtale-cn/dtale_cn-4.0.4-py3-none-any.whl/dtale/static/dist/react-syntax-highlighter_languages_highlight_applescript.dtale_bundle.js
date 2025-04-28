(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_applescript"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/applescript.js":
/*!******************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/applescript.js ***!
  \******************************************************************************************************/
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
Language: AppleScript
Authors: Nathan Grigg <nathan@nathanamy.org>, Dr. Drang <drdrang@gmail.com>
Category: scripting
Website: https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/introduction/ASLR_intro.html
Audit: 2020
*/

/** @type LanguageFn */
function applescript(hljs) {
  const STRING = hljs.inherit(
    hljs.QUOTE_STRING_MODE, {
      illegal: null
    });
  const PARAMS = {
    className: 'params',
    begin: /\(/,
    end: /\)/,
    contains: [
      'self',
      hljs.C_NUMBER_MODE,
      STRING
    ]
  };
  const COMMENT_MODE_1 = hljs.COMMENT(/--/, /$/);
  const COMMENT_MODE_2 = hljs.COMMENT(
    /\(\*/,
    /\*\)/,
    {
      contains: [
        'self', // allow nesting
        COMMENT_MODE_1
      ]
    }
  );
  const COMMENTS = [
    COMMENT_MODE_1,
    COMMENT_MODE_2,
    hljs.HASH_COMMENT_MODE
  ];

  const KEYWORD_PATTERNS = [
    /apart from/,
    /aside from/,
    /instead of/,
    /out of/,
    /greater than/,
    /isn't|(doesn't|does not) (equal|come before|come after|contain)/,
    /(greater|less) than( or equal)?/,
    /(starts?|ends|begins?) with/,
    /contained by/,
    /comes (before|after)/,
    /a (ref|reference)/,
    /POSIX (file|path)/,
    /(date|time) string/,
    /quoted form/
  ];

  const BUILT_IN_PATTERNS = [
    /clipboard info/,
    /the clipboard/,
    /info for/,
    /list (disks|folder)/,
    /mount volume/,
    /path to/,
    /(close|open for) access/,
    /(get|set) eof/,
    /current date/,
    /do shell script/,
    /get volume settings/,
    /random number/,
    /set volume/,
    /system attribute/,
    /system info/,
    /time to GMT/,
    /(load|run|store) script/,
    /scripting components/,
    /ASCII (character|number)/,
    /localized string/,
    /choose (application|color|file|file name|folder|from list|remote application|URL)/,
    /display (alert|dialog)/
  ];

  return {
    name: 'AppleScript',
    aliases: [ 'osascript' ],
    keywords: {
      keyword:
        'about above after against and around as at back before beginning ' +
        'behind below beneath beside between but by considering ' +
        'contain contains continue copy div does eighth else end equal ' +
        'equals error every exit fifth first for fourth from front ' +
        'get given global if ignoring in into is it its last local me ' +
        'middle mod my ninth not of on onto or over prop property put ref ' +
        'reference repeat returning script second set seventh since ' +
        'sixth some tell tenth that the|0 then third through thru ' +
        'timeout times to transaction try until where while whose with ' +
        'without',
      literal:
        'AppleScript false linefeed return pi quote result space tab true',
      built_in:
        'alias application boolean class constant date file integer list ' +
        'number real record string text ' +
        'activate beep count delay launch log offset read round ' +
        'run say summarize write ' +
        'character characters contents day frontmost id item length ' +
        'month name paragraph paragraphs rest reverse running time version ' +
        'weekday word words year'
    },
    contains: [
      STRING,
      hljs.C_NUMBER_MODE,
      {
        className: 'built_in',
        begin: concat(
          /\b/,
          either(...BUILT_IN_PATTERNS),
          /\b/
        )
      },
      {
        className: 'built_in',
        begin: /^\s*return\b/
      },
      {
        className: 'literal',
        begin:
          /\b(text item delimiters|current application|missing value)\b/
      },
      {
        className: 'keyword',
        begin: concat(
          /\b/,
          either(...KEYWORD_PATTERNS),
          /\b/
        )
      },
      {
        beginKeywords: 'on',
        illegal: /[${=;\n]/,
        contains: [
          hljs.UNDERSCORE_TITLE_MODE,
          PARAMS
        ]
      },
      ...COMMENTS
    ],
    illegal: /\/\/|->|=>|\[\[/
  };
}

module.exports = applescript;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYXBwbGVzY3JpcHQuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQSxXQUFXLFFBQVE7QUFDbkIsYUFBYTtBQUNiOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQSxXQUFXLHVCQUF1QjtBQUNsQyxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVcsc0JBQXNCO0FBQ2pDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxxQkFBcUIsRUFBRTtBQUN2QjtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9hcHBsZXNjcmlwdC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKipcbiAqIEBwYXJhbSB7c3RyaW5nfSB2YWx1ZVxuICogQHJldHVybnMge1JlZ0V4cH1cbiAqICovXG5cbi8qKlxuICogQHBhcmFtIHtSZWdFeHAgfCBzdHJpbmcgfSByZVxuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gc291cmNlKHJlKSB7XG4gIGlmICghcmUpIHJldHVybiBudWxsO1xuICBpZiAodHlwZW9mIHJlID09PSBcInN0cmluZ1wiKSByZXR1cm4gcmU7XG5cbiAgcmV0dXJuIHJlLnNvdXJjZTtcbn1cblxuLyoqXG4gKiBAcGFyYW0gey4uLihSZWdFeHAgfCBzdHJpbmcpIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gY29uY2F0KC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcIlwiKTtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuLyoqXG4gKiBBbnkgb2YgdGhlIHBhc3NlZCBleHByZXNzc2lvbnMgbWF5IG1hdGNoXG4gKlxuICogQ3JlYXRlcyBhIGh1Z2UgdGhpcyB8IHRoaXMgfCB0aGF0IHwgdGhhdCBtYXRjaFxuICogQHBhcmFtIHsoUmVnRXhwIHwgc3RyaW5nKVtdIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gZWl0aGVyKC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gJygnICsgYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcInxcIikgKyBcIilcIjtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuLypcbkxhbmd1YWdlOiBBcHBsZVNjcmlwdFxuQXV0aG9yczogTmF0aGFuIEdyaWdnIDxuYXRoYW5AbmF0aGFuYW15Lm9yZz4sIERyLiBEcmFuZyA8ZHJkcmFuZ0BnbWFpbC5jb20+XG5DYXRlZ29yeTogc2NyaXB0aW5nXG5XZWJzaXRlOiBodHRwczovL2RldmVsb3Blci5hcHBsZS5jb20vbGlicmFyeS9hcmNoaXZlL2RvY3VtZW50YXRpb24vQXBwbGVTY3JpcHQvQ29uY2VwdHVhbC9BcHBsZVNjcmlwdExhbmdHdWlkZS9pbnRyb2R1Y3Rpb24vQVNMUl9pbnRyby5odG1sXG5BdWRpdDogMjAyMFxuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGFwcGxlc2NyaXB0KGhsanMpIHtcbiAgY29uc3QgU1RSSU5HID0gaGxqcy5pbmhlcml0KFxuICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsIHtcbiAgICAgIGlsbGVnYWw6IG51bGxcbiAgICB9KTtcbiAgY29uc3QgUEFSQU1TID0ge1xuICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgYmVnaW46IC9cXCgvLFxuICAgIGVuZDogL1xcKS8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgICdzZWxmJyxcbiAgICAgIGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgIFNUUklOR1xuICAgIF1cbiAgfTtcbiAgY29uc3QgQ09NTUVOVF9NT0RFXzEgPSBobGpzLkNPTU1FTlQoLy0tLywgLyQvKTtcbiAgY29uc3QgQ09NTUVOVF9NT0RFXzIgPSBobGpzLkNPTU1FTlQoXG4gICAgL1xcKFxcKi8sXG4gICAgL1xcKlxcKS8sXG4gICAge1xuICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgJ3NlbGYnLCAvLyBhbGxvdyBuZXN0aW5nXG4gICAgICAgIENPTU1FTlRfTU9ERV8xXG4gICAgICBdXG4gICAgfVxuICApO1xuICBjb25zdCBDT01NRU5UUyA9IFtcbiAgICBDT01NRU5UX01PREVfMSxcbiAgICBDT01NRU5UX01PREVfMixcbiAgICBobGpzLkhBU0hfQ09NTUVOVF9NT0RFXG4gIF07XG5cbiAgY29uc3QgS0VZV09SRF9QQVRURVJOUyA9IFtcbiAgICAvYXBhcnQgZnJvbS8sXG4gICAgL2FzaWRlIGZyb20vLFxuICAgIC9pbnN0ZWFkIG9mLyxcbiAgICAvb3V0IG9mLyxcbiAgICAvZ3JlYXRlciB0aGFuLyxcbiAgICAvaXNuJ3R8KGRvZXNuJ3R8ZG9lcyBub3QpIChlcXVhbHxjb21lIGJlZm9yZXxjb21lIGFmdGVyfGNvbnRhaW4pLyxcbiAgICAvKGdyZWF0ZXJ8bGVzcykgdGhhbiggb3IgZXF1YWwpPy8sXG4gICAgLyhzdGFydHM/fGVuZHN8YmVnaW5zPykgd2l0aC8sXG4gICAgL2NvbnRhaW5lZCBieS8sXG4gICAgL2NvbWVzIChiZWZvcmV8YWZ0ZXIpLyxcbiAgICAvYSAocmVmfHJlZmVyZW5jZSkvLFxuICAgIC9QT1NJWCAoZmlsZXxwYXRoKS8sXG4gICAgLyhkYXRlfHRpbWUpIHN0cmluZy8sXG4gICAgL3F1b3RlZCBmb3JtL1xuICBdO1xuXG4gIGNvbnN0IEJVSUxUX0lOX1BBVFRFUk5TID0gW1xuICAgIC9jbGlwYm9hcmQgaW5mby8sXG4gICAgL3RoZSBjbGlwYm9hcmQvLFxuICAgIC9pbmZvIGZvci8sXG4gICAgL2xpc3QgKGRpc2tzfGZvbGRlcikvLFxuICAgIC9tb3VudCB2b2x1bWUvLFxuICAgIC9wYXRoIHRvLyxcbiAgICAvKGNsb3NlfG9wZW4gZm9yKSBhY2Nlc3MvLFxuICAgIC8oZ2V0fHNldCkgZW9mLyxcbiAgICAvY3VycmVudCBkYXRlLyxcbiAgICAvZG8gc2hlbGwgc2NyaXB0LyxcbiAgICAvZ2V0IHZvbHVtZSBzZXR0aW5ncy8sXG4gICAgL3JhbmRvbSBudW1iZXIvLFxuICAgIC9zZXQgdm9sdW1lLyxcbiAgICAvc3lzdGVtIGF0dHJpYnV0ZS8sXG4gICAgL3N5c3RlbSBpbmZvLyxcbiAgICAvdGltZSB0byBHTVQvLFxuICAgIC8obG9hZHxydW58c3RvcmUpIHNjcmlwdC8sXG4gICAgL3NjcmlwdGluZyBjb21wb25lbnRzLyxcbiAgICAvQVNDSUkgKGNoYXJhY3RlcnxudW1iZXIpLyxcbiAgICAvbG9jYWxpemVkIHN0cmluZy8sXG4gICAgL2Nob29zZSAoYXBwbGljYXRpb258Y29sb3J8ZmlsZXxmaWxlIG5hbWV8Zm9sZGVyfGZyb20gbGlzdHxyZW1vdGUgYXBwbGljYXRpb258VVJMKS8sXG4gICAgL2Rpc3BsYXkgKGFsZXJ0fGRpYWxvZykvXG4gIF07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnQXBwbGVTY3JpcHQnLFxuICAgIGFsaWFzZXM6IFsgJ29zYXNjcmlwdCcgXSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAga2V5d29yZDpcbiAgICAgICAgJ2Fib3V0IGFib3ZlIGFmdGVyIGFnYWluc3QgYW5kIGFyb3VuZCBhcyBhdCBiYWNrIGJlZm9yZSBiZWdpbm5pbmcgJyArXG4gICAgICAgICdiZWhpbmQgYmVsb3cgYmVuZWF0aCBiZXNpZGUgYmV0d2VlbiBidXQgYnkgY29uc2lkZXJpbmcgJyArXG4gICAgICAgICdjb250YWluIGNvbnRhaW5zIGNvbnRpbnVlIGNvcHkgZGl2IGRvZXMgZWlnaHRoIGVsc2UgZW5kIGVxdWFsICcgK1xuICAgICAgICAnZXF1YWxzIGVycm9yIGV2ZXJ5IGV4aXQgZmlmdGggZmlyc3QgZm9yIGZvdXJ0aCBmcm9tIGZyb250ICcgK1xuICAgICAgICAnZ2V0IGdpdmVuIGdsb2JhbCBpZiBpZ25vcmluZyBpbiBpbnRvIGlzIGl0IGl0cyBsYXN0IGxvY2FsIG1lICcgK1xuICAgICAgICAnbWlkZGxlIG1vZCBteSBuaW50aCBub3Qgb2Ygb24gb250byBvciBvdmVyIHByb3AgcHJvcGVydHkgcHV0IHJlZiAnICtcbiAgICAgICAgJ3JlZmVyZW5jZSByZXBlYXQgcmV0dXJuaW5nIHNjcmlwdCBzZWNvbmQgc2V0IHNldmVudGggc2luY2UgJyArXG4gICAgICAgICdzaXh0aCBzb21lIHRlbGwgdGVudGggdGhhdCB0aGV8MCB0aGVuIHRoaXJkIHRocm91Z2ggdGhydSAnICtcbiAgICAgICAgJ3RpbWVvdXQgdGltZXMgdG8gdHJhbnNhY3Rpb24gdHJ5IHVudGlsIHdoZXJlIHdoaWxlIHdob3NlIHdpdGggJyArXG4gICAgICAgICd3aXRob3V0JyxcbiAgICAgIGxpdGVyYWw6XG4gICAgICAgICdBcHBsZVNjcmlwdCBmYWxzZSBsaW5lZmVlZCByZXR1cm4gcGkgcXVvdGUgcmVzdWx0IHNwYWNlIHRhYiB0cnVlJyxcbiAgICAgIGJ1aWx0X2luOlxuICAgICAgICAnYWxpYXMgYXBwbGljYXRpb24gYm9vbGVhbiBjbGFzcyBjb25zdGFudCBkYXRlIGZpbGUgaW50ZWdlciBsaXN0ICcgK1xuICAgICAgICAnbnVtYmVyIHJlYWwgcmVjb3JkIHN0cmluZyB0ZXh0ICcgK1xuICAgICAgICAnYWN0aXZhdGUgYmVlcCBjb3VudCBkZWxheSBsYXVuY2ggbG9nIG9mZnNldCByZWFkIHJvdW5kICcgK1xuICAgICAgICAncnVuIHNheSBzdW1tYXJpemUgd3JpdGUgJyArXG4gICAgICAgICdjaGFyYWN0ZXIgY2hhcmFjdGVycyBjb250ZW50cyBkYXkgZnJvbnRtb3N0IGlkIGl0ZW0gbGVuZ3RoICcgK1xuICAgICAgICAnbW9udGggbmFtZSBwYXJhZ3JhcGggcGFyYWdyYXBocyByZXN0IHJldmVyc2UgcnVubmluZyB0aW1lIHZlcnNpb24gJyArXG4gICAgICAgICd3ZWVrZGF5IHdvcmQgd29yZHMgeWVhcidcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBTVFJJTkcsXG4gICAgICBobGpzLkNfTlVNQkVSX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2J1aWx0X2luJyxcbiAgICAgICAgYmVnaW46IGNvbmNhdChcbiAgICAgICAgICAvXFxiLyxcbiAgICAgICAgICBlaXRoZXIoLi4uQlVJTFRfSU5fUEFUVEVSTlMpLFxuICAgICAgICAgIC9cXGIvXG4gICAgICAgIClcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2J1aWx0X2luJyxcbiAgICAgICAgYmVnaW46IC9eXFxzKnJldHVyblxcYi9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2xpdGVyYWwnLFxuICAgICAgICBiZWdpbjpcbiAgICAgICAgICAvXFxiKHRleHQgaXRlbSBkZWxpbWl0ZXJzfGN1cnJlbnQgYXBwbGljYXRpb258bWlzc2luZyB2YWx1ZSlcXGIvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdrZXl3b3JkJyxcbiAgICAgICAgYmVnaW46IGNvbmNhdChcbiAgICAgICAgICAvXFxiLyxcbiAgICAgICAgICBlaXRoZXIoLi4uS0VZV09SRF9QQVRURVJOUyksXG4gICAgICAgICAgL1xcYi9cbiAgICAgICAgKVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ29uJyxcbiAgICAgICAgaWxsZWdhbDogL1skez07XFxuXS8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgaGxqcy5VTkRFUlNDT1JFX1RJVExFX01PREUsXG4gICAgICAgICAgUEFSQU1TXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICAuLi5DT01NRU5UU1xuICAgIF0sXG4gICAgaWxsZWdhbDogL1xcL1xcL3wtPnw9PnxcXFtcXFsvXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gYXBwbGVzY3JpcHQ7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=