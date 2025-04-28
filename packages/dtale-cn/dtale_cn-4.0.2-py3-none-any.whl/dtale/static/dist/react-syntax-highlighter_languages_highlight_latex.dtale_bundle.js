(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_latex"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/latex.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/latex.js ***!
  \************************************************************************************************/
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
Language: LaTeX
Author: Benedikt Wilde <bwilde@posteo.de>
Website: https://www.latex-project.org
Category: markup
*/

/** @type LanguageFn */
function latex(hljs) {
  const KNOWN_CONTROL_WORDS = either(...[
      '(?:NeedsTeXFormat|RequirePackage|GetIdInfo)',
      'Provides(?:Expl)?(?:Package|Class|File)',
      '(?:DeclareOption|ProcessOptions)',
      '(?:documentclass|usepackage|input|include)',
      'makeat(?:letter|other)',
      'ExplSyntax(?:On|Off)',
      '(?:new|renew|provide)?command',
      '(?:re)newenvironment',
      '(?:New|Renew|Provide|Declare)(?:Expandable)?DocumentCommand',
      '(?:New|Renew|Provide|Declare)DocumentEnvironment',
      '(?:(?:e|g|x)?def|let)',
      '(?:begin|end)',
      '(?:part|chapter|(?:sub){0,2}section|(?:sub)?paragraph)',
      'caption',
      '(?:label|(?:eq|page|name)?ref|(?:paren|foot|super)?cite)',
      '(?:alpha|beta|[Gg]amma|[Dd]elta|(?:var)?epsilon|zeta|eta|[Tt]heta|vartheta)',
      '(?:iota|(?:var)?kappa|[Ll]ambda|mu|nu|[Xx]i|[Pp]i|varpi|(?:var)rho)',
      '(?:[Ss]igma|varsigma|tau|[Uu]psilon|[Pp]hi|varphi|chi|[Pp]si|[Oo]mega)',
      '(?:frac|sum|prod|lim|infty|times|sqrt|leq|geq|left|right|middle|[bB]igg?)',
      '(?:[lr]angle|q?quad|[lcvdi]?dots|d?dot|hat|tilde|bar)'
    ].map(word => word + '(?![a-zA-Z@:_])'));
  const L3_REGEX = new RegExp([
      // A function \module_function_name:signature or \__module_function_name:signature,
      // where both module and function_name need at least two characters and
      // function_name may contain single underscores.
      '(?:__)?[a-zA-Z]{2,}_[a-zA-Z](?:_?[a-zA-Z])+:[a-zA-Z]*',
      // A variable \scope_module_and_name_type or \scope__module_ane_name_type,
      // where scope is one of l, g or c, type needs at least two characters
      // and module_and_name may contain single underscores.
      '[lgc]__?[a-zA-Z](?:_?[a-zA-Z])*_[a-zA-Z]{2,}',
      // A quark \q_the_name or \q__the_name or
      // scan mark \s_the_name or \s__vthe_name,
      // where variable_name needs at least two characters and
      // may contain single underscores.
      '[qs]__?[a-zA-Z](?:_?[a-zA-Z])+',
      // Other LaTeX3 macro names that are not covered by the three rules above.
      'use(?:_i)?:[a-zA-Z]*',
      '(?:else|fi|or):',
      '(?:if|cs|exp):w',
      '(?:hbox|vbox):n',
      '::[a-zA-Z]_unbraced',
      '::[a-zA-Z:]'
    ].map(pattern => pattern + '(?![a-zA-Z:_])').join('|'));
  const L2_VARIANTS = [
    {begin: /[a-zA-Z@]+/}, // control word
    {begin: /[^a-zA-Z@]?/} // control symbol
  ];
  const DOUBLE_CARET_VARIANTS = [
    {begin: /\^{6}[0-9a-f]{6}/},
    {begin: /\^{5}[0-9a-f]{5}/},
    {begin: /\^{4}[0-9a-f]{4}/},
    {begin: /\^{3}[0-9a-f]{3}/},
    {begin: /\^{2}[0-9a-f]{2}/},
    {begin: /\^{2}[\u0000-\u007f]/}
  ];
  const CONTROL_SEQUENCE = {
    className: 'keyword',
    begin: /\\/,
    relevance: 0,
    contains: [
      {
        endsParent: true,
        begin: KNOWN_CONTROL_WORDS
      },
      {
        endsParent: true,
        begin: L3_REGEX
      },
      {
        endsParent: true,
        variants: DOUBLE_CARET_VARIANTS
      },
      {
        endsParent: true,
        relevance: 0,
        variants: L2_VARIANTS
      }
    ]
  };
  const MACRO_PARAM = {
    className: 'params',
    relevance: 0,
    begin: /#+\d?/
  };
  const DOUBLE_CARET_CHAR = {
    // relevance: 1
    variants: DOUBLE_CARET_VARIANTS
  };
  const SPECIAL_CATCODE = {
    className: 'built_in',
    relevance: 0,
    begin: /[$&^_]/
  };
  const MAGIC_COMMENT = {
    className: 'meta',
    begin: '% !TeX',
    end: '$',
    relevance: 10
  };
  const COMMENT = hljs.COMMENT(
    '%',
    '$',
    {
      relevance: 0
    }
  );
  const EVERYTHING_BUT_VERBATIM = [
    CONTROL_SEQUENCE,
    MACRO_PARAM,
    DOUBLE_CARET_CHAR,
    SPECIAL_CATCODE,
    MAGIC_COMMENT,
    COMMENT
  ];
  const BRACE_GROUP_NO_VERBATIM = {
    begin: /\{/, end: /\}/,
    relevance: 0,
    contains: ['self', ...EVERYTHING_BUT_VERBATIM]
  };
  const ARGUMENT_BRACES = hljs.inherit(
    BRACE_GROUP_NO_VERBATIM,
    {
      relevance: 0,
      endsParent: true,
      contains: [BRACE_GROUP_NO_VERBATIM, ...EVERYTHING_BUT_VERBATIM]
    }
  );
  const ARGUMENT_BRACKETS = {
    begin: /\[/,
      end: /\]/,
    endsParent: true,
    relevance: 0,
    contains: [BRACE_GROUP_NO_VERBATIM, ...EVERYTHING_BUT_VERBATIM]
  };
  const SPACE_GOBBLER = {
    begin: /\s+/,
    relevance: 0
  };
  const ARGUMENT_M = [ARGUMENT_BRACES];
  const ARGUMENT_O = [ARGUMENT_BRACKETS];
  const ARGUMENT_AND_THEN = function(arg, starts_mode) {
    return {
      contains: [SPACE_GOBBLER],
      starts: {
        relevance: 0,
        contains: arg,
        starts: starts_mode
      }
    };
  };
  const CSNAME = function(csname, starts_mode) {
    return {
        begin: '\\\\' + csname + '(?![a-zA-Z@:_])',
        keywords: {$pattern: /\\[a-zA-Z]+/, keyword: '\\' + csname},
        relevance: 0,
        contains: [SPACE_GOBBLER],
        starts: starts_mode
      };
  };
  const BEGIN_ENV = function(envname, starts_mode) {
    return hljs.inherit(
      {
        begin: '\\\\begin(?=[ \t]*(\\r?\\n[ \t]*)?\\{' + envname + '\\})',
        keywords: {$pattern: /\\[a-zA-Z]+/, keyword: '\\begin'},
        relevance: 0,
      },
      ARGUMENT_AND_THEN(ARGUMENT_M, starts_mode)
    );
  };
  const VERBATIM_DELIMITED_EQUAL = (innerName = "string") => {
    return hljs.END_SAME_AS_BEGIN({
      className: innerName,
      begin: /(.|\r?\n)/,
      end: /(.|\r?\n)/,
      excludeBegin: true,
      excludeEnd: true,
      endsParent: true
    });
  };
  const VERBATIM_DELIMITED_ENV = function(envname) {
    return {
      className: 'string',
      end: '(?=\\\\end\\{' + envname + '\\})'
    };
  };

  const VERBATIM_DELIMITED_BRACES = (innerName = "string") => {
    return {
      relevance: 0,
      begin: /\{/,
      starts: {
        endsParent: true,
        contains: [
          {
            className: innerName,
            end: /(?=\})/,
            endsParent:true,
            contains: [
              {
                begin: /\{/,
                end: /\}/,
                relevance: 0,
                contains: ["self"]
              }
            ],
          }
        ]
      }
    };
  };
  const VERBATIM = [
    ...['verb', 'lstinline'].map(csname => CSNAME(csname, {contains: [VERBATIM_DELIMITED_EQUAL()]})),
    CSNAME('mint', ARGUMENT_AND_THEN(ARGUMENT_M, {contains: [VERBATIM_DELIMITED_EQUAL()]})),
    CSNAME('mintinline', ARGUMENT_AND_THEN(ARGUMENT_M, {contains: [VERBATIM_DELIMITED_BRACES(), VERBATIM_DELIMITED_EQUAL()]})),
    CSNAME('url', {contains: [VERBATIM_DELIMITED_BRACES("link"), VERBATIM_DELIMITED_BRACES("link")]}),
    CSNAME('hyperref', {contains: [VERBATIM_DELIMITED_BRACES("link")]}),
    CSNAME('href', ARGUMENT_AND_THEN(ARGUMENT_O, {contains: [VERBATIM_DELIMITED_BRACES("link")]})),
    ...[].concat(...['', '\\*'].map(suffix => [
      BEGIN_ENV('verbatim' + suffix, VERBATIM_DELIMITED_ENV('verbatim' + suffix)),
      BEGIN_ENV('filecontents' + suffix,  ARGUMENT_AND_THEN(ARGUMENT_M, VERBATIM_DELIMITED_ENV('filecontents' + suffix))),
      ...['', 'B', 'L'].map(prefix =>
        BEGIN_ENV(prefix + 'Verbatim' + suffix, ARGUMENT_AND_THEN(ARGUMENT_O, VERBATIM_DELIMITED_ENV(prefix + 'Verbatim' + suffix)))
      )
    ])),
    BEGIN_ENV('minted', ARGUMENT_AND_THEN(ARGUMENT_O, ARGUMENT_AND_THEN(ARGUMENT_M, VERBATIM_DELIMITED_ENV('minted')))),
  ];

  return {
    name: 'LaTeX',
    aliases: ['tex'],
    contains: [
      ...VERBATIM,
      ...EVERYTHING_BUT_VERBATIM
    ]
  };
}

module.exports = latex;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbGF0ZXguZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQSxXQUFXLFFBQVE7QUFDbkIsYUFBYTtBQUNiOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXLHNCQUFzQjtBQUNqQyxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsK0JBQStCLElBQUk7QUFDbkM7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsdUJBQXVCLEdBQUc7QUFDMUI7QUFDQTtBQUNBO0FBQ0EsZ0RBQWdELEdBQUc7QUFDbkQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUssb0JBQW9CO0FBQ3pCLEtBQUssc0JBQXNCO0FBQzNCO0FBQ0E7QUFDQSxLQUFLLFdBQVcsRUFBRSxTQUFTLEVBQUUsRUFBRTtBQUMvQixLQUFLLFdBQVcsRUFBRSxTQUFTLEVBQUUsRUFBRTtBQUMvQixLQUFLLFdBQVcsRUFBRSxTQUFTLEVBQUUsRUFBRTtBQUMvQixLQUFLLFdBQVcsRUFBRSxTQUFTLEVBQUUsRUFBRTtBQUMvQixLQUFLLFdBQVcsRUFBRSxTQUFTLEVBQUUsRUFBRTtBQUMvQixLQUFLLFdBQVcsRUFBRTtBQUNsQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGNBQWMsV0FBVztBQUN6QjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG1CQUFtQixnREFBZ0Q7QUFDbkU7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHFEQUFxRCxrQkFBa0I7QUFDdkUsbUJBQW1CLDRDQUE0QztBQUMvRDtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0EseUJBQXlCLGtCQUFrQjtBQUMzQztBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLGdCQUFnQjtBQUNoQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsdUJBQXVCO0FBQ3ZCO0FBQ0E7QUFDQTtBQUNBLDBCQUEwQjtBQUMxQix3QkFBd0I7QUFDeEI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSwyREFBMkQsdUNBQXVDO0FBQ2xHLGtEQUFrRCx1Q0FBdUM7QUFDekYsd0RBQXdELG9FQUFvRTtBQUM1SCxtQkFBbUIsaUZBQWlGO0FBQ3BHLHdCQUF3Qiw4Q0FBOEM7QUFDdEUsa0RBQWtELDhDQUE4QztBQUNoRztBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9sYXRleC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKipcbiAqIEBwYXJhbSB7c3RyaW5nfSB2YWx1ZVxuICogQHJldHVybnMge1JlZ0V4cH1cbiAqICovXG5cbi8qKlxuICogQHBhcmFtIHtSZWdFeHAgfCBzdHJpbmcgfSByZVxuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gc291cmNlKHJlKSB7XG4gIGlmICghcmUpIHJldHVybiBudWxsO1xuICBpZiAodHlwZW9mIHJlID09PSBcInN0cmluZ1wiKSByZXR1cm4gcmU7XG5cbiAgcmV0dXJuIHJlLnNvdXJjZTtcbn1cblxuLyoqXG4gKiBBbnkgb2YgdGhlIHBhc3NlZCBleHByZXNzc2lvbnMgbWF5IG1hdGNoXG4gKlxuICogQ3JlYXRlcyBhIGh1Z2UgdGhpcyB8IHRoaXMgfCB0aGF0IHwgdGhhdCBtYXRjaFxuICogQHBhcmFtIHsoUmVnRXhwIHwgc3RyaW5nKVtdIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gZWl0aGVyKC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gJygnICsgYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcInxcIikgKyBcIilcIjtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuLypcbkxhbmd1YWdlOiBMYVRlWFxuQXV0aG9yOiBCZW5lZGlrdCBXaWxkZSA8YndpbGRlQHBvc3Rlby5kZT5cbldlYnNpdGU6IGh0dHBzOi8vd3d3LmxhdGV4LXByb2plY3Qub3JnXG5DYXRlZ29yeTogbWFya3VwXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gbGF0ZXgoaGxqcykge1xuICBjb25zdCBLTk9XTl9DT05UUk9MX1dPUkRTID0gZWl0aGVyKC4uLltcbiAgICAgICcoPzpOZWVkc1RlWEZvcm1hdHxSZXF1aXJlUGFja2FnZXxHZXRJZEluZm8pJyxcbiAgICAgICdQcm92aWRlcyg/OkV4cGwpPyg/OlBhY2thZ2V8Q2xhc3N8RmlsZSknLFxuICAgICAgJyg/OkRlY2xhcmVPcHRpb258UHJvY2Vzc09wdGlvbnMpJyxcbiAgICAgICcoPzpkb2N1bWVudGNsYXNzfHVzZXBhY2thZ2V8aW5wdXR8aW5jbHVkZSknLFxuICAgICAgJ21ha2VhdCg/OmxldHRlcnxvdGhlciknLFxuICAgICAgJ0V4cGxTeW50YXgoPzpPbnxPZmYpJyxcbiAgICAgICcoPzpuZXd8cmVuZXd8cHJvdmlkZSk/Y29tbWFuZCcsXG4gICAgICAnKD86cmUpbmV3ZW52aXJvbm1lbnQnLFxuICAgICAgJyg/Ok5ld3xSZW5ld3xQcm92aWRlfERlY2xhcmUpKD86RXhwYW5kYWJsZSk/RG9jdW1lbnRDb21tYW5kJyxcbiAgICAgICcoPzpOZXd8UmVuZXd8UHJvdmlkZXxEZWNsYXJlKURvY3VtZW50RW52aXJvbm1lbnQnLFxuICAgICAgJyg/Oig/OmV8Z3x4KT9kZWZ8bGV0KScsXG4gICAgICAnKD86YmVnaW58ZW5kKScsXG4gICAgICAnKD86cGFydHxjaGFwdGVyfCg/OnN1Yil7MCwyfXNlY3Rpb258KD86c3ViKT9wYXJhZ3JhcGgpJyxcbiAgICAgICdjYXB0aW9uJyxcbiAgICAgICcoPzpsYWJlbHwoPzplcXxwYWdlfG5hbWUpP3JlZnwoPzpwYXJlbnxmb290fHN1cGVyKT9jaXRlKScsXG4gICAgICAnKD86YWxwaGF8YmV0YXxbR2ddYW1tYXxbRGRdZWx0YXwoPzp2YXIpP2Vwc2lsb258emV0YXxldGF8W1R0XWhldGF8dmFydGhldGEpJyxcbiAgICAgICcoPzppb3RhfCg/OnZhcik/a2FwcGF8W0xsXWFtYmRhfG11fG51fFtYeF1pfFtQcF1pfHZhcnBpfCg/OnZhcilyaG8pJyxcbiAgICAgICcoPzpbU3NdaWdtYXx2YXJzaWdtYXx0YXV8W1V1XXBzaWxvbnxbUHBdaGl8dmFycGhpfGNoaXxbUHBdc2l8W09vXW1lZ2EpJyxcbiAgICAgICcoPzpmcmFjfHN1bXxwcm9kfGxpbXxpbmZ0eXx0aW1lc3xzcXJ0fGxlcXxnZXF8bGVmdHxyaWdodHxtaWRkbGV8W2JCXWlnZz8pJyxcbiAgICAgICcoPzpbbHJdYW5nbGV8cT9xdWFkfFtsY3ZkaV0/ZG90c3xkP2RvdHxoYXR8dGlsZGV8YmFyKSdcbiAgICBdLm1hcCh3b3JkID0+IHdvcmQgKyAnKD8hW2EtekEtWkA6X10pJykpO1xuICBjb25zdCBMM19SRUdFWCA9IG5ldyBSZWdFeHAoW1xuICAgICAgLy8gQSBmdW5jdGlvbiBcXG1vZHVsZV9mdW5jdGlvbl9uYW1lOnNpZ25hdHVyZSBvciBcXF9fbW9kdWxlX2Z1bmN0aW9uX25hbWU6c2lnbmF0dXJlLFxuICAgICAgLy8gd2hlcmUgYm90aCBtb2R1bGUgYW5kIGZ1bmN0aW9uX25hbWUgbmVlZCBhdCBsZWFzdCB0d28gY2hhcmFjdGVycyBhbmRcbiAgICAgIC8vIGZ1bmN0aW9uX25hbWUgbWF5IGNvbnRhaW4gc2luZ2xlIHVuZGVyc2NvcmVzLlxuICAgICAgJyg/Ol9fKT9bYS16QS1aXXsyLH1fW2EtekEtWl0oPzpfP1thLXpBLVpdKSs6W2EtekEtWl0qJyxcbiAgICAgIC8vIEEgdmFyaWFibGUgXFxzY29wZV9tb2R1bGVfYW5kX25hbWVfdHlwZSBvciBcXHNjb3BlX19tb2R1bGVfYW5lX25hbWVfdHlwZSxcbiAgICAgIC8vIHdoZXJlIHNjb3BlIGlzIG9uZSBvZiBsLCBnIG9yIGMsIHR5cGUgbmVlZHMgYXQgbGVhc3QgdHdvIGNoYXJhY3RlcnNcbiAgICAgIC8vIGFuZCBtb2R1bGVfYW5kX25hbWUgbWF5IGNvbnRhaW4gc2luZ2xlIHVuZGVyc2NvcmVzLlxuICAgICAgJ1tsZ2NdX18/W2EtekEtWl0oPzpfP1thLXpBLVpdKSpfW2EtekEtWl17Mix9JyxcbiAgICAgIC8vIEEgcXVhcmsgXFxxX3RoZV9uYW1lIG9yIFxccV9fdGhlX25hbWUgb3JcbiAgICAgIC8vIHNjYW4gbWFyayBcXHNfdGhlX25hbWUgb3IgXFxzX192dGhlX25hbWUsXG4gICAgICAvLyB3aGVyZSB2YXJpYWJsZV9uYW1lIG5lZWRzIGF0IGxlYXN0IHR3byBjaGFyYWN0ZXJzIGFuZFxuICAgICAgLy8gbWF5IGNvbnRhaW4gc2luZ2xlIHVuZGVyc2NvcmVzLlxuICAgICAgJ1txc11fXz9bYS16QS1aXSg/Ol8/W2EtekEtWl0pKycsXG4gICAgICAvLyBPdGhlciBMYVRlWDMgbWFjcm8gbmFtZXMgdGhhdCBhcmUgbm90IGNvdmVyZWQgYnkgdGhlIHRocmVlIHJ1bGVzIGFib3ZlLlxuICAgICAgJ3VzZSg/Ol9pKT86W2EtekEtWl0qJyxcbiAgICAgICcoPzplbHNlfGZpfG9yKTonLFxuICAgICAgJyg/OmlmfGNzfGV4cCk6dycsXG4gICAgICAnKD86aGJveHx2Ym94KTpuJyxcbiAgICAgICc6OlthLXpBLVpdX3VuYnJhY2VkJyxcbiAgICAgICc6OlthLXpBLVo6XSdcbiAgICBdLm1hcChwYXR0ZXJuID0+IHBhdHRlcm4gKyAnKD8hW2EtekEtWjpfXSknKS5qb2luKCd8JykpO1xuICBjb25zdCBMMl9WQVJJQU5UUyA9IFtcbiAgICB7YmVnaW46IC9bYS16QS1aQF0rL30sIC8vIGNvbnRyb2wgd29yZFxuICAgIHtiZWdpbjogL1teYS16QS1aQF0/L30gLy8gY29udHJvbCBzeW1ib2xcbiAgXTtcbiAgY29uc3QgRE9VQkxFX0NBUkVUX1ZBUklBTlRTID0gW1xuICAgIHtiZWdpbjogL1xcXns2fVswLTlhLWZdezZ9L30sXG4gICAge2JlZ2luOiAvXFxeezV9WzAtOWEtZl17NX0vfSxcbiAgICB7YmVnaW46IC9cXF57NH1bMC05YS1mXXs0fS99LFxuICAgIHtiZWdpbjogL1xcXnszfVswLTlhLWZdezN9L30sXG4gICAge2JlZ2luOiAvXFxeezJ9WzAtOWEtZl17Mn0vfSxcbiAgICB7YmVnaW46IC9cXF57Mn1bXFx1MDAwMC1cXHUwMDdmXS99XG4gIF07XG4gIGNvbnN0IENPTlRST0xfU0VRVUVOQ0UgPSB7XG4gICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgYmVnaW46IC9cXFxcLyxcbiAgICByZWxldmFuY2U6IDAsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgZW5kc1BhcmVudDogdHJ1ZSxcbiAgICAgICAgYmVnaW46IEtOT1dOX0NPTlRST0xfV09SRFNcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGVuZHNQYXJlbnQ6IHRydWUsXG4gICAgICAgIGJlZ2luOiBMM19SRUdFWFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgZW5kc1BhcmVudDogdHJ1ZSxcbiAgICAgICAgdmFyaWFudHM6IERPVUJMRV9DQVJFVF9WQVJJQU5UU1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgZW5kc1BhcmVudDogdHJ1ZSxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICB2YXJpYW50czogTDJfVkFSSUFOVFNcbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIGNvbnN0IE1BQ1JPX1BBUkFNID0ge1xuICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIGJlZ2luOiAvIytcXGQ/L1xuICB9O1xuICBjb25zdCBET1VCTEVfQ0FSRVRfQ0hBUiA9IHtcbiAgICAvLyByZWxldmFuY2U6IDFcbiAgICB2YXJpYW50czogRE9VQkxFX0NBUkVUX1ZBUklBTlRTXG4gIH07XG4gIGNvbnN0IFNQRUNJQUxfQ0FUQ09ERSA9IHtcbiAgICBjbGFzc05hbWU6ICdidWlsdF9pbicsXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIGJlZ2luOiAvWyQmXl9dL1xuICB9O1xuICBjb25zdCBNQUdJQ19DT01NRU5UID0ge1xuICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgIGJlZ2luOiAnJSAhVGVYJyxcbiAgICBlbmQ6ICckJyxcbiAgICByZWxldmFuY2U6IDEwXG4gIH07XG4gIGNvbnN0IENPTU1FTlQgPSBobGpzLkNPTU1FTlQoXG4gICAgJyUnLFxuICAgICckJyxcbiAgICB7XG4gICAgICByZWxldmFuY2U6IDBcbiAgICB9XG4gICk7XG4gIGNvbnN0IEVWRVJZVEhJTkdfQlVUX1ZFUkJBVElNID0gW1xuICAgIENPTlRST0xfU0VRVUVOQ0UsXG4gICAgTUFDUk9fUEFSQU0sXG4gICAgRE9VQkxFX0NBUkVUX0NIQVIsXG4gICAgU1BFQ0lBTF9DQVRDT0RFLFxuICAgIE1BR0lDX0NPTU1FTlQsXG4gICAgQ09NTUVOVFxuICBdO1xuICBjb25zdCBCUkFDRV9HUk9VUF9OT19WRVJCQVRJTSA9IHtcbiAgICBiZWdpbjogL1xcey8sIGVuZDogL1xcfS8sXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIGNvbnRhaW5zOiBbJ3NlbGYnLCAuLi5FVkVSWVRISU5HX0JVVF9WRVJCQVRJTV1cbiAgfTtcbiAgY29uc3QgQVJHVU1FTlRfQlJBQ0VTID0gaGxqcy5pbmhlcml0KFxuICAgIEJSQUNFX0dST1VQX05PX1ZFUkJBVElNLFxuICAgIHtcbiAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgIGVuZHNQYXJlbnQ6IHRydWUsXG4gICAgICBjb250YWluczogW0JSQUNFX0dST1VQX05PX1ZFUkJBVElNLCAuLi5FVkVSWVRISU5HX0JVVF9WRVJCQVRJTV1cbiAgICB9XG4gICk7XG4gIGNvbnN0IEFSR1VNRU5UX0JSQUNLRVRTID0ge1xuICAgIGJlZ2luOiAvXFxbLyxcbiAgICAgIGVuZDogL1xcXS8sXG4gICAgZW5kc1BhcmVudDogdHJ1ZSxcbiAgICByZWxldmFuY2U6IDAsXG4gICAgY29udGFpbnM6IFtCUkFDRV9HUk9VUF9OT19WRVJCQVRJTSwgLi4uRVZFUllUSElOR19CVVRfVkVSQkFUSU1dXG4gIH07XG4gIGNvbnN0IFNQQUNFX0dPQkJMRVIgPSB7XG4gICAgYmVnaW46IC9cXHMrLyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgY29uc3QgQVJHVU1FTlRfTSA9IFtBUkdVTUVOVF9CUkFDRVNdO1xuICBjb25zdCBBUkdVTUVOVF9PID0gW0FSR1VNRU5UX0JSQUNLRVRTXTtcbiAgY29uc3QgQVJHVU1FTlRfQU5EX1RIRU4gPSBmdW5jdGlvbihhcmcsIHN0YXJ0c19tb2RlKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIGNvbnRhaW5zOiBbU1BBQ0VfR09CQkxFUl0sXG4gICAgICBzdGFydHM6IHtcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogYXJnLFxuICAgICAgICBzdGFydHM6IHN0YXJ0c19tb2RlXG4gICAgICB9XG4gICAgfTtcbiAgfTtcbiAgY29uc3QgQ1NOQU1FID0gZnVuY3Rpb24oY3NuYW1lLCBzdGFydHNfbW9kZSkge1xuICAgIHJldHVybiB7XG4gICAgICAgIGJlZ2luOiAnXFxcXFxcXFwnICsgY3NuYW1lICsgJyg/IVthLXpBLVpAOl9dKScsXG4gICAgICAgIGtleXdvcmRzOiB7JHBhdHRlcm46IC9cXFxcW2EtekEtWl0rLywga2V5d29yZDogJ1xcXFwnICsgY3NuYW1lfSxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogW1NQQUNFX0dPQkJMRVJdLFxuICAgICAgICBzdGFydHM6IHN0YXJ0c19tb2RlXG4gICAgICB9O1xuICB9O1xuICBjb25zdCBCRUdJTl9FTlYgPSBmdW5jdGlvbihlbnZuYW1lLCBzdGFydHNfbW9kZSkge1xuICAgIHJldHVybiBobGpzLmluaGVyaXQoXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXFxcXFxcXFxiZWdpbig/PVsgXFx0XSooXFxcXHI/XFxcXG5bIFxcdF0qKT9cXFxceycgKyBlbnZuYW1lICsgJ1xcXFx9KScsXG4gICAgICAgIGtleXdvcmRzOiB7JHBhdHRlcm46IC9cXFxcW2EtekEtWl0rLywga2V5d29yZDogJ1xcXFxiZWdpbid9LFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICB9LFxuICAgICAgQVJHVU1FTlRfQU5EX1RIRU4oQVJHVU1FTlRfTSwgc3RhcnRzX21vZGUpXG4gICAgKTtcbiAgfTtcbiAgY29uc3QgVkVSQkFUSU1fREVMSU1JVEVEX0VRVUFMID0gKGlubmVyTmFtZSA9IFwic3RyaW5nXCIpID0+IHtcbiAgICByZXR1cm4gaGxqcy5FTkRfU0FNRV9BU19CRUdJTih7XG4gICAgICBjbGFzc05hbWU6IGlubmVyTmFtZSxcbiAgICAgIGJlZ2luOiAvKC58XFxyP1xcbikvLFxuICAgICAgZW5kOiAvKC58XFxyP1xcbikvLFxuICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgIGVuZHNQYXJlbnQ6IHRydWVcbiAgICB9KTtcbiAgfTtcbiAgY29uc3QgVkVSQkFUSU1fREVMSU1JVEVEX0VOViA9IGZ1bmN0aW9uKGVudm5hbWUpIHtcbiAgICByZXR1cm4ge1xuICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgIGVuZDogJyg/PVxcXFxcXFxcZW5kXFxcXHsnICsgZW52bmFtZSArICdcXFxcfSknXG4gICAgfTtcbiAgfTtcblxuICBjb25zdCBWRVJCQVRJTV9ERUxJTUlURURfQlJBQ0VTID0gKGlubmVyTmFtZSA9IFwic3RyaW5nXCIpID0+IHtcbiAgICByZXR1cm4ge1xuICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgYmVnaW46IC9cXHsvLFxuICAgICAgc3RhcnRzOiB7XG4gICAgICAgIGVuZHNQYXJlbnQ6IHRydWUsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiBpbm5lck5hbWUsXG4gICAgICAgICAgICBlbmQ6IC8oPz1cXH0pLyxcbiAgICAgICAgICAgIGVuZHNQYXJlbnQ6dHJ1ZSxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICBiZWdpbjogL1xcey8sXG4gICAgICAgICAgICAgICAgZW5kOiAvXFx9LyxcbiAgICAgICAgICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgICAgICAgICAgY29udGFpbnM6IFtcInNlbGZcIl1cbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgXSxcbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH1cbiAgICB9O1xuICB9O1xuICBjb25zdCBWRVJCQVRJTSA9IFtcbiAgICAuLi5bJ3ZlcmInLCAnbHN0aW5saW5lJ10ubWFwKGNzbmFtZSA9PiBDU05BTUUoY3NuYW1lLCB7Y29udGFpbnM6IFtWRVJCQVRJTV9ERUxJTUlURURfRVFVQUwoKV19KSksXG4gICAgQ1NOQU1FKCdtaW50JywgQVJHVU1FTlRfQU5EX1RIRU4oQVJHVU1FTlRfTSwge2NvbnRhaW5zOiBbVkVSQkFUSU1fREVMSU1JVEVEX0VRVUFMKCldfSkpLFxuICAgIENTTkFNRSgnbWludGlubGluZScsIEFSR1VNRU5UX0FORF9USEVOKEFSR1VNRU5UX00sIHtjb250YWluczogW1ZFUkJBVElNX0RFTElNSVRFRF9CUkFDRVMoKSwgVkVSQkFUSU1fREVMSU1JVEVEX0VRVUFMKCldfSkpLFxuICAgIENTTkFNRSgndXJsJywge2NvbnRhaW5zOiBbVkVSQkFUSU1fREVMSU1JVEVEX0JSQUNFUyhcImxpbmtcIiksIFZFUkJBVElNX0RFTElNSVRFRF9CUkFDRVMoXCJsaW5rXCIpXX0pLFxuICAgIENTTkFNRSgnaHlwZXJyZWYnLCB7Y29udGFpbnM6IFtWRVJCQVRJTV9ERUxJTUlURURfQlJBQ0VTKFwibGlua1wiKV19KSxcbiAgICBDU05BTUUoJ2hyZWYnLCBBUkdVTUVOVF9BTkRfVEhFTihBUkdVTUVOVF9PLCB7Y29udGFpbnM6IFtWRVJCQVRJTV9ERUxJTUlURURfQlJBQ0VTKFwibGlua1wiKV19KSksXG4gICAgLi4uW10uY29uY2F0KC4uLlsnJywgJ1xcXFwqJ10ubWFwKHN1ZmZpeCA9PiBbXG4gICAgICBCRUdJTl9FTlYoJ3ZlcmJhdGltJyArIHN1ZmZpeCwgVkVSQkFUSU1fREVMSU1JVEVEX0VOVigndmVyYmF0aW0nICsgc3VmZml4KSksXG4gICAgICBCRUdJTl9FTlYoJ2ZpbGVjb250ZW50cycgKyBzdWZmaXgsICBBUkdVTUVOVF9BTkRfVEhFTihBUkdVTUVOVF9NLCBWRVJCQVRJTV9ERUxJTUlURURfRU5WKCdmaWxlY29udGVudHMnICsgc3VmZml4KSkpLFxuICAgICAgLi4uWycnLCAnQicsICdMJ10ubWFwKHByZWZpeCA9PlxuICAgICAgICBCRUdJTl9FTlYocHJlZml4ICsgJ1ZlcmJhdGltJyArIHN1ZmZpeCwgQVJHVU1FTlRfQU5EX1RIRU4oQVJHVU1FTlRfTywgVkVSQkFUSU1fREVMSU1JVEVEX0VOVihwcmVmaXggKyAnVmVyYmF0aW0nICsgc3VmZml4KSkpXG4gICAgICApXG4gICAgXSkpLFxuICAgIEJFR0lOX0VOVignbWludGVkJywgQVJHVU1FTlRfQU5EX1RIRU4oQVJHVU1FTlRfTywgQVJHVU1FTlRfQU5EX1RIRU4oQVJHVU1FTlRfTSwgVkVSQkFUSU1fREVMSU1JVEVEX0VOVignbWludGVkJykpKSksXG4gIF07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnTGFUZVgnLFxuICAgIGFsaWFzZXM6IFsndGV4J10sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIC4uLlZFUkJBVElNLFxuICAgICAgLi4uRVZFUllUSElOR19CVVRfVkVSQkFUSU1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gbGF0ZXg7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=