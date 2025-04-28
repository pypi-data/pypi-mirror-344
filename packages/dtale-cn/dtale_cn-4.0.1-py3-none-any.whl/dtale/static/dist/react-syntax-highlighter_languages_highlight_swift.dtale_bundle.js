(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_swift"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/swift.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/swift.js ***!
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

const keywordWrapper = keyword => concat(
  /\b/,
  keyword,
  /\w$/.test(keyword) ? /\b/ : /\B/
);

// Keywords that require a leading dot.
const dotKeywords = [
  'Protocol', // contextual
  'Type' // contextual
].map(keywordWrapper);

// Keywords that may have a leading dot.
const optionalDotKeywords = [
  'init',
  'self'
].map(keywordWrapper);

// should register as keyword, not type
const keywordTypes = [
  'Any',
  'Self'
];

// Regular keywords and literals.
const keywords = [
  // strings below will be fed into the regular `keywords` engine while regex
  // will result in additional modes being created to scan for those keywords to
  // avoid conflicts with other rules
  'associatedtype',
  'async',
  'await',
  /as\?/, // operator
  /as!/, // operator
  'as', // operator
  'break',
  'case',
  'catch',
  'class',
  'continue',
  'convenience', // contextual
  'default',
  'defer',
  'deinit',
  'didSet', // contextual
  'do',
  'dynamic', // contextual
  'else',
  'enum',
  'extension',
  'fallthrough',
  /fileprivate\(set\)/,
  'fileprivate',
  'final', // contextual
  'for',
  'func',
  'get', // contextual
  'guard',
  'if',
  'import',
  'indirect', // contextual
  'infix', // contextual
  /init\?/,
  /init!/,
  'inout',
  /internal\(set\)/,
  'internal',
  'in',
  'is', // operator
  'lazy', // contextual
  'let',
  'mutating', // contextual
  'nonmutating', // contextual
  /open\(set\)/, // contextual
  'open', // contextual
  'operator',
  'optional', // contextual
  'override', // contextual
  'postfix', // contextual
  'precedencegroup',
  'prefix', // contextual
  /private\(set\)/,
  'private',
  'protocol',
  /public\(set\)/,
  'public',
  'repeat',
  'required', // contextual
  'rethrows',
  'return',
  'set', // contextual
  'some', // contextual
  'static',
  'struct',
  'subscript',
  'super',
  'switch',
  'throws',
  'throw',
  /try\?/, // operator
  /try!/, // operator
  'try', // operator
  'typealias',
  /unowned\(safe\)/, // contextual
  /unowned\(unsafe\)/, // contextual
  'unowned', // contextual
  'var',
  'weak', // contextual
  'where',
  'while',
  'willSet' // contextual
];

// NOTE: Contextual keywords are reserved only in specific contexts.
// Ideally, these should be matched using modes to avoid false positives.

// Literals.
const literals = [
  'false',
  'nil',
  'true'
];

// Keywords used in precedence groups.
const precedencegroupKeywords = [
  'assignment',
  'associativity',
  'higherThan',
  'left',
  'lowerThan',
  'none',
  'right'
];

// Keywords that start with a number sign (#).
// #available is handled separately.
const numberSignKeywords = [
  '#colorLiteral',
  '#column',
  '#dsohandle',
  '#else',
  '#elseif',
  '#endif',
  '#error',
  '#file',
  '#fileID',
  '#fileLiteral',
  '#filePath',
  '#function',
  '#if',
  '#imageLiteral',
  '#keyPath',
  '#line',
  '#selector',
  '#sourceLocation',
  '#warn_unqualified_access',
  '#warning'
];

// Global functions in the Standard Library.
const builtIns = [
  'abs',
  'all',
  'any',
  'assert',
  'assertionFailure',
  'debugPrint',
  'dump',
  'fatalError',
  'getVaList',
  'isKnownUniquelyReferenced',
  'max',
  'min',
  'numericCast',
  'pointwiseMax',
  'pointwiseMin',
  'precondition',
  'preconditionFailure',
  'print',
  'readLine',
  'repeatElement',
  'sequence',
  'stride',
  'swap',
  'swift_unboxFromSwiftValueWithType',
  'transcode',
  'type',
  'unsafeBitCast',
  'unsafeDowncast',
  'withExtendedLifetime',
  'withUnsafeMutablePointer',
  'withUnsafePointer',
  'withVaList',
  'withoutActuallyEscaping',
  'zip'
];

// Valid first characters for operators.
const operatorHead = either(
  /[/=\-+!*%<>&|^~?]/,
  /[\u00A1-\u00A7]/,
  /[\u00A9\u00AB]/,
  /[\u00AC\u00AE]/,
  /[\u00B0\u00B1]/,
  /[\u00B6\u00BB\u00BF\u00D7\u00F7]/,
  /[\u2016-\u2017]/,
  /[\u2020-\u2027]/,
  /[\u2030-\u203E]/,
  /[\u2041-\u2053]/,
  /[\u2055-\u205E]/,
  /[\u2190-\u23FF]/,
  /[\u2500-\u2775]/,
  /[\u2794-\u2BFF]/,
  /[\u2E00-\u2E7F]/,
  /[\u3001-\u3003]/,
  /[\u3008-\u3020]/,
  /[\u3030]/
);

// Valid characters for operators.
const operatorCharacter = either(
  operatorHead,
  /[\u0300-\u036F]/,
  /[\u1DC0-\u1DFF]/,
  /[\u20D0-\u20FF]/,
  /[\uFE00-\uFE0F]/,
  /[\uFE20-\uFE2F]/
  // TODO: The following characters are also allowed, but the regex isn't supported yet.
  // /[\u{E0100}-\u{E01EF}]/u
);

// Valid operator.
const operator = concat(operatorHead, operatorCharacter, '*');

// Valid first characters for identifiers.
const identifierHead = either(
  /[a-zA-Z_]/,
  /[\u00A8\u00AA\u00AD\u00AF\u00B2-\u00B5\u00B7-\u00BA]/,
  /[\u00BC-\u00BE\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u00FF]/,
  /[\u0100-\u02FF\u0370-\u167F\u1681-\u180D\u180F-\u1DBF]/,
  /[\u1E00-\u1FFF]/,
  /[\u200B-\u200D\u202A-\u202E\u203F-\u2040\u2054\u2060-\u206F]/,
  /[\u2070-\u20CF\u2100-\u218F\u2460-\u24FF\u2776-\u2793]/,
  /[\u2C00-\u2DFF\u2E80-\u2FFF]/,
  /[\u3004-\u3007\u3021-\u302F\u3031-\u303F\u3040-\uD7FF]/,
  /[\uF900-\uFD3D\uFD40-\uFDCF\uFDF0-\uFE1F\uFE30-\uFE44]/,
  /[\uFE47-\uFEFE\uFF00-\uFFFD]/ // Should be /[\uFE47-\uFFFD]/, but we have to exclude FEFF.
  // The following characters are also allowed, but the regexes aren't supported yet.
  // /[\u{10000}-\u{1FFFD}\u{20000-\u{2FFFD}\u{30000}-\u{3FFFD}\u{40000}-\u{4FFFD}]/u,
  // /[\u{50000}-\u{5FFFD}\u{60000-\u{6FFFD}\u{70000}-\u{7FFFD}\u{80000}-\u{8FFFD}]/u,
  // /[\u{90000}-\u{9FFFD}\u{A0000-\u{AFFFD}\u{B0000}-\u{BFFFD}\u{C0000}-\u{CFFFD}]/u,
  // /[\u{D0000}-\u{DFFFD}\u{E0000-\u{EFFFD}]/u
);

// Valid characters for identifiers.
const identifierCharacter = either(
  identifierHead,
  /\d/,
  /[\u0300-\u036F\u1DC0-\u1DFF\u20D0-\u20FF\uFE20-\uFE2F]/
);

// Valid identifier.
const identifier = concat(identifierHead, identifierCharacter, '*');

// Valid type identifier.
const typeIdentifier = concat(/[A-Z]/, identifierCharacter, '*');

// Built-in attributes, which are highlighted as keywords.
// @available is handled separately.
const keywordAttributes = [
  'autoclosure',
  concat(/convention\(/, either('swift', 'block', 'c'), /\)/),
  'discardableResult',
  'dynamicCallable',
  'dynamicMemberLookup',
  'escaping',
  'frozen',
  'GKInspectable',
  'IBAction',
  'IBDesignable',
  'IBInspectable',
  'IBOutlet',
  'IBSegueAction',
  'inlinable',
  'main',
  'nonobjc',
  'NSApplicationMain',
  'NSCopying',
  'NSManaged',
  concat(/objc\(/, identifier, /\)/),
  'objc',
  'objcMembers',
  'propertyWrapper',
  'requires_stored_property_inits',
  'testable',
  'UIApplicationMain',
  'unknown',
  'usableFromInline'
];

// Contextual keywords used in @available and #available.
const availabilityKeywords = [
  'iOS',
  'iOSApplicationExtension',
  'macOS',
  'macOSApplicationExtension',
  'macCatalyst',
  'macCatalystApplicationExtension',
  'watchOS',
  'watchOSApplicationExtension',
  'tvOS',
  'tvOSApplicationExtension',
  'swift'
];

/*
Language: Swift
Description: Swift is a general-purpose programming language built using a modern approach to safety, performance, and software design patterns.
Author: Steven Van Impe <steven.vanimpe@icloud.com>
Contributors: Chris Eidhof <chris@eidhof.nl>, Nate Cook <natecook@gmail.com>, Alexander Lichter <manniL@gmx.net>, Richard Gibson <gibson042@github>
Website: https://swift.org
Category: common, system
*/

/** @type LanguageFn */
function swift(hljs) {
  const WHITESPACE = {
    match: /\s+/,
    relevance: 0
  };
  // https://docs.swift.org/swift-book/ReferenceManual/LexicalStructure.html#ID411
  const BLOCK_COMMENT = hljs.COMMENT(
    '/\\*',
    '\\*/',
    {
      contains: [ 'self' ]
    }
  );
  const COMMENTS = [
    hljs.C_LINE_COMMENT_MODE,
    BLOCK_COMMENT
  ];

  // https://docs.swift.org/swift-book/ReferenceManual/LexicalStructure.html#ID413
  // https://docs.swift.org/swift-book/ReferenceManual/zzSummaryOfTheGrammar.html
  const DOT_KEYWORD = {
    className: 'keyword',
    begin: concat(/\./, lookahead(either(...dotKeywords, ...optionalDotKeywords))),
    end: either(...dotKeywords, ...optionalDotKeywords),
    excludeBegin: true
  };
  const KEYWORD_GUARD = {
    // Consume .keyword to prevent highlighting properties and methods as keywords.
    match: concat(/\./, either(...keywords)),
    relevance: 0
  };
  const PLAIN_KEYWORDS = keywords
    .filter(kw => typeof kw === 'string')
    .concat([ "_|0" ]); // seems common, so 0 relevance
  const REGEX_KEYWORDS = keywords
    .filter(kw => typeof kw !== 'string') // find regex
    .concat(keywordTypes)
    .map(keywordWrapper);
  const KEYWORD = {
    variants: [
      {
        className: 'keyword',
        match: either(...REGEX_KEYWORDS, ...optionalDotKeywords)
      }
    ]
  };
  // find all the regular keywords
  const KEYWORDS = {
    $pattern: either(
      /\b\w+/, // regular keywords
      /#\w+/ // number keywords
    ),
    keyword: PLAIN_KEYWORDS
      .concat(numberSignKeywords),
    literal: literals
  };
  const KEYWORD_MODES = [
    DOT_KEYWORD,
    KEYWORD_GUARD,
    KEYWORD
  ];

  // https://github.com/apple/swift/tree/main/stdlib/public/core
  const BUILT_IN_GUARD = {
    // Consume .built_in to prevent highlighting properties and methods.
    match: concat(/\./, either(...builtIns)),
    relevance: 0
  };
  const BUILT_IN = {
    className: 'built_in',
    match: concat(/\b/, either(...builtIns), /(?=\()/)
  };
  const BUILT_INS = [
    BUILT_IN_GUARD,
    BUILT_IN
  ];

  // https://docs.swift.org/swift-book/ReferenceManual/LexicalStructure.html#ID418
  const OPERATOR_GUARD = {
    // Prevent -> from being highlighting as an operator.
    match: /->/,
    relevance: 0
  };
  const OPERATOR = {
    className: 'operator',
    relevance: 0,
    variants: [
      {
        match: operator
      },
      {
        // dot-operator: only operators that start with a dot are allowed to use dots as
        // characters (..., ...<, .*, etc). So there rule here is: a dot followed by one or more
        // characters that may also include dots.
        match: `\\.(\\.|${operatorCharacter})+`
      }
    ]
  };
  const OPERATORS = [
    OPERATOR_GUARD,
    OPERATOR
  ];

  // https://docs.swift.org/swift-book/ReferenceManual/LexicalStructure.html#grammar_numeric-literal
  // TODO: Update for leading `-` after lookbehind is supported everywhere
  const decimalDigits = '([0-9]_*)+';
  const hexDigits = '([0-9a-fA-F]_*)+';
  const NUMBER = {
    className: 'number',
    relevance: 0,
    variants: [
      // decimal floating-point-literal (subsumes decimal-literal)
      {
        match: `\\b(${decimalDigits})(\\.(${decimalDigits}))?` + `([eE][+-]?(${decimalDigits}))?\\b`
      },
      // hexadecimal floating-point-literal (subsumes hexadecimal-literal)
      {
        match: `\\b0x(${hexDigits})(\\.(${hexDigits}))?` + `([pP][+-]?(${decimalDigits}))?\\b`
      },
      // octal-literal
      {
        match: /\b0o([0-7]_*)+\b/
      },
      // binary-literal
      {
        match: /\b0b([01]_*)+\b/
      }
    ]
  };

  // https://docs.swift.org/swift-book/ReferenceManual/LexicalStructure.html#grammar_string-literal
  const ESCAPED_CHARACTER = (rawDelimiter = "") => ({
    className: 'subst',
    variants: [
      {
        match: concat(/\\/, rawDelimiter, /[0\\tnr"']/)
      },
      {
        match: concat(/\\/, rawDelimiter, /u\{[0-9a-fA-F]{1,8}\}/)
      }
    ]
  });
  const ESCAPED_NEWLINE = (rawDelimiter = "") => ({
    className: 'subst',
    match: concat(/\\/, rawDelimiter, /[\t ]*(?:[\r\n]|\r\n)/)
  });
  const INTERPOLATION = (rawDelimiter = "") => ({
    className: 'subst',
    label: "interpol",
    begin: concat(/\\/, rawDelimiter, /\(/),
    end: /\)/
  });
  const MULTILINE_STRING = (rawDelimiter = "") => ({
    begin: concat(rawDelimiter, /"""/),
    end: concat(/"""/, rawDelimiter),
    contains: [
      ESCAPED_CHARACTER(rawDelimiter),
      ESCAPED_NEWLINE(rawDelimiter),
      INTERPOLATION(rawDelimiter)
    ]
  });
  const SINGLE_LINE_STRING = (rawDelimiter = "") => ({
    begin: concat(rawDelimiter, /"/),
    end: concat(/"/, rawDelimiter),
    contains: [
      ESCAPED_CHARACTER(rawDelimiter),
      INTERPOLATION(rawDelimiter)
    ]
  });
  const STRING = {
    className: 'string',
    variants: [
      MULTILINE_STRING(),
      MULTILINE_STRING("#"),
      MULTILINE_STRING("##"),
      MULTILINE_STRING("###"),
      SINGLE_LINE_STRING(),
      SINGLE_LINE_STRING("#"),
      SINGLE_LINE_STRING("##"),
      SINGLE_LINE_STRING("###")
    ]
  };

  // https://docs.swift.org/swift-book/ReferenceManual/LexicalStructure.html#ID412
  const QUOTED_IDENTIFIER = {
    match: concat(/`/, identifier, /`/)
  };
  const IMPLICIT_PARAMETER = {
    className: 'variable',
    match: /\$\d+/
  };
  const PROPERTY_WRAPPER_PROJECTION = {
    className: 'variable',
    match: `\\$${identifierCharacter}+`
  };
  const IDENTIFIERS = [
    QUOTED_IDENTIFIER,
    IMPLICIT_PARAMETER,
    PROPERTY_WRAPPER_PROJECTION
  ];

  // https://docs.swift.org/swift-book/ReferenceManual/Attributes.html
  const AVAILABLE_ATTRIBUTE = {
    match: /(@|#)available/,
    className: "keyword",
    starts: {
      contains: [
        {
          begin: /\(/,
          end: /\)/,
          keywords: availabilityKeywords,
          contains: [
            ...OPERATORS,
            NUMBER,
            STRING
          ]
        }
      ]
    }
  };
  const KEYWORD_ATTRIBUTE = {
    className: 'keyword',
    match: concat(/@/, either(...keywordAttributes))
  };
  const USER_DEFINED_ATTRIBUTE = {
    className: 'meta',
    match: concat(/@/, identifier)
  };
  const ATTRIBUTES = [
    AVAILABLE_ATTRIBUTE,
    KEYWORD_ATTRIBUTE,
    USER_DEFINED_ATTRIBUTE
  ];

  // https://docs.swift.org/swift-book/ReferenceManual/Types.html
  const TYPE = {
    match: lookahead(/\b[A-Z]/),
    relevance: 0,
    contains: [
      { // Common Apple frameworks, for relevance boost
        className: 'type',
        match: concat(/(AV|CA|CF|CG|CI|CL|CM|CN|CT|MK|MP|MTK|MTL|NS|SCN|SK|UI|WK|XC)/, identifierCharacter, '+')
      },
      { // Type identifier
        className: 'type',
        match: typeIdentifier,
        relevance: 0
      },
      { // Optional type
        match: /[?!]+/,
        relevance: 0
      },
      { // Variadic parameter
        match: /\.\.\./,
        relevance: 0
      },
      { // Protocol composition
        match: concat(/\s+&\s+/, lookahead(typeIdentifier)),
        relevance: 0
      }
    ]
  };
  const GENERIC_ARGUMENTS = {
    begin: /</,
    end: />/,
    keywords: KEYWORDS,
    contains: [
      ...COMMENTS,
      ...KEYWORD_MODES,
      ...ATTRIBUTES,
      OPERATOR_GUARD,
      TYPE
    ]
  };
  TYPE.contains.push(GENERIC_ARGUMENTS);

  // https://docs.swift.org/swift-book/ReferenceManual/Expressions.html#ID552
  // Prevents element names from being highlighted as keywords.
  const TUPLE_ELEMENT_NAME = {
    match: concat(identifier, /\s*:/),
    keywords: "_|0",
    relevance: 0
  };
  // Matches tuples as well as the parameter list of a function type.
  const TUPLE = {
    begin: /\(/,
    end: /\)/,
    relevance: 0,
    keywords: KEYWORDS,
    contains: [
      'self',
      TUPLE_ELEMENT_NAME,
      ...COMMENTS,
      ...KEYWORD_MODES,
      ...BUILT_INS,
      ...OPERATORS,
      NUMBER,
      STRING,
      ...IDENTIFIERS,
      ...ATTRIBUTES,
      TYPE
    ]
  };

  // https://docs.swift.org/swift-book/ReferenceManual/Declarations.html#ID362
  // Matches both the keyword func and the function title.
  // Grouping these lets us differentiate between the operator function <
  // and the start of the generic parameter clause (also <).
  const FUNC_PLUS_TITLE = {
    beginKeywords: 'func',
    contains: [
      {
        className: 'title',
        match: either(QUOTED_IDENTIFIER.match, identifier, operator),
        // Required to make sure the opening < of the generic parameter clause
        // isn't parsed as a second title.
        endsParent: true,
        relevance: 0
      },
      WHITESPACE
    ]
  };
  const GENERIC_PARAMETERS = {
    begin: /</,
    end: />/,
    contains: [
      ...COMMENTS,
      TYPE
    ]
  };
  const FUNCTION_PARAMETER_NAME = {
    begin: either(
      lookahead(concat(identifier, /\s*:/)),
      lookahead(concat(identifier, /\s+/, identifier, /\s*:/))
    ),
    end: /:/,
    relevance: 0,
    contains: [
      {
        className: 'keyword',
        match: /\b_\b/
      },
      {
        className: 'params',
        match: identifier
      }
    ]
  };
  const FUNCTION_PARAMETERS = {
    begin: /\(/,
    end: /\)/,
    keywords: KEYWORDS,
    contains: [
      FUNCTION_PARAMETER_NAME,
      ...COMMENTS,
      ...KEYWORD_MODES,
      ...OPERATORS,
      NUMBER,
      STRING,
      ...ATTRIBUTES,
      TYPE,
      TUPLE
    ],
    endsParent: true,
    illegal: /["']/
  };
  const FUNCTION = {
    className: 'function',
    match: lookahead(/\bfunc\b/),
    contains: [
      FUNC_PLUS_TITLE,
      GENERIC_PARAMETERS,
      FUNCTION_PARAMETERS,
      WHITESPACE
    ],
    illegal: [
      /\[/,
      /%/
    ]
  };

  // https://docs.swift.org/swift-book/ReferenceManual/Declarations.html#ID375
  // https://docs.swift.org/swift-book/ReferenceManual/Declarations.html#ID379
  const INIT_SUBSCRIPT = {
    className: 'function',
    match: /\b(subscript|init[?!]?)\s*(?=[<(])/,
    keywords: {
      keyword: "subscript init init? init!",
      $pattern: /\w+[?!]?/
    },
    contains: [
      GENERIC_PARAMETERS,
      FUNCTION_PARAMETERS,
      WHITESPACE
    ],
    illegal: /\[|%/
  };
  // https://docs.swift.org/swift-book/ReferenceManual/Declarations.html#ID380
  const OPERATOR_DECLARATION = {
    beginKeywords: 'operator',
    end: hljs.MATCH_NOTHING_RE,
    contains: [
      {
        className: 'title',
        match: operator,
        endsParent: true,
        relevance: 0
      }
    ]
  };

  // https://docs.swift.org/swift-book/ReferenceManual/Declarations.html#ID550
  const PRECEDENCEGROUP = {
    beginKeywords: 'precedencegroup',
    end: hljs.MATCH_NOTHING_RE,
    contains: [
      {
        className: 'title',
        match: typeIdentifier,
        relevance: 0
      },
      {
        begin: /{/,
        end: /}/,
        relevance: 0,
        endsParent: true,
        keywords: [
          ...precedencegroupKeywords,
          ...literals
        ],
        contains: [ TYPE ]
      }
    ]
  };

  // Add supported submodes to string interpolation.
  for (const variant of STRING.variants) {
    const interpolation = variant.contains.find(mode => mode.label === "interpol");
    // TODO: Interpolation can contain any expression, so there's room for improvement here.
    interpolation.keywords = KEYWORDS;
    const submodes = [
      ...KEYWORD_MODES,
      ...BUILT_INS,
      ...OPERATORS,
      NUMBER,
      STRING,
      ...IDENTIFIERS
    ];
    interpolation.contains = [
      ...submodes,
      {
        begin: /\(/,
        end: /\)/,
        contains: [
          'self',
          ...submodes
        ]
      }
    ];
  }

  return {
    name: 'Swift',
    keywords: KEYWORDS,
    contains: [
      ...COMMENTS,
      FUNCTION,
      INIT_SUBSCRIPT,
      {
        className: 'class',
        beginKeywords: 'struct protocol class extension enum',
        end: '\\{',
        excludeEnd: true,
        keywords: KEYWORDS,
        contains: [
          hljs.inherit(hljs.TITLE_MODE, {
            begin: /[A-Za-z$_][\u00C0-\u02B80-9A-Za-z$_]*/
          }),
          ...KEYWORD_MODES
        ]
      },
      OPERATOR_DECLARATION,
      PRECEDENCEGROUP,
      {
        beginKeywords: 'import',
        end: /$/,
        contains: [ ...COMMENTS ],
        relevance: 0
      },
      ...KEYWORD_MODES,
      ...BUILT_INS,
      ...OPERATORS,
      NUMBER,
      STRING,
      ...IDENTIFIERS,
      ...ATTRIBUTES,
      TYPE,
      TUPLE
    ]
  };
}

module.exports = swift;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfc3dpZnQuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQSxXQUFXLFFBQVE7QUFDbkIsYUFBYTtBQUNiOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQSxXQUFXLHVCQUF1QjtBQUNsQyxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVcsc0JBQXNCO0FBQ2pDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxVQUFVLE1BQU0sSUFBSSxNQUFNO0FBQzFCOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFVBQVUsTUFBTSxJQUFJLE1BQU0sR0FBRyxTQUFTLE1BQU0sR0FBRyxNQUFNLElBQUksTUFBTSxHQUFHLE1BQU0sSUFBSSxNQUFNO0FBQ2xGLFVBQVUsTUFBTSxJQUFJLE1BQU0sR0FBRyxTQUFTLE1BQU0sR0FBRyxNQUFNLElBQUksTUFBTSxHQUFHLE1BQU0sSUFBSSxNQUFNO0FBQ2xGLFVBQVUsTUFBTSxJQUFJLE1BQU0sR0FBRyxTQUFTLE1BQU0sR0FBRyxNQUFNLElBQUksTUFBTSxHQUFHLE1BQU0sSUFBSSxNQUFNO0FBQ2xGLFVBQVUsTUFBTSxJQUFJLE1BQU0sR0FBRyxTQUFTLE1BQU07QUFDNUM7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esd0JBQXdCO0FBQ3hCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLDBCQUEwQixrQkFBa0I7QUFDNUM7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxzQkFBc0IsY0FBYyxRQUFRLGNBQWMscUJBQXFCLGNBQWM7QUFDN0YsT0FBTztBQUNQO0FBQ0E7QUFDQSx3QkFBd0IsVUFBVSxRQUFRLFVBQVUscUJBQXFCLGNBQWM7QUFDdkYsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0EsOENBQThDLFlBQVksSUFBSSxFQUFFO0FBQ2hFO0FBQ0E7QUFDQSxHQUFHO0FBQ0g7QUFDQTtBQUNBO0FBQ0EsR0FBRztBQUNIO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxHQUFHO0FBQ0g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQixvQkFBb0I7QUFDckM7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFFBQVE7QUFDUjtBQUNBO0FBQ0EsT0FBTztBQUNQLFFBQVE7QUFDUjtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1AsUUFBUTtBQUNSO0FBQ0E7QUFDQSxPQUFPO0FBQ1AsUUFBUTtBQUNSO0FBQ0E7QUFDQSxPQUFPO0FBQ1AsUUFBUTtBQUNSO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQSxpQkFBaUI7QUFDakIsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaUJBQWlCO0FBQ2pCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3N3aWZ0LmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogQHBhcmFtIHtzdHJpbmd9IHZhbHVlXG4gKiBAcmV0dXJucyB7UmVnRXhwfVxuICogKi9cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBzb3VyY2UocmUpIHtcbiAgaWYgKCFyZSkgcmV0dXJuIG51bGw7XG4gIGlmICh0eXBlb2YgcmUgPT09IFwic3RyaW5nXCIpIHJldHVybiByZTtcblxuICByZXR1cm4gcmUuc291cmNlO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGxvb2thaGVhZChyZSkge1xuICByZXR1cm4gY29uY2F0KCcoPz0nLCByZSwgJyknKTtcbn1cblxuLyoqXG4gKiBAcGFyYW0gey4uLihSZWdFeHAgfCBzdHJpbmcpIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gY29uY2F0KC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcIlwiKTtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuLyoqXG4gKiBBbnkgb2YgdGhlIHBhc3NlZCBleHByZXNzc2lvbnMgbWF5IG1hdGNoXG4gKlxuICogQ3JlYXRlcyBhIGh1Z2UgdGhpcyB8IHRoaXMgfCB0aGF0IHwgdGhhdCBtYXRjaFxuICogQHBhcmFtIHsoUmVnRXhwIHwgc3RyaW5nKVtdIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gZWl0aGVyKC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gJygnICsgYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcInxcIikgKyBcIilcIjtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuY29uc3Qga2V5d29yZFdyYXBwZXIgPSBrZXl3b3JkID0+IGNvbmNhdChcbiAgL1xcYi8sXG4gIGtleXdvcmQsXG4gIC9cXHckLy50ZXN0KGtleXdvcmQpID8gL1xcYi8gOiAvXFxCL1xuKTtcblxuLy8gS2V5d29yZHMgdGhhdCByZXF1aXJlIGEgbGVhZGluZyBkb3QuXG5jb25zdCBkb3RLZXl3b3JkcyA9IFtcbiAgJ1Byb3RvY29sJywgLy8gY29udGV4dHVhbFxuICAnVHlwZScgLy8gY29udGV4dHVhbFxuXS5tYXAoa2V5d29yZFdyYXBwZXIpO1xuXG4vLyBLZXl3b3JkcyB0aGF0IG1heSBoYXZlIGEgbGVhZGluZyBkb3QuXG5jb25zdCBvcHRpb25hbERvdEtleXdvcmRzID0gW1xuICAnaW5pdCcsXG4gICdzZWxmJ1xuXS5tYXAoa2V5d29yZFdyYXBwZXIpO1xuXG4vLyBzaG91bGQgcmVnaXN0ZXIgYXMga2V5d29yZCwgbm90IHR5cGVcbmNvbnN0IGtleXdvcmRUeXBlcyA9IFtcbiAgJ0FueScsXG4gICdTZWxmJ1xuXTtcblxuLy8gUmVndWxhciBrZXl3b3JkcyBhbmQgbGl0ZXJhbHMuXG5jb25zdCBrZXl3b3JkcyA9IFtcbiAgLy8gc3RyaW5ncyBiZWxvdyB3aWxsIGJlIGZlZCBpbnRvIHRoZSByZWd1bGFyIGBrZXl3b3Jkc2AgZW5naW5lIHdoaWxlIHJlZ2V4XG4gIC8vIHdpbGwgcmVzdWx0IGluIGFkZGl0aW9uYWwgbW9kZXMgYmVpbmcgY3JlYXRlZCB0byBzY2FuIGZvciB0aG9zZSBrZXl3b3JkcyB0b1xuICAvLyBhdm9pZCBjb25mbGljdHMgd2l0aCBvdGhlciBydWxlc1xuICAnYXNzb2NpYXRlZHR5cGUnLFxuICAnYXN5bmMnLFxuICAnYXdhaXQnLFxuICAvYXNcXD8vLCAvLyBvcGVyYXRvclxuICAvYXMhLywgLy8gb3BlcmF0b3JcbiAgJ2FzJywgLy8gb3BlcmF0b3JcbiAgJ2JyZWFrJyxcbiAgJ2Nhc2UnLFxuICAnY2F0Y2gnLFxuICAnY2xhc3MnLFxuICAnY29udGludWUnLFxuICAnY29udmVuaWVuY2UnLCAvLyBjb250ZXh0dWFsXG4gICdkZWZhdWx0JyxcbiAgJ2RlZmVyJyxcbiAgJ2RlaW5pdCcsXG4gICdkaWRTZXQnLCAvLyBjb250ZXh0dWFsXG4gICdkbycsXG4gICdkeW5hbWljJywgLy8gY29udGV4dHVhbFxuICAnZWxzZScsXG4gICdlbnVtJyxcbiAgJ2V4dGVuc2lvbicsXG4gICdmYWxsdGhyb3VnaCcsXG4gIC9maWxlcHJpdmF0ZVxcKHNldFxcKS8sXG4gICdmaWxlcHJpdmF0ZScsXG4gICdmaW5hbCcsIC8vIGNvbnRleHR1YWxcbiAgJ2ZvcicsXG4gICdmdW5jJyxcbiAgJ2dldCcsIC8vIGNvbnRleHR1YWxcbiAgJ2d1YXJkJyxcbiAgJ2lmJyxcbiAgJ2ltcG9ydCcsXG4gICdpbmRpcmVjdCcsIC8vIGNvbnRleHR1YWxcbiAgJ2luZml4JywgLy8gY29udGV4dHVhbFxuICAvaW5pdFxcPy8sXG4gIC9pbml0IS8sXG4gICdpbm91dCcsXG4gIC9pbnRlcm5hbFxcKHNldFxcKS8sXG4gICdpbnRlcm5hbCcsXG4gICdpbicsXG4gICdpcycsIC8vIG9wZXJhdG9yXG4gICdsYXp5JywgLy8gY29udGV4dHVhbFxuICAnbGV0JyxcbiAgJ211dGF0aW5nJywgLy8gY29udGV4dHVhbFxuICAnbm9ubXV0YXRpbmcnLCAvLyBjb250ZXh0dWFsXG4gIC9vcGVuXFwoc2V0XFwpLywgLy8gY29udGV4dHVhbFxuICAnb3BlbicsIC8vIGNvbnRleHR1YWxcbiAgJ29wZXJhdG9yJyxcbiAgJ29wdGlvbmFsJywgLy8gY29udGV4dHVhbFxuICAnb3ZlcnJpZGUnLCAvLyBjb250ZXh0dWFsXG4gICdwb3N0Zml4JywgLy8gY29udGV4dHVhbFxuICAncHJlY2VkZW5jZWdyb3VwJyxcbiAgJ3ByZWZpeCcsIC8vIGNvbnRleHR1YWxcbiAgL3ByaXZhdGVcXChzZXRcXCkvLFxuICAncHJpdmF0ZScsXG4gICdwcm90b2NvbCcsXG4gIC9wdWJsaWNcXChzZXRcXCkvLFxuICAncHVibGljJyxcbiAgJ3JlcGVhdCcsXG4gICdyZXF1aXJlZCcsIC8vIGNvbnRleHR1YWxcbiAgJ3JldGhyb3dzJyxcbiAgJ3JldHVybicsXG4gICdzZXQnLCAvLyBjb250ZXh0dWFsXG4gICdzb21lJywgLy8gY29udGV4dHVhbFxuICAnc3RhdGljJyxcbiAgJ3N0cnVjdCcsXG4gICdzdWJzY3JpcHQnLFxuICAnc3VwZXInLFxuICAnc3dpdGNoJyxcbiAgJ3Rocm93cycsXG4gICd0aHJvdycsXG4gIC90cnlcXD8vLCAvLyBvcGVyYXRvclxuICAvdHJ5IS8sIC8vIG9wZXJhdG9yXG4gICd0cnknLCAvLyBvcGVyYXRvclxuICAndHlwZWFsaWFzJyxcbiAgL3Vub3duZWRcXChzYWZlXFwpLywgLy8gY29udGV4dHVhbFxuICAvdW5vd25lZFxcKHVuc2FmZVxcKS8sIC8vIGNvbnRleHR1YWxcbiAgJ3Vub3duZWQnLCAvLyBjb250ZXh0dWFsXG4gICd2YXInLFxuICAnd2VhaycsIC8vIGNvbnRleHR1YWxcbiAgJ3doZXJlJyxcbiAgJ3doaWxlJyxcbiAgJ3dpbGxTZXQnIC8vIGNvbnRleHR1YWxcbl07XG5cbi8vIE5PVEU6IENvbnRleHR1YWwga2V5d29yZHMgYXJlIHJlc2VydmVkIG9ubHkgaW4gc3BlY2lmaWMgY29udGV4dHMuXG4vLyBJZGVhbGx5LCB0aGVzZSBzaG91bGQgYmUgbWF0Y2hlZCB1c2luZyBtb2RlcyB0byBhdm9pZCBmYWxzZSBwb3NpdGl2ZXMuXG5cbi8vIExpdGVyYWxzLlxuY29uc3QgbGl0ZXJhbHMgPSBbXG4gICdmYWxzZScsXG4gICduaWwnLFxuICAndHJ1ZSdcbl07XG5cbi8vIEtleXdvcmRzIHVzZWQgaW4gcHJlY2VkZW5jZSBncm91cHMuXG5jb25zdCBwcmVjZWRlbmNlZ3JvdXBLZXl3b3JkcyA9IFtcbiAgJ2Fzc2lnbm1lbnQnLFxuICAnYXNzb2NpYXRpdml0eScsXG4gICdoaWdoZXJUaGFuJyxcbiAgJ2xlZnQnLFxuICAnbG93ZXJUaGFuJyxcbiAgJ25vbmUnLFxuICAncmlnaHQnXG5dO1xuXG4vLyBLZXl3b3JkcyB0aGF0IHN0YXJ0IHdpdGggYSBudW1iZXIgc2lnbiAoIykuXG4vLyAjYXZhaWxhYmxlIGlzIGhhbmRsZWQgc2VwYXJhdGVseS5cbmNvbnN0IG51bWJlclNpZ25LZXl3b3JkcyA9IFtcbiAgJyNjb2xvckxpdGVyYWwnLFxuICAnI2NvbHVtbicsXG4gICcjZHNvaGFuZGxlJyxcbiAgJyNlbHNlJyxcbiAgJyNlbHNlaWYnLFxuICAnI2VuZGlmJyxcbiAgJyNlcnJvcicsXG4gICcjZmlsZScsXG4gICcjZmlsZUlEJyxcbiAgJyNmaWxlTGl0ZXJhbCcsXG4gICcjZmlsZVBhdGgnLFxuICAnI2Z1bmN0aW9uJyxcbiAgJyNpZicsXG4gICcjaW1hZ2VMaXRlcmFsJyxcbiAgJyNrZXlQYXRoJyxcbiAgJyNsaW5lJyxcbiAgJyNzZWxlY3RvcicsXG4gICcjc291cmNlTG9jYXRpb24nLFxuICAnI3dhcm5fdW5xdWFsaWZpZWRfYWNjZXNzJyxcbiAgJyN3YXJuaW5nJ1xuXTtcblxuLy8gR2xvYmFsIGZ1bmN0aW9ucyBpbiB0aGUgU3RhbmRhcmQgTGlicmFyeS5cbmNvbnN0IGJ1aWx0SW5zID0gW1xuICAnYWJzJyxcbiAgJ2FsbCcsXG4gICdhbnknLFxuICAnYXNzZXJ0JyxcbiAgJ2Fzc2VydGlvbkZhaWx1cmUnLFxuICAnZGVidWdQcmludCcsXG4gICdkdW1wJyxcbiAgJ2ZhdGFsRXJyb3InLFxuICAnZ2V0VmFMaXN0JyxcbiAgJ2lzS25vd25VbmlxdWVseVJlZmVyZW5jZWQnLFxuICAnbWF4JyxcbiAgJ21pbicsXG4gICdudW1lcmljQ2FzdCcsXG4gICdwb2ludHdpc2VNYXgnLFxuICAncG9pbnR3aXNlTWluJyxcbiAgJ3ByZWNvbmRpdGlvbicsXG4gICdwcmVjb25kaXRpb25GYWlsdXJlJyxcbiAgJ3ByaW50JyxcbiAgJ3JlYWRMaW5lJyxcbiAgJ3JlcGVhdEVsZW1lbnQnLFxuICAnc2VxdWVuY2UnLFxuICAnc3RyaWRlJyxcbiAgJ3N3YXAnLFxuICAnc3dpZnRfdW5ib3hGcm9tU3dpZnRWYWx1ZVdpdGhUeXBlJyxcbiAgJ3RyYW5zY29kZScsXG4gICd0eXBlJyxcbiAgJ3Vuc2FmZUJpdENhc3QnLFxuICAndW5zYWZlRG93bmNhc3QnLFxuICAnd2l0aEV4dGVuZGVkTGlmZXRpbWUnLFxuICAnd2l0aFVuc2FmZU11dGFibGVQb2ludGVyJyxcbiAgJ3dpdGhVbnNhZmVQb2ludGVyJyxcbiAgJ3dpdGhWYUxpc3QnLFxuICAnd2l0aG91dEFjdHVhbGx5RXNjYXBpbmcnLFxuICAnemlwJ1xuXTtcblxuLy8gVmFsaWQgZmlyc3QgY2hhcmFjdGVycyBmb3Igb3BlcmF0b3JzLlxuY29uc3Qgb3BlcmF0b3JIZWFkID0gZWl0aGVyKFxuICAvWy89XFwtKyEqJTw+Jnxefj9dLyxcbiAgL1tcXHUwMEExLVxcdTAwQTddLyxcbiAgL1tcXHUwMEE5XFx1MDBBQl0vLFxuICAvW1xcdTAwQUNcXHUwMEFFXS8sXG4gIC9bXFx1MDBCMFxcdTAwQjFdLyxcbiAgL1tcXHUwMEI2XFx1MDBCQlxcdTAwQkZcXHUwMEQ3XFx1MDBGN10vLFxuICAvW1xcdTIwMTYtXFx1MjAxN10vLFxuICAvW1xcdTIwMjAtXFx1MjAyN10vLFxuICAvW1xcdTIwMzAtXFx1MjAzRV0vLFxuICAvW1xcdTIwNDEtXFx1MjA1M10vLFxuICAvW1xcdTIwNTUtXFx1MjA1RV0vLFxuICAvW1xcdTIxOTAtXFx1MjNGRl0vLFxuICAvW1xcdTI1MDAtXFx1Mjc3NV0vLFxuICAvW1xcdTI3OTQtXFx1MkJGRl0vLFxuICAvW1xcdTJFMDAtXFx1MkU3Rl0vLFxuICAvW1xcdTMwMDEtXFx1MzAwM10vLFxuICAvW1xcdTMwMDgtXFx1MzAyMF0vLFxuICAvW1xcdTMwMzBdL1xuKTtcblxuLy8gVmFsaWQgY2hhcmFjdGVycyBmb3Igb3BlcmF0b3JzLlxuY29uc3Qgb3BlcmF0b3JDaGFyYWN0ZXIgPSBlaXRoZXIoXG4gIG9wZXJhdG9ySGVhZCxcbiAgL1tcXHUwMzAwLVxcdTAzNkZdLyxcbiAgL1tcXHUxREMwLVxcdTFERkZdLyxcbiAgL1tcXHUyMEQwLVxcdTIwRkZdLyxcbiAgL1tcXHVGRTAwLVxcdUZFMEZdLyxcbiAgL1tcXHVGRTIwLVxcdUZFMkZdL1xuICAvLyBUT0RPOiBUaGUgZm9sbG93aW5nIGNoYXJhY3RlcnMgYXJlIGFsc28gYWxsb3dlZCwgYnV0IHRoZSByZWdleCBpc24ndCBzdXBwb3J0ZWQgeWV0LlxuICAvLyAvW1xcdXtFMDEwMH0tXFx1e0UwMUVGfV0vdVxuKTtcblxuLy8gVmFsaWQgb3BlcmF0b3IuXG5jb25zdCBvcGVyYXRvciA9IGNvbmNhdChvcGVyYXRvckhlYWQsIG9wZXJhdG9yQ2hhcmFjdGVyLCAnKicpO1xuXG4vLyBWYWxpZCBmaXJzdCBjaGFyYWN0ZXJzIGZvciBpZGVudGlmaWVycy5cbmNvbnN0IGlkZW50aWZpZXJIZWFkID0gZWl0aGVyKFxuICAvW2EtekEtWl9dLyxcbiAgL1tcXHUwMEE4XFx1MDBBQVxcdTAwQURcXHUwMEFGXFx1MDBCMi1cXHUwMEI1XFx1MDBCNy1cXHUwMEJBXS8sXG4gIC9bXFx1MDBCQy1cXHUwMEJFXFx1MDBDMC1cXHUwMEQ2XFx1MDBEOC1cXHUwMEY2XFx1MDBGOC1cXHUwMEZGXS8sXG4gIC9bXFx1MDEwMC1cXHUwMkZGXFx1MDM3MC1cXHUxNjdGXFx1MTY4MS1cXHUxODBEXFx1MTgwRi1cXHUxREJGXS8sXG4gIC9bXFx1MUUwMC1cXHUxRkZGXS8sXG4gIC9bXFx1MjAwQi1cXHUyMDBEXFx1MjAyQS1cXHUyMDJFXFx1MjAzRi1cXHUyMDQwXFx1MjA1NFxcdTIwNjAtXFx1MjA2Rl0vLFxuICAvW1xcdTIwNzAtXFx1MjBDRlxcdTIxMDAtXFx1MjE4RlxcdTI0NjAtXFx1MjRGRlxcdTI3NzYtXFx1Mjc5M10vLFxuICAvW1xcdTJDMDAtXFx1MkRGRlxcdTJFODAtXFx1MkZGRl0vLFxuICAvW1xcdTMwMDQtXFx1MzAwN1xcdTMwMjEtXFx1MzAyRlxcdTMwMzEtXFx1MzAzRlxcdTMwNDAtXFx1RDdGRl0vLFxuICAvW1xcdUY5MDAtXFx1RkQzRFxcdUZENDAtXFx1RkRDRlxcdUZERjAtXFx1RkUxRlxcdUZFMzAtXFx1RkU0NF0vLFxuICAvW1xcdUZFNDctXFx1RkVGRVxcdUZGMDAtXFx1RkZGRF0vIC8vIFNob3VsZCBiZSAvW1xcdUZFNDctXFx1RkZGRF0vLCBidXQgd2UgaGF2ZSB0byBleGNsdWRlIEZFRkYuXG4gIC8vIFRoZSBmb2xsb3dpbmcgY2hhcmFjdGVycyBhcmUgYWxzbyBhbGxvd2VkLCBidXQgdGhlIHJlZ2V4ZXMgYXJlbid0IHN1cHBvcnRlZCB5ZXQuXG4gIC8vIC9bXFx1ezEwMDAwfS1cXHV7MUZGRkR9XFx1ezIwMDAwLVxcdXsyRkZGRH1cXHV7MzAwMDB9LVxcdXszRkZGRH1cXHV7NDAwMDB9LVxcdXs0RkZGRH1dL3UsXG4gIC8vIC9bXFx1ezUwMDAwfS1cXHV7NUZGRkR9XFx1ezYwMDAwLVxcdXs2RkZGRH1cXHV7NzAwMDB9LVxcdXs3RkZGRH1cXHV7ODAwMDB9LVxcdXs4RkZGRH1dL3UsXG4gIC8vIC9bXFx1ezkwMDAwfS1cXHV7OUZGRkR9XFx1e0EwMDAwLVxcdXtBRkZGRH1cXHV7QjAwMDB9LVxcdXtCRkZGRH1cXHV7QzAwMDB9LVxcdXtDRkZGRH1dL3UsXG4gIC8vIC9bXFx1e0QwMDAwfS1cXHV7REZGRkR9XFx1e0UwMDAwLVxcdXtFRkZGRH1dL3Vcbik7XG5cbi8vIFZhbGlkIGNoYXJhY3RlcnMgZm9yIGlkZW50aWZpZXJzLlxuY29uc3QgaWRlbnRpZmllckNoYXJhY3RlciA9IGVpdGhlcihcbiAgaWRlbnRpZmllckhlYWQsXG4gIC9cXGQvLFxuICAvW1xcdTAzMDAtXFx1MDM2RlxcdTFEQzAtXFx1MURGRlxcdTIwRDAtXFx1MjBGRlxcdUZFMjAtXFx1RkUyRl0vXG4pO1xuXG4vLyBWYWxpZCBpZGVudGlmaWVyLlxuY29uc3QgaWRlbnRpZmllciA9IGNvbmNhdChpZGVudGlmaWVySGVhZCwgaWRlbnRpZmllckNoYXJhY3RlciwgJyonKTtcblxuLy8gVmFsaWQgdHlwZSBpZGVudGlmaWVyLlxuY29uc3QgdHlwZUlkZW50aWZpZXIgPSBjb25jYXQoL1tBLVpdLywgaWRlbnRpZmllckNoYXJhY3RlciwgJyonKTtcblxuLy8gQnVpbHQtaW4gYXR0cmlidXRlcywgd2hpY2ggYXJlIGhpZ2hsaWdodGVkIGFzIGtleXdvcmRzLlxuLy8gQGF2YWlsYWJsZSBpcyBoYW5kbGVkIHNlcGFyYXRlbHkuXG5jb25zdCBrZXl3b3JkQXR0cmlidXRlcyA9IFtcbiAgJ2F1dG9jbG9zdXJlJyxcbiAgY29uY2F0KC9jb252ZW50aW9uXFwoLywgZWl0aGVyKCdzd2lmdCcsICdibG9jaycsICdjJyksIC9cXCkvKSxcbiAgJ2Rpc2NhcmRhYmxlUmVzdWx0JyxcbiAgJ2R5bmFtaWNDYWxsYWJsZScsXG4gICdkeW5hbWljTWVtYmVyTG9va3VwJyxcbiAgJ2VzY2FwaW5nJyxcbiAgJ2Zyb3plbicsXG4gICdHS0luc3BlY3RhYmxlJyxcbiAgJ0lCQWN0aW9uJyxcbiAgJ0lCRGVzaWduYWJsZScsXG4gICdJQkluc3BlY3RhYmxlJyxcbiAgJ0lCT3V0bGV0JyxcbiAgJ0lCU2VndWVBY3Rpb24nLFxuICAnaW5saW5hYmxlJyxcbiAgJ21haW4nLFxuICAnbm9ub2JqYycsXG4gICdOU0FwcGxpY2F0aW9uTWFpbicsXG4gICdOU0NvcHlpbmcnLFxuICAnTlNNYW5hZ2VkJyxcbiAgY29uY2F0KC9vYmpjXFwoLywgaWRlbnRpZmllciwgL1xcKS8pLFxuICAnb2JqYycsXG4gICdvYmpjTWVtYmVycycsXG4gICdwcm9wZXJ0eVdyYXBwZXInLFxuICAncmVxdWlyZXNfc3RvcmVkX3Byb3BlcnR5X2luaXRzJyxcbiAgJ3Rlc3RhYmxlJyxcbiAgJ1VJQXBwbGljYXRpb25NYWluJyxcbiAgJ3Vua25vd24nLFxuICAndXNhYmxlRnJvbUlubGluZSdcbl07XG5cbi8vIENvbnRleHR1YWwga2V5d29yZHMgdXNlZCBpbiBAYXZhaWxhYmxlIGFuZCAjYXZhaWxhYmxlLlxuY29uc3QgYXZhaWxhYmlsaXR5S2V5d29yZHMgPSBbXG4gICdpT1MnLFxuICAnaU9TQXBwbGljYXRpb25FeHRlbnNpb24nLFxuICAnbWFjT1MnLFxuICAnbWFjT1NBcHBsaWNhdGlvbkV4dGVuc2lvbicsXG4gICdtYWNDYXRhbHlzdCcsXG4gICdtYWNDYXRhbHlzdEFwcGxpY2F0aW9uRXh0ZW5zaW9uJyxcbiAgJ3dhdGNoT1MnLFxuICAnd2F0Y2hPU0FwcGxpY2F0aW9uRXh0ZW5zaW9uJyxcbiAgJ3R2T1MnLFxuICAndHZPU0FwcGxpY2F0aW9uRXh0ZW5zaW9uJyxcbiAgJ3N3aWZ0J1xuXTtcblxuLypcbkxhbmd1YWdlOiBTd2lmdFxuRGVzY3JpcHRpb246IFN3aWZ0IGlzIGEgZ2VuZXJhbC1wdXJwb3NlIHByb2dyYW1taW5nIGxhbmd1YWdlIGJ1aWx0IHVzaW5nIGEgbW9kZXJuIGFwcHJvYWNoIHRvIHNhZmV0eSwgcGVyZm9ybWFuY2UsIGFuZCBzb2Z0d2FyZSBkZXNpZ24gcGF0dGVybnMuXG5BdXRob3I6IFN0ZXZlbiBWYW4gSW1wZSA8c3RldmVuLnZhbmltcGVAaWNsb3VkLmNvbT5cbkNvbnRyaWJ1dG9yczogQ2hyaXMgRWlkaG9mIDxjaHJpc0BlaWRob2Yubmw+LCBOYXRlIENvb2sgPG5hdGVjb29rQGdtYWlsLmNvbT4sIEFsZXhhbmRlciBMaWNodGVyIDxtYW5uaUxAZ214Lm5ldD4sIFJpY2hhcmQgR2lic29uIDxnaWJzb24wNDJAZ2l0aHViPlxuV2Vic2l0ZTogaHR0cHM6Ly9zd2lmdC5vcmdcbkNhdGVnb3J5OiBjb21tb24sIHN5c3RlbVxuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIHN3aWZ0KGhsanMpIHtcbiAgY29uc3QgV0hJVEVTUEFDRSA9IHtcbiAgICBtYXRjaDogL1xccysvLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuICAvLyBodHRwczovL2RvY3Muc3dpZnQub3JnL3N3aWZ0LWJvb2svUmVmZXJlbmNlTWFudWFsL0xleGljYWxTdHJ1Y3R1cmUuaHRtbCNJRDQxMVxuICBjb25zdCBCTE9DS19DT01NRU5UID0gaGxqcy5DT01NRU5UKFxuICAgICcvXFxcXConLFxuICAgICdcXFxcKi8nLFxuICAgIHtcbiAgICAgIGNvbnRhaW5zOiBbICdzZWxmJyBdXG4gICAgfVxuICApO1xuICBjb25zdCBDT01NRU5UUyA9IFtcbiAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgQkxPQ0tfQ09NTUVOVFxuICBdO1xuXG4gIC8vIGh0dHBzOi8vZG9jcy5zd2lmdC5vcmcvc3dpZnQtYm9vay9SZWZlcmVuY2VNYW51YWwvTGV4aWNhbFN0cnVjdHVyZS5odG1sI0lENDEzXG4gIC8vIGh0dHBzOi8vZG9jcy5zd2lmdC5vcmcvc3dpZnQtYm9vay9SZWZlcmVuY2VNYW51YWwvenpTdW1tYXJ5T2ZUaGVHcmFtbWFyLmh0bWxcbiAgY29uc3QgRE9UX0tFWVdPUkQgPSB7XG4gICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgYmVnaW46IGNvbmNhdCgvXFwuLywgbG9va2FoZWFkKGVpdGhlciguLi5kb3RLZXl3b3JkcywgLi4ub3B0aW9uYWxEb3RLZXl3b3JkcykpKSxcbiAgICBlbmQ6IGVpdGhlciguLi5kb3RLZXl3b3JkcywgLi4ub3B0aW9uYWxEb3RLZXl3b3JkcyksXG4gICAgZXhjbHVkZUJlZ2luOiB0cnVlXG4gIH07XG4gIGNvbnN0IEtFWVdPUkRfR1VBUkQgPSB7XG4gICAgLy8gQ29uc3VtZSAua2V5d29yZCB0byBwcmV2ZW50IGhpZ2hsaWdodGluZyBwcm9wZXJ0aWVzIGFuZCBtZXRob2RzIGFzIGtleXdvcmRzLlxuICAgIG1hdGNoOiBjb25jYXQoL1xcLi8sIGVpdGhlciguLi5rZXl3b3JkcykpLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuICBjb25zdCBQTEFJTl9LRVlXT1JEUyA9IGtleXdvcmRzXG4gICAgLmZpbHRlcihrdyA9PiB0eXBlb2Yga3cgPT09ICdzdHJpbmcnKVxuICAgIC5jb25jYXQoWyBcIl98MFwiIF0pOyAvLyBzZWVtcyBjb21tb24sIHNvIDAgcmVsZXZhbmNlXG4gIGNvbnN0IFJFR0VYX0tFWVdPUkRTID0ga2V5d29yZHNcbiAgICAuZmlsdGVyKGt3ID0+IHR5cGVvZiBrdyAhPT0gJ3N0cmluZycpIC8vIGZpbmQgcmVnZXhcbiAgICAuY29uY2F0KGtleXdvcmRUeXBlcylcbiAgICAubWFwKGtleXdvcmRXcmFwcGVyKTtcbiAgY29uc3QgS0VZV09SRCA9IHtcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdrZXl3b3JkJyxcbiAgICAgICAgbWF0Y2g6IGVpdGhlciguLi5SRUdFWF9LRVlXT1JEUywgLi4ub3B0aW9uYWxEb3RLZXl3b3JkcylcbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIC8vIGZpbmQgYWxsIHRoZSByZWd1bGFyIGtleXdvcmRzXG4gIGNvbnN0IEtFWVdPUkRTID0ge1xuICAgICRwYXR0ZXJuOiBlaXRoZXIoXG4gICAgICAvXFxiXFx3Ky8sIC8vIHJlZ3VsYXIga2V5d29yZHNcbiAgICAgIC8jXFx3Ky8gLy8gbnVtYmVyIGtleXdvcmRzXG4gICAgKSxcbiAgICBrZXl3b3JkOiBQTEFJTl9LRVlXT1JEU1xuICAgICAgLmNvbmNhdChudW1iZXJTaWduS2V5d29yZHMpLFxuICAgIGxpdGVyYWw6IGxpdGVyYWxzXG4gIH07XG4gIGNvbnN0IEtFWVdPUkRfTU9ERVMgPSBbXG4gICAgRE9UX0tFWVdPUkQsXG4gICAgS0VZV09SRF9HVUFSRCxcbiAgICBLRVlXT1JEXG4gIF07XG5cbiAgLy8gaHR0cHM6Ly9naXRodWIuY29tL2FwcGxlL3N3aWZ0L3RyZWUvbWFpbi9zdGRsaWIvcHVibGljL2NvcmVcbiAgY29uc3QgQlVJTFRfSU5fR1VBUkQgPSB7XG4gICAgLy8gQ29uc3VtZSAuYnVpbHRfaW4gdG8gcHJldmVudCBoaWdobGlnaHRpbmcgcHJvcGVydGllcyBhbmQgbWV0aG9kcy5cbiAgICBtYXRjaDogY29uY2F0KC9cXC4vLCBlaXRoZXIoLi4uYnVpbHRJbnMpKSxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgY29uc3QgQlVJTFRfSU4gPSB7XG4gICAgY2xhc3NOYW1lOiAnYnVpbHRfaW4nLFxuICAgIG1hdGNoOiBjb25jYXQoL1xcYi8sIGVpdGhlciguLi5idWlsdElucyksIC8oPz1cXCgpLylcbiAgfTtcbiAgY29uc3QgQlVJTFRfSU5TID0gW1xuICAgIEJVSUxUX0lOX0dVQVJELFxuICAgIEJVSUxUX0lOXG4gIF07XG5cbiAgLy8gaHR0cHM6Ly9kb2NzLnN3aWZ0Lm9yZy9zd2lmdC1ib29rL1JlZmVyZW5jZU1hbnVhbC9MZXhpY2FsU3RydWN0dXJlLmh0bWwjSUQ0MThcbiAgY29uc3QgT1BFUkFUT1JfR1VBUkQgPSB7XG4gICAgLy8gUHJldmVudCAtPiBmcm9tIGJlaW5nIGhpZ2hsaWdodGluZyBhcyBhbiBvcGVyYXRvci5cbiAgICBtYXRjaDogLy0+LyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgY29uc3QgT1BFUkFUT1IgPSB7XG4gICAgY2xhc3NOYW1lOiAnb3BlcmF0b3InLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBtYXRjaDogb3BlcmF0b3JcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIGRvdC1vcGVyYXRvcjogb25seSBvcGVyYXRvcnMgdGhhdCBzdGFydCB3aXRoIGEgZG90IGFyZSBhbGxvd2VkIHRvIHVzZSBkb3RzIGFzXG4gICAgICAgIC8vIGNoYXJhY3RlcnMgKC4uLiwgLi4uPCwgLiosIGV0YykuIFNvIHRoZXJlIHJ1bGUgaGVyZSBpczogYSBkb3QgZm9sbG93ZWQgYnkgb25lIG9yIG1vcmVcbiAgICAgICAgLy8gY2hhcmFjdGVycyB0aGF0IG1heSBhbHNvIGluY2x1ZGUgZG90cy5cbiAgICAgICAgbWF0Y2g6IGBcXFxcLihcXFxcLnwke29wZXJhdG9yQ2hhcmFjdGVyfSkrYFxuICAgICAgfVxuICAgIF1cbiAgfTtcbiAgY29uc3QgT1BFUkFUT1JTID0gW1xuICAgIE9QRVJBVE9SX0dVQVJELFxuICAgIE9QRVJBVE9SXG4gIF07XG5cbiAgLy8gaHR0cHM6Ly9kb2NzLnN3aWZ0Lm9yZy9zd2lmdC1ib29rL1JlZmVyZW5jZU1hbnVhbC9MZXhpY2FsU3RydWN0dXJlLmh0bWwjZ3JhbW1hcl9udW1lcmljLWxpdGVyYWxcbiAgLy8gVE9ETzogVXBkYXRlIGZvciBsZWFkaW5nIGAtYCBhZnRlciBsb29rYmVoaW5kIGlzIHN1cHBvcnRlZCBldmVyeXdoZXJlXG4gIGNvbnN0IGRlY2ltYWxEaWdpdHMgPSAnKFswLTldXyopKyc7XG4gIGNvbnN0IGhleERpZ2l0cyA9ICcoWzAtOWEtZkEtRl1fKikrJztcbiAgY29uc3QgTlVNQkVSID0ge1xuICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICAvLyBkZWNpbWFsIGZsb2F0aW5nLXBvaW50LWxpdGVyYWwgKHN1YnN1bWVzIGRlY2ltYWwtbGl0ZXJhbClcbiAgICAgIHtcbiAgICAgICAgbWF0Y2g6IGBcXFxcYigke2RlY2ltYWxEaWdpdHN9KShcXFxcLigke2RlY2ltYWxEaWdpdHN9KSk/YCArIGAoW2VFXVsrLV0/KCR7ZGVjaW1hbERpZ2l0c30pKT9cXFxcYmBcbiAgICAgIH0sXG4gICAgICAvLyBoZXhhZGVjaW1hbCBmbG9hdGluZy1wb2ludC1saXRlcmFsIChzdWJzdW1lcyBoZXhhZGVjaW1hbC1saXRlcmFsKVxuICAgICAge1xuICAgICAgICBtYXRjaDogYFxcXFxiMHgoJHtoZXhEaWdpdHN9KShcXFxcLigke2hleERpZ2l0c30pKT9gICsgYChbcFBdWystXT8oJHtkZWNpbWFsRGlnaXRzfSkpP1xcXFxiYFxuICAgICAgfSxcbiAgICAgIC8vIG9jdGFsLWxpdGVyYWxcbiAgICAgIHtcbiAgICAgICAgbWF0Y2g6IC9cXGIwbyhbMC03XV8qKStcXGIvXG4gICAgICB9LFxuICAgICAgLy8gYmluYXJ5LWxpdGVyYWxcbiAgICAgIHtcbiAgICAgICAgbWF0Y2g6IC9cXGIwYihbMDFdXyopK1xcYi9cbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgLy8gaHR0cHM6Ly9kb2NzLnN3aWZ0Lm9yZy9zd2lmdC1ib29rL1JlZmVyZW5jZU1hbnVhbC9MZXhpY2FsU3RydWN0dXJlLmh0bWwjZ3JhbW1hcl9zdHJpbmctbGl0ZXJhbFxuICBjb25zdCBFU0NBUEVEX0NIQVJBQ1RFUiA9IChyYXdEZWxpbWl0ZXIgPSBcIlwiKSA9PiAoe1xuICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBtYXRjaDogY29uY2F0KC9cXFxcLywgcmF3RGVsaW1pdGVyLCAvWzBcXFxcdG5yXCInXS8pXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBtYXRjaDogY29uY2F0KC9cXFxcLywgcmF3RGVsaW1pdGVyLCAvdVxce1swLTlhLWZBLUZdezEsOH1cXH0vKVxuICAgICAgfVxuICAgIF1cbiAgfSk7XG4gIGNvbnN0IEVTQ0FQRURfTkVXTElORSA9IChyYXdEZWxpbWl0ZXIgPSBcIlwiKSA9PiAoe1xuICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICBtYXRjaDogY29uY2F0KC9cXFxcLywgcmF3RGVsaW1pdGVyLCAvW1xcdCBdKig/OltcXHJcXG5dfFxcclxcbikvKVxuICB9KTtcbiAgY29uc3QgSU5URVJQT0xBVElPTiA9IChyYXdEZWxpbWl0ZXIgPSBcIlwiKSA9PiAoe1xuICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICBsYWJlbDogXCJpbnRlcnBvbFwiLFxuICAgIGJlZ2luOiBjb25jYXQoL1xcXFwvLCByYXdEZWxpbWl0ZXIsIC9cXCgvKSxcbiAgICBlbmQ6IC9cXCkvXG4gIH0pO1xuICBjb25zdCBNVUxUSUxJTkVfU1RSSU5HID0gKHJhd0RlbGltaXRlciA9IFwiXCIpID0+ICh7XG4gICAgYmVnaW46IGNvbmNhdChyYXdEZWxpbWl0ZXIsIC9cIlwiXCIvKSxcbiAgICBlbmQ6IGNvbmNhdCgvXCJcIlwiLywgcmF3RGVsaW1pdGVyKSxcbiAgICBjb250YWluczogW1xuICAgICAgRVNDQVBFRF9DSEFSQUNURVIocmF3RGVsaW1pdGVyKSxcbiAgICAgIEVTQ0FQRURfTkVXTElORShyYXdEZWxpbWl0ZXIpLFxuICAgICAgSU5URVJQT0xBVElPTihyYXdEZWxpbWl0ZXIpXG4gICAgXVxuICB9KTtcbiAgY29uc3QgU0lOR0xFX0xJTkVfU1RSSU5HID0gKHJhd0RlbGltaXRlciA9IFwiXCIpID0+ICh7XG4gICAgYmVnaW46IGNvbmNhdChyYXdEZWxpbWl0ZXIsIC9cIi8pLFxuICAgIGVuZDogY29uY2F0KC9cIi8sIHJhd0RlbGltaXRlciksXG4gICAgY29udGFpbnM6IFtcbiAgICAgIEVTQ0FQRURfQ0hBUkFDVEVSKHJhd0RlbGltaXRlciksXG4gICAgICBJTlRFUlBPTEFUSU9OKHJhd0RlbGltaXRlcilcbiAgICBdXG4gIH0pO1xuICBjb25zdCBTVFJJTkcgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICB2YXJpYW50czogW1xuICAgICAgTVVMVElMSU5FX1NUUklORygpLFxuICAgICAgTVVMVElMSU5FX1NUUklORyhcIiNcIiksXG4gICAgICBNVUxUSUxJTkVfU1RSSU5HKFwiIyNcIiksXG4gICAgICBNVUxUSUxJTkVfU1RSSU5HKFwiIyMjXCIpLFxuICAgICAgU0lOR0xFX0xJTkVfU1RSSU5HKCksXG4gICAgICBTSU5HTEVfTElORV9TVFJJTkcoXCIjXCIpLFxuICAgICAgU0lOR0xFX0xJTkVfU1RSSU5HKFwiIyNcIiksXG4gICAgICBTSU5HTEVfTElORV9TVFJJTkcoXCIjIyNcIilcbiAgICBdXG4gIH07XG5cbiAgLy8gaHR0cHM6Ly9kb2NzLnN3aWZ0Lm9yZy9zd2lmdC1ib29rL1JlZmVyZW5jZU1hbnVhbC9MZXhpY2FsU3RydWN0dXJlLmh0bWwjSUQ0MTJcbiAgY29uc3QgUVVPVEVEX0lERU5USUZJRVIgPSB7XG4gICAgbWF0Y2g6IGNvbmNhdCgvYC8sIGlkZW50aWZpZXIsIC9gLylcbiAgfTtcbiAgY29uc3QgSU1QTElDSVRfUEFSQU1FVEVSID0ge1xuICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICBtYXRjaDogL1xcJFxcZCsvXG4gIH07XG4gIGNvbnN0IFBST1BFUlRZX1dSQVBQRVJfUFJPSkVDVElPTiA9IHtcbiAgICBjbGFzc05hbWU6ICd2YXJpYWJsZScsXG4gICAgbWF0Y2g6IGBcXFxcJCR7aWRlbnRpZmllckNoYXJhY3Rlcn0rYFxuICB9O1xuICBjb25zdCBJREVOVElGSUVSUyA9IFtcbiAgICBRVU9URURfSURFTlRJRklFUixcbiAgICBJTVBMSUNJVF9QQVJBTUVURVIsXG4gICAgUFJPUEVSVFlfV1JBUFBFUl9QUk9KRUNUSU9OXG4gIF07XG5cbiAgLy8gaHR0cHM6Ly9kb2NzLnN3aWZ0Lm9yZy9zd2lmdC1ib29rL1JlZmVyZW5jZU1hbnVhbC9BdHRyaWJ1dGVzLmh0bWxcbiAgY29uc3QgQVZBSUxBQkxFX0FUVFJJQlVURSA9IHtcbiAgICBtYXRjaDogLyhAfCMpYXZhaWxhYmxlLyxcbiAgICBjbGFzc05hbWU6IFwia2V5d29yZFwiLFxuICAgIHN0YXJ0czoge1xuICAgICAgY29udGFpbnM6IFtcbiAgICAgICAge1xuICAgICAgICAgIGJlZ2luOiAvXFwoLyxcbiAgICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICAgIGtleXdvcmRzOiBhdmFpbGFiaWxpdHlLZXl3b3JkcyxcbiAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgLi4uT1BFUkFUT1JTLFxuICAgICAgICAgICAgTlVNQkVSLFxuICAgICAgICAgICAgU1RSSU5HXG4gICAgICAgICAgXVxuICAgICAgICB9XG4gICAgICBdXG4gICAgfVxuICB9O1xuICBjb25zdCBLRVlXT1JEX0FUVFJJQlVURSA9IHtcbiAgICBjbGFzc05hbWU6ICdrZXl3b3JkJyxcbiAgICBtYXRjaDogY29uY2F0KC9ALywgZWl0aGVyKC4uLmtleXdvcmRBdHRyaWJ1dGVzKSlcbiAgfTtcbiAgY29uc3QgVVNFUl9ERUZJTkVEX0FUVFJJQlVURSA9IHtcbiAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICBtYXRjaDogY29uY2F0KC9ALywgaWRlbnRpZmllcilcbiAgfTtcbiAgY29uc3QgQVRUUklCVVRFUyA9IFtcbiAgICBBVkFJTEFCTEVfQVRUUklCVVRFLFxuICAgIEtFWVdPUkRfQVRUUklCVVRFLFxuICAgIFVTRVJfREVGSU5FRF9BVFRSSUJVVEVcbiAgXTtcblxuICAvLyBodHRwczovL2RvY3Muc3dpZnQub3JnL3N3aWZ0LWJvb2svUmVmZXJlbmNlTWFudWFsL1R5cGVzLmh0bWxcbiAgY29uc3QgVFlQRSA9IHtcbiAgICBtYXRjaDogbG9va2FoZWFkKC9cXGJbQS1aXS8pLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICBjb250YWluczogW1xuICAgICAgeyAvLyBDb21tb24gQXBwbGUgZnJhbWV3b3JrcywgZm9yIHJlbGV2YW5jZSBib29zdFxuICAgICAgICBjbGFzc05hbWU6ICd0eXBlJyxcbiAgICAgICAgbWF0Y2g6IGNvbmNhdCgvKEFWfENBfENGfENHfENJfENMfENNfENOfENUfE1LfE1QfE1US3xNVEx8TlN8U0NOfFNLfFVJfFdLfFhDKS8sIGlkZW50aWZpZXJDaGFyYWN0ZXIsICcrJylcbiAgICAgIH0sXG4gICAgICB7IC8vIFR5cGUgaWRlbnRpZmllclxuICAgICAgICBjbGFzc05hbWU6ICd0eXBlJyxcbiAgICAgICAgbWF0Y2g6IHR5cGVJZGVudGlmaWVyLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7IC8vIE9wdGlvbmFsIHR5cGVcbiAgICAgICAgbWF0Y2g6IC9bPyFdKy8sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHsgLy8gVmFyaWFkaWMgcGFyYW1ldGVyXG4gICAgICAgIG1hdGNoOiAvXFwuXFwuXFwuLyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAgeyAvLyBQcm90b2NvbCBjb21wb3NpdGlvblxuICAgICAgICBtYXRjaDogY29uY2F0KC9cXHMrJlxccysvLCBsb29rYWhlYWQodHlwZUlkZW50aWZpZXIpKSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9XG4gICAgXVxuICB9O1xuICBjb25zdCBHRU5FUklDX0FSR1VNRU5UUyA9IHtcbiAgICBiZWdpbjogLzwvLFxuICAgIGVuZDogLz4vLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICBjb250YWluczogW1xuICAgICAgLi4uQ09NTUVOVFMsXG4gICAgICAuLi5LRVlXT1JEX01PREVTLFxuICAgICAgLi4uQVRUUklCVVRFUyxcbiAgICAgIE9QRVJBVE9SX0dVQVJELFxuICAgICAgVFlQRVxuICAgIF1cbiAgfTtcbiAgVFlQRS5jb250YWlucy5wdXNoKEdFTkVSSUNfQVJHVU1FTlRTKTtcblxuICAvLyBodHRwczovL2RvY3Muc3dpZnQub3JnL3N3aWZ0LWJvb2svUmVmZXJlbmNlTWFudWFsL0V4cHJlc3Npb25zLmh0bWwjSUQ1NTJcbiAgLy8gUHJldmVudHMgZWxlbWVudCBuYW1lcyBmcm9tIGJlaW5nIGhpZ2hsaWdodGVkIGFzIGtleXdvcmRzLlxuICBjb25zdCBUVVBMRV9FTEVNRU5UX05BTUUgPSB7XG4gICAgbWF0Y2g6IGNvbmNhdChpZGVudGlmaWVyLCAvXFxzKjovKSxcbiAgICBrZXl3b3JkczogXCJffDBcIixcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgLy8gTWF0Y2hlcyB0dXBsZXMgYXMgd2VsbCBhcyB0aGUgcGFyYW1ldGVyIGxpc3Qgb2YgYSBmdW5jdGlvbiB0eXBlLlxuICBjb25zdCBUVVBMRSA9IHtcbiAgICBiZWdpbjogL1xcKC8sXG4gICAgZW5kOiAvXFwpLyxcbiAgICByZWxldmFuY2U6IDAsXG4gICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICAnc2VsZicsXG4gICAgICBUVVBMRV9FTEVNRU5UX05BTUUsXG4gICAgICAuLi5DT01NRU5UUyxcbiAgICAgIC4uLktFWVdPUkRfTU9ERVMsXG4gICAgICAuLi5CVUlMVF9JTlMsXG4gICAgICAuLi5PUEVSQVRPUlMsXG4gICAgICBOVU1CRVIsXG4gICAgICBTVFJJTkcsXG4gICAgICAuLi5JREVOVElGSUVSUyxcbiAgICAgIC4uLkFUVFJJQlVURVMsXG4gICAgICBUWVBFXG4gICAgXVxuICB9O1xuXG4gIC8vIGh0dHBzOi8vZG9jcy5zd2lmdC5vcmcvc3dpZnQtYm9vay9SZWZlcmVuY2VNYW51YWwvRGVjbGFyYXRpb25zLmh0bWwjSUQzNjJcbiAgLy8gTWF0Y2hlcyBib3RoIHRoZSBrZXl3b3JkIGZ1bmMgYW5kIHRoZSBmdW5jdGlvbiB0aXRsZS5cbiAgLy8gR3JvdXBpbmcgdGhlc2UgbGV0cyB1cyBkaWZmZXJlbnRpYXRlIGJldHdlZW4gdGhlIG9wZXJhdG9yIGZ1bmN0aW9uIDxcbiAgLy8gYW5kIHRoZSBzdGFydCBvZiB0aGUgZ2VuZXJpYyBwYXJhbWV0ZXIgY2xhdXNlIChhbHNvIDwpLlxuICBjb25zdCBGVU5DX1BMVVNfVElUTEUgPSB7XG4gICAgYmVnaW5LZXl3b3JkczogJ2Z1bmMnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3RpdGxlJyxcbiAgICAgICAgbWF0Y2g6IGVpdGhlcihRVU9URURfSURFTlRJRklFUi5tYXRjaCwgaWRlbnRpZmllciwgb3BlcmF0b3IpLFxuICAgICAgICAvLyBSZXF1aXJlZCB0byBtYWtlIHN1cmUgdGhlIG9wZW5pbmcgPCBvZiB0aGUgZ2VuZXJpYyBwYXJhbWV0ZXIgY2xhdXNlXG4gICAgICAgIC8vIGlzbid0IHBhcnNlZCBhcyBhIHNlY29uZCB0aXRsZS5cbiAgICAgICAgZW5kc1BhcmVudDogdHJ1ZSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAgV0hJVEVTUEFDRVxuICAgIF1cbiAgfTtcbiAgY29uc3QgR0VORVJJQ19QQVJBTUVURVJTID0ge1xuICAgIGJlZ2luOiAvPC8sXG4gICAgZW5kOiAvPi8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIC4uLkNPTU1FTlRTLFxuICAgICAgVFlQRVxuICAgIF1cbiAgfTtcbiAgY29uc3QgRlVOQ1RJT05fUEFSQU1FVEVSX05BTUUgPSB7XG4gICAgYmVnaW46IGVpdGhlcihcbiAgICAgIGxvb2thaGVhZChjb25jYXQoaWRlbnRpZmllciwgL1xccyo6LykpLFxuICAgICAgbG9va2FoZWFkKGNvbmNhdChpZGVudGlmaWVyLCAvXFxzKy8sIGlkZW50aWZpZXIsIC9cXHMqOi8pKVxuICAgICksXG4gICAgZW5kOiAvOi8sXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2tleXdvcmQnLFxuICAgICAgICBtYXRjaDogL1xcYl9cXGIvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgICAgICBtYXRjaDogaWRlbnRpZmllclxuICAgICAgfVxuICAgIF1cbiAgfTtcbiAgY29uc3QgRlVOQ1RJT05fUEFSQU1FVEVSUyA9IHtcbiAgICBiZWdpbjogL1xcKC8sXG4gICAgZW5kOiAvXFwpLyxcbiAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIEZVTkNUSU9OX1BBUkFNRVRFUl9OQU1FLFxuICAgICAgLi4uQ09NTUVOVFMsXG4gICAgICAuLi5LRVlXT1JEX01PREVTLFxuICAgICAgLi4uT1BFUkFUT1JTLFxuICAgICAgTlVNQkVSLFxuICAgICAgU1RSSU5HLFxuICAgICAgLi4uQVRUUklCVVRFUyxcbiAgICAgIFRZUEUsXG4gICAgICBUVVBMRVxuICAgIF0sXG4gICAgZW5kc1BhcmVudDogdHJ1ZSxcbiAgICBpbGxlZ2FsOiAvW1wiJ10vXG4gIH07XG4gIGNvbnN0IEZVTkNUSU9OID0ge1xuICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICBtYXRjaDogbG9va2FoZWFkKC9cXGJmdW5jXFxiLyksXG4gICAgY29udGFpbnM6IFtcbiAgICAgIEZVTkNfUExVU19USVRMRSxcbiAgICAgIEdFTkVSSUNfUEFSQU1FVEVSUyxcbiAgICAgIEZVTkNUSU9OX1BBUkFNRVRFUlMsXG4gICAgICBXSElURVNQQUNFXG4gICAgXSxcbiAgICBpbGxlZ2FsOiBbXG4gICAgICAvXFxbLyxcbiAgICAgIC8lL1xuICAgIF1cbiAgfTtcblxuICAvLyBodHRwczovL2RvY3Muc3dpZnQub3JnL3N3aWZ0LWJvb2svUmVmZXJlbmNlTWFudWFsL0RlY2xhcmF0aW9ucy5odG1sI0lEMzc1XG4gIC8vIGh0dHBzOi8vZG9jcy5zd2lmdC5vcmcvc3dpZnQtYm9vay9SZWZlcmVuY2VNYW51YWwvRGVjbGFyYXRpb25zLmh0bWwjSUQzNzlcbiAgY29uc3QgSU5JVF9TVUJTQ1JJUFQgPSB7XG4gICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgIG1hdGNoOiAvXFxiKHN1YnNjcmlwdHxpbml0Wz8hXT8pXFxzKig/PVs8KF0pLyxcbiAgICBrZXl3b3Jkczoge1xuICAgICAga2V5d29yZDogXCJzdWJzY3JpcHQgaW5pdCBpbml0PyBpbml0IVwiLFxuICAgICAgJHBhdHRlcm46IC9cXHcrWz8hXT8vXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAgR0VORVJJQ19QQVJBTUVURVJTLFxuICAgICAgRlVOQ1RJT05fUEFSQU1FVEVSUyxcbiAgICAgIFdISVRFU1BBQ0VcbiAgICBdLFxuICAgIGlsbGVnYWw6IC9cXFt8JS9cbiAgfTtcbiAgLy8gaHR0cHM6Ly9kb2NzLnN3aWZ0Lm9yZy9zd2lmdC1ib29rL1JlZmVyZW5jZU1hbnVhbC9EZWNsYXJhdGlvbnMuaHRtbCNJRDM4MFxuICBjb25zdCBPUEVSQVRPUl9ERUNMQVJBVElPTiA9IHtcbiAgICBiZWdpbktleXdvcmRzOiAnb3BlcmF0b3InLFxuICAgIGVuZDogaGxqcy5NQVRDSF9OT1RISU5HX1JFLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3RpdGxlJyxcbiAgICAgICAgbWF0Y2g6IG9wZXJhdG9yLFxuICAgICAgICBlbmRzUGFyZW50OiB0cnVlLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgLy8gaHR0cHM6Ly9kb2NzLnN3aWZ0Lm9yZy9zd2lmdC1ib29rL1JlZmVyZW5jZU1hbnVhbC9EZWNsYXJhdGlvbnMuaHRtbCNJRDU1MFxuICBjb25zdCBQUkVDRURFTkNFR1JPVVAgPSB7XG4gICAgYmVnaW5LZXl3b3JkczogJ3ByZWNlZGVuY2Vncm91cCcsXG4gICAgZW5kOiBobGpzLk1BVENIX05PVEhJTkdfUkUsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndGl0bGUnLFxuICAgICAgICBtYXRjaDogdHlwZUlkZW50aWZpZXIsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC97LyxcbiAgICAgICAgZW5kOiAvfS8sXG4gICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgZW5kc1BhcmVudDogdHJ1ZSxcbiAgICAgICAga2V5d29yZHM6IFtcbiAgICAgICAgICAuLi5wcmVjZWRlbmNlZ3JvdXBLZXl3b3JkcyxcbiAgICAgICAgICAuLi5saXRlcmFsc1xuICAgICAgICBdLFxuICAgICAgICBjb250YWluczogWyBUWVBFIF1cbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgLy8gQWRkIHN1cHBvcnRlZCBzdWJtb2RlcyB0byBzdHJpbmcgaW50ZXJwb2xhdGlvbi5cbiAgZm9yIChjb25zdCB2YXJpYW50IG9mIFNUUklORy52YXJpYW50cykge1xuICAgIGNvbnN0IGludGVycG9sYXRpb24gPSB2YXJpYW50LmNvbnRhaW5zLmZpbmQobW9kZSA9PiBtb2RlLmxhYmVsID09PSBcImludGVycG9sXCIpO1xuICAgIC8vIFRPRE86IEludGVycG9sYXRpb24gY2FuIGNvbnRhaW4gYW55IGV4cHJlc3Npb24sIHNvIHRoZXJlJ3Mgcm9vbSBmb3IgaW1wcm92ZW1lbnQgaGVyZS5cbiAgICBpbnRlcnBvbGF0aW9uLmtleXdvcmRzID0gS0VZV09SRFM7XG4gICAgY29uc3Qgc3VibW9kZXMgPSBbXG4gICAgICAuLi5LRVlXT1JEX01PREVTLFxuICAgICAgLi4uQlVJTFRfSU5TLFxuICAgICAgLi4uT1BFUkFUT1JTLFxuICAgICAgTlVNQkVSLFxuICAgICAgU1RSSU5HLFxuICAgICAgLi4uSURFTlRJRklFUlNcbiAgICBdO1xuICAgIGludGVycG9sYXRpb24uY29udGFpbnMgPSBbXG4gICAgICAuLi5zdWJtb2RlcyxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICdzZWxmJyxcbiAgICAgICAgICAuLi5zdWJtb2Rlc1xuICAgICAgICBdXG4gICAgICB9XG4gICAgXTtcbiAgfVxuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1N3aWZ0JyxcbiAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIC4uLkNPTU1FTlRTLFxuICAgICAgRlVOQ1RJT04sXG4gICAgICBJTklUX1NVQlNDUklQVCxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnc3RydWN0IHByb3RvY29sIGNsYXNzIGV4dGVuc2lvbiBlbnVtJyxcbiAgICAgICAgZW5kOiAnXFxcXHsnLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgaGxqcy5pbmhlcml0KGhsanMuVElUTEVfTU9ERSwge1xuICAgICAgICAgICAgYmVnaW46IC9bQS1aYS16JF9dW1xcdTAwQzAtXFx1MDJCODAtOUEtWmEteiRfXSovXG4gICAgICAgICAgfSksXG4gICAgICAgICAgLi4uS0VZV09SRF9NT0RFU1xuICAgICAgICBdXG4gICAgICB9LFxuICAgICAgT1BFUkFUT1JfREVDTEFSQVRJT04sXG4gICAgICBQUkVDRURFTkNFR1JPVVAsXG4gICAgICB7XG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdpbXBvcnQnLFxuICAgICAgICBlbmQ6IC8kLyxcbiAgICAgICAgY29udGFpbnM6IFsgLi4uQ09NTUVOVFMgXSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAgLi4uS0VZV09SRF9NT0RFUyxcbiAgICAgIC4uLkJVSUxUX0lOUyxcbiAgICAgIC4uLk9QRVJBVE9SUyxcbiAgICAgIE5VTUJFUixcbiAgICAgIFNUUklORyxcbiAgICAgIC4uLklERU5USUZJRVJTLFxuICAgICAgLi4uQVRUUklCVVRFUyxcbiAgICAgIFRZUEUsXG4gICAgICBUVVBMRVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBzd2lmdDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==