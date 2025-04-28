(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_d"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/d.js":
/*!********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/d.js ***!
  \********************************************************************************************/
/***/ ((module) => {

/*
Language: D
Author: Aleksandar Ruzicic <aleksandar@ruzicic.info>
Description: D is a language with C-like syntax and static typing. It pragmatically combines efficiency, control, and modeling power, with safety and programmer productivity.
Version: 1.0a
Website: https://dlang.org
Date: 2012-04-08
*/

/**
 * Known issues:
 *
 * - invalid hex string literals will be recognized as a double quoted strings
 *   but 'x' at the beginning of string will not be matched
 *
 * - delimited string literals are not checked for matching end delimiter
 *   (not possible to do with js regexp)
 *
 * - content of token string is colored as a string (i.e. no keyword coloring inside a token string)
 *   also, content of token string is not validated to contain only valid D tokens
 *
 * - special token sequence rule is not strictly following D grammar (anything following #line
 *   up to the end of line is matched as special token sequence)
 */

/** @type LanguageFn */
function d(hljs) {
  /**
   * Language keywords
   *
   * @type {Object}
   */
  const D_KEYWORDS = {
    $pattern: hljs.UNDERSCORE_IDENT_RE,
    keyword:
      'abstract alias align asm assert auto body break byte case cast catch class ' +
      'const continue debug default delete deprecated do else enum export extern final ' +
      'finally for foreach foreach_reverse|10 goto if immutable import in inout int ' +
      'interface invariant is lazy macro mixin module new nothrow out override package ' +
      'pragma private protected public pure ref return scope shared static struct ' +
      'super switch synchronized template this throw try typedef typeid typeof union ' +
      'unittest version void volatile while with __FILE__ __LINE__ __gshared|10 ' +
      '__thread __traits __DATE__ __EOF__ __TIME__ __TIMESTAMP__ __VENDOR__ __VERSION__',
    built_in:
      'bool cdouble cent cfloat char creal dchar delegate double dstring float function ' +
      'idouble ifloat ireal long real short string ubyte ucent uint ulong ushort wchar ' +
      'wstring',
    literal:
      'false null true'
  };

  /**
   * Number literal regexps
   *
   * @type {String}
   */
  const decimal_integer_re = '(0|[1-9][\\d_]*)';
  const decimal_integer_nosus_re = '(0|[1-9][\\d_]*|\\d[\\d_]*|[\\d_]+?\\d)';
  const binary_integer_re = '0[bB][01_]+';
  const hexadecimal_digits_re = '([\\da-fA-F][\\da-fA-F_]*|_[\\da-fA-F][\\da-fA-F_]*)';
  const hexadecimal_integer_re = '0[xX]' + hexadecimal_digits_re;

  const decimal_exponent_re = '([eE][+-]?' + decimal_integer_nosus_re + ')';
  const decimal_float_re = '(' + decimal_integer_nosus_re + '(\\.\\d*|' + decimal_exponent_re + ')|' +
                '\\d+\\.' + decimal_integer_nosus_re + '|' +
                '\\.' + decimal_integer_re + decimal_exponent_re + '?' +
              ')';
  const hexadecimal_float_re = '(0[xX](' +
                  hexadecimal_digits_re + '\\.' + hexadecimal_digits_re + '|' +
                  '\\.?' + hexadecimal_digits_re +
                 ')[pP][+-]?' + decimal_integer_nosus_re + ')';

  const integer_re = '(' +
      decimal_integer_re + '|' +
      binary_integer_re + '|' +
       hexadecimal_integer_re +
    ')';

  const float_re = '(' +
      hexadecimal_float_re + '|' +
      decimal_float_re +
    ')';

  /**
   * Escape sequence supported in D string and character literals
   *
   * @type {String}
   */
  const escape_sequence_re = '\\\\(' +
              '[\'"\\?\\\\abfnrtv]|' + // common escapes
              'u[\\dA-Fa-f]{4}|' + // four hex digit unicode codepoint
              '[0-7]{1,3}|' + // one to three octal digit ascii char code
              'x[\\dA-Fa-f]{2}|' + // two hex digit ascii char code
              'U[\\dA-Fa-f]{8}' + // eight hex digit unicode codepoint
              ')|' +
              '&[a-zA-Z\\d]{2,};'; // named character entity

  /**
   * D integer number literals
   *
   * @type {Object}
   */
  const D_INTEGER_MODE = {
    className: 'number',
    begin: '\\b' + integer_re + '(L|u|U|Lu|LU|uL|UL)?',
    relevance: 0
  };

  /**
   * [D_FLOAT_MODE description]
   * @type {Object}
   */
  const D_FLOAT_MODE = {
    className: 'number',
    begin: '\\b(' +
        float_re + '([fF]|L|i|[fF]i|Li)?|' +
        integer_re + '(i|[fF]i|Li)' +
      ')',
    relevance: 0
  };

  /**
   * D character literal
   *
   * @type {Object}
   */
  const D_CHARACTER_MODE = {
    className: 'string',
    begin: '\'(' + escape_sequence_re + '|.)',
    end: '\'',
    illegal: '.'
  };

  /**
   * D string escape sequence
   *
   * @type {Object}
   */
  const D_ESCAPE_SEQUENCE = {
    begin: escape_sequence_re,
    relevance: 0
  };

  /**
   * D double quoted string literal
   *
   * @type {Object}
   */
  const D_STRING_MODE = {
    className: 'string',
    begin: '"',
    contains: [D_ESCAPE_SEQUENCE],
    end: '"[cwd]?'
  };

  /**
   * D wysiwyg and delimited string literals
   *
   * @type {Object}
   */
  const D_WYSIWYG_DELIMITED_STRING_MODE = {
    className: 'string',
    begin: '[rq]"',
    end: '"[cwd]?',
    relevance: 5
  };

  /**
   * D alternate wysiwyg string literal
   *
   * @type {Object}
   */
  const D_ALTERNATE_WYSIWYG_STRING_MODE = {
    className: 'string',
    begin: '`',
    end: '`[cwd]?'
  };

  /**
   * D hexadecimal string literal
   *
   * @type {Object}
   */
  const D_HEX_STRING_MODE = {
    className: 'string',
    begin: 'x"[\\da-fA-F\\s\\n\\r]*"[cwd]?',
    relevance: 10
  };

  /**
   * D delimited string literal
   *
   * @type {Object}
   */
  const D_TOKEN_STRING_MODE = {
    className: 'string',
    begin: 'q"\\{',
    end: '\\}"'
  };

  /**
   * Hashbang support
   *
   * @type {Object}
   */
  const D_HASHBANG_MODE = {
    className: 'meta',
    begin: '^#!',
    end: '$',
    relevance: 5
  };

  /**
   * D special token sequence
   *
   * @type {Object}
   */
  const D_SPECIAL_TOKEN_SEQUENCE_MODE = {
    className: 'meta',
    begin: '#(line)',
    end: '$',
    relevance: 5
  };

  /**
   * D attributes
   *
   * @type {Object}
   */
  const D_ATTRIBUTE_MODE = {
    className: 'keyword',
    begin: '@[a-zA-Z_][a-zA-Z_\\d]*'
  };

  /**
   * D nesting comment
   *
   * @type {Object}
   */
  const D_NESTING_COMMENT_MODE = hljs.COMMENT(
    '\\/\\+',
    '\\+\\/',
    {
      contains: ['self'],
      relevance: 10
    }
  );

  return {
    name: 'D',
    keywords: D_KEYWORDS,
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      D_NESTING_COMMENT_MODE,
      D_HEX_STRING_MODE,
      D_STRING_MODE,
      D_WYSIWYG_DELIMITED_STRING_MODE,
      D_ALTERNATE_WYSIWYG_STRING_MODE,
      D_TOKEN_STRING_MODE,
      D_FLOAT_MODE,
      D_INTEGER_MODE,
      D_CHARACTER_MODE,
      D_HASHBANG_MODE,
      D_SPECIAL_TOKEN_SEQUENCE_MODE,
      D_ATTRIBUTE_MODE
    ]
  };
}

module.exports = d;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBLDRCQUE0QixFQUFFO0FBQzlCLHFCQUFxQixJQUFJO0FBQ3pCLDRCQUE0QixFQUFFO0FBQzlCLDRCQUE0QixFQUFFO0FBQzlCO0FBQ0EsNEJBQTRCLElBQUksR0FBRzs7QUFFbkM7QUFDQTtBQUNBO0FBQ0EsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0EsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxZQUFZO0FBQ1o7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxZQUFZO0FBQ1o7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQjtBQUNqQixhQUFhO0FBQ2I7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxZQUFZO0FBQ1o7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxZQUFZO0FBQ1o7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvZC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IERcbkF1dGhvcjogQWxla3NhbmRhciBSdXppY2ljIDxhbGVrc2FuZGFyQHJ1emljaWMuaW5mbz5cbkRlc2NyaXB0aW9uOiBEIGlzIGEgbGFuZ3VhZ2Ugd2l0aCBDLWxpa2Ugc3ludGF4IGFuZCBzdGF0aWMgdHlwaW5nLiBJdCBwcmFnbWF0aWNhbGx5IGNvbWJpbmVzIGVmZmljaWVuY3ksIGNvbnRyb2wsIGFuZCBtb2RlbGluZyBwb3dlciwgd2l0aCBzYWZldHkgYW5kIHByb2dyYW1tZXIgcHJvZHVjdGl2aXR5LlxuVmVyc2lvbjogMS4wYVxuV2Vic2l0ZTogaHR0cHM6Ly9kbGFuZy5vcmdcbkRhdGU6IDIwMTItMDQtMDhcbiovXG5cbi8qKlxuICogS25vd24gaXNzdWVzOlxuICpcbiAqIC0gaW52YWxpZCBoZXggc3RyaW5nIGxpdGVyYWxzIHdpbGwgYmUgcmVjb2duaXplZCBhcyBhIGRvdWJsZSBxdW90ZWQgc3RyaW5nc1xuICogICBidXQgJ3gnIGF0IHRoZSBiZWdpbm5pbmcgb2Ygc3RyaW5nIHdpbGwgbm90IGJlIG1hdGNoZWRcbiAqXG4gKiAtIGRlbGltaXRlZCBzdHJpbmcgbGl0ZXJhbHMgYXJlIG5vdCBjaGVja2VkIGZvciBtYXRjaGluZyBlbmQgZGVsaW1pdGVyXG4gKiAgIChub3QgcG9zc2libGUgdG8gZG8gd2l0aCBqcyByZWdleHApXG4gKlxuICogLSBjb250ZW50IG9mIHRva2VuIHN0cmluZyBpcyBjb2xvcmVkIGFzIGEgc3RyaW5nIChpLmUuIG5vIGtleXdvcmQgY29sb3JpbmcgaW5zaWRlIGEgdG9rZW4gc3RyaW5nKVxuICogICBhbHNvLCBjb250ZW50IG9mIHRva2VuIHN0cmluZyBpcyBub3QgdmFsaWRhdGVkIHRvIGNvbnRhaW4gb25seSB2YWxpZCBEIHRva2Vuc1xuICpcbiAqIC0gc3BlY2lhbCB0b2tlbiBzZXF1ZW5jZSBydWxlIGlzIG5vdCBzdHJpY3RseSBmb2xsb3dpbmcgRCBncmFtbWFyIChhbnl0aGluZyBmb2xsb3dpbmcgI2xpbmVcbiAqICAgdXAgdG8gdGhlIGVuZCBvZiBsaW5lIGlzIG1hdGNoZWQgYXMgc3BlY2lhbCB0b2tlbiBzZXF1ZW5jZSlcbiAqL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gZChobGpzKSB7XG4gIC8qKlxuICAgKiBMYW5ndWFnZSBrZXl3b3Jkc1xuICAgKlxuICAgKiBAdHlwZSB7T2JqZWN0fVxuICAgKi9cbiAgY29uc3QgRF9LRVlXT1JEUyA9IHtcbiAgICAkcGF0dGVybjogaGxqcy5VTkRFUlNDT1JFX0lERU5UX1JFLFxuICAgIGtleXdvcmQ6XG4gICAgICAnYWJzdHJhY3QgYWxpYXMgYWxpZ24gYXNtIGFzc2VydCBhdXRvIGJvZHkgYnJlYWsgYnl0ZSBjYXNlIGNhc3QgY2F0Y2ggY2xhc3MgJyArXG4gICAgICAnY29uc3QgY29udGludWUgZGVidWcgZGVmYXVsdCBkZWxldGUgZGVwcmVjYXRlZCBkbyBlbHNlIGVudW0gZXhwb3J0IGV4dGVybiBmaW5hbCAnICtcbiAgICAgICdmaW5hbGx5IGZvciBmb3JlYWNoIGZvcmVhY2hfcmV2ZXJzZXwxMCBnb3RvIGlmIGltbXV0YWJsZSBpbXBvcnQgaW4gaW5vdXQgaW50ICcgK1xuICAgICAgJ2ludGVyZmFjZSBpbnZhcmlhbnQgaXMgbGF6eSBtYWNybyBtaXhpbiBtb2R1bGUgbmV3IG5vdGhyb3cgb3V0IG92ZXJyaWRlIHBhY2thZ2UgJyArXG4gICAgICAncHJhZ21hIHByaXZhdGUgcHJvdGVjdGVkIHB1YmxpYyBwdXJlIHJlZiByZXR1cm4gc2NvcGUgc2hhcmVkIHN0YXRpYyBzdHJ1Y3QgJyArXG4gICAgICAnc3VwZXIgc3dpdGNoIHN5bmNocm9uaXplZCB0ZW1wbGF0ZSB0aGlzIHRocm93IHRyeSB0eXBlZGVmIHR5cGVpZCB0eXBlb2YgdW5pb24gJyArXG4gICAgICAndW5pdHRlc3QgdmVyc2lvbiB2b2lkIHZvbGF0aWxlIHdoaWxlIHdpdGggX19GSUxFX18gX19MSU5FX18gX19nc2hhcmVkfDEwICcgK1xuICAgICAgJ19fdGhyZWFkIF9fdHJhaXRzIF9fREFURV9fIF9fRU9GX18gX19USU1FX18gX19USU1FU1RBTVBfXyBfX1ZFTkRPUl9fIF9fVkVSU0lPTl9fJyxcbiAgICBidWlsdF9pbjpcbiAgICAgICdib29sIGNkb3VibGUgY2VudCBjZmxvYXQgY2hhciBjcmVhbCBkY2hhciBkZWxlZ2F0ZSBkb3VibGUgZHN0cmluZyBmbG9hdCBmdW5jdGlvbiAnICtcbiAgICAgICdpZG91YmxlIGlmbG9hdCBpcmVhbCBsb25nIHJlYWwgc2hvcnQgc3RyaW5nIHVieXRlIHVjZW50IHVpbnQgdWxvbmcgdXNob3J0IHdjaGFyICcgK1xuICAgICAgJ3dzdHJpbmcnLFxuICAgIGxpdGVyYWw6XG4gICAgICAnZmFsc2UgbnVsbCB0cnVlJ1xuICB9O1xuXG4gIC8qKlxuICAgKiBOdW1iZXIgbGl0ZXJhbCByZWdleHBzXG4gICAqXG4gICAqIEB0eXBlIHtTdHJpbmd9XG4gICAqL1xuICBjb25zdCBkZWNpbWFsX2ludGVnZXJfcmUgPSAnKDB8WzEtOV1bXFxcXGRfXSopJztcbiAgY29uc3QgZGVjaW1hbF9pbnRlZ2VyX25vc3VzX3JlID0gJygwfFsxLTldW1xcXFxkX10qfFxcXFxkW1xcXFxkX10qfFtcXFxcZF9dKz9cXFxcZCknO1xuICBjb25zdCBiaW5hcnlfaW50ZWdlcl9yZSA9ICcwW2JCXVswMV9dKyc7XG4gIGNvbnN0IGhleGFkZWNpbWFsX2RpZ2l0c19yZSA9ICcoW1xcXFxkYS1mQS1GXVtcXFxcZGEtZkEtRl9dKnxfW1xcXFxkYS1mQS1GXVtcXFxcZGEtZkEtRl9dKiknO1xuICBjb25zdCBoZXhhZGVjaW1hbF9pbnRlZ2VyX3JlID0gJzBbeFhdJyArIGhleGFkZWNpbWFsX2RpZ2l0c19yZTtcblxuICBjb25zdCBkZWNpbWFsX2V4cG9uZW50X3JlID0gJyhbZUVdWystXT8nICsgZGVjaW1hbF9pbnRlZ2VyX25vc3VzX3JlICsgJyknO1xuICBjb25zdCBkZWNpbWFsX2Zsb2F0X3JlID0gJygnICsgZGVjaW1hbF9pbnRlZ2VyX25vc3VzX3JlICsgJyhcXFxcLlxcXFxkKnwnICsgZGVjaW1hbF9leHBvbmVudF9yZSArICcpfCcgK1xuICAgICAgICAgICAgICAgICdcXFxcZCtcXFxcLicgKyBkZWNpbWFsX2ludGVnZXJfbm9zdXNfcmUgKyAnfCcgK1xuICAgICAgICAgICAgICAgICdcXFxcLicgKyBkZWNpbWFsX2ludGVnZXJfcmUgKyBkZWNpbWFsX2V4cG9uZW50X3JlICsgJz8nICtcbiAgICAgICAgICAgICAgJyknO1xuICBjb25zdCBoZXhhZGVjaW1hbF9mbG9hdF9yZSA9ICcoMFt4WF0oJyArXG4gICAgICAgICAgICAgICAgICBoZXhhZGVjaW1hbF9kaWdpdHNfcmUgKyAnXFxcXC4nICsgaGV4YWRlY2ltYWxfZGlnaXRzX3JlICsgJ3wnICtcbiAgICAgICAgICAgICAgICAgICdcXFxcLj8nICsgaGV4YWRlY2ltYWxfZGlnaXRzX3JlICtcbiAgICAgICAgICAgICAgICAgJylbcFBdWystXT8nICsgZGVjaW1hbF9pbnRlZ2VyX25vc3VzX3JlICsgJyknO1xuXG4gIGNvbnN0IGludGVnZXJfcmUgPSAnKCcgK1xuICAgICAgZGVjaW1hbF9pbnRlZ2VyX3JlICsgJ3wnICtcbiAgICAgIGJpbmFyeV9pbnRlZ2VyX3JlICsgJ3wnICtcbiAgICAgICBoZXhhZGVjaW1hbF9pbnRlZ2VyX3JlICtcbiAgICAnKSc7XG5cbiAgY29uc3QgZmxvYXRfcmUgPSAnKCcgK1xuICAgICAgaGV4YWRlY2ltYWxfZmxvYXRfcmUgKyAnfCcgK1xuICAgICAgZGVjaW1hbF9mbG9hdF9yZSArXG4gICAgJyknO1xuXG4gIC8qKlxuICAgKiBFc2NhcGUgc2VxdWVuY2Ugc3VwcG9ydGVkIGluIEQgc3RyaW5nIGFuZCBjaGFyYWN0ZXIgbGl0ZXJhbHNcbiAgICpcbiAgICogQHR5cGUge1N0cmluZ31cbiAgICovXG4gIGNvbnN0IGVzY2FwZV9zZXF1ZW5jZV9yZSA9ICdcXFxcXFxcXCgnICtcbiAgICAgICAgICAgICAgJ1tcXCdcIlxcXFw/XFxcXFxcXFxhYmZucnR2XXwnICsgLy8gY29tbW9uIGVzY2FwZXNcbiAgICAgICAgICAgICAgJ3VbXFxcXGRBLUZhLWZdezR9fCcgKyAvLyBmb3VyIGhleCBkaWdpdCB1bmljb2RlIGNvZGVwb2ludFxuICAgICAgICAgICAgICAnWzAtN117MSwzfXwnICsgLy8gb25lIHRvIHRocmVlIG9jdGFsIGRpZ2l0IGFzY2lpIGNoYXIgY29kZVxuICAgICAgICAgICAgICAneFtcXFxcZEEtRmEtZl17Mn18JyArIC8vIHR3byBoZXggZGlnaXQgYXNjaWkgY2hhciBjb2RlXG4gICAgICAgICAgICAgICdVW1xcXFxkQS1GYS1mXXs4fScgKyAvLyBlaWdodCBoZXggZGlnaXQgdW5pY29kZSBjb2RlcG9pbnRcbiAgICAgICAgICAgICAgJyl8JyArXG4gICAgICAgICAgICAgICcmW2EtekEtWlxcXFxkXXsyLH07JzsgLy8gbmFtZWQgY2hhcmFjdGVyIGVudGl0eVxuXG4gIC8qKlxuICAgKiBEIGludGVnZXIgbnVtYmVyIGxpdGVyYWxzXG4gICAqXG4gICAqIEB0eXBlIHtPYmplY3R9XG4gICAqL1xuICBjb25zdCBEX0lOVEVHRVJfTU9ERSA9IHtcbiAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgIGJlZ2luOiAnXFxcXGInICsgaW50ZWdlcl9yZSArICcoTHx1fFV8THV8TFV8dUx8VUwpPycsXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG5cbiAgLyoqXG4gICAqIFtEX0ZMT0FUX01PREUgZGVzY3JpcHRpb25dXG4gICAqIEB0eXBlIHtPYmplY3R9XG4gICAqL1xuICBjb25zdCBEX0ZMT0FUX01PREUgPSB7XG4gICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICBiZWdpbjogJ1xcXFxiKCcgK1xuICAgICAgICBmbG9hdF9yZSArICcoW2ZGXXxMfGl8W2ZGXWl8TGkpP3wnICtcbiAgICAgICAgaW50ZWdlcl9yZSArICcoaXxbZkZdaXxMaSknICtcbiAgICAgICcpJyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcblxuICAvKipcbiAgICogRCBjaGFyYWN0ZXIgbGl0ZXJhbFxuICAgKlxuICAgKiBAdHlwZSB7T2JqZWN0fVxuICAgKi9cbiAgY29uc3QgRF9DSEFSQUNURVJfTU9ERSA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAnXFwnKCcgKyBlc2NhcGVfc2VxdWVuY2VfcmUgKyAnfC4pJyxcbiAgICBlbmQ6ICdcXCcnLFxuICAgIGlsbGVnYWw6ICcuJ1xuICB9O1xuXG4gIC8qKlxuICAgKiBEIHN0cmluZyBlc2NhcGUgc2VxdWVuY2VcbiAgICpcbiAgICogQHR5cGUge09iamVjdH1cbiAgICovXG4gIGNvbnN0IERfRVNDQVBFX1NFUVVFTkNFID0ge1xuICAgIGJlZ2luOiBlc2NhcGVfc2VxdWVuY2VfcmUsXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG5cbiAgLyoqXG4gICAqIEQgZG91YmxlIHF1b3RlZCBzdHJpbmcgbGl0ZXJhbFxuICAgKlxuICAgKiBAdHlwZSB7T2JqZWN0fVxuICAgKi9cbiAgY29uc3QgRF9TVFJJTkdfTU9ERSA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAnXCInLFxuICAgIGNvbnRhaW5zOiBbRF9FU0NBUEVfU0VRVUVOQ0VdLFxuICAgIGVuZDogJ1wiW2N3ZF0/J1xuICB9O1xuXG4gIC8qKlxuICAgKiBEIHd5c2l3eWcgYW5kIGRlbGltaXRlZCBzdHJpbmcgbGl0ZXJhbHNcbiAgICpcbiAgICogQHR5cGUge09iamVjdH1cbiAgICovXG4gIGNvbnN0IERfV1lTSVdZR19ERUxJTUlURURfU1RSSU5HX01PREUgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogJ1tycV1cIicsXG4gICAgZW5kOiAnXCJbY3dkXT8nLFxuICAgIHJlbGV2YW5jZTogNVxuICB9O1xuXG4gIC8qKlxuICAgKiBEIGFsdGVybmF0ZSB3eXNpd3lnIHN0cmluZyBsaXRlcmFsXG4gICAqXG4gICAqIEB0eXBlIHtPYmplY3R9XG4gICAqL1xuICBjb25zdCBEX0FMVEVSTkFURV9XWVNJV1lHX1NUUklOR19NT0RFID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgYmVnaW46ICdgJyxcbiAgICBlbmQ6ICdgW2N3ZF0/J1xuICB9O1xuXG4gIC8qKlxuICAgKiBEIGhleGFkZWNpbWFsIHN0cmluZyBsaXRlcmFsXG4gICAqXG4gICAqIEB0eXBlIHtPYmplY3R9XG4gICAqL1xuICBjb25zdCBEX0hFWF9TVFJJTkdfTU9ERSA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAneFwiW1xcXFxkYS1mQS1GXFxcXHNcXFxcblxcXFxyXSpcIltjd2RdPycsXG4gICAgcmVsZXZhbmNlOiAxMFxuICB9O1xuXG4gIC8qKlxuICAgKiBEIGRlbGltaXRlZCBzdHJpbmcgbGl0ZXJhbFxuICAgKlxuICAgKiBAdHlwZSB7T2JqZWN0fVxuICAgKi9cbiAgY29uc3QgRF9UT0tFTl9TVFJJTkdfTU9ERSA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAncVwiXFxcXHsnLFxuICAgIGVuZDogJ1xcXFx9XCInXG4gIH07XG5cbiAgLyoqXG4gICAqIEhhc2hiYW5nIHN1cHBvcnRcbiAgICpcbiAgICogQHR5cGUge09iamVjdH1cbiAgICovXG4gIGNvbnN0IERfSEFTSEJBTkdfTU9ERSA9IHtcbiAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICBiZWdpbjogJ14jIScsXG4gICAgZW5kOiAnJCcsXG4gICAgcmVsZXZhbmNlOiA1XG4gIH07XG5cbiAgLyoqXG4gICAqIEQgc3BlY2lhbCB0b2tlbiBzZXF1ZW5jZVxuICAgKlxuICAgKiBAdHlwZSB7T2JqZWN0fVxuICAgKi9cbiAgY29uc3QgRF9TUEVDSUFMX1RPS0VOX1NFUVVFTkNFX01PREUgPSB7XG4gICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgYmVnaW46ICcjKGxpbmUpJyxcbiAgICBlbmQ6ICckJyxcbiAgICByZWxldmFuY2U6IDVcbiAgfTtcblxuICAvKipcbiAgICogRCBhdHRyaWJ1dGVzXG4gICAqXG4gICAqIEB0eXBlIHtPYmplY3R9XG4gICAqL1xuICBjb25zdCBEX0FUVFJJQlVURV9NT0RFID0ge1xuICAgIGNsYXNzTmFtZTogJ2tleXdvcmQnLFxuICAgIGJlZ2luOiAnQFthLXpBLVpfXVthLXpBLVpfXFxcXGRdKidcbiAgfTtcblxuICAvKipcbiAgICogRCBuZXN0aW5nIGNvbW1lbnRcbiAgICpcbiAgICogQHR5cGUge09iamVjdH1cbiAgICovXG4gIGNvbnN0IERfTkVTVElOR19DT01NRU5UX01PREUgPSBobGpzLkNPTU1FTlQoXG4gICAgJ1xcXFwvXFxcXCsnLFxuICAgICdcXFxcK1xcXFwvJyxcbiAgICB7XG4gICAgICBjb250YWluczogWydzZWxmJ10sXG4gICAgICByZWxldmFuY2U6IDEwXG4gICAgfVxuICApO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0QnLFxuICAgIGtleXdvcmRzOiBEX0tFWVdPUkRTLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAgRF9ORVNUSU5HX0NPTU1FTlRfTU9ERSxcbiAgICAgIERfSEVYX1NUUklOR19NT0RFLFxuICAgICAgRF9TVFJJTkdfTU9ERSxcbiAgICAgIERfV1lTSVdZR19ERUxJTUlURURfU1RSSU5HX01PREUsXG4gICAgICBEX0FMVEVSTkFURV9XWVNJV1lHX1NUUklOR19NT0RFLFxuICAgICAgRF9UT0tFTl9TVFJJTkdfTU9ERSxcbiAgICAgIERfRkxPQVRfTU9ERSxcbiAgICAgIERfSU5URUdFUl9NT0RFLFxuICAgICAgRF9DSEFSQUNURVJfTU9ERSxcbiAgICAgIERfSEFTSEJBTkdfTU9ERSxcbiAgICAgIERfU1BFQ0lBTF9UT0tFTl9TRVFVRU5DRV9NT0RFLFxuICAgICAgRF9BVFRSSUJVVEVfTU9ERVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBkO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9